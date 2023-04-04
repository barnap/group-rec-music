from datetime import datetime
import sys
import json

from dao.db_initialization_old import get_existing_tracks, generate_insert_tracks_query

sys.path.append('../')
import config
import spotipy
import spotipy.util as sputil
from _helper_functions import authenticate_spotify, get_top_tracks, get_track_information

'''
Just for testing purposes! Testing the authentication of Spotify APi using SPOTIPY
'''


def util():
    username = "messe_"
    # token = sputil.prompt_for_user_token(username, config.scope, config.client_id, config.client_secret, config.redirect_uri)
    # print(token)token =''
    token = 'BQDSx_s3UP74T7fk3u-5DD5NvYgYkzDQ3kN3YfwZCWy1gRULvk8F1dwnptuHIqoXJNVg_O-GRyXpDV1zIjrFracNwvLa3wpss78Ck-1h5EDl208bTqX0QLZKlkr3YQfEkSXV4rCscaLOM-d0NZ2gYHuR_H6AhMUPGXs-iE2yET7SToschRUbMQQuvO3PMs84KOdwXCRfXtEJzMYBVWdZEfehMdsTHvIIrCz34lDWBIXh'
    # sp = spotipy.Spotify()
    sp = authenticate_spotify(token)
    top_track_ids = get_top_tracks(sp, "short_term")

    tracks_dict, tracks_audio_dict = get_track_information(sp, top_track_ids)
    # Insert the tracks to DB!
    generate_insert_tracks_query(tracks_dict, tracks_audio_dict)

    print('END')

    # spotipy.util.oauth2.SpotifyOAuth(config.client_id, config.client_secret, config.redirect_uri)


if __name__ == '__main__':
    invitation_time = datetime.fromtimestamp(float("1569851389.173106"))
    print(invitation_time)
