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


def load_user_data(user_id):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
        select id,email,nickname,friend_id,friend_nickname,stranger_id,stranger_nickname,current_state,is_invited,is_user,is_admin
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


def update_friend_email_nick(user_id, friend_email, friend_nickname, next_state):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            UPDATE user_app 
            SET friend_email = %s, friend_nickname = %s, current_state = %s
            WHERE id = %s
            """, (friend_email, friend_nickname.title(), next_state, user_id))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_age_gender(user_id, age, gender, next_state):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
                UPDATE user_app 
                SET age_group = %s, gender = %s, current_state = %s
                WHERE id = %s
                """, (age, gender, next_state, user_id))
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
            select id,email,nickname,friend_id,friend_nickname,stranger_id,stranger_nickname,current_state,is_invited,is_user,is_admin
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
        users_list.append(user_dict)

    print(len(users_list), "users loaded")
    return users_list