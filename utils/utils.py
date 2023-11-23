from collections import deque
import random
import json
from flask_mail import Mail, Message
import base64
from flask import request
import requests

from spotipy.oauth2 import SpotifyOauthError

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config



def __create_list_from_pairs_list(pairs_list, index):
    if index >= len(pairs_list):
        return []
    elif index == 0:
        return [pairs_list[index][1]] + __create_list_from_pairs_list(pairs_list, index + 1)
    else:
        return [pairs_list[index][1]] + __create_list_from_pairs_list(pairs_list, index + 1) + [pairs_list[index][0]]


def __create_pairs_list_from_list(list, i_1, i_2):
    if i_1 >= len(list)/2:
        return []
    else:
        return [[list[i_2], list[i_1]]] + __create_pairs_list_from_list(list, i_1 + 1, i_2 - 1)


def create_random_pairs_from_pairs_list(pairs_list):
    random.shuffle(pairs_list)
    first_element = pairs_list[0][0]
    deque_to_shift = deque(__create_list_from_pairs_list(pairs_list, 0))
    deque_to_shift.rotate(random.randint(1, len(deque_to_shift)-1))
    shifted = list(deque_to_shift) + [first_element]
    return __create_pairs_list_from_list(shifted, 0, len(shifted) - 1)


def send_invite_friend(friend_email, current_user_email, mail):
    # email_text = config.INVITATION_EMAIL_TEXT.replace("<EmailFriend>", current_user_email)
    # print("MAIL_USE_SSL", config.mail_settings["MAIL_USE_SSL"])
    # print("MAIL_USE_TLS", config.mail_settings["MAIL_USE_TLS"])
    # msg = Message(subject="Invitation to participate in a user study",
    #               # sender=config.mail_settings["MAIL_USERNAME"],
    #               recipients=[friend_email],
    #               body=email_text)
    # mail.send(msg)

    # ALTERNATIVE EMAIL

    email_address = friend_email
    email_subject = "Invitation to participate in a user study"
    email_message = config.INVITATION_EMAIL_TEXT.replace("<EmailFriend>", current_user_email)

    sender_email = config.mail_settings["MAIL_DEFAULT_SENDER"]
    sender_password = config.mail_settings["MAIL_PASSWORD"]
    receiver_email = friend_email

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = email_subject
    message.attach(MIMEText(email_message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

    print('Email Sent!')


def send_email_start_session(email_to_send, session_to_start):
    email_address = email_to_send
    email_subject = config.NOTIFICATION_SESSION_START_EMAIL_SUBJECT[session_to_start]
    email_message = config.NOTIFICATION_SESSION_START_EMAIL_TEXT[session_to_start]

    sender_email = config.mail_settings["MAIL_DEFAULT_SENDER"]
    sender_password = config.mail_settings["MAIL_PASSWORD"]
    receiver_email = email_to_send

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = email_subject
    message.attach(MIMEText(email_message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

    print('Email Sent!')




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

def get_current_user_details(sp):
    '''
    Gets current user from SPOTIPY API
    :param sp: Spotipy api connection object!
    :return: current_user: a dictionary containing user details!
    '''
    current_user = sp.current_user()
    return current_user