import json
import sys
from collections import defaultdict

sys.path.append('../')
import psycopg2
import config
import time
import string
import random
from datetime import datetime
from psycopg2 import pool


# # TODO Maybe all dao methods should return query params!
# # TODO use connection pooling! https://pynative.com/psycopg2-python-postgresql-connection-pooling/
# # https://bbengfort.github.io/observations/2017/12/06/psycopg2-transactions.html
# # TODO Also make sure that I am not every time opening and closing connection to DB!
#
# def create_connection_pool():
#     '''
#     Creates and returns Connection Pool!
#     :return:
#     '''
#     try:
#         threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(10, 40, user=config.user,
#                                                                         password=config.password,
#                                                                         host=config.host,
#                                                                         port=config.port,
#                                                                         database=config.database)
#         if threaded_postgreSQL_pool:
#             print("Connection pool created successfully using ThreadedConnectionPool")
#             return threaded_postgreSQL_pool
#
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("Error while connecting to PostgreSQL", error)
#         return None
#
#
# def create_connection_db():
#     '''
#     Creates connection to the database!
#     :return:
#     '''
#     connection = psycopg2.connect(user=config.user,
#                                   password=config.password,
#                                   host=config.host,
#                                   port=config.port,
#                                   database=config.database)
#     return connection
#
#
# def db_select(query, params):
#     '''
#     Generic SELECT
#     :param query:
#     :param params:
#     :return:
#     '''
#     db = create_connection_db()
#     cur = db.cursor()
#     cur.execute(query, params)
#     result = cur.fetchall()
#     print('Executed the query')
#     db.close()
#     return result
#
#
# def db_insert(query, params):
#     '''
#     Generic INSERT QUERY!
#     :param query:
#     :param params:
#     :return:
#     '''
#     db = create_connection_db()
#     cur = db.cursor()
#     cur.execute(query, params)
#     db.commit()
#     print('Executed the query')
#     db.close()
#     print('Closed the dao!')
#     return cur


def create_table(query):
    '''
    Creates table by executing the query!
    :param query:
    :return:
    '''
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(query)

        connection.commit()
        print("Table created successfully in PostgreSQL ")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

#
# def generate_insert_group_query(group_name, current_user_id, inviteds):
#     '''
#     when a user creates a new group, this method is called!
#     :param group_name:
#     :param current_user_id: userID that creates the group.
#     :param inviteds: invited people. we will save them in DB in the following format email$$invited_by$$timestamp
#                      where the timestamp is the one below (current_time that is used in group ID). We do this to know
#                      which user accepts the invitation, so that we can remove them from inviteds column later when they
#                      accept the group invitation.
#     :return:
#     '''
#     # To have unique ID's for the same group name add current time to the group ID!
#     current_time = str(time.time())
#     group_id = group_name
#     for ch in string.punctuation:
#         group_id = group_id.replace(ch, '')
#     group_id = group_id.replace(' ', '_')
#     group_id += '_' + current_time
#     invited_members = []
#     for person in inviteds:
#         invited_members.append(person + config.PREFERENCE_DELIMITER + current_user_id + config.PREFERENCE_DELIMITER +
#                                current_time)
#
#     query = '''
#             INSERT INTO groups (ID,GROUP_NAME,GROUP_MEMBERS,CREATED_BY, INVITED, CREATED_AT) VALUES (%s,%s,%s,%s,%s,%s)
#             ON CONFLICT (ID)
#             DO NOTHING
#             '''
#     params = (group_id, group_name, [current_user_id], current_user_id, invited_members,
#               datetime.fromtimestamp(float(current_time)))
#     return query, params, group_id, current_time
#
#
# def generate_insert_tracks_query(tracks_dict, tracks_audio_dict):
#     '''
#     Insert tracks to DB!
#     :param tracks_dict:
#     :param tracks_audio_dict:
#     :return:
#     '''
#     db = create_connection_db()
#     cur = db.cursor()
#     tup = []
#     for track_id in tracks_dict:
#         track = tracks_dict[track_id]
#         track_name = track['name']
#         track_info_json = json.dumps(track)
#         if track_id in tracks_audio_dict:
#             track_audio_json = json.dumps(tracks_audio_dict[track_id])
#         else:
#             track_audio_json = json.dumps({})
#         tup.append((track_id, track_name, track_info_json, track_audio_json))
#     # args_str = ','.join(cur.mogrify("(%s,%s,%s,%s)", x) for x in tup)
#     cur.executemany(
#         "INSERT INTO tracks (ID,NAME,INFO_JSON,AUDIO_FEATURES_JSON) VALUES(%s,%s,%s,%s) ON CONFLICT (ID) DO NOTHING",
#         tup)
#     db.commit()
#     db.close()
#
#
# #  When through the my groups page members of the group invites more members!
# def update_groups_invited_list(group_id, inviteds, invited_by):
#     '''
#     through my_groups page, if a member wants to invite more members to an unfinalized group, this method is called to
#     generate update query!
#     :param group_id:
#     :param inviteds:
#     :param invited_by:
#     :return:
#     '''
#     current_time = str(time.time())
#     invited_members = []
#     newly_invited = []
#     for person in inviteds:
#         invited_members.append(person + config.PREFERENCE_DELIMITER + invited_by + config.PREFERENCE_DELIMITER +
#                                current_time)
#         newly_invited.append((person, invited_by, "Today"))
#     query = '''
#             UPDATE groups SET INVITED = INVITED || (%s)
#             WHERE ID = (%s)
#             '''
#     params = (invited_members, group_id)
#     return query, params, current_time, newly_invited
#
#
# def generate_insert_user_ratings_query(user_id, group_id, ratings):
#     '''
#     After user gives initial ratings to the group preference list, this method is triggered to save user's ratings
#     for the group. Primary key is ID which is combination of user_id and group_id!
#     :param user_id:
#     :param group_id:
#     :param ratings:
#     :return:
#     '''
#     current_time = time.time()
#     rating_array = []
#     for k, v in ratings.items():
#         temp = str(k) + config.PREFERENCE_DELIMITER + str(v)
#         rating_array.append(temp)
#     query = '''
#             INSERT INTO user_initial_ratings (ID,USER_ID, GROUP_ID, RATINGS, rate_time) VALUES(%s,%s,%s,%s,%s)
#             ON CONFLICT (ID)
#             DO NOTHING
#             '''
#     params = (user_id + group_id, user_id, group_id, rating_array, datetime.fromtimestamp(current_time))
#     return query, params
#
#
# def generate_insert_group_survey_query(group_id, aggregation_strategy, explanation_style, survey_result):
#     '''
#
#     :param group_id:
#     :param aggregation_strategy:
#     :param explanation_style:
#     :param survey_result: a stringified json comes after finalizing the survey! See tracks as an exaple for JSON!
#     :return:
#     '''
#     current_time = time.time()
#     id = group_id + aggregation_strategy + explanation_style
#     query = '''
#             INSERT INTO group_survey (ID, GROUP_ID,AGGREGATION_STRATEGY, EXPLANATION_STYLE,SURVEY,created_at)
#             VALUES(%s,%s,%s,%s,%s,%s)
#             ON CONFLICT (ID)
#             DO NOTHING
#             '''
#     params = (id, group_id, aggregation_strategy, explanation_style, json.dumps(survey_result),
#               datetime.fromtimestamp(current_time))
#     return query, params
#
#
# def generate_insert_personalized_survey_query(user_id, group_id, aggregation_strategy, explanation_style,
#                                               survey_result):
#     '''
#
#     :param user_id:
#     :param group_id:
#     :param aggregation_strategy:
#     :param explanation_style:
#     :param survey_result: a stringified json comes after finalizing the survey!
#     :return:
#     '''
#     current_time = time.time()
#     id = user_id + group_id + aggregation_strategy + explanation_style
#     query = '''
#             INSERT INTO group_survey (ID,USER_ID, GROUP_ID,AGGREGATION_STRATEGY, EXPLANATION_STYLE,SURVEY,created_at)
#             VALUES(%s,%s,%s,%s,%s,%s,%s)
#             ON CONFLICT (ID)
#             DO NOTHING
#             '''
#     params = (id, user_id, group_id, aggregation_strategy, explanation_style, json.dumps(survey_result),
#               datetime.fromtimestamp(current_time))
#     return query, params
#
#
# def generate_insert_user_query(current_user, refresh_token):
#     '''
#     When user logins to system with Spotify credentials, save her to the DB. If user already exists, do nothing!
#     :param current_user: dictionary returned from spotipy containing current user's information!
#     :return:
#     '''
#     current_time = time.time()
#     email = current_user['email'] if 'email' in current_user else ''
#     # TODO add has key checks for all of the fields just in case
#     spotify_url = current_user['external_urls']['spotify']
#     href = current_user['href']
#     image_url = ''
#     display_name = current_user['display_name'] if 'display_name' in current_user else ''
#     if 'images' in current_user and len(current_user['images']) != 0 and 'url' in current_user['images'][0]:
#         image_url = current_user['images'][0]['url']
#     uri = current_user['uri']
#     country = current_user['country'] if 'country' in current_user else ''
#
#     query = '''INSERT INTO users (ID,SPOTIFY_URL,HREF,IMAGE_URL,URI,COUNTRY,EMAIL,DISPLAY_NAME,created_at, token) VALUES (%s,%s,%s,%s,
#     %s,%s,%s,%s,%s,%s) ON CONFLICT (ID) DO NOTHING '''
#     params = (current_user['id'], spotify_url, href, image_url, uri, country, email, display_name,
#               datetime.fromtimestamp(current_time), refresh_token)
#     print(params)
#     return query, params
#
#
# def generate_insert_group_recommendations_query(group_id, recommendations, aggregation_strategy="average"):
#     '''
#     Once the recommendations are generated for a group by using an aggregating strategy, this method generates
#     insert query for DB!
#
#     :param group_id:
#     :param recommendations: In the following format! [(songid,rating),...]
#     :param aggregation_strategy:
#     :return:
#     '''
#     current_time = time.time()
#     id = group_id + "_" + aggregation_strategy  # Unique_id is the combination of group_id and aggregation_strategy!
#
#     recs = [k + config.PREFERENCE_DELIMITER + str(v) for k, v in recommendations]
#     query = '''
#             INSERT INTO group_recommendations (ID, GROUP_ID, AGGREGATION_STRATEGY, RECOMMENDATIONS,created_at) VALUES (%s,%s,%s,%s,%s)
#             ON CONFLICT (ID) DO NOTHING
#             '''
#     params = (id, group_id, aggregation_strategy, recs, datetime.fromtimestamp(current_time))
#     return query, params
#
#
# def get_group_invited_members(group_id):
#     '''
#     Get a group's invited members!
#     :param group_id:
#     :return: The format is email$$invited_by$$timestamp
#     '''
#     query = '''
#             SELECT invited from groups
#             where id = (%s)
#             '''
#     params = (group_id,)
#     result = db_select(query, params)
#     if result[0][0] is None:
#         return []
#     return result[0][0]
#
#
# def get_group_initial_songs(group_id):
#     '''
#     Gets group's initial tracks from DB! 10 songs from each group member will be added to the GROUP_TRACKS after group
#     is finalized (alternatively, we can append GROUP_TRACKS every time a new member joins the group!)
#     This will be called when a user clicks on rate initial songs button!
#     :param group_id:
#     :return:
#     '''
#     query = '''
#             SELECT GROUP_TRACKS FROM groups
#             where id = (%s)
#             '''
#     params = (group_id,)
#     result = db_select(query, params)
#     # TODO maybe shuffle the items here!
#     if result[0][0] is None:
#         return dict()
#     else:
#         return result[0][0]
#
#
# # TODO check if this method is efficient! I am not querying the DB by unique ID (user_id + group_id)! Alternative is,
# # TODO first get group members' ids from DB then get each of their initial ratings! Have to compare the performance!
# def get_group_members_initial_ratings(group_id):
#     '''
#     After group members rated the initial songs for a group, to compute recommendations, this method gets initial
#     ratings for a group!
#     :param group_id:
#     :return: a dictionary {songID:{userID:rating,...},...}, this will be used in aggregation strategies!
#     '''
#     query = '''
#             SELECT USER_ID,RATINGS from user_initial_ratings
#             where GROUP_ID = (%s)
#             '''
#     params = (group_id,)
#     result = db_select(query, params)
#     initial_ratings = defaultdict(dict)
#     for r in result:
#         user_id = r[0]
#         ratings = r[1]
#         for rating in ratings:
#             splitted = rating.split(config.PREFERENCE_DELIMITER)
#             song_id = splitted[0]
#             rating_value = splitted[1]
#             initial_ratings[song_id][user_id] = int(rating_value)
#     return initial_ratings
#
#
# def is_user_in_db(user_id):
#     '''
#     check if the user is already in the DB!
#     :param user_id:
#     :return:
#     '''
#     query = '''
#                 select id,complete_profile from users
#                 where id = (%s)
#             '''
#     params = (user_id,)
#     result = db_select(query, params)
#     if result == [] or result is None:
#         return [], False
#     else:
#         id = result[0][0]
#         if result[0][1] is None:
#             completed = False
#         else:
#             completed = result[0][1]
#         return id, completed
#
#
# # TODO Maybe set invited = []!
# def update_group_preferences(group_id, preferences):
#     '''
#     Given a set of initial songs (10 from each group member) it updates group_tracks! Later user's will rate these
#     preferences! For now we assume that when we update the group preferences (from the below function), the group is
#     finalized!
#     :param group_id:
#     :param preferences:
#     :return:
#     '''
#     query = '''
#           UPDATE groups SET
#           GROUP_TRACKS = (%s), finalized = TRUE
#           WHERE ID = (%s)
#           '''
#     params = (preferences, group_id)
#     db_insert(query, params)
#
#
# def finalize_the_group(group_id):
#     '''
#     Finalizes the group by merging each group members top 10 songs!
#     :param group_id:
#     :return:
#     '''
#     group_members = get_group_members(group_id)
#     top_tracks = get_group_members_top_tracks(group_members, group_id)
#     initial_group_preferences = []
#     for member, tracks in top_tracks:
#         initial_group_preferences += tracks
#
#     update_group_preferences(group_id, list(set(initial_group_preferences)))
#
#
# # TODO this will not be used!!
# def generate_random_ratings(song_ids, user_id, group_id):
#     '''
#     For test purposes, it simulates the scenario where users listen to the group initial song lists!
#     :param song_ids:
#     :param user_id:
#     :param group_id:
#     :return:
#     '''
#     ratings = dict()
#     for song in song_ids:
#         rating = random.randint(1, 5)
#         ratings[song] = rating
#     query, params = generate_insert_user_ratings_query(user_id, group_id, ratings)
#     db_insert(query, params)
#     return ratings
#
#
# def remove_invited_from_group(email, invited_by, timestamp, group_id):
#     '''
#     Either when a user accepts the invitation or invitation expires, call this method!
#     :param email:
#     :param invited_by:
#     :param timestamp:
#     :return:
#     '''
#     query = '''
#             UPDATE groups SET invited = array_remove(invited, %s)
#             WHERE ID = (%s)
#             '''
#     invited = email + config.PREFERENCE_DELIMITER + invited_by + config.PREFERENCE_DELIMITER + timestamp
#     params = (invited, group_id)
#     print("REMOVE_INVITATION", invited, group_id)
#     return query, params
#
#
# def complete_user_profile(user_id, profile_details):
#     '''
#     Complete the user profile information and save it to the json field in users table!
#     :param user_id:
#     :param profile_details:
#     :return:
#     '''
#     query = '''
#             UPDATE users SET profile_details = (%s), complete_profile = TRUE
#             WHERE ID = (%s)
#             '''
#     params = (profile_details, user_id)
#     db_insert(query, params)
#
#
# def generate_insert_group_rec_explanations(group_id, explanations, aggregation_strategy="average",
#                                            explanation_style="highest_rated"):
#     '''
#     Generates insert query for group recommendation explanations!
#     :param group_id:
#     :param explanations: {songID:explanation}
#     :param aggregation_strategy:
#     :param explanation_style:
#     :return:
#     '''
#     id = group_id + aggregation_strategy + explanation_style
#     exps = [song + config.PREFERENCE_DELIMITER + explanations[song] for song in explanations]
#     query = '''
#             INSERT INTO group_recommendation_explanations
#             (ID, GROUP_ID,AGGREGATION_STRATEGY,EXPLANATION_STYLE,EXPLANATIONS) VALUES (%s,%s,%s,%s,%s)
#             ON CONFLICT (ID) DO NOTHING
#             '''
#     params = (id, group_id, aggregation_strategy, explanation_style, exps)
#     return query, params
#
#
# def insert_personalized_group_rec_explanations(group_id, explanations, aggregation_strategy="average",
#                                                explanation_style="highest_rated"):
#     '''
#
#     :param group_id:
#     :param explanations: {userID:{songID:explanation,...},...}
#     :param aggregation_strategy:
#     :param explanation_style:
#     :return:
#     '''
#     db = create_connection_db()
#     cur = db.cursor()
#     tups = []
#     for user in explanations:
#         id = user + group_id + aggregation_strategy + explanation_style
#         user_exps = explanations[user]
#         exps = [song + config.PREFERENCE_DELIMITER + user_exps[song] for song in user_exps]
#         tups.append((id, user, group_id, aggregation_strategy, explanation_style, exps))
#     cur.executemany(
#         "INSERT INTO recommendation_explanations (ID, USER_ID, GROUP_ID,AGGREGATION_STRATEGY,EXPLANATION_STYLE,EXPLANATIONS) VALUES (%s,%s,%s,%s,%s,%s)",
#         tups)
#     db.commit()
#     db.close()
#
#
# def get_group_recommendations(group_id, aggregation_strategy="average"):
#     '''
#     Get recommendations of a group for a specific aggregation strategy!
#     :param group_id: unique group id
#     :param aggregation_strategy: default is average now!
#     :return: a ranked list of song id, first element is the highest ranked song!
#     '''
#     id = group_id + "_" + aggregation_strategy
#     query = '''
#             SELECT recommendations from group_recommendations
#             where id = (%s)
#             '''
#     params = (id,)
#     result = db_select(query, params)
#     if result[0][0] is None:
#         return []
#     else:
#         return result[0][0]
#
#
# def get_group_recommendation_explanations(group_id, aggregation_strategy, explanation_style):
#     '''
#     Gets explanations generated for the group given aggregation strategy and explanation_style!
#     :param group_id:
#     :param aggregation_strategy:
#     :param explanation_style:
#     :return:
#     '''
#     id = group_id + aggregation_strategy + explanation_style
#     query = '''
#             SELECT explanations from group_recommendation_explanations
#             where id = (%s)
#             '''
#     params = (id,)
#     result = db_select(query, params)
#     if result[0][0] is None:
#         return {}
#     else:
#         explanations = {}
#         for r in result[0][0]:
#             splitted = r.split(config.PREFERENCE_DELIMITER)
#             songID = splitted[0]
#             explanation = splitted[1]
#             explanations[songID] = explanation
#         return explanations
#
#
# def get_personalized_group_recommendation_explanations(user_id, group_id, aggregation_strategy, explanation_style):
#     '''
#     Gets personalized explanations generated for the group given aggregation strategy and explanation_style!
#     :param user_id:
#     :param group_id:
#     :param aggregation_strategy:
#     :param explanation_style:
#     :return:
#     '''
#     id = user_id + group_id + aggregation_strategy + explanation_style
#
#     query = '''
#             SELECT explanations recommendation_explanations
#             where id = (%s)
#             '''
#     params = (id,)
#     result = db_select(query, params)
#     if result[0][0] is None:
#         return {}
#     else:
#         explanations = {}
#         for r in result[0][0]:
#             splitted = r.split(config.PREFERENCE_DELIMITER)
#             songID = splitted[0]
#             explanation = splitted[1]
#             explanations[songID] = explanation
#         return explanations
# # TODO Maybe here instead of deleting the old preferences,  keep them as well!
#
#
# def update_users_top_tracks(top_tracks, user_id):
#     '''
#     inserts or updates user's top tracks, since Spotify api is updating those tracks daily!
#     :param top_tracks:
#     :param user_id:
#     :return:
#     '''
#     track_ids = []
#     for track in top_tracks:
#         track_ids.append(track)
#
#     query = '''
#             UPDATE users SET
#                 TOP_TRACKS = (%s)
#                 WHERE ID = (%s)
#             '''
#     params = (track_ids, user_id)
#     return query, params
#
#
# def insert_users_top_tracks(user_id, top_tracks):
#     '''
#     Everytime user refreshes the top tracks we add them to DB! In the users table the top_tracks are the most recent
#     ones, but here we keep all of them!
#     :param user_id:
#     :param top_tracks:
#     :return:
#     '''
#     current_time = time.time()
#     id = user_id + str(current_time)
#     track_ids = []
#     for track in top_tracks:
#         track_ids.append(track)
#     query = '''
#                 INSERT INTO users_top_tracks (ID, USER_ID, TOP_TRACKS,TIMESTAMP) VALUES(%s,%s,%s,%s)
#                 ON CONFLICT (ID) DO NOTHING
#                 '''
#     params = (id, user_id, track_ids, datetime.fromtimestamp(current_time))
#     return query, params
#
#
# def update_users_groups(user_id, group_id):
#     '''
#     When user creates a new group or accept invitation to a new group call this!
#     :param user_id:
#     :param group_id:
#     :return:
#     '''
#     query = '''
#             UPDATE users SET
#                 GROUPS = GROUPS || (%s)
#                 WHERE ID = (%s)
#             '''
#     params = ([group_id], user_id)
#     return query, params
#
#
# def add_user_to_group(user_id, group_id):
#     '''
#     When an invited user accepts the group invitation add her to the group members!
#     :param user_id:
#     :param group_id:
#     :return:
#     '''
#     query = '''
#             UPDATE groups SET
#                 GROUP_MEMBERS = GROUP_MEMBERS || (%s)
#                 WHERE ID = (%s)
#             '''
#     params = ([user_id], group_id)
#     return query, params
#
#
# def update_recommended_column(group_id):
#     '''
#     Once the recommendations are computed, change the recommended from FALSE to TRUE for a given group!
#     :param group_id:
#     :return:
#     '''
#     query = '''
#             UPDATE groups SET
#             recommended = TRUE
#             WHERE ID = (%s)
#             '''
#     params = (group_id,)
#     db_insert(query, params)
#
#
# def get_users_groups(user_id):
#     '''
#     To show in my groups page, get user's existing groups!
#     :param user_id:
#     :return: a list of group ids!
#     '''
#     query = '''
#             SELECT GROUPS FROM users
#                 WHERE ID = (%s)
#             '''
#     params = (user_id,)
#     result = db_select(query, params)
#     if result[0][0] is None:
#         return dict()
#     else:
#         return list(set(result[0][0]))
#
#
# def get_users_preferences(user_id):
#     '''
#     Get user's top tracks from DB!
#     :param user_id:
#     :return:
#     '''
#     query = '''
#             select TOP_TRACKS from users
#             where id = (%s)
#             '''
#     params = (user_id,)
#     result = db_select(query, params)
#     if result[0][0] is None:
#         return dict()
#     else:
#         return result[0][0]
# # TODO Will not be used!
#
#
# def update_users_awaiting_group_requests(user_id, group_id):
#     '''
#     If we are going to use invite by spotify user_name! Then we have to use this method!
#     :param user_id:
#     :param group_id:
#     :return:
#     '''
#     query = '''
#             UPDATE users SET
#                 GROUP_REQUESTS = GROUP_REQUESTS || (%s)
#                 WHERE ID = (%s)
#             '''
#     params = ([group_id], user_id)
#     return query, params
# # TODO Will not be used!
#
#
# def get_existing_user_ids(current_user_id):
#     '''
#     during create a group this will be used to autocomplete the user names from the user table!
#     :param current_user_id:
#     :return:
#     '''
#
#     query = '''
#             SELECT ID FROM users
#                 WHERE ID != (%s)
#             '''
#     params = (current_user_id,)
#     result = db_select(query, params)
#     ids = [a[0] for a in result]
#     return ids
#
#
# def get_users_rated_the_group(group_member_ids):
#     '''
#     Get user IDs that rated a group's initial songs!
#     :param group_member_ids: primary ids for user_initial_ratings table (userID + groupID)
#     :return: a list of user IDs that rated the songs.
#     '''
#     query = '''
#             SELECT user_id FROM user_initial_ratings
#             where id in %s
#             '''
#     params = (tuple(group_member_ids),)
#     result = db_select(query, params)
#     return [r[0] for r in result]
#
#
# def get_existing_tracks(track_ids):
#     '''
#     Given a list of track IDs check which ones already exist in the DB! This way we will not try to get track info
#     and audio features every time from Spotigy API! We will do it only once for each track!
#     :param track_ids:
#     :return: a list of track ids that are already in the DB!
#     '''
#     query = '''
#             SELECT id from tracks
#             where id in %s
#             '''
#     params = (tuple(track_ids),)
#     result = db_select(query, params)
#     return [r[0] for r in result]
#
#
# def get_groups(current_user, groups):
#     '''
#     This is used to show user's groups! in my groups page!
#     :param groups: a list of ids of user's groups!
#     :return:
#     '''
#     current_time = datetime.now()
#     query = '''
#             SELECT ID,GROUP_NAME,GROUP_MEMBERS,invited,finalized,recommended,created_by FROM groups
#             where id in %s
#             '''
#     params = (tuple(groups),)
#     result = db_select(query, params)
#     print(result)
#     users_groups = defaultdict(dict)
#     for i in range(0, len(result)):
#         id = result[i][0]
#         name = result[i][1]
#         group_members = result[i][2]
#         rated = False
#         if result[i][3] is not None:
#             inviteds = result[i][3]
#         else:
#             inviteds = []
#         if result[i][4] is not None:
#             finalized = result[i][4]
#         else:
#             finalized = False
#         if result[i][5] is not None:
#             recommended = result[i][5]
#         else:
#             recommended = False
#         if result[i][6] is not None:
#             created_by = result[i][6]
#         if finalized and not recommended:
#             if user_rated_groups_initial_songs(current_user, id) != 0:
#                 rated = True
#         if finalized and recommended:
#             rated = True
#             # Here check if the user rated the group's initial songs
#         users_groups[id]["name"] = name
#         users_groups[id]["members"] = group_members
#         users_groups[id]["inviteds"] = []
#         users_groups[id]["finalized"] = finalized
#         users_groups[id]["recommended"] = recommended
#         users_groups[id]["rated"] = rated
#         users_groups[id]["created_by"] = created_by
#         for invited in inviteds:
#             splitted = invited.split(config.PREFERENCE_DELIMITER)
#             user_mail = splitted[0]
#             invited_by = splitted[1]
#             invitation_time = datetime.fromtimestamp(float(splitted[2]))
#             time_diff_days, time_diff_str = get_time_diff(current_time, invitation_time)
#             # Here remove expired invitations!
#             # TODO We also have to keep the log of which invitations are removed!
#             if time_diff_days >= config.INVITATION_EXPIRY_DATE:
#                 query, params = remove_invited_from_group(user_mail, invited_by, splitted[2], id)
#                 db_insert(query, params)
#             else:
#                 users_groups[id]["inviteds"].append((user_mail, invited_by, time_diff_str, time_diff_days))
#     return users_groups
#
#
# def user_rated_groups_initial_songs(user_id, group_id):
#     '''
#     check if a user rated the initial songs for a group or not! Based on this a button for finalized groups will be
#     shown to user to rate the initial preferences!
#     :param user_id:
#     :param group_id:
#     :return:
#     '''
#     query = '''
#             SELECT ID FROM user_initial_ratings
#             WHERE ID = (%s)
#             '''
#     params = (user_id + group_id,)
#     result = db_select(query, params)
#     return len(result)
#
#
# def get_time_diff(time1, time2):
#     time_diff = time1 - time2
#     days = time_diff.days
#     time_diff_str = ""
#     if days == 0:
#         time_diff_str = "Today"
#     elif days == 1:
#         time_diff_str = "Yesterday"
#     else:
#         time_diff_str = str(days) + " days ago"
#     return days, time_diff_str
#
#
# def get_group_members_top_tracks(group_members, group_id, number_of_tracks=10):
#     '''
#     Get group_members' top tracks! This will be called to create initial songs for the group! Later each group member
#     will rate these songs!
#
#     :param group_members: a list of user ID's
#     :param group_id:
#     :param number_of_tracks: For now we get 10 songs for each group member, we can modify it easily!
#     :return:
#     '''
#     query = '''
#             SELECT ID,TOP_TRACKS FROM users
#             where id in %s
#             '''
#     params = (tuple(group_members),)
#     result = db_select(query, params)
#     top_tracks = []
#     for i in range(0, len(result)):
#         userID = result[i][0]
#         tracks = result[i][1]
#         top_tracks.append((userID, tracks[:number_of_tracks]))
#     return top_tracks
#
#
# def get_group_members_emails(group_members):
#     query = '''
#             SELECT EMAIL FROM users
#             where id in %s
#             '''
#     params = (tuple(group_members),)
#     result = db_select(query, params)
#     return [r[0] for r in result]
#
#
# def get_group_members(group_id):
#     '''
#     Get group members of a given group!
#     :param group_id:
#     :return: a list of IDs of group members!
#     '''
#     query = '''
#             SELECT GROUP_MEMBERS FROM groups
#             where id = (%s)
#             '''
#     params = (group_id,)
#     result = db_select(query, params)
#     return result[0][0]


if __name__ == '__main__':
    create_groups_table_query = '''
                                CREATE TABLE groups
                                (ID TEXT PRIMARY KEY NOT NULL,
                                GROUP_NAME TEXT,
                                CREATED_BY TEXT,
                                GROUP_MEMBERS TEXT[],
                                GROUP_TRACKS TEXT[],
                                GROUP_RECOMMENDATIONS TEXT[],
                                invited TEXT[],
                                finalized BOOLEAN,
                                recommended BOOLEAN,
                                created_at timestamp);
                                '''

    create_users_table_query = '''CREATE TABLE users
      (ID TEXT PRIMARY KEY NOT NULL,
      SPOTIFY_URL TEXT,
      HREF TEXT,
      IMAGE_URL TEXT,
      URI TEXT,
      COUNTRY VARCHAR(2),
      EMAIL TEXT UNIQUE,
      GROUPS TEXT[],
      GROUP_REQUESTS TEXT[],
      TOP_TRACKS TEXT[],
      TOKEN TEXT,
      DISPLAY_NAME TEXT,
      complete_profile BOOLEAN,
      profile_details json,
      created_at timestamp); 
      '''

    create_user_ratings_table_query = '''
            CREATE TABLE user_initial_ratings
            (ID TEXT PRIMARY KEY NOT NULL,
            USER_ID TEXT NOT NULL,
            GROUP_ID TEXT NOT NULL,
            RATINGS TEXT[],
            rate_time timestamp);
            '''

    create_group_invitations_table = '''
                                     CREATE TABLE group_invitations
                                     (ID TEXT PRIMARY KEY NOT NULL)
                                     '''

    create_group_recommendations_table_query = '''
                                         CREATE TABLE group_recommendations
                                         (ID TEXT PRIMARY KEY NOT NULL,
                                         GROUP_ID TEXT NOT NULL,
                                         AGGREGATION_STRATEGY TEXT NOT NULL,
                                         RECOMMENDATIONS TEXT[],
                                         created_at timestamp);
                                         '''
    # ID = userID + group_id + agg_strategy + explanation_style!
    create_personalized_explanations_table_query = '''
                                            CREATE TABLE recommendation_explanations
                                            (ID TEXT PRIMARY KEY NOT NULL,
                                            USER_ID TEXT NOT NULL,
                                            GROUP_ID TEXT NOT NULL,
                                            AGGREGATION_STRATEGY TEXT NOT NULL,
                                            EXPLANATION_STYLE TEXT NOT NULL,
                                            EXPLANATIONS TEXT[]);
                                            '''

    # ID = group_id + agg_strategy + explanation_style!
    create_group_explanations_table_query = '''
                                            CREATE TABLE group_recommendation_explanations
                                            (ID TEXT PRIMARY KEY NOT NULL,
                                            GROUP_ID TEXT NOT NULL,
                                            AGGREGATION_STRATEGY TEXT NOT NULL,
                                            EXPLANATION_STYLE TEXT NOT NULL,
                                            EXPLANATIONS TEXT[]);
                                            '''

    # ID = group_id + agg_strategy + explanation_style!
    create_group_survey_table_query = '''
                                      CREATE TABLE group_survey
                                      (ID TEXT PRIMARY KEY NOT NULL,
                                      GROUP_ID TEXT NOT NULL,
                                      AGGREGATION_STRATEGY TEXT NOT NULL,
                                      EXPLANATION_STYLE TEXT NOT NULL,
                                      SURVEY json,
                                      created_at timestamp);
                                      '''

    # ID = userID + group_id + agg_strategy + explanation_style!
    create_personalized_survey_table_query = '''
                                       CREATE TABLE personalized_survey
                                       (ID TEXT PRIMARY KEY NOT NULL,
                                       USER_ID TEXT NOT NULL,
                                       GROUP_ID TEXT NOT NULL,
                                       AGGREGATION_STRATEGY TEXT NOT NULL,
                                       EXPLANATION_STYLE TEXT NOT NULL,
                                       SURVEY json,
                                       created_at timestamp);
                                       '''

    create_tracks_table_query = '''
                                CREATE TABLE tracks
                                (ID TEXT PRIMARY KEY NOT NULL,
                                 NAME TEXT,
                                 INFO_JSON json,
                                 AUDIO_FEATURES_JSON json);
                                '''

    create_users_top_tracks_table_query = '''
                                        CREATE TABLE users_top_tracks
                                        (ID TEXT PRIMARY KEY NOT NULL,
                                        USER_ID TEXT,
                                        TIMESTAMP timestamp,
                                        TOP_TRACKS TEXT[]);
                                          '''

    # This are to create the tables in the DB!
    create_table(create_tracks_table_query)
    create_table(create_personalized_survey_table_query)
    create_table(create_group_survey_table_query)
    create_table(create_group_explanations_table_query)
    create_table(create_personalized_explanations_table_query)
    create_table(create_group_recommendations_table_query)
    create_table(create_user_ratings_table_query)
    create_table(create_users_table_query)
    create_table(create_groups_table_query)
    create_table(create_users_top_tracks_table_query)

    # result = get_groups(['messe__dinner_with_friends', 'messe__car_trip'])
    # print(result)
    # get_users_preferences('messe_')
    # update_query, update_params = update_users_groups("1175674493", "test_group_1569851389.173106")
    # db_insert(update_query, update_params)
    # add_query, add_params = add_user_to_group("1175674493", "test_group_1569851389.173106")
    # db_insert(add_query, add_params)
    # result = get_group_members("test_group_1569851389.173106")
    # print(result)
    # print(get_group_members_top_tracks(["messe_", "1175674493", "tmdrws"], ""))
    # finalize_the_group("Bokum_1570365869.101963")
    # generate_random_ratings(get_group_initial_songs("test_group_1569851389.173106"), "1175674493", "test_group_1569851389.173106")
    # get_group_members_initial_ratings("test_group_1569851389.173106")
    # create_table(create_group_recommendations_table_query)
    # query, params = remove_invited_from_group("mesutt.kayaa@gmail.com", "devrimgl", "1570365869.101963")
    # db_insert(query, params)
    # user_rated_groups_initial_songs('messe3_', 'test_group_1569851389.173106')
    # print(get_users_rated_the_group(['messe_test_group_1569851389.173106']))
    # print("Test")
