import sys
import random

from dao import dao_user, dao_playlist, dao_session_info, db_utils
import config

from utils import utils, spotify_utils as helper

sys.path.append('../')


def manage_logged_user(current_user_id, invited, sp):
    """
    Check if the user is in the DB. If not, it creates the instances for the user
    :param current_user_id:
    :param sp:
    :return:
    """

    # check if the user exists in the DB: load user info, if the user doesn't exist we receive an empty dict
    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        # we create a new user with the given id

        is_user = True
        is_admin = False

        if current_user_id in config.ADMIN_USER_ID_LIST:
            is_admin = True

        #TODO: CREATE TRANSACTION ? IF THE USER IS CREATED AND THE SONGS ARE NOT INITIALIZED?
        dao_user.create_new_user(current_user_id, invited, is_user, is_admin)

        # select the tracks for the user

        top_track_ids = helper.get_selected_tracks(sp)

        print("selected tracks: ", len(top_track_ids))

        dao_playlist.create_basic_playlists_for_user(current_user_id, top_track_ids)

        user = dao_user.load_user_data(current_user_id)

        # # Here get track information and audio features as well and save them to DB!
        # tracks_dict, tracks_audio_dict = help.get_track_information(sp, top_track_ids)
        #
        # # Insert the tracks to DB!
        # generate_insert_tracks_query(tracks_dict, tracks_audio_dict)
        # query, params = update_users_top_tracks(top_track_ids, current_user_id)
        # db_insert(query, params)
        # query, params = insert_users_top_tracks(current_user_id, top_track_ids)
        # db_insert(query, params)

    return user, config.CURRENT_VIEW_DICT[user['current_state']]


def get_current_view_for_user(current_user_id):
    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return None, config.ERROR_VIEW_DICT['INVALID_USER']

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

    invited = user['is_invited']
    current_state, error_msg, add_to_session = __perform_submit(user['current_state'], user, invited, form, mail)

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

    if current_state == 'INSERT_EMAIL_NICK':
        current_state, error_msg, email_friend = __manage_insert_nick_email(current_state, current_user_id, form, invited)
        add_to_session['email_friend'] = email_friend
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
        add_to_session['ROCI'] = generate_roci_dict(current_user_id)
    elif current_state == 'START_SESSION_2':
        current_state, error_msg = __manage_start_session_two(current_state, current_user_id, form, invited)
        add_to_session['FFM'] = generate_ffm_dict(current_user_id)
    elif current_state == 'INSERT_FRIEND_FFM':
        current_state, error_msg = __manage_insert_ffm(current_state, current_user_id, form, invited)
        add_to_session['ROCI'] = generate_roci_dict(current_user_id)
    elif current_state == 'INSERT_FRIEND_ROCI':
        current_state, error_msg = __manage_insert_roci(current_state, current_user_id, form, invited)
        add_to_session['INDIVIDUAL_SONGS'] = generate_individual_songs_dict(current_user_id)
    elif current_state == 'EVALUATE_SONGS_INDIVIDUAL':
        current_state, error_msg = __manage_insert_individual_evaluations(current_state, current_user_id, form, invited)
    elif current_state == 'START_SESSION_3':
        current_state, error_msg = __manage_start_session_three(current_state, current_user_id, form, invited)
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
        # find new state to update it
        if invited:
            # update ids of the friend for both the current user and the user who invited him
            dao_user.update_id_friend(current_user_id, invited_by_id)
        next_state = __find_next_state(current_state)
        dao_user.update_user_email_nick(current_user_id, email, nickname, next_state)

        user = dao_user.load_user_data(current_user_id)
        current_state = user['current_state']

    return current_state, error_msg, invited_by_email


def __manage_insert_nick_email_friend(current_state, current_user_id, current_user_email, form, invited, mail):
    # retrieve values of the requested parameters

    error_msg = None
    friend_nickname = form.get('friend_nickname')
    friend_email = form.get('friend_email')

    print(friend_email, friend_nickname)

    if not invited:
        # TODO: Send the invitation!!!
        utils.send_invite_friend(friend_email, current_user_email, mail)
        print("TODO: SEND EMAIL INVITATION")

    # find new state to update it
    next_state = __find_next_state(current_state)
    dao_user.update_friend_email_nick(current_user_id, friend_email, friend_nickname, next_state)

    user = dao_user.load_user_data(current_user_id)
    current_state = user['current_state']
    return current_state, error_msg


def __manage_insert_age_gender(current_state, current_user_id, form, invited):
    # retrieve values of the requested parameters

    error_msg = None
    age = form.get('age')
    gender = form.get('gender')

    print(age, gender)

    # find new state to update it
    next_state = __find_next_state(current_state)
    dao_user.update_age_gender(current_user_id, age, gender, next_state)

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
    for i in range(3*config.TRACK_TO_SELECT):
        song_evals_dict = dict()
        song_evals_dict["song_eval"] = float(form.get("SONG_" + str(i)))
        song_evals_dict["song_id"] = form.get("SONG_" + str(i) + "_SONG_ID")
        song_evals_list.append(song_evals_dict)
    attention = float(form.get("SONG_" + str(3*config.TRACK_TO_SELECT)))
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
    for i in range(2*config.TRACK_TO_SELECT):
        song_evals_dict = dict()
        print("SONG_" + str(i))
        print(form.get("SONG_" + str(i)))
        song_evals_dict["song_eval"] = float(form.get("SONG_" + str(i)))
        song_evals_dict["song_id"] = form.get("SONG_" + str(i) + "_SONG_ID")
        song_evals_dict["relationship"] = relationship
        song_evals_list.append(song_evals_dict)

    attention = float(form.get("SONG_" + str(2*config.TRACK_TO_SELECT)))
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
    current_session = db_utils.get_current_session()
    next_state_index = config.STATUSES[current_session].index(current_state) + 1
    if next_state_index >= len(config.STATUSES[current_session]):
        next_state_index = len(config.STATUSES[current_session])
    return config.STATUSES[current_session][next_state_index]


def __create_missing_parameters_msg(missing_parameters):
    if not missing_parameters:
        return None
    else:
        return "Please insert all the required information"


def generate_ffm_dict(user_id):
    user = dao_user.load_user_data(user_id)
    current_session = db_utils.get_current_session()
    if current_session == 1:
        nickname = user['nickname']
    else:
        nickname = user['friend_nickname']
    nickname = nickname.title()
    ffm_dict = dict()
    ffm_dict['instruction'] = config.FFM_INSTRUCTION[current_session].replace("<Nickname>", nickname)
    ffm_dict['instruction_short'] = config.FFM_INSTRUCTION_SHORT[current_session].replace("<Nickname>", nickname)
    ffm_dict['title'] = config.FFM_TITLE[current_session].replace("<Nickname>", nickname)
    ffm_dict['questionnaire'] = list()
    indexes = [i for i in range(len(config.FFM_STORIES))]
    random.shuffle(indexes)
    for i in range(len(config.FFM_STORIES)):
        trait_story = config.FFM_STORIES[indexes[i]]
        input_id = trait_story['INPUT_ID']
        low_story = trait_story['LOW_STORY'].replace("<Nickname>", nickname)
        high_story = trait_story['HIGH_STORY'].replace("<Nickname>", nickname)
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
    if current_session == 1:
        nickname = user['nickname']
    else:
        nickname = user['friend_nickname']
    nickname = nickname.title()
    roci_dict = dict()
    roci_dict['instruction'] = config.ROCI_INSTRUCTIONS[current_session].replace("<Nickname>", nickname)
    roci_dict['instruction_short'] = config.ROCI_INSTRUCTIONS_SHORT[current_session].replace("<Nickname>", nickname)
    roci_dict['title'] = config.ROCI_TITLE[current_session].replace("<Nickname>", nickname)
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
        question_text = question.replace("<Nickname>", nickname)
        roci_dict['questionnaire'].append(
            {
                'INPUT_ID': input_id,
                'QUESTION_TEXT': question_text
            }
        )
    return roci_dict


def generate_individual_songs_dict(user_id):
    user = dao_user.load_user_data(user_id)
    nickname = user['nickname']

    nickname = nickname.title()
    individual_songs_dict = dict()
    individual_songs_dict['instruction'] = config.IND_EVAL_INSTRUCTIONS.replace("<Nickname>", nickname)
    individual_songs_dict['instruction_short'] = config.IND_EVAL_INSTRUCTIONS_SHORT.replace("<Nickname>",nickname)
    individual_songs_dict['title'] = config.IND_EVAL_TITLE.replace("<Nickname>", nickname)
    individual_song_id_list = dao_playlist.load_songs_for_user(user_id)
    individual_song_list = list()
    attention_index = random.randint(0, 3 * config.TRACK_TO_SELECT)
    print(attention_index)
    for index, song_id in zip(range(3*config.TRACK_TO_SELECT), individual_song_id_list):
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
            song['SONG_INDEX'] = 3*config.TRACK_TO_SELECT
            song['SONG_ID'] = 'attention'
            song['SONG_URL'] = 'no_url'
            individual_song_list.append(song)

    individual_songs_dict['individual_song_list'] = individual_song_list

    return individual_songs_dict


def generate_group_songs_dict(user_id, relationship):
    user = dao_user.load_user_data(user_id)
    nickname = user['nickname']
    if relationship == 'friend':
        nickname_peer = user['friend_nickname']
    else:
        nickname_peer = user['stranger_nickname']

    nickname = nickname.title()
    nickname_peer = nickname_peer.title()
    group_songs_dict = dict()
    group_songs_dict['instruction'] = config.GROUP_EVAL_INSTRUCTIONS[relationship].replace("<Nickname>", nickname_peer)
    group_songs_dict['instruction_short'] = config.GROUP_EVAL_INSTRUCTIONS_SHORT[relationship].replace("<Nickname>", nickname_peer)
    group_songs_dict['title'] = config.GROUP_EVAL_TITLE[relationship].replace("<Nickname>", nickname_peer)
    group_songs_dict['self_eval_message'] = config.GROUP_SELF_EVAL_MSG.replace("<Nickname>", nickname_peer)
    group_songs_dict['peer_eval_message'] = config.GROUP_PEER_EVAL_MSG.replace("<Nickname>", nickname_peer)


    group_song_id_list = dao_playlist.load_songs_for_user_for_group_eval(user_id, relationship)
    group_song_list = list()

    attention_index = random.randint(0, 2 * config.TRACK_TO_SELECT)
    print("ATTENTION", attention_index)

    for index, song_to_eval in zip(range(2 * config.TRACK_TO_SELECT), group_song_id_list):
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
            song['SONG_INDEX'] = 2*config.TRACK_TO_SELECT
            song['SONG_ID'] = 'attention'
            song['SONG_URL'] = 'no_url'
            song['SELF_EVAL'] = 50
            song['PEER_EVAL'] = 50
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

    __remove_pairs_songs_from_playlists()

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

    print("GENERATE STRANGERS PAIRS")
    strangers_pairs_list = utils.create_random_pairs_from_pairs_list(friends_pairs_list)
    print(strangers_pairs_list)

    print("UPDATING DB")
    dao_user.update_strangers_from_pairs_list(strangers_pairs_list)

    return strangers_pairs_list


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

        print("Adding songs for user " + user_id + " friend playlist")
        dao_playlist.add_songs_to_user_playlist(user_id, friends_songs_to_add, 'friend', friend_id)
        dao_playlist.update_pair_id_for_original_songs(user_id, 'friend', friend_id)

        print("Adding songs for user " + user_id + " stranger playlist")
        dao_playlist.add_songs_to_user_playlist(user_id, stranger_songs_to_add, 'stranger', stranger_id)
        dao_playlist.update_pair_id_for_original_songs(user_id, 'stranger', stranger_id)


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


def start_session_three(current_user_id):
    # 1) check if user_id is admin, if not return error no admin page
    # 2) if admin, go on

    user = dao_user.load_user_data(current_user_id)

    if not user:
        # the user is not in the DB
        return config.ERROR_VIEW_DICT['INVALID_USER'], None, None

    if not user["is_admin"]:
        # the user is not an admin
        return config.ERROR_VIEW_DICT['NO_ADMIN_USER'], None, None

    dao_user.start_session_three()
    dao_session_info.update_current_session(3)

    return config.ADMIN_VIEW_DICT['PROCESS_COMPLETED'], None, None


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

def __load_users_info():
    add_to_session = dict()
    add_to_session['users_info'] = dao_user.load_all_users()
    add_to_session['current_session'] = db_utils.get_current_session()

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


def is_current_session(session_number):
    current_session = db_utils.get_current_session()
    if current_session == session_number:
        return True
    else:
        return False


def get_spotify_app_configurations():
    return config.client_id, config.client_secret, config.scope


def get_mail_settings():
    return config.mail_settings


def get_session_route(current_session):
    return config.SESSION_ROUTE[current_session]


def get_port():
    return config.PORT