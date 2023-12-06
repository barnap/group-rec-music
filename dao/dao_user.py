import json
import sys
from collections import defaultdict

sys.path.append('../')
import dao.db_utils as db_utils
import psycopg2
import config
import time
import string
import random
from datetime import datetime
from psycopg2 import pool

from random import choice

from math import ceil;

def load_user_data(user_id):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
        select id,email,nickname,friend_id,friend_nickname,stranger_id,stranger_nickname,current_state,is_invited,is_user,is_admin,pronoun,friend_pronoun
        from user_app
        where id = (%s)
        """, (user_id, ))

    result = cur.fetchone()
    print('Executed the query')
    print(result)
    db.close()

    user_dict = dict()
    if result:
        print(result[0])
        user_dict["id"] = result[0]
        user_dict["email"] = result[1]
        user_dict["nickname"] = result[2]
        user_dict["friend_email"] = result[3]
        user_dict["friend_nickname"] = result[4]
        user_dict["stranger_email"] = result[5]
        user_dict["stranger_nickname"] = result[6]
        user_dict["current_state"] = result[7]
        user_dict["is_invited"] = result[8]
        user_dict["is_user"] = result[9]
        user_dict["is_admin"] = result[10]
        user_dict["pronoun"] = result[11]
        user_dict["friend_pronoun"] = result[12]

    print(user_dict)
    return user_dict


def create_new_user(user_id, invited, is_user, is_admin):
    initial_state = config.STATUSES[1][0]

    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO user_app (id, is_invited, is_user, is_admin, current_state) VALUES (%s, %s, %s, %s, %s)
        """, (user_id, invited, is_user, is_admin, initial_state))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_user_email_nick(user_id, email, nickname, next_state):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE user_app 
        SET email = %s, nickname = %s, current_state = %s
        WHERE id = %s
        """, (email, nickname.title(), next_state, user_id))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def check_user_invited(email):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            select id, email
            from user_app
            where friend_email = (%s)
            """, (email,))

    result = cur.fetchone()
    print('Executed the query')
    db.close()

    if result:
        return result[0], result[1]
    return None, None


def update_friend_info(user_id, friend_email, friend_nickname, friend_pronoun, next_state):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            UPDATE user_app 
            SET friend_email = %s, friend_nickname = %s, friend_pronoun = %s, current_state = %s
            WHERE id = %s
            """, (friend_email, friend_nickname.title(), friend_pronoun, next_state, user_id))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_demographics(user_id, age, gender, pronoun, next_state):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
                UPDATE user_app 
                SET age_group = %s, gender = %s, pronoun = %s, current_state = %s
                WHERE id = %s
                """, (age, gender, pronoun, next_state, user_id))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_self_ffm(user_id, agreeableness, conscentiousness,
        extraversion, emotional_stability, openess, attention_passed, next_state):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
                    UPDATE user_app 
                    SET agreableness_self_eval = %s, 
                    conscentiousness_self_eval = %s,
                    extraversion_self_eval = %s,
                    emotional_stability_self_eval = %s,
                    openess_self_eval = %s,current_state = %s,
                    attention_ffm_self = %s
                    WHERE id = %s
                    """, (agreeableness, conscentiousness,
                          extraversion, emotional_stability,
                          openess, next_state, attention_passed, user_id))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_self_roci(user_id, integrating, obliging, dominating, avoiding, compromising, attention_passed, next_state):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
                    UPDATE user_app 
                    SET integrating_self_eval = %s, 
                    obliging_self_eval = %s,
                    dominating_self_eval = %s,
                    avoiding_self_eval = %s,
                    compromising_self_eval = %s,current_state = %s,
                    attention_roci_self = %s
                    WHERE id = %s
                    """, (integrating, obliging,
                          dominating, avoiding,
                          compromising, next_state, attention_passed, user_id))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_friend_ffm_and_update_user(user_id, agreeableness, conscentiousness,
                                      extraversion, emotional_stability, openess, attention_passed, next_state):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
                    UPDATE user_app 
                    SET agreableness_friend_eval = %s, 
                    conscentiousness_friend_eval = %s,
                    extraversion_friend_eval = %s,
                    emotional_stability_friend_eval = %s,
                    openess_friend_eval = %s
                    WHERE friend_id = %s
                    """, (agreeableness, conscentiousness,
                          extraversion, emotional_stability,
                          openess, user_id))
    cur = db.cursor()
    cur.execute("""
                UPDATE user_app 
                SET current_state = %s,
                attention_ffm_peer = %s
                WHERE id = %s
                """, (next_state, attention_passed, user_id))

    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_friend_roci_and_update_user(user_id, integrating, obliging, dominating, avoiding, compromising, attention_passed, next_state):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
                    UPDATE user_app 
                    SET integrating_friend_eval = %s, 
                    obliging_friend_eval = %s,
                    dominating_friend_eval = %s,
                    avoiding_friend_eval = %s,
                    compromising_friend_eval = %s
                    WHERE friend_id = %s
                    """, (integrating, obliging,
                          dominating, avoiding,
                          compromising, user_id))

    cur = db.cursor()
    cur.execute("""
                UPDATE user_app 
                SET current_state = %s,
                attention_roci_peer = %s
                WHERE id = %s
                """, (next_state, attention_passed, user_id))

    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_id_friend(user_id, invited_by_id):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
                        UPDATE user_app 
                        SET friend_id = %s
                        WHERE id = %s
                        """, (invited_by_id, user_id))
    cur = db.cursor()
    cur.execute("""
                            UPDATE user_app 
                            SET friend_id = %s
                            WHERE id = %s
                            """, (user_id, invited_by_id))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def load_friends_pairs_list():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
                            SELECT id, friend_id
                            FROM user_app
                            WHERE is_admin = false
                            """)

    results = cur.fetchall()
    print('Executed the query')
    print(len(results))

    pair_list = list()
    for res in results:
        pair = list()
        rev_pair = list()
        pair.append(res[0])
        pair.append(res[1])
        rev_pair.append(res[1])
        rev_pair.append(res[0])
        if rev_pair not in pair_list:
            pair_list.append(pair)

    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return pair_list


def update_strangers_from_pairs_list(strangers_pairs_list):
    db = db_utils.create_connection_db()

    for pair in strangers_pairs_list:
        user_id = pair[0]
        stranger_id = pair[1]

        cur = db.cursor()
        cur.execute("""
                                UPDATE user_app 
                                SET stranger_id = %s,
                                stranger_nickname = %s
                                WHERE id = %s
                                """, (stranger_id, choice(config.STRANGERS_NICKNAMES).title(), user_id))
        cur = db.cursor()
        cur.execute("""
                                UPDATE user_app 
                                SET stranger_id = %s,
                                stranger_nickname = %s
                                WHERE id = %s
                                """, (user_id, choice(config.STRANGERS_NICKNAMES), stranger_id))
    db.commit()
    print('Executed the queries')
    db.close()
    print('Closed the dao!')
    return None


def load_relationships_dict():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
                            SELECT id, friend_id, stranger_id
                            FROM user_app
                            where is_admin = false
                            """)

    results = cur.fetchall()
    print('Executed the query')
    print(len(results))

    rel_dict = dict()
    for res in results:
        rel = dict()
        rel['friend_id'] = res[1]
        rel['stranger_id'] = res[2]

        rel_dict[res[0]] = rel

    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return rel_dict


def update_user_status(user_id, next_state):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            UPDATE user_app 
            SET current_state = %s
            WHERE id = %s
            """, (next_state, user_id))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def start_session_two():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            UPDATE user_app 
            SET current_state = %s
            WHERE is_user = %s
            """, (config.SESSION_2_STATUSES[0], True))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def start_session_three():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            UPDATE user_app 
            SET current_state = %s
            WHERE is_user = %s
            """, (config.SESSION_3_STATUSES[0], True))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def load_all_users():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            select id,email,nickname,friend_id,friend_email,friend_nickname,stranger_id,stranger_nickname,current_state,is_invited,is_user,is_admin
            from user_app
            where is_admin = false
            """)

    results = cur.fetchall()
    print('Executed the query')

    db.close()

    users_list = list()
    users_mail_list = list()
    for result in results:
        user_dict = dict()
        print(result[0])

        user_dict["id"] = result[0]
        user_dict["email"] = result[1]
        user_dict["nickname"] = result[2]
        user_dict["friend_id"] = result[3]
        user_dict["friend_email"] = result[4]
        user_dict["friend_nickname"] = result[5]
        user_dict["stranger_id"] = result[6]
        user_dict["stranger_nickname"] = result[7]
        user_dict["current_state"] = result[8]
        user_dict["is_invited"] = result[9]
        user_dict["is_user"] = result[10]
        user_dict["is_admin"] = result[11]
        if not user_dict["is_invited"]:
            user_dict["invited_friend"] = user_dict["friend_email"]
        else:
            user_dict["invited_friend"] = "---"

        user_dict["friend_accepted"] = False

        current_session = db_utils.get_current_session()
        completion_percentage = 0
        current_session_statuses = config.STATUSES[current_session]
        for (i, state) in zip(range(len(current_session_statuses)), current_session_statuses):
            if state == user_dict["current_state"]:
                completion_percentage = ceil(100 * ((i+1) / len(current_session_statuses)))
                print("completion_percentage", completion_percentage)

        user_dict["completion_percentage"] = completion_percentage
        users_list.append(user_dict)
        users_mail_list.append(user_dict["email"])


    for user_dict in users_list:
        print(">>>", user_dict["friend_email"])
        if (not user_dict["is_invited"]) and user_dict["friend_email"] in users_mail_list:
            user_dict["friend_accepted"] = True
    print(len(users_list), "users loaded")
    return users_list


def get_user_email_list():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            select email
            from user_app
            where is_admin = false
            """)

    results = cur.fetchall()
    print('Executed the query')

    db.close()

    users_mail_list = list()
    for result in results:
        users_mail_list.append(result[0])

    return(users_mail_list)


def load_users_table_as_json():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            select 
            id,
            age_group,
            email,
            friend_id,
            friend_nickname,
            gender,
            nickname,
            spotify_url,
            stranger_id,
            stranger_nickname,
            agreableness_self_eval,
            conscentiousness_self_eval,
            extraversion_self_eval,
            emotional_stability_self_eval,
            openess_self_eval,
            agreableness_friend_eval,
            conscentiousness_friend_eval,
            extraversion_friend_eval,
            emotional_stability_friend_eval,
            openess_friend_eval,
            integrating_self_eval,
            obliging_self_eval,
            dominating_self_eval,
            avoiding_self_eval,
            compromising_self_eval,
            integrating_friend_eval,
            obliging_friend_eval,
            dominating_friend_eval,
            avoiding_friend_eval,
            compromising_friend_eval,
            current_state,
            is_invited,
            friend_email,
            is_user,
            is_admin,
            attention_ffm_self,
            attention_roci_self,
            attention_ffm_peer,
            attention_roci_peer,
            attention_individual,
            attention_group_friend,
            attention_group_stranger,
            pronoun,
            friend_pronoun
            from user_app
            where is_admin = false
            """)

    results = cur.fetchall()
    print('Executed the query')

    db.close()

    users_list = list()
    for result in results:
        user_dict = dict()
        print(result[0])

        user_dict["id"] = result[0]
        user_dict["age_group"] = result[1]
        user_dict["email"] = result[2]
        user_dict["friend_id"] = result[3]
        user_dict["friend_nickname"] = result[4]
        user_dict["gender"] = result[5]
        user_dict["nickname"] = result[6]
        user_dict["spotify_url"] = result[7]
        user_dict["stranger_id"] = result[8]
        user_dict["stranger_nickname"] = result[9]
        user_dict["agreableness_self_eval"] = result[10]
        user_dict["conscentiousness_self_eval"] = result[11]
        user_dict["extraversion_self_eval"] = result[12]
        user_dict["emotional_stability_self_eval"] = result[13]
        user_dict["openess_self_eval"] = result[14]
        user_dict["agreableness_friend_eval"] = result[15]
        user_dict["conscentiousness_friend_eval"] = result[16]
        user_dict["extraversion_friend_eval"] = result[17]
        user_dict["emotional_stability_friend_eval"] = result[18]
        user_dict["openess_friend_eval"] = result[19]
        user_dict["integrating_self_eval"] = result[20]
        user_dict["obliging_self_eval"] = result[21]
        user_dict["dominating_self_eval"] = result[22]
        user_dict["avoiding_self_eval"] = result[23]
        user_dict["compromising_self_eval"] = result[24]
        user_dict["integrating_friend_eval"] = result[25]
        user_dict["obliging_friend_eval"] = result[26]
        user_dict["dominating_friend_eval"] = result[27]
        user_dict["avoiding_friend_eval"] = result[28]
        user_dict["compromising_friend_eval"] = result[29]
        user_dict["current_state"] = result[30]
        user_dict["is_invited"] = result[31]
        user_dict["friend_email"] = result[32]
        user_dict["is_user"] = result[33]
        user_dict["is_admin"] = result[34]
        user_dict["attention_ffm_self"] = result[35]
        user_dict["attention_roci_self"] = result[36]
        user_dict["attention_ffm_peer"] = result[37]
        user_dict["attention_roci_peer"] = result[38]
        user_dict["attention_individual"] = result[39]
        user_dict["attention_group_friend"] = result[40]
        user_dict["attention_group_stranger"] = result[41]
        user_dict["pronoun"] = result[42]
        user_dict["friend_pronoun"] = result[43]

        users_list.append(user_dict)

    return json.dumps(users_list, indent=2)




def load_personality_values():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            SELECT agreableness_self_eval, conscentiousness_self_eval, extraversion_self_eval, emotional_stability_self_eval, openess_self_eval, 
                    agreableness_friend_eval, conscentiousness_friend_eval, extraversion_friend_eval, emotional_stability_friend_eval, openess_friend_eval, 
                    integrating_self_eval, obliging_self_eval, dominating_self_eval, avoiding_self_eval, compromising_self_eval, 
                    integrating_friend_eval, obliging_friend_eval, dominating_friend_eval, avoiding_friend_eval, compromising_friend_eval
            FROM user_app
            WHERE is_admin='false'
            """)

    results = cur.fetchall()
    print('Executed the query')

    db.close()

    personality_values = {
        'FFM' : {
            'AGR': {'SELF' : list(), 'PEER' : list()},
            'CON': {'SELF' : list(), 'PEER' : list()},
            'EXT': {'SELF' : list(), 'PEER' : list()},
            'EMO': {'SELF' : list(), 'PEER' : list()},
            'OPE': {'SELF' : list(), 'PEER' : list()}
        },
        'ROCI': {
            'INT': {'SELF': list(), 'PEER': list()},
            'OBL': {'SELF': list(), 'PEER': list()},
            'DOM': {'SELF': list(), 'PEER': list()},
            'AVO': {'SELF': list(), 'PEER': list()},
            'COM': {'SELF': list(), 'PEER': list()}
        }
    }

    for result in results:
        if result[0]: personality_values['FFM']['AGR']['SELF'].append(float(result[0]))
        if result[1]: personality_values['FFM']['CON']['SELF'].append(float(result[1]))
        if result[2]: personality_values['FFM']['EXT']['SELF'].append(float(result[2]))
        if result[3]: personality_values['FFM']['EMO']['SELF'].append(float(result[3]))
        if result[4]: personality_values['FFM']['OPE']['SELF'].append(float(result[4]))
        if result[5]: personality_values['FFM']['AGR']['PEER'].append(float(result[5]))
        if result[6]: personality_values['FFM']['CON']['PEER'].append(float(result[6]))
        if result[7]: personality_values['FFM']['EXT']['PEER'].append(float(result[7]))
        if result[8]: personality_values['FFM']['EMO']['PEER'].append(float(result[8]))
        if result[9]: personality_values['FFM']['OPE']['PEER'].append(float(result[9]))

        if result[10]: personality_values['ROCI']['INT']['SELF'].append(float(result[10]))
        if result[11]: personality_values['ROCI']['OBL']['SELF'].append(float(result[11]))
        if result[12]: personality_values['ROCI']['DOM']['SELF'].append(float(result[12]))
        if result[13]: personality_values['ROCI']['AVO']['SELF'].append(float(result[13]))
        if result[14]: personality_values['ROCI']['COM']['SELF'].append(float(result[14]))
        if result[15]: personality_values['ROCI']['INT']['PEER'].append(float(result[15]))
        if result[16]: personality_values['ROCI']['OBL']['PEER'].append(float(result[16]))
        if result[17]: personality_values['ROCI']['DOM']['PEER'].append(float(result[17]))
        if result[18]: personality_values['ROCI']['AVO']['PEER'].append(float(result[18]))
        if result[19]: personality_values['ROCI']['COM']['PEER'].append(float(result[19]))

    return personality_values