import sys
import random

from dao import dao_user, dao_playlist, dao_session_info, db_utils
import config

from utils import utils, spotify_utils as helper
from flask import Response

from math import floor
from random import randint

sys.path.append('../')


def manage_logged_user(current_user_id, invited, sp=None):
    """
    Check if the user is in the DB. If not, it creates the instances for the user
    :param current_user_id:
    :param sp:
    :return:
    """

    # check if the user exists in the DB: load user info, if the user doesn't exist we receive an empty dict
    user = dao_user.load_user_data(current_user_id)

    is_admin = False

    if current_user_id in config.ADMIN_USER_ID_LIST:
        is_admin = True

    if not user:
        # the user is not in the DB
        # we create a new user with the given id

        is_user = True
        dao_user.create_new_user(current_user_id, invited, is_user, is_admin)

        #TODO: CREATE TRANSACTION ? IF THE USER IS CREATED AND THE SONGS ARE NOT INITIALIZED?

        # select the tracks for the user
        if not is_admin:
            user_track_ids = helper.get_selected_tracks(sp)

            print("selected tracks: ", len(user_track_ids))

            dao_playlist.create_basic_playlists_for_user(current_user_id, user_track_ids)

        user = dao_user.load_user_data(current_user_id)

    if is_admin:
        return user, config.ADMIN_VIEW_DICT['ADMIN_DASHBOARD']
    else:
        return user, config.CURRENT_VIEW_DICT[user['current_state']]


def get_current_view_for_user(current_user_id):
    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return None, config.ERROR_VIEW_DICT['INVALID_USER'], 'INVALID_USER'

    if user["current_state"]=="INCOMPLETE_USER":
        return None, config.ERROR_VIEW_DICT['INCOMPLETE_USER'], 'INCOMPLETE_USER'

    current_state = user['current_state']
    return user, config.CURRENT_VIEW_DICT[current_state], current_state


def get_user(current_user_id):
    user = dao_user.load_user_data(current_user_id)

    return user


def manage_submit(current_user_id, form, mail):
    # check if the user exists in the DB: load user info, if the user doesn't exist we receive an empty dict
    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return config.ERROR_VIEW_DICT['INVALID_USER'], None, None
    if user["current_state"]=="INCOMPLETE_USER":
        return config.ERROR_VIEW_DICT['INCOMPLETE_USER'], None, None

    invited = user['is_invited']
    current_state, error_msg, add_to_session = __perform_submit(user['current_state'], user, invited, form, mail)

    add_to_session['PERCENTAGE'] = config.PERCENTAGE_COMP[current_state]
    add_to_session['user_email'] = user['email']
    return config.CURRENT_VIEW_DICT[current_state], error_msg, add_to_session


def __check_missing_parameters(current_state, form):
    missing_parameters = list()
    required_parameters = config.REQUIRED_PARAMETERS[current_state]
    for param in required_parameters:
        if not form.get(param):
            missing_parameters.append(param)
    return missing_parameters


def __perform_submit(current_state, user, invited, form, mail):
    current_user_id = user['id']
    print("perform submit - Invited:", invited, " - current_state: ", current_state)
    error_msg = None
    missing_parameters = __check_missing_parameters(current_state, form)
    add_to_session = dict()
    add_to_session['invited'] = invited
    add_to_session['friend_nickname'] = user['friend_nickname']
    if missing_parameters:
        error_msg = __create_missing_parameters_msg(missing_parameters)

    # TODO: in each state we prepare the session for the next at the end; this is not very "generic" and needs to be reengineered
    if current_state == 'START_SESSION_1':
        current_state, error_msg = __manage_start_session_one(current_state, current_user_id, form, invited)
        # add_to_session['FFM'] = generate_ffm_dict(current_user_id)
    elif current_state == 'INSERT_EMAIL_NICK':
        current_state, error_msg, email_friend, invited = __manage_insert_nick_email(current_state, current_user_id, form, invited)
        add_to_session['email_friend'] = email_friend
        add_to_session['invited'] = invited
    elif current_state == 'INSERT_EMAIL_NICK_FRIEND':
        current_state, error_msg = __manage_insert_nick_email_friend(current_state, current_user_id, user['email'], form, invited, mail)
    elif current_state == 'INSERT_AGE_GENDER':
        current_state, error_msg = __manage_insert_age_gender(current_state, current_user_id, form, invited)
        add_to_session['FFM'] = generate_ffm_dict(current_user_id)
    elif current_state == 'INSERT_SELF_FFM':
        current_state, error_msg = __manage_insert_ffm(current_state, current_user_id, form, invited)
        add_to_session['ROCI'] = generate_roci_dict(current_user_id)
    elif current_state == 'INSERT_SELF_ROCI':
        current_state, error_msg = __manage_insert_roci(current_state, current_user_id, form, invited)
        add_to_session['INDIVIDUAL_SONGS'] = generate_individual_songs_dict(current_user_id)
    elif current_state == 'EVALUATE_SONGS_INDIVIDUAL':
        current_state, error_msg = __manage_insert_individual_evaluations(current_state, current_user_id, form, invited)

    # SESSION 2
    elif current_state == 'START_SESSION_2':
        current_state, error_msg = __manage_start_session_two(current_state, current_user_id, form, invited)
        add_to_session['FFM'] = generate_ffm_dict(current_user_id)
    elif current_state == 'INSERT_FRIEND_FFM':
        current_state, error_msg = __manage_insert_ffm(current_state, current_user_id, form, invited)
        add_to_session['ROCI'] = generate_roci_dict(current_user_id)
    elif current_state == 'INSERT_FRIEND_ROCI':
        current_state, error_msg = __manage_insert_roci(current_state, current_user_id, form, invited)
    # elif current_state == 'START_SESSION_3':
    #     current_state, error_msg = __manage_start_session_three(current_state, current_user_id, form, invited)
        add_to_session['GROUP_SONGS'] = generate_group_songs_dict(current_user_id, "friend")
    elif current_state == 'EVALUATE_SONGS_GROUP_FRIEND':
        current_state, error_msg = __manage_insert_group_eval(current_state, current_user_id, form, invited, "friend")
        add_to_session['GROUP_SONGS'] = generate_group_songs_dict(current_user_id, "stranger")
    elif current_state == 'EVALUATE_SONGS_GROUP_STRANGER':
        current_state, error_msg = __manage_insert_group_eval(current_state, current_user_id, form, invited, "stranger")
    print(error_msg)
    return current_state, error_msg, add_to_session


def __manage_insert_nick_email(current_state, current_user_id, form, invited):
    # retrieve values of the requested parameters
    error_msg = None
    email = form.get('email')
    nickname = form.get('nickname')

    invited_by_id, invited_by_email = dao_user.check_user_invited(email)
    print(email, nickname, invited_by_id, invited_by_email)

    # check if the user has been invited
    if invited and not invited_by_id:
        error_msg = "Please insert the email on which you received your invitation"
    else:
        # if invited_by_id not null the user has been invited: we set invited to true
        if invited_by_id:
            print("invited")
            invited = True

        # find new state to update it
        if invited:
            # update ids of the friend for both the current user and the user who invited him
            dao_user.update_info_friend(current_user_id, invited_by_id, invited_by_email, invited)
        next_state = __find_next_state(current_state)
        dao_user.update_user_email_nick(current_user_id, email, nickname, next_state)

        user = dao_user.load_user_data(current_user_id)
        current_state = user['current_state']

    return current_state, error_msg, invited_by_email, invited


def __manage_insert_nick_email_friend(current_state, current_user_id, current_user_email, form, invited, mail):
    # retrieve values of the requested parameters

    error_msg = None
    friend_nickname = form.get('friend_nickname')
    friend_email = form.get('friend_email')
    friend_pronoun = form.get('friend_pronoun')

    print(friend_email, friend_nickname, friend_pronoun)

    if not invited:
        # TODO: Send the invitation!!!
        utils.send_invite_friend(friend_email, current_user_email, mail)
        print("TODO: SEND EMAIL INVITATION")

    # find new state to update it
    next_state = __find_next_state(current_state)
    dao_user.update_friend_info(current_user_id, friend_email, friend_nickname, friend_pronoun, next_state)

    user = dao_user.load_user_data(current_user_id)
    current_state = user['current_state']
    return current_state, error_msg


def __manage_insert_age_gender(current_state, current_user_id, form, invited):
    # retrieve values of the requested parameters

    error_msg = None
    age = form.get('age')
    gender = form.get('gender')
    pronoun = form.get('pronoun')

    print(age, gender)

    # find new state to update it
    next_state = __find_next_state(current_state)
    dao_user.update_demographics(current_user_id, age, gender, pronoun, next_state)

    user = dao_user.load_user_data(current_user_id)
    current_state = user['current_state']
    return current_state, error_msg


def __manage_insert_ffm(current_state, current_user_id, form, invited):
    # retrieve values of the requested parameters

    error_msg = None
    agreeableness = float(form.get('agreeableness'))
    agreeableness_swap = form.get('agreeableness_swap')
    conscentiousness = float(form.get('conscentiousness'))
    conscentiousness_swap = form.get('conscentiousness_swap')
    extraversion = float(form.get('extraversion'))
    extraversion_swap = form.get('extraversion_swap')
    emotional_stability = float(form.get('emotional_stability'))
    emotional_stability_swap = form.get('emotional_stability_swap')
    openess = float(form.get('openess'))
    openess_swap = form.get('openess_swap')
    attention = float(form.get('attention_check'))
    attention_swap = form.get('attention_check_swap')

    print(agreeableness_swap)

    if "True" == agreeableness_swap:
        agreeableness = 162 - (agreeableness - 18)
    if "True" == conscentiousness_swap:
        conscentiousness = 162 - (conscentiousness - 18)
    if "True" == extraversion_swap:
        extraversion = 162 - (extraversion - 18)
    if "True" == emotional_stability_swap:
        emotional_stability = 162 - (emotional_stability - 18)
    if "True" == openess_swap:
        openess = 162 - (openess - 18)
    # if "True" == attention_swap:
    #     attention = 162 - (attention - 18)

    if attention > ((162+18) / 2):
        attention_passed = True
    else:
        attention_passed = False

    # find new state to update it
    next_state = __find_next_state(current_state)
    current_session = db_utils.get_current_session()
    if current_session == 1:
        dao_user.update_self_ffm(current_user_id, agreeableness, conscentiousness,
            extraversion, emotional_stability, openess, attention_passed, next_state)
    else:
        dao_user.update_friend_ffm_and_update_user(current_user_id, agreeableness, conscentiousness,
                                                   extraversion, emotional_stability, openess, attention_passed, next_state)
        # dao_user.update_user_status(current_user_id, next_state)
    user = dao_user.load_user_data(current_user_id)
    current_state = user['current_state']
    return current_state, error_msg


def __manage_insert_roci(current_state, current_user_id, form, invited):
    # retrieve values of the requested parameters

    error_msg = None
    integrating_questions = (1, 4, 5, 12, 22, 23, 28)
    obliging_questions = (2, 10, 11, 13, 19, 24)
    dominating_questions = (8, 9, 18, 21, 25)
    avoiding_questions = (3, 6, 16, 17, 26, 27)
    compromising_questions = (7, 14, 15, 20)

    integrating_values = list(int(form.get("question_" + str(i))) for i in list(integrating_questions))
    obliging_values = list(int(form.get("question_" + str(i))) for i in list(obliging_questions))
    dominating_values = list(int(form.get("question_" + str(i))) for i in list(dominating_questions))
    avoiding_values = list(int(form.get("question_" + str(i))) for i in list(avoiding_questions))
    compromising_values = list(int(form.get("question_" + str(i))) for i in list(compromising_questions))

    integrating = sum(integrating_values) / len(integrating_values)
    obliging = sum(obliging_values) / len(obliging_values)
    dominating = sum(dominating_values) / len(dominating_values)
    avoiding = sum(avoiding_values) / len(avoiding_values)
    compromising = sum(compromising_values) / len(compromising_values)

    attention = int(form.get("question_29"))

    if attention == 5:
        attention_passed = True
    else:
        attention_passed = False

    # find new state to update it
    next_state = __find_next_state(current_state)
    current_session = db_utils.get_current_session()
    print(next_state)
    if current_session == 1:
        dao_user.update_self_roci(current_user_id, integrating, obliging,
            dominating, avoiding, compromising, attention_passed, next_state)
    else:
        dao_user.update_friend_roci_and_update_user(current_user_id, integrating, obliging,
                                                    dominating, avoiding, compromising, attention_passed, next_state)
        # dao_user.update_user_status(current_user_id, next_state)
    user = dao_user.load_user_data(current_user_id)
    current_state = user['current_state']
    return current_state, error_msg


def __manage_insert_individual_evaluations(current_state, current_user_id, form, invited):
    # find new state to update it
    next_state = __find_next_state(current_state)
    print(next_state)

    error_message = None
    song_evals_list = list()
    for i in range(config.TRACK_NUMBER):
        song_evals_dict = dict()
        song_evals_dict["song_eval"] = float(form.get("SONG_" + str(i)))
        song_evals_dict["song_id"] = form.get("SONG_" + str(i) + "_SONG_ID")
        song_evals_list.append(song_evals_dict)
    attention = float(form.get("SONG_" + str(config.TRACK_NUMBER)))
    if attention >= 75:
        attention_passed = True
    else:
        attention_passed = False

    dao_playlist.update_individual_evaluations_and_update_user(
        current_user_id, song_evals_list, attention_passed, next_state)
    # dao_user.update_user_status(current_user_id, next_state)
    user = dao_user.load_user_data(current_user_id)
    current_state = user['current_state']
    return current_state, error_message


def __manage_insert_group_eval(current_state, current_user_id, form, invited, relationship):
    # find new state to update it
    next_state = __find_next_state(current_state)
    print(next_state)

    error_message = None
    song_evals_list = list()
    for i in range(config.TRACK_NUMBER):
        song_evals_dict = dict()
        print("SONG_" + str(i))
        print(form.get("SONG_" + str(i)))
        song_evals_dict["song_eval"] = float(form.get("SONG_" + str(i)))
        song_evals_dict["song_id"] = form.get("SONG_" + str(i) + "_SONG_ID")
        song_evals_dict["relationship"] = relationship
        song_evals_list.append(song_evals_dict)

    attention = float(form.get("SONG_" + str(config.TRACK_NUMBER)))
    if attention >= 75:
        attention_passed = True
    else:
        attention_passed = False

    dao_playlist.update_group_evaluations_and_update_user(
        current_user_id, song_evals_list, attention_passed, next_state)
    # dao_user.update_user_status(current_user_id, next_state)
    user = dao_user.load_user_data(current_user_id)
    current_state = user['current_state']
    return current_state, error_message


def __manage_start_session_one(current_state, current_user_id, form, invited):
    error_msg = None

    # find new state to update it
    next_state = __find_next_state(current_state)
    dao_user.update_user_status(current_user_id, next_state)

    user = dao_user.load_user_data(current_user_id)
    current_state = user['current_state']
    return current_state, error_msg


def __manage_start_session_two(current_state, current_user_id, form, invited):
    error_msg = None

    # find new state to update it
    next_state = __find_next_state(current_state)
    dao_user.update_user_status(current_user_id, next_state)

    user = dao_user.load_user_data(current_user_id)
    current_state = user['current_state']
    return current_state, error_msg


def __manage_start_session_three(current_state, current_user_id, form, invited):
    error_msg = None

    # find new state to update it
    next_state = __find_next_state(current_state)
    dao_user.update_user_status(current_user_id, next_state)

    user = dao_user.load_user_data(current_user_id)
    current_state = user['current_state']
    return current_state, error_msg


def __retrieve_required_parameters_values(params, required_parameters):
    required_parameters_values = list()
    for param in required_parameters:
        required_parameters_values.append(params[param])
    return required_parameters_values


def __find_next_state(current_state):
    print("===== FIND NEXT STATE =====")
    current_session = db_utils.get_current_session()
    current_state_index = config.STATUSES[current_session].index(current_state)
    next_state_index = current_state_index + 1

    print("current state: ", current_state)
    print("current state index: ", current_state_index)

    if next_state_index >= len(config.STATUSES[current_session]):
        next_state_index = len(config.STATUSES[current_session])

    next_state = config.STATUSES[current_session][next_state_index]
    print("next state: ", next_state)
    print("next state index: ", next_state_index)
    print("============================")
    return next_state


def __create_missing_parameters_msg(missing_parameters):
    if not missing_parameters:
        return None
    else:
        return "Please insert all the required information"


def __create_string_for_preferred_pronouns(user, current_session, string, relationship=None):
    if current_session == 1:
        nickname = user['nickname']
        pronoun_key = int(user['pronoun'])
    else:
        nickname = user['friend_nickname']
        pronoun_key = int(user['friend_pronoun'])

    nickname_peer = ""
    if relationship:
        if relationship == 'friend':
            nickname_peer = user['friend_nickname']
        else:
            nickname_peer = user['stranger_nickname']

    print(nickname, nickname_peer, pronoun_key)
    string = string.replace("<Nickname>", nickname.capitalize())\
        .replace("<Nickname_peer>", nickname_peer.capitalize())\
        .replace("<Subject>", config.PRONOUNS[pronoun_key]['SUBJECT'].capitalize())\
        .replace("<subject>", config.PRONOUNS[pronoun_key]['SUBJECT'])\
        .replace("<object>", config.PRONOUNS[pronoun_key]['OBJECT'])\
        .replace("<possessive_adj>", config.PRONOUNS[pronoun_key]['POSSESSIVE_ADJ']) \
        .replace("<possessive>", config.PRONOUNS[pronoun_key]['POSSESSIVE'])\
        .replace("<reflexive>", config.PRONOUNS[pronoun_key]['REFLEXIVE'])\
        .replace("<to_be_con>", config.PRONOUNS[pronoun_key]['TO_BE_CON'])\
        .replace("<to_have_con>", config.PRONOUNS[pronoun_key]['TO_HAVE_CON'])\
        .replace("<to_carry_con>", config.PRONOUNS[pronoun_key]['TO_CARRY_CON'])\
        .replace("<to_worry_con>", config.PRONOUNS[pronoun_key]['TO_WORRY_CON'])\
        .replace("<to_try_con>", config.PRONOUNS[pronoun_key]['TO_TRY_CON'])\
        .replace("<verb_con>", config.PRONOUNS[pronoun_key]['VERB_CON'])\
        .replace("<irr_verb_con>", config.PRONOUNS[pronoun_key]['IRR_VERB_CON'])

    return string


def generate_ffm_dict(user_id):
    user = dao_user.load_user_data(user_id)
    current_session = db_utils.get_current_session()

    ffm_dict = dict()
    ffm_dict['instruction'] = __create_string_for_preferred_pronouns(user, current_session, config.FFM_INSTRUCTION[current_session])
    ffm_dict['instruction_short'] = __create_string_for_preferred_pronouns(user, current_session, config.FFM_INSTRUCTION_SHORT[current_session])
    ffm_dict['title'] = __create_string_for_preferred_pronouns(user, current_session, config.FFM_TITLE[current_session])
    ffm_dict['questionnaire'] = list()
    indexes = [i for i in range(len(config.FFM_STORIES))]
    random.shuffle(indexes)
    for i in range(len(config.FFM_STORIES)):
        trait_story = config.FFM_STORIES[indexes[i]]
        input_id = trait_story['INPUT_ID']
        low_story = __create_string_for_preferred_pronouns(user, current_session, trait_story['LOW_STORY'])
        high_story = __create_string_for_preferred_pronouns(user, current_session, trait_story['HIGH_STORY'])
        swap_stories = bool(random.getrandbits(1))
        ffm_dict['questionnaire'].append(
            {
                'INPUT_ID': input_id,
                'LOW_STORY': low_story,
                'HIGH_STORY': high_story,
                'SWAP': swap_stories
            }
        )
    return ffm_dict


def generate_roci_dict(user_id):
    user = dao_user.load_user_data(user_id)
    current_session = db_utils.get_current_session()

    roci_dict = dict()
    roci_dict['instruction'] = __create_string_for_preferred_pronouns(user, current_session, config.ROCI_INSTRUCTIONS[current_session])
    roci_dict['instruction_short'] = __create_string_for_preferred_pronouns(user, current_session, config.ROCI_INSTRUCTIONS_SHORT[current_session])
    roci_dict['title'] = __create_string_for_preferred_pronouns(user, current_session, config.ROCI_TITLE[current_session])
    roci_dict['questionnaire'] = list()

    if current_session == 1:
        questionnaire = config.ROCI_QUESTIONS_SELF
    else:
        questionnaire = config.ROCI_QUESTIONS_PEER

    print(len(questionnaire)+1)
    indexes = list(range(1, len(questionnaire)+1))
    print(indexes)
    random.shuffle(indexes)

    for i in indexes:
        question = questionnaire[i]
        input_id = i
        print(i, question)
        question_text = __create_string_for_preferred_pronouns(user, current_session, question)
        roci_dict['questionnaire'].append(
            {
                'INPUT_ID': input_id,
                'QUESTION_TEXT': question_text
            }
        )
    return roci_dict


def generate_individual_songs_dict(user_id):
    user = dao_user.load_user_data(user_id)
    current_session = db_utils.get_current_session()

    individual_songs_dict = dict()
    individual_songs_dict['instruction'] = __create_string_for_preferred_pronouns(user, current_session, config.IND_EVAL_INSTRUCTIONS)
    individual_songs_dict['instruction_short'] = __create_string_for_preferred_pronouns(user, current_session, config.IND_EVAL_INSTRUCTIONS_SHORT)
    individual_songs_dict['title'] = __create_string_for_preferred_pronouns(user, current_session, config.IND_EVAL_TITLE)
    individual_song_id_list = dao_playlist.load_songs_for_user(user_id)
    individual_song_list = list()
    attention_index = random.randint(0, config.TRACK_NUMBER)
    print(attention_index)
    for index, song_id in zip(range(config.TRACK_NUMBER), individual_song_id_list):
        print(index)
        song = dict()
        song['attention'] = False
        song['SONG_INDEX'] = index
        song['SONG_ID'] = song_id
        song['SONG_URL'] = helper.get_track_embed_uri(song_id)
        individual_song_list.append(song)
        if index == attention_index:
            song = dict()
            song['attention'] = True
            song['SONG_INDEX'] = config.TRACK_NUMBER
            song['SONG_ID'] = 'attention'
            song['SONG_URL'] = 'no_url'
            individual_song_list.append(song)

    individual_songs_dict['individual_song_list'] = individual_song_list

    return individual_songs_dict


def generate_group_songs_dict(user_id, relationship):
    user = dao_user.load_user_data(user_id)
    current_session = db_utils.get_current_session()

    group_songs_dict = dict()
    group_songs_dict['instruction'] = __create_string_for_preferred_pronouns(user, current_session, config.GROUP_EVAL_INSTRUCTIONS[relationship], relationship)
    group_songs_dict['instruction_short'] = __create_string_for_preferred_pronouns(user, current_session, config.GROUP_EVAL_INSTRUCTIONS_SHORT[relationship], relationship)
    group_songs_dict['title'] = __create_string_for_preferred_pronouns(user, current_session, config.GROUP_EVAL_TITLE[relationship], relationship)
    group_songs_dict['self_eval_message'] = __create_string_for_preferred_pronouns(user, current_session, config.GROUP_SELF_EVAL_MSG, relationship)
    group_songs_dict['peer_eval_message'] = __create_string_for_preferred_pronouns(user, current_session, config.GROUP_PEER_EVAL_MSG, relationship)

    group_song_id_list = dao_playlist.load_songs_for_user_for_group_eval(user_id, relationship)
    group_song_list = list()

    attention_index = random.randint(0, config.TRACK_NUMBER)
    print("ATTENTION", attention_index)

    for index, song_to_eval in zip(range(config.TRACK_NUMBER), group_song_id_list):
        print(index)
        song = dict()
        song['SONG_INDEX'] = index
        song['SONG_ID'] = song_to_eval['SONG_ID']
        song['SELF_EVAL'] = song_to_eval['SELF_EVAL']
        song['PEER_EVAL'] = song_to_eval['PEER_EVAL']
        song['SONG_URL'] = helper.get_track_embed_uri(song_to_eval['SONG_ID'])
        group_song_list.append(song)
        if index == attention_index:
            song = dict()
            song['attention'] = True
            song['SONG_INDEX'] = config.TRACK_NUMBER
            song['SONG_ID'] = 'attention'
            song['SONG_URL'] = 'no_url'
            song['SELF_EVAL'] = 100
            song['PEER_EVAL'] = 100
            group_song_list.append(song)
    print("songs", len(group_song_list))
    group_songs_dict['individual_song_list'] = group_song_list

    return group_songs_dict

def manage_offline_pairing(current_user_id):
    # 1) check if user_id is admin, if not return error no admin page
    # 2) if admin, go on

    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return config.ERROR_VIEW_DICT['INVALID_USER'], None, None

    if not user["is_admin"]:
        # the user is not an admin
        return config.ERROR_VIEW_DICT['NO_ADMIN_USER'], None, None

    # __remove_pairs_songs_from_playlists()

    __generate_strangers_pairs()

    __complete_playlists()

    return config.ADMIN_VIEW_DICT['PROCESS_COMPLETED'], None, None


def __remove_pairs_songs_from_playlists():
    print("REMOVING PAIRS SONGS FROM PLAYLISTS")
    dao_playlist.remove_pairs_songs_from_playlists()

def __generate_strangers_pairs():
    print("RECOVERING ORIGINAL PAIRS")
    friends_pairs_list = dao_user.load_friends_pairs_list()
    print(friends_pairs_list)

    not_completed = dao_user.load_not_completed_session1_list()
    print("NOT COMPLETED", not_completed)

    completed_pairs, not_completed_pairs = __filter_pairs(friends_pairs_list,not_completed)
    print("COMPLETED AND NOT COMPLETED PAIRS")
    print(completed_pairs)
    print(not_completed_pairs)

    print("GENERATE STRANGERS PAIRS")

    strangers_pairs_list = utils.create_random_pairs_from_pairs_list(completed_pairs)
    print(strangers_pairs_list)

    print("UPDATING DB")
    dao_user.update_strangers_from_pairs_list(strangers_pairs_list)

    print("UPDATE USER STATUSES")
    dao_user.set_uncomplete_end_state(not_completed_pairs)
    dao_user.set_session_two_state(completed_pairs)

    return strangers_pairs_list


def __filter_pairs(friends_pairs_list,not_completed):
    completed_pairs = list()
    not_completed_pairs = list()

    for pair in friends_pairs_list:
        if pair[0] in not_completed or pair[1] in not_completed:
            not_completed_pairs.append(pair)
        else:
            completed_pairs.append(pair)
    return completed_pairs, not_completed_pairs



def __complete_playlists():
    relationships_dict = dao_user.load_relationships_dict()
    print(relationships_dict)
    songs_dict = dao_playlist.load_songs_dict_for_all_users()
    print(songs_dict)

    for user_id in relationships_dict:
        friend_id = relationships_dict[user_id]['friend_id']
        stranger_id = relationships_dict[user_id]['stranger_id']

        friends_songs_to_add = songs_dict[friend_id]
        stranger_songs_to_add = songs_dict[stranger_id]

        # print("Adding songs for user " + user_id + " friend playlist")
        # dao_playlist.add_songs_to_user_playlist(user_id, friends_songs_to_add, 'friend', friend_id)
        dao_playlist.update_pair_id_for_original_songs(user_id, 'friend', friend_id)

        # print("Adding songs for user " + user_id + " stranger playlist")
        # dao_playlist.add_songs_to_user_playlist(user_id, stranger_songs_to_add, 'stranger', stranger_id)
        dao_playlist.update_pair_id_for_original_songs(user_id, 'stranger', stranger_id)

    playlist_table_list = dao_playlist.load_playlists_table()

    for eval_dict in playlist_table_list:
        original_song_id = eval_dict["song_id"]
        original_user_id = eval_dict["user_id"]
        original_self_eval = eval_dict["self_eval"]
        original_peer_id = eval_dict["peer_id"]

        dao_playlist.update_peer_evaluation(original_peer_id, original_user_id, original_song_id, original_self_eval)




def start_session_two(current_user_id):
    # 1) check if user_id is admin, if not return error no admin page
    # 2) if admin, go on

    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return config.ERROR_VIEW_DICT['INVALID_USER'], None, None

    if not user["is_admin"]:
        # the user is not an admin
        return config.ERROR_VIEW_DICT['NO_ADMIN_USER'], None, None

    dao_user.start_session_two()
    dao_session_info.update_current_session(2)

    return config.ADMIN_VIEW_DICT['PROCESS_COMPLETED'], None, None
#
#
# def start_session_three(current_user_id):
#     # 1) check if user_id is admin, if not return error no admin page
#     # 2) if admin, go on
#
#     user = dao_user.load_user_data(current_user_id)
#
#     if not user:
#         # the user is not in the DB
#         return config.ERROR_VIEW_DICT['INVALID_USER'], None, None
#
#     if not user["is_admin"]:
#         # the user is not an admin
#         return config.ERROR_VIEW_DICT['NO_ADMIN_USER'], None, None
#
#     dao_user.start_session_three()
#     dao_session_info.update_current_session(3)
#
#     return config.ADMIN_VIEW_DICT['PROCESS_COMPLETED'], None, None


def start_next_session(current_user_id):
    # 1) check if user_id is admin, if not return error no admin page
    # 2) if admin, go on

    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return config.ERROR_VIEW_DICT['INVALID_USER'], None, None

    if not user["is_admin"]:
        # the user is not an admin
        return config.ERROR_VIEW_DICT['NO_ADMIN_USER'], None, None

    current_session = dao_session_info.load_current_session()

    if current_session==1:
        # Offline pairing
        # __remove_pairs_songs_from_playlists()
        __generate_strangers_pairs() # GENERATES PAIRS OF STRANGERS AND SAVES THEM IN THE USER_APP TABLE
        __complete_playlists() # SAVES PAIRS EVALUATIONS

        # Start session 2
        # dao_user.start_session_two()
        dao_session_info.update_current_session(2)
        __send_notification_start_session(2)
    # elif current_session==2:
    #
    #     # Start session 3
    #     dao_user.start_session_three()
    #     dao_session_info.update_current_session(3)
    #     __send_notification_start_session(3)

    # LOAD INFO FOR ADMIN DASHBOARD
    current_state, error_msg, add_to_session = __load_users_info()

    return config.ADMIN_VIEW_DICT[current_state], None, None


def change_is_user(current_user_id, user_to_remove, user_to_add):
    # 1) check if user_id is admin, if not return error no admin page
    # 2) if admin, go on

    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return config.ERROR_VIEW_DICT['INVALID_USER'], None, None

    if not user["is_admin"]:
        # the user is not an admin
        return config.ERROR_VIEW_DICT['NO_ADMIN_USER'], None, None

    if user_to_add:
        user_id = user_to_add
        is_user = True
    else:
        user_id = user_to_remove
        is_user = False

    dao_user.change_is_user(user_id, is_user)

    # LOAD INFO FOR ADMIN DASHBOARD
    current_state, error_msg, add_to_session = __load_users_info()

    return config.ADMIN_VIEW_DICT[current_state], error_msg, add_to_session


def __send_notification_start_session(session_to_start):
    user_email_list = dao_user.get_user_email_list()
    for email in user_email_list:
        utils.send_email_start_session(email, session_to_start)


def manage_submit_admin(current_user_id):
    # 1) check if user_id is admin, if not return error no admin page
    # 2) if admin, go on

    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return config.ERROR_VIEW_DICT['INVALID_USER'], None, None

    if not user["is_admin"]:
        # the user is not an admin
        return config.ERROR_VIEW_DICT['NO_ADMIN_USER'], None, None

    # LOAD INFO FOR ADMIN DASHBOARD
    current_state, error_msg, add_to_session = __load_users_info()

    return config.ADMIN_VIEW_DICT[current_state], error_msg, add_to_session


def manage_download_users_admin(current_user_id):
    # 1) check if user_id is admin, if not return error no admin page
    # 2) if admin, go on

    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return config.ERROR_VIEW_DICT['INVALID_USER'], None, None

    if not user["is_admin"]:
        # the user is not an admin
        return config.ERROR_VIEW_DICT['NO_ADMIN_USER'], None, None

    # LOAD INFO FOR ADMIN DASHBOARD
    json = dao_user.load_users_table_as_json()

    return config.ADMIN_VIEW_DICT['ADMIN_DASHBOARD'], "OK", json


def manage_download_playlists_admin(current_user_id):
    # 1) check if user_id is admin, if not return error no admin page
    # 2) if admin, go on

    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return config.ERROR_VIEW_DICT['INVALID_USER'], None, None

    if not user["is_admin"]:
        # the user is not an admin
        return config.ERROR_VIEW_DICT['NO_ADMIN_USER'], None, None

    # LOAD INFO FOR ADMIN DASHBOARD
    json = dao_playlist.load_playlists_table_as_json()

    return config.ADMIN_VIEW_DICT['ADMIN_DASHBOARD'], "OK", json


def manage_load_admin_stats(current_user_id):
    # 1) check if user_id is admin, if not return error no admin page
    # 2) if admin, go on

    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return config.ERROR_VIEW_DICT['INVALID_USER'], None, None

    if not user["is_admin"]:
        # the user is not an admin
        return config.ERROR_VIEW_DICT['NO_ADMIN_USER'], None, None

    # LOAD INFO FOR ADMIN DASHBOARD
    current_state, error_msg, add_to_session = __load_admin_stats()

    return config.ADMIN_VIEW_DICT[current_state], error_msg, add_to_session


def __load_admin_stats():
    add_to_session = dict()

    # load initial evaluations ratings
    songs_eval = dao_playlist.load_songs_self_eval()
    bins = dict()
    bins[-1] = 0
    for i in range(10):
        # bins[i] = randint(1,100)
        bins[i] = 0

    for song_eval in songs_eval:
        if song_eval == 100:
            bins[9] = bins[9] + 1
        else:
            bins[floor(song_eval/10)] = bins[floor(song_eval/10)] + 1

    add_to_session['self_evals'] = bins

    # load self and peer evaluations for FFM traits
    personality_values = dao_user.load_personality_values()
    for instrument in config.PERSONALITY_INSTRUMENTS:
        for trait in config.PERSONALITY_TRAITS[instrument]:
            add_to_session[instrument + '_' + trait] = __generate_bins_trait(
                personality_values[instrument][trait], 5,
                config.PERSONALITY_INSTRUMENT_MIN_VALUE[instrument], config.PERSONALITY_INSTRUMENT_MAX_VALUE[instrument])

    # bins = dict()
    # bins[-1] = 0
    # for i in range(10):
    #     # bins[i] = randint(1,100)
    #     bins[i] = 0
    #
    # for song_eval in songs_eval:
    #     if song_eval == 100:
    #         bins[9] = bins[9] + 1
    #     else:
    #         bins[floor(song_eval/10)] = bins[floor(song_eval/10)] + 1
    #
    # add_to_session['self_evals'] = bins

    return 'ADMIN_STATS', None, add_to_session


def __generate_bins_trait(personality_trait_values, n_bins, min, max):
    returned_bins = {
        'SELF' : None, 'PEER' : None
    }

    bins = dict()
    for i in range(n_bins):
        bins[i] = 0

    #SELF
    for val in personality_trait_values['SELF']:
        if val == max:
            bins[n_bins-1] = bins[n_bins-1] + 1
        else:
            norm_val = n_bins * ((val-min)/(max-min))
            print(val, norm_val)
            bins[floor(norm_val)] = bins[floor(norm_val)] + 1

    returned_bins['SELF'] = bins

    #PEER
    bins = dict()
    for i in range(n_bins):
        bins[i] = 0

    for val in personality_trait_values['PEER']:
        if val == max:
            bins[n_bins - 1] = bins[n_bins - 1] + 1
        else:
            norm_val = n_bins * ((val - min) / (max - min))
            print(val, norm_val)
            bins[floor(norm_val)] = bins[floor(norm_val)] + 1

    returned_bins['PEER'] = bins

    print(returned_bins)
    return returned_bins

def __load_users_info():
    add_to_session = dict()
    add_to_session['users_info'] = dao_user.load_all_users()
    current_session = db_utils.get_current_session()
    add_to_session['current_session'] = current_session
    if current_session < 2:
        add_to_session['next_session_button'] = "Start Session " + str(int(current_session)+1)
    else:
        add_to_session['next_session_button'] = "---"
    add_to_session['current_session_statuses'] = config.STATUSES[current_session]

    return 'ADMIN_DASHBOARD', None, add_to_session

def get_session_url():
    current_session = db_utils.get_current_session()
    if current_session == 1:
        return 'session_one'
    elif current_session == 2:
        return 'session_two'
    elif current_session == 3:
        return 'session_three'
    else:
        return 'session_close'

def get_admin_url():
    return 'admin'


def is_current_session(session_number):
    current_session = db_utils.get_current_session()
    if current_session == session_number:
        return True
    else:
        return False


def get_spotify_app_configurations():
    return config.client_id, config.client_secret, config.scope

def get_google_app_configurations():
    return config.client_id, config.client_secret, config.google_discovery_url


def get_mail_settings():
    return config.mail_settings


def get_session_route(current_session):
    return config.SESSION_ROUTE[current_session]


def get_link_invited():
    return "https://<Host>:5000/consent_form_invited".replace("<Host>", config.HOST)


def get_port():
    return config.PORT


def get_url_for_server_mode(url):
    if config.SERVER_MODE:
        return url.replace('http://', 'https://', 1)
    else:
        return url

def get_percentage_comp(current_state):
    return config.PERCENTAGE_COMP[current_state]


def is_server_mode():
    return config.SERVER_MODE