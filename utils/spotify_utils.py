import base64
import json
import sys
from collections import defaultdict
import random

import numpy as np

sys.path.append('../')
import config

import spotipy
from datetime import date

from dao import dao_playlist

from flask import request
import requests

from spotipy.oauth2 import SpotifyOauthError

# from dao.db_operations import get_group_members_initial_ratings, generate_insert_group_recommendations_query, db_insert, \
#     update_recommended_column, generate_insert_group_rec_explanations, get_existing_tracks, \
#     insert_personalized_group_rec_explanations

# from dao import dao_playlist

'''
Some helper functions that is used across the project!
'''


def authenticate_spotify(token):
    '''
    Given a valid access token, using Spotipy Library connects to Spotify API.
    :param token:
    :return: spotipy object!
    '''
    print('...connecting to Spotify')
    sp = spotipy.Spotify(auth=token)
    return sp


def get_access_token(code):
    '''
    Given a code returned from spotify api, this method gets access token that is valid for 1 hour!
    :param code:
    :return: refresh_token, access_token
    '''
    print('Getting the access token')
    post_url = 'https://accounts.spotify.com/api/token'
    grant_type = 'authorization_code'

    callback_url = request.url_root + 'callback'
    auth_header = base64.b64encode(str(config.client_id + ':' + config.client_secret).encode())
    authorization = 'Basic %s' % auth_header.decode()

    post = {'redirect_uri': callback_url, 'code': code, 'grant_type': grant_type}
    headers = {'Authorization': authorization, 'Accept': 'application/json',
               'Content-Type': 'application/x-www-form-urlencoded'}

    # TODO fix this part!
    r = requests.post(post_url, headers=headers, data=post)

    if r.status_code != 200:
        raise SpotifyOauthError(r.reason)

    auth_json = json.loads(r.text)
    try:
        access_token = auth_json['access_token']
        refresh_token = auth_json['refresh_token']
        print('Access Token is: ' + access_token)
        return access_token, refresh_token
    except Exception as e:
        print("Something went wrong at the Spotify end - press back and try again")
        return "Something went wrong at the Spotify end - press back and try again"


def get_track_embed_uri(song_id):
    return config.EMBED_URI + song_id

def refresh_access_token(refresh_token):
    '''
    Once an access_token expired (After 1 hour), by using user's refresh_token we can get a new access_token!
    :param refresh_token:
    :return: access_token
    '''
    post_url = 'https://accounts.spotify.com/api/token'
    callback_url = request.url_root + 'callback'

    auth_header = base64.b64encode(str(config.client_id + ':' + config.client_secret).encode())
    authorization = 'Basic %s' % auth_header.decode()
    grant_type = 'refresh_token'

    post = {'refresh_token': refresh_token, 'grant_type': grant_type}
    headers = {'Authorization': authorization, 'Accept': 'application/json',
               'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post(post_url, headers=headers, data=post)

    if r.status_code is not 200:
        raise SpotifyOauthError(r.reason)

    auth_json = json.loads(r.text)
    try:
        access_token = auth_json['access_token']
        print('Access Token is: ' + access_token)
        return access_token
    except Exception as e:
        print("Something went wrong at the Spotify end - press back and try again")
        return "Something went wrong at the Spotify end - press back and try again"


def get_top_tracks_embed_uris(top_tracks):
    '''
    Given a list of track IDs, this method generates embed URIs for each of them. By using generated embed URIs, we are
    able to embed the songs to html files and users can listen to them!
    :param top_tracks:
    :return:
    '''
    EMBED_URI = "https://open.spotify.com/embed/track/"
    top_tracks_embed_uris = []
    for track in top_tracks:
        top_tracks_embed_uris.append(EMBED_URI + track)
    return top_tracks_embed_uris


def get_top_track_ids(top_tracks):
    '''
    Given a dictionary of top_tracks (using Spotify API), returns the ids of those tracks!
    :param top_tracks:
    :return:
    '''
    track_ids = []
    for track in top_tracks:
        track_ids.append(track['id'])
    return track_ids


def get_selected_tracks(sp):
    '''
    Gets top tracks of a user from Spotify! We try to get 10 songs using short_term time range, If we cannol fill 10
    songs we look for top tracks using medium_term time range, again if we cannot fill 10 songs we finally get top
    tracks using long_term time range!
    :param sp: spotipy instance
    :return: a list of spotify tracks!
    '''
    if not sp:
        top_track_ids = get_fix_track_ids()
    else:
        top_track_ids = get_user_top_track_ids(sp)

    return top_track_ids


def get_fix_track_ids():
    return config.FIX_TRACK_ID_LIST


def get_user_top_track_ids(sp):
    # Recover the last 50 played songs
    recently_played_tracks_all_data = sp.current_user_recently_played(limit=50)['items']
    # it returns an array of PlayHistoryObject, iterate and select the track, containing a SimplifiedTrackObject

    recently_played_tracks = list()
    for play_history_object in recently_played_tracks_all_data:
        recently_played_tracks.append(play_history_object['track'])

    # Recover the last 50 saved tracks
    saved_tracks_all_data = sp.current_user_saved_tracks(limit=50)['items']
    # it returns an array of SavedTrackObject, iterate and select the track, containing a TrackObject

    saved_tracks = list()
    for saved_track_object in saved_tracks_all_data:
        saved_tracks.append(saved_track_object['track'])

    # concatenate the two lists
    candidate_tracks = recently_played_tracks + saved_tracks
    print(len(candidate_tracks))
    tracks_in_db_ids = dao_playlist.get_track_unique_id_list()
    # tracks_in_db_ids = []
    print("######## tracks in db\n", tracks_in_db_ids)

    top_tracks = list()
    for track in candidate_tracks:
        if track['id'] not in tracks_in_db_ids:
            top_tracks.append(track)

    print("selected tracks: ", len(top_tracks))

    # select 10 songs from different artists
    selected_tracks = list()
    selected_artists = set()

    random.shuffle(top_tracks)

    for track in top_tracks:
        if len(selected_tracks) == config.TRACK_TO_SELECT:
            break
        track_artists_urls = list()
        for artist in track['artists']:
            spotify_url = artist['external_urls']['spotify']
            track_artists_urls.append(spotify_url)
        intersect = selected_artists.intersection(set(track_artists_urls))
        if not intersect:
            selected_tracks.append(track)
            selected_artists = selected_artists.union(set(track_artists_urls))
            print(track['name'], set(track_artists_urls))

    print(len(selected_tracks))
    print(len(selected_artists))

    selected_tracks_ids = get_top_track_ids(selected_tracks)

    # TODO: Manage the case in which the user doesn't have enough songs selected

    if len(selected_tracks) < config.TRACK_TO_SELECT:
        top_song = random.sample(config.TOP_TRACK_ID_LIST, (config.TRACK_TO_SELECT-len(selected_tracks)))
        selected_tracks_ids.extend(top_song)

    return selected_tracks_ids


def get_top_tracks(sp, time_range):
    '''
    Gets top tracks of a user from Spotify! We try to get 10 songs using short_term time range, If we cannol fill 10
    songs we look for top tracks using medium_term time range, again if we cannot fill 10 songs we finally get top
    tracks using long_term time range!
    :param sp: spotipy instance
    :param time_range: one of the ['short_term', 'medium_term', 'long_term']
    :return: a list of spotify tracks!
    '''
    top_tracks_all_data = sp.current_user_top_tracks(limit=50, time_range=time_range)

    top_tracks_data = top_tracks_all_data['items']

    short_term_top_track_ids = get_top_track_ids(top_tracks_data)
    if len(short_term_top_track_ids) < 10:
        medium_term_top_tracks_all_data = sp.current_user_top_tracks(limit=50, time_range="medium_term")
        medium_term_top_tracks_data = medium_term_top_tracks_all_data['items']
        medium_term_top_track_ids = get_top_track_ids(medium_term_top_tracks_data)
        for track_id in medium_term_top_track_ids:
            if len(short_term_top_track_ids) == 10:
                break
            if track_id not in short_term_top_track_ids:
                short_term_top_track_ids.append(track_id)
        if len(short_term_top_track_ids) < 10:
            long_term_top_tracks_all_data = sp.current_user_top_tracks(limit=50, time_range="long_term")
            long_term_top_tracks_data = long_term_top_tracks_all_data['items']
            long_term_top_track_ids = get_top_track_ids(long_term_top_tracks_data)
            for track_id in long_term_top_track_ids:
                if len(short_term_top_track_ids) == 10:
                    break
                if track_id not in short_term_top_track_ids:
                    short_term_top_track_ids.append(track_id)
    return short_term_top_track_ids


def get_track_information(sp, track_ids):
    '''
    Given a list of track IDs, we get track information and their audio features. Notice that for some songs we may get
    track info but not audio features, and the other way around!
    :param sp: Spotipy instance object!
    :param tracks: Maximum of 50 track IDs.
    :return:
    '''
    # First query DB whether we already have info about the songs or not!
    existing_tracks = get_existing_tracks(track_ids)
    print(existing_tracks)
    final_track_ids = list(set(track_ids) - set(existing_tracks))
    print(final_track_ids)
    if len(final_track_ids) > 0:
        tracks = sp.tracks(final_track_ids)
        tracks_audio = sp.audio_features(final_track_ids)
        tracks_dict = {}
        tracks_audio_dict = {}
        for track in tracks['tracks']:
            track_id = track['id']
            tracks_dict[track_id] = track
        for i in range(0, len(tracks_audio)):
            track_audio = tracks_audio[i]
            track_id = track_audio['id']
            tracks_audio_dict[track_id] = track_audio
    else:
        return {}, {}
    # tracks_json = json.dumps(tracks['tracks'][0]).__str__()
    # track_audio_features_json = json.dumps(tracks_audio[0]).__str__()
    return tracks_dict, tracks_audio_dict

#
# #   Later use this to create a playlist from recommended songs to a group on current user's profile!
# def create_playlist(sp, tracks_uri, tracks_ratings, group_name):
#     print("...creating playlist")
#     user_all_data = sp.current_user()
#     user_id = user_all_data["id"]
#     today = date.today()
#     d1 = today.strftime("%d-%m-%Y")
#
#     playlist_all_data = sp.user_playlist_create(user_id, group_name + str(d1))
#     playlist_id = playlist_all_data["id"]
#     playlist_uri = playlist_all_data["uri"]
#
#     selected_tracks_uri = []
#     for i in range(0, len(tracks_uri)):
#         track_uri = tracks_uri[i]
#         rating = tracks_ratings[i]
#
#         if rating >= config.ADD_TO_PLAYLIST_THRESHOLD:
#             selected_tracks_uri.append(track_uri)
#     # random.shuffle(selected_tracks_uri)
#     try:
#         sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks_uri)
#     except spotipy.client.SpotifyException as s:
#         print("could not add tracks")
#
#     return playlist_uri

#
# def get_current_user_details(sp):
#     '''
#     Gets current user from SPOTIPY API
#     :param sp: Spotipy api connection object!
#     :return: current_user: a dictionary containing user details!
#     '''
#     current_user = sp.current_user()
#     return current_user

#
# # TODO get top_N recommendations for a group method will be a different method!
# def aggregate_preferences(preferences, aggregate_strategy_function=np.mean):
#     '''
#     Aggregate preferences function, it accepts aggregate strategies as a function, the default method is average!
#     :param preferences: a dictionary {songID:{userID:rating,...},...}
#     :param aggregate_strategy_function: the default function is the average!
#     :return: a list of sorted songs based on their aggregated ratings! The first element of the list is the highest
#              rated after the aggregation strategy!
#     '''
#     aggregated_results = dict()
#     for song in preferences:
#         aggregate_rating = aggregate_strategy_function(list(preferences[song].values()))
#         aggregated_results[song] = aggregate_rating
#     # TODO Maybe for a strategy like fairness, the below is not generic! Fix this!
#     result = [(song, aggregated_results[song]) for song in
#               sorted(aggregated_results, key=aggregated_results.get, reverse=True)]
#     return result
#
#
# # TODO Maybe just generate explanations for top-N recommendations, not for the whole list!
# # TODO Should we get song details from Spotif  API? Will they be used within the explanation?
# def generate_personalized_explanations(initial_ratings, aggregated_list, explanation_style, aggregation_strategy):
#     '''
#     Here personalzied explanations can be generated.
#     :param aggregation_strategy:
#     :param explanation_style:
#     :param initial_ratings: In the following format! {songID:{userID:rating,...},...}
#     :param aggregated_list: In the following format, sorted based on aggregated_rating [(songID, aggregated_rating)..]
#     :return: {userID:{songID:explanation,...},...}
#     '''
#     # For each recommended song generate explanation!
#     group_rec_explanations = defaultdict(dict)  # {userID}
#     for i in range(0, len(aggregated_list)):
#         ranking = i + 1
#         song, agg_rating = aggregated_list[i]
#         song_ratings = initial_ratings[song]  # {userID:rating,...}
#         # TODO Here for each user an explanation can be generated maybe by calling another function!
#         for user in song_ratings:
#             explanation = config.PERSONALIZED_EXPLANATION_STYLES_FUNCTION_MAPPINGS[explanation_style](user, ranking,
#                                                                                                       song,
#                                                                                                       song_ratings,
#                                                                                                       aggregation_strategy)
#             group_rec_explanations[user][song] = explanation
#     return group_rec_explanations
#
#
# def generate_group_explanations(initial_ratings, aggregated_list, explanation_style, aggregation_strategy="average"):
#     '''
#     Here explanations for the whole group can be generated.
#     :param aggregation_strategy: the default strategy is average!
#     :param explanation_style:
#     :param initial_ratings: In the following format! {songID:{userID:rating,...},...}
#     :param aggregated_list: In the following format, sorted based on aggregated_rating [(songID, aggregated_rating)..]
#     :return:
#     '''
#     # {songID:explanation, ...}
#     group_rec_explanations = dict()
#     for i in range(0, len(aggregated_list)):
#         ranking = i + 1
#         song, agg_rating = aggregated_list[i]
#         song_ratings = initial_ratings[song]  # {userID:rating,...}
#         explanation = config.EXPLANATION_STYLES_FUNCTION_MAPPINGS[explanation_style](ranking, song, song_ratings,
#                                                                                      aggregation_strategy)
#         group_rec_explanations[song] = explanation
#     return group_rec_explanations
#
#
# def generate_recommendations(group_id):
#     '''
#     Here this method will be called when all the group members in a finalized group rates group initial songs. This
#     method first will get group members initial ratings from DB, then for different aggregation strategies will
#     compute top-N recommendations and save them to DB!
#     :param group_id:
#     :return:
#     '''
#     # First get group members' initial ratings from DB!
#     initial_ratings = get_group_members_initial_ratings(group_id)
#     # Then for each aggregation strategy apply it and save the recommendations to DB!
#     for strategy in config.AGGREGATION_STRATEGIES:
#         aggregated_list = aggregate_preferences(initial_ratings, aggregate_strategy_function=
#         config.AGGREGATION_STRATEGIES_FUNCTION_MAPPINGS[strategy])
#         query, params = generate_insert_group_recommendations_query(group_id, aggregated_list,
#                                                                     aggregation_strategy=strategy)
#         db_insert(query, params)
#         #  Generate the group explanations here!
#         for exp_style in config.EXPLANATION_STYLES:
#             # Here generate explanations for the whole group!
#             group_explanations = generate_group_explanations(initial_ratings, aggregated_list, exp_style, strategy)
#             #  Insert Explanations to the DB Here!
#             query, params = generate_insert_group_rec_explanations(group_id, group_explanations,
#                                                                    aggregation_strategy=strategy,
#                                                                    explanation_style=exp_style)
#             db_insert(query, params)
#             #  Here generate personalized explanations and insert them into DB!
#             personalized_group_explanations = generate_personalized_explanations(initial_ratings, aggregated_list,
#                                                                                  exp_style, strategy)
#             insert_personalized_group_rec_explanations(group_id, personalized_group_explanations,
#                                                        aggregation_strategy=strategy,
#                                                        explanation_style=exp_style)
#
#     # Here for the groups table change recommended column to true!
#     update_recommended_column(group_id)
#
#
# def split_recommendations_field(recommendations):
#     '''
#     from the group recommendations when we retrieve recommendations column we split each element here to get ids and
#     ratings.
#     :param recommendations:
#     :return:
#     '''
#     song_ids = []
#     ratings = []
#     for rec in recommendations:
#         splitted = rec.split(config.PREFERENCE_DELIMITER)
#         id = splitted[0]
#         # Here just check since in the older version we were just keeping
#         if len(splitted) > 1:
#             rating = float(splitted[1])
#         else:
#             rating = 5
#         song_ids.append(id)
#         ratings.append(rating)
#     return song_ids, ratings


if __name__ == '__main__':
    # group_id = "test_group_1569851389.173106"
    # generate_recommendations("test_group_1569851389.173106")
    # result = aggregate_preferences(get_group_members_initial_ratings(group_id))
    # query, params = generate_insert_group_recommendations_query(group_id, result)
    # db_insert(query, params)
    refresh_token = 'AQCGXAgPzMn8qf4ceDiwTy8kjMJLK0XXCbu8wRCBChKGxd6oiUCfv5pevWPjJkn7vAAcrZvJ9DPr0RTPWpk2fKGf80nRNtebhMdaQU50H7dazXNP9j58z-9M5cpOvQ-D0sDlsw'
    print(refresh_access_token(refresh_token))
