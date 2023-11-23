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


def __generate_params_string_and_list(user_id_list, track_list, relationships_list, is_original, peer_id=None):
    param_string = ""
    param_list = list()
    for user_id in user_id_list:
        for track in track_list:
            for rel in relationships_list:
                param_string = param_string + " (%s, %s, %s, %s, %s),"
                param_list.append(track)
                param_list.append(user_id)
                param_list.append(rel)
                param_list.append(is_original)
                param_list.append(peer_id)
    param_string = param_string[:-1]
    return param_string, param_list


def create_basic_playlists_for_user(user_id, track_list):
    db = db_utils.create_connection_db()
    cur = db.cursor()

    param_string, param_list = __generate_params_string_and_list([user_id], track_list, ['friend', 'stranger'], is_original=True)

    print(param_string)
    print(param_list)

    query = """
            INSERT INTO playlist_evaluation (song_id, user_id, relationship, is_original, peer_id) VALUES """ + param_string
    print(query)

    cur.execute("""
            INSERT INTO playlist_evaluation (song_id, user_id, relationship, is_original, peer_id) VALUES """ +
                param_string, param_list)
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_pair_id_for_original_songs(user_id, playlist_type, peer_id):
    db = db_utils.create_connection_db()
    cur = db.cursor()

    cur.execute("""
                UPDATE playlist_evaluation SET peer_id = %s WHERE user_id = %s AND relationship = %s AND is_original = %s """,
                (peer_id, user_id, playlist_type, True))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def add_songs_to_user_playlist(user_id, track_list, playlist_type, peer_id):
    db = db_utils.create_connection_db()
    cur = db.cursor()

    param_string, param_list = __generate_params_string_and_list([user_id], track_list, [playlist_type], is_original=False, peer_id=peer_id)

    query = """
            INSERT INTO playlist_evaluation (song_id, user_id, relationship, is_original, peer_id) VALUES """ + param_string
    print(query)
    print(param_list)

    cur.execute("""
            INSERT INTO playlist_evaluation (song_id, user_id, relationship, is_original, peer_id) VALUES """ +
                param_string, param_list)
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def remove_pairs_songs_from_playlists():
    db = db_utils.create_connection_db()
    cur = db.cursor()

    cur.execute("""
                DELETE FROM playlist_evaluation WHERE is_original = %s """, (False,))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_individual_evaluations_and_update_user(user_id, song_evals_list, attention_passed, next_state):
    db = db_utils.create_connection_db()

    for song in song_evals_list:
        song_id = song['song_id']
        song_eval = song['song_eval']

        cur = db.cursor()
        cur.execute("""
                                UPDATE playlist_evaluation 
                                SET self_eval = %s
                                WHERE user_id = %s AND song_id = %s
                                """, (song_eval, user_id, song_id))
        # cur = db.cursor()
        # cur.execute("""
        #                         UPDATE playlist_evaluation
        #                         SET peer_eval = %s
        #                         WHERE peer_id = %s AND song_id = %s
        #                         """, (song_eval, user_id, song_id))

    cur = db.cursor()
    cur.execute("""
                UPDATE user_app 
                SET current_state = %s,
                attention_individual = %s
                WHERE id = %s
                """, (next_state, attention_passed, user_id))

    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return None



def update_peer_evaluation(user_id, peer_id, song_id, peer_eval):
    db = db_utils.create_connection_db()



    cur = db.cursor()
    cur.execute("""
                            UPDATE playlist_evaluation 
                            SET peer_eval = %s
                            WHERE user_id = %s AND song_id = %s AND peer_id = %s
                            """, (peer_eval, user_id, song_id, peer_id))

    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return None


def update_group_evaluations_and_update_user(user_id, song_evals_list, attention_passed, next_state):
    db = db_utils.create_connection_db()

    rel = None
    for song in song_evals_list:
        song_id = song['song_id']
        song_eval = song['song_eval']
        rel = song['relationship']

        cur = db.cursor()
        cur.execute("""
                                UPDATE playlist_evaluation 
                                SET group_self_eval = %s
                                WHERE user_id = %s AND song_id = %s AND relationship = %s
                                """, (song_eval, user_id, song_id, rel))

    cur = db.cursor()

    cur.execute(" UPDATE user_app "
                " SET current_state = %s,"
                " attention_group_" + rel + " = %s"
                " WHERE id = %s ", (next_state, attention_passed, user_id))

    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return None


def get_track_unique_id_list():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""select distinct song_id from playlist_evaluation""")

    results = cur.fetchall()
    print('Executed the query')
    print(len(results))
    db.close()

    id_list = list()
    for res in results:
        id_list.append(res[0])

    print(id_list)
    return id_list


def load_songs_dict_for_all_users():
    db = db_utils.create_connection_db()
    cur = db.cursor()

    cur.execute("""
                                SELECT DISTINCT user_id, song_id
                                FROM playlist_evaluation
                                WHERE is_original = True
                                """)

    results = cur.fetchall()
    print('Executed the query')
    print(len(results))
    db.close()

    songs_dict = dict()
    for res in results:
        id = res[0]
        song_id = res[1]
        if id not in songs_dict:
            songs_dict[id] = list()
        songs_dict[id].append(song_id)

    print(songs_dict)
    return songs_dict


def load_songs_for_user(user_id):
    db = db_utils.create_connection_db()
    cur = db.cursor()

    cur.execute("""
                                    SELECT DISTINCT song_id
                                    FROM playlist_evaluation
                                    WHERE user_id = %s
                                    """, (user_id, ))

    results = cur.fetchall()
    print('Executed the query')
    print(len(results))
    db.close()

    songs = list()
    for res in results:
        songs.append(res[0])

    print(songs)
    return songs


def load_songs_for_user_for_group_eval(user_id, playlist_type):
    db = db_utils.create_connection_db()
    cur = db.cursor()

    cur.execute("""
                                    SELECT song_id, self_eval, peer_eval
                                    FROM playlist_evaluation
                                    WHERE user_id = %s and relationship = %s
                                    """, (user_id, playlist_type))

    results = cur.fetchall()
    print('Executed the query')
    print(len(results))
    db.close()

    songs = list()
    for res in results:
        song = dict()
        song['SONG_ID'] = res[0]
        song['SELF_EVAL'] = res[1]
        song['PEER_EVAL'] = res[2]
        songs.append(song)

    print(songs)
    return songs


def load_playlists_table():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            select 
                song_id,
                user_id,
                relationship,
                self_eval,
                peer_eval,
                group_self_eval,
                is_original,
                peer_id
            from playlist_evaluation
            """)

    results = cur.fetchall()
    print('Executed the query')

    db.close()

    playlist_eval_list = list()
    for result in results:
        eval_dict = dict()
        print(result[0])

        eval_dict["song_id"] = result[0]
        eval_dict["user_id"] = result[1]
        eval_dict["relationship"] = result[2]
        eval_dict["self_eval"] = result[3]
        eval_dict["peer_eval"] = result[4]
        eval_dict["group_self_eval"] = result[5]
        eval_dict["is_original"] = result[6]
        eval_dict["peer_id"] = result[7]

        playlist_eval_list.append(eval_dict)

    return playlist_eval_list


def load_playlists_table_as_json():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
            select 
                song_id,
                user_id,
                relationship,
                self_eval,
                peer_eval,
                group_self_eval,
                is_original,
                peer_id
            from playlist_evaluation
            """)

    results = cur.fetchall()
    print('Executed the query')

    db.close()

    playlist_eval_list = list()
    for result in results:
        eval_dict = dict()
        print(result[0])

        eval_dict["song_id"] = result[0]
        eval_dict["user_id"] = result[1]
        eval_dict["relationship"] = result[2]
        eval_dict["self_eval"] = result[3]
        eval_dict["peer_eval"] = result[4]
        eval_dict["group_self_eval"] = result[5]
        eval_dict["is_original"] = result[6]
        eval_dict["peer_id"] = result[7]

        playlist_eval_list.append(eval_dict)

    return json.dumps(playlist_eval_list, indent=2)


def load_songs_self_eval():
    db = db_utils.create_connection_db()
    cur = db.cursor()

    cur.execute("""
                                    SELECT self_eval
                                    FROM playlist_evaluation
                                    WHERE relationship = 'friend' and is_original = 'true'
                                    """)

    results = cur.fetchall()
    print('Executed the query')
    print(len(results))
    db.close()

    songs_eval = list()
    for res in results:
        if res[0] == None:
            songs_eval.append(-1)
        else:
            songs_eval.append(int(res[0]))

    db = db_utils.create_connection_db()
    cur = db.cursor()

    cur.execute("""
                                        SELECT self_eval
                                        FROM playlist_evaluation
                                        WHERE is_original = 'false'
                                        """)

    results = cur.fetchall()
    print('Executed the query')
    print(len(results))
    db.close()

    for res in results:
        if res[0] == None:
            songs_eval.append(-1)
        else:
            songs_eval.append(int(res[0]))

    print(songs_eval)
    return songs_eval