import sys

from flask import Flask, redirect, render_template, request, make_response, session, flash, jsonify, url_for
from flask_mail import Mail, Message
from flask_session import Session
import spotipy

import control as ctrl
from utils import utils

client_id, client_secret, scope = ctrl.get_spotify_app_configurations()
redirect_uri = ""

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
app.config.update(ctrl.get_mail_settings())
mail = Mail(app)

Session(app)

# ######### NEW ROUTES #########

@app.route('/consent_form', methods=['GET', 'POST'])
def consent_form():
    '''
    access to the login page with spotify account
    :return:
    '''
    session.clear()
    session['invited'] = False
    return render_template('consent.html')


@app.route('/consent_form_invited', methods=['GET', 'POST'])
def consent_form_invited():
    '''
    access to the login page with spotify account
    :return:
    '''
    session.clear()
    session['invited'] = True
    return render_template('consent.html')


@app.route('/login', methods=['GET', 'POST'])
def login_spotify():
    '''
    access to the login page with spotify account
    :return:
    '''
    return render_template('login.html')


@app.route("/go", methods=['GET', 'POST'])
def go():
    '''
    When a user from main page clicks on "Login with your Spotify Account!", by using Spotify API, we ask users to
    signup or login by their Spotify Account. On success Spotify API returns a code to the '/callback' method below!

    :return:
    '''
    callback_url = request.url_root + 'callback'
    base_url = 'https://accounts.spotify.com/en/authorize?client_id=' + client_id + '&response_type=code&redirect_uri=' \
               + callback_url + '&scope=user-read-email%20playlist-read-private%20user-follow-read%20user-library-read%20user-top-read%20playlist-modify-private%20playlist-modify-public%20user-read-recently-played&state=34fFs29kd09'

    # this is how we set the Cookie when its a Redirect instead of return_response
    # https://stackoverflow.com/questions/12272418/in-flask-set-a-cookie-and-then-re-direct-user
    response = make_response(redirect(base_url, 302))
    return response


@app.route('/callback')
def callback():
    '''
    Assuming that users signed up by their Spotify Accounts, here we get access token for them and get their top tracks
    from Spotify. Notice that, they may come from an e-mail invitation, in that case we also automatically add them to
    the group that their friends invited them to join to!
    We redirect the user to my_profile.html page to see her top tracks. there she can see create group and my groups
    links as well!
    '''

    # Get access token for user
    code = request.args.get('code')
    session['code'] = code
    access_token, refresh_token = utils.get_access_token(code)
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    sp = spotipy.Spotify(auth=access_token)
    current_user = utils.get_current_user_details(sp)
    current_user_id = current_user['id']
    print("CURRENT USER ID: ", current_user_id)
    session['current_user'] = current_user_id

    if 'invited' in session:
        invited = session['invited']
    else:
        invited = None

    # Call control to check if the user is in the DB
    user, next_view = ctrl.manage_logged_user(current_user_id, invited, sp)

    session['invited'] = user['is_invited']
    # session['current_user'] = user

    return redirect(url_for(ctrl.get_session_url()))


@app.route('/session_one', methods=['GET', 'POST'])
def session_one():

    if not ctrl.is_current_session(1):
        return redirect(url_for(ctrl.get_session_url()))

    session['missing_parameters_msg'] = None
    session['FFM'] = None
    session['ROCI'] = None
    session['session_route'] = ctrl.get_session_route(1)

    if "current_user" not in session:
        next_view = 'login.html'
    else:
        current_user_id = session["current_user"]
        # user = ctrl.get_user(current_user_id)
        btn = request.form.get('s1_submit')
        # invited = session['invited']
        print(">>>>>>>>>", btn)
        if not btn:
            # not a submit: redirect to the current view for the user
            user, next_view, current_state = ctrl.get_current_view_for_user(current_user_id)
            session['invited'] = user['is_invited']

            print(current_state, next_view)
            if current_state == 'INSERT_SELF_FFM':
                session['FFM'] = ctrl.generate_ffm_dict(current_user_id)
            elif current_state == 'INSERT_SELF_ROCI':
                session['ROCI'] = ctrl.generate_roci_dict(current_user_id)
        else:
            # retrieve submit parameters
            next_view, missing_parameters_msg, add_to_session = \
                ctrl.manage_submit(current_user_id, request.form, mail)
            session['missing_parameters_msg'] = missing_parameters_msg
            if add_to_session:
                for key in add_to_session:
                    session[key] = add_to_session[key]
    return render_template(next_view)


@app.route('/session_two', methods=['GET', 'POST'])
def session_two():

    if not ctrl.is_current_session(2):
        return redirect(url_for(ctrl.get_session_url()))

    session['missing_parameters_msg'] = None
    session['FFM'] = None
    session['ROCI'] = None
    session['session_route'] = ctrl.get_session_route(2)
    session['INDIVIDUAL_SONGS'] = None

    if "current_user" not in session:
        next_view = 'login.html'
    else:
        current_user_id = session["current_user"]
        # user = ctrl.get_user(current_user_id)
        btn = request.form.get('s1_submit')
        # invited = session['invited']
        print(">>>>>>>>>", btn)
        if not btn:
            # not a submit: redirect to the current view for the user
            user, next_view, current_state = ctrl.get_current_view_for_user(current_user_id)
            session['invited'] = user['is_invited']
            session['friend_nickname'] = user['friend_nickname']

            print(current_state, next_view)
            if current_state == 'INSERT_FRIEND_FFM':
                session['FFM'] = ctrl.generate_ffm_dict(current_user_id)
            elif current_state == 'INSERT_FRIEND_ROCI':
                session['ROCI'] = ctrl.generate_roci_dict(current_user_id)
            elif current_state == 'EVALUATE_SONGS_INDIVIDUAL':
                session['INDIVIDUAL_SONGS'] = ctrl.generate_individual_songs_dict(current_user_id)
                # for question in session['ROCI']['questionnaire']:
                #     print(question['INPUT_ID'], question['QUESTION_TEXT'])
        else:
            # retrieve submit parameters
            next_view, missing_parameters_msg, add_to_session = \
                ctrl.manage_submit(current_user_id, request.form, mail)
            session['missing_parameters_msg'] = missing_parameters_msg
            if add_to_session:
                for key in add_to_session:
                    session[key] = add_to_session[key]
    return render_template(next_view)


@app.route('/session_three', methods=['GET', 'POST'])
def session_three():

    if not ctrl.is_current_session(3):
        return redirect(url_for(ctrl.get_session_url()))

    session['missing_parameters_msg'] = None
    session['GROUP_SONGS'] = None
    session['session_route'] = ctrl.get_session_route(3)

    if "current_user" not in session:
        next_view = 'login.html'
    else:
        current_user_id = session["current_user"]
        # user = ctrl.get_user(current_user_id)
        btn = request.form.get('s1_submit')
        # invited = session['invited']
        print(">>>>>>>>>", btn)
        if not btn:
            # not a submit: redirect to the current view for the user
            user, next_view, current_state = ctrl.get_current_view_for_user(current_user_id)
            session['invited'] = user['is_invited']
            session['friend_nickname'] = user['friend_nickname']
            session['stranger_nickname'] = user['stranger_nickname']

            print(current_state, next_view)
            if current_state == 'EVALUATE_SONGS_GROUP_FRIEND':
                session['GROUP_SONGS'] = ctrl.generate_group_songs_dict(current_user_id, "friend")
            elif current_state == 'EVALUATE_SONGS_GROUP_STRANGER':
                session['GROUP_SONGS'] = ctrl.generate_group_songs_dict(current_user_id, "stranger")

        else:
            # retrieve submit parameters
            next_view, missing_parameters_msg, add_to_session = \
                ctrl.manage_submit(current_user_id, request.form, mail)
            session['missing_parameters_msg'] = missing_parameters_msg
            if add_to_session:
                for key in add_to_session:
                    session[key] = add_to_session[key]
    return render_template(next_view)


########## ADMIN ROUTES ##########


@app.route('/offline_pairing', methods=['GET', 'POST'])
def offline_pairing():
    if "current_user" not in session:
        return render_template('login.html')
    else:
        current_user_id = session["current_user"]
        next_view = ctrl.manage_offline_pairing(current_user_id)
    return render_template(next_view)


@app.route('/start_session_two', methods=['GET', 'POST'])
def start_session_two():
    if "current_user" not in session:
        return render_template('login.html')
    else:
        current_user_id = session["current_user"]
        next_view = ctrl.start_session_two(current_user_id)
    return render_template(next_view)


@app.route('/start_session_three', methods=['GET', 'POST'])
def start_session_three():
    if "current_user" not in session:
        return render_template('login.html')
    else:
        current_user_id = session["current_user"]
        next_view = ctrl.start_session_three(current_user_id)
    return render_template(next_view)


@app.route('/admin', methods=['GET', 'POST'])
def admin_routes():
    print(">>>>> ADMIN")
    if "current_user" not in session:
        return render_template('login.html')
    else:
        current_user_id = session["current_user"]
        next_view, error_msg, add_to_session = ctrl.manage_submit_admin(current_user_id)

        session['error_msg'] = error_msg
        if add_to_session:
            for key in add_to_session:
                session[key] = add_to_session[key]

    return render_template(next_view)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=ctrl.get_port())
