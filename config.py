import os

#################### GENERAL CONFIG TO SET UP IN ENVIRONMENTAL VARIABLES ############################

# This are Spotify API Credentials! Create another spotify account create an application!
# client_id = os.environ['SPOTIFY_CLIENT_ID']
# client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

client_id = os.environ['GOOGLE_CLIENT_ID']
client_secret = os.environ['GOOGLE_CLIENT_SECRET']
google_discovery_url = "https://accounts.google.com/.well-known/openid-configuration"

HOST = os.environ['HOST']
PORT =  os.environ['PORT']
main_page_uri = "http://"+HOST+":"+PORT

SERVER_MODE = os.environ['SERVER_MODE']=='True'

# Below link must be added to spotify Application callback links through developer.spotify.account
redirect_uri = main_page_uri+"/callback"

scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
EMBED_URI = "https://open.spotify.com/embed/track/"

# DB

user = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
database = os.environ['DB_DATABASE']
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']

PREFERENCE_DELIMITER = '$$'

# Mail settings! REMEMBER THAT FOR GMAIL SOMETIMES YOU NEED TO GIVE PERMISSION TO 3RD PARTY APPS!
mail_settings = {
    "MAIL_SERVER": os.environ['MAIL_SERVER'],
    "MAIL_PORT": os.environ['MAIL_PORT'],
    "MAIL_USE_TLS": os.environ['MAIL_USE_TLS'],
    "MAIL_USE_SSL": os.environ['MAIL_USE_SSL'],
    "MAIL_USERNAME": os.environ['MAIL_USERNAME'],
    "MAIL_PASSWORD": os.environ['MAIL_PASSWORD'],
    "MAIL_DEFAULT_SENDER": os.environ['MAIL_DEFAULT_SENDER'],
}

TEST_MODE = os.environ['TEST_MODE']=='True'
TRACK_TO_SELECT = int(os.environ['TRACK_TO_SELECT'])

# FIX_TRACK_ID_LIST = ['3k79jB4aGmMDUQzEwa46Rz',
# '1BxfuPKGuaTgP7aM0Bbdwr',
# '3qQbCzHBycnDpGskqOWY0E',
# '7ro0hRteUMfnOioTFI5TG1',
# '4DHcnVTT87F0zZhRPYmZ3B',
# '2UW7JaomAMuX9pZrjVpHAU',
# '6pD0ufEQq0xdHSsRbg9LBK',
# '1odExI7RdWc4BT515LTAwj',
# '4Dvkj6JhhA12EX05fT7y2e',
# '1Qrg8KqiBpW07V7PNxwwwL',
# '7FbrGaHYVDmfr7KoLIZnQ7',
# '4eMKD8MRroxCqugpsxCCNb',
# '7mXuWTczZNxG5EDcjFEuJR',
# '2FDTHlrBguDzQkp7PVj16Q',
# '7ABLbnD53cQK00mhcaOUVG']

FIX_TRACK_ID_LIST = [
    '490eG6GdyHsKOFi9pPMERK',
    '5xQr5TxQ77siaKfuyiJbT0',
    '4EncKcnRsZd3VgOQd9N8Jf',
    '0RT86wBrufYQZSdN852Wjn',
    '4jQCJchULcVfb3LTjJ5rn1',
    '79h7F2ZL2jfysXEYdHfwyq',
    '6djFRgAtFL0qTELYJqVicP',
    '7dbyaRWWFvB9UG2vcwTd3J',
    '11n8LudggXuZXmldSlAadR',
    '7l6glc1SRrt6BAncgDPrPu',
    '1uTfgYieZbJ2qZ2v2ICndT',
    '2uE5JDb0ZJsJkzZ8gvL5jw',
    '1gPNdHsHpLKziD7ASH9RCd',
    '2e3FFYFj3PuH9rMwKmjgYF',
    '30cEVc7Nq5EC0149zqCNBM'
    ###### ALTERNATIVE SET #####
    # '3OB8tXG4qxdvs5Y9cZDsMa',
    # '0x23fPcfGI5FCpeVadnCdo',
    # '59ujQJCSRNgLtKQ1ly3b7c',
    # '4EncKcnRsZd3VgOQd9N8Jf',
    # '0ZFq3raMFdXllZJoTbBRnQ',
    # '7z4VPtZm9g9dxC83ratUFM',
    # '4LzdviA9tys39CccjkJubr',
    # '2I0kfxKcQTLoer605Q74aQ',
    # '0QV3swr7L8MZr72lL2izV1',
    # '5ezVqhuo9PDNqsGKsKOPyG',
    # '53ILZZz0cySVRbHwgovlQI',
    # '1Dww8WMEA5C9jp01ILGzzW',
    # '5j72kVstS2gHKl8zWJDNz0',
    # '31AYjxq6VkR57EgcwAJFmO',
    # '6MD6xpFK4cfquxRqXxqwjq'
  ]

TRACK_NUMBER = len(FIX_TRACK_ID_LIST)
ADMIN_USER_ID_LIST = (os.environ['SUPER_ADMIN'],)

#################### EMAIL TEXT  ############################

PARTICIPATION_EMAIL_TEXT = "We will conduct a user study evaluating the satisfaction related on listening to different " \
                           "songs in different contexts, alone or in a group. For the participation, it is necessary that " \
                           "you have a Google account.\n" \
                           "The experiment is composed by two sessions, scheduled in the next 2 weeks: Both sessions should" \
                            " take approximately 30 minutes. You will be" \
                            " asked to register on our web application using your Google account and to indicate the" \
                           " email address and the nickname of a second person who can perform the experiment with you" \
                           " (each one will carry out the experiment individually). Such person should be somebody with" \
                           " whom you have a close relationship (e.g., your partner or a close friend).\n" \
                           "We will use your email address to notify the start of sessions 2," \
                           " and to provide the link for i. You will be able to" \
                           " withdraw from the study in any moment. After the end of the last session, you will have 30" \
                           " days to ask for deleting your data; after that, we will delete all the email addresses, and" \
                           " all the provided data will be stored anonymously. Among the participants, we will extract" \
                           " one winner for an Amazon voucher worth 20 euros.\n" \
                           "Please use the following link to start the session 1: https://<Host>:5000/consent_form \n" \
                           "If you need further information or clarification, do not hesitate to write via email to:\n" \
                           "f.barile@maastrichtuniversity.nl. \n" \
                           "Thanks in advance for your kind cooperation."

INVITATION_EMAIL_TEXT = "You have been invited by your friend <EmailFriend> to participate in our study user study " \
                        "evaluating the satisfaction related on listening to different " \
                        "songs in different contexts, alone or in a group. For the participation, it is necessary that " \
                        "you have a Google account.\n" \
                        "The experiment is composed by two sessions, scheduled in the next 2 weeks: Both sessions should" \
                        " take approximately 30 minutes. You will be" \
                        " asked to register on our web application using your Google account." \
                        "We will use your email address to notify the start of the session 2," \
                        " and to provide the link for it. You will be able to" \
                        " withdraw from the study in any moment. After the end of the last session, you will have 30" \
                        " days to ask for deleting your data; after that, we will delete all the email addresses, and" \
                        " all the provided data will be stored anonymously. Among the participants, we will extract" \
                        " one winner for an Amazon voucher worth 20 euros.\n" \
                        "Please use the following link to start the session 1: https://<Host>:5000/consent_form_invited \n" \
                        "If you need further information or clarification, do not hesitate to write via email to:\n" \
                        "f.barile@maastrichtuniversity.nl. \n" \
                        "Thanks in advance for your kind cooperation."

NOTIFICATION_SESSION_START_EMAIL_SUBJECT = dict()
NOTIFICATION_SESSION_START_EMAIL_TEXT = dict()

NOTIFICATION_SESSION_START_EMAIL_SUBJECT[2] = "Notification of the start of user study session 2"
NOTIFICATION_SESSION_START_EMAIL_TEXT[2] = "Thanks again for your participation in our user study evaluating the satisfaction related " \
                                          "on listening to different songs in different contexts, alone or in a group.\n" \
                                          "The experiment is composed by two sessions, and now you can start the second session. " \
                                          "It will take approximately 30 minutes. \n" \
                                       "Please use the following link to start the session 2: https://<Host>:5000/session_two \n" \
                                       "If you need further information or clarification, do not hesitate to write via email to:\n" \
                                       "f.barile@maastrichtuniversity.nl. \n" \
                                       "Thanks in advance for your kind cooperation."

# NOTIFICATION_SESSION_START_EMAIL_SUBJECT[3] = "Notification of the start of user study session 3"
# NOTIFICATION_SESSION_START_EMAIL_TEXT[3] = "Thanks again for your participation in our user study evaluating the satisfaction related " \
#                                           "on listening to different songs in different contexts, alone or in a group.\n" \
#                                           "The experiment is composed by three sessions, and now you can start the last session. " \
#                                           "It will take approximately 5 minutes. \n" \
#                                        "Please use the following link to start the session 1: https://127.0.0.1:5000/session_three \n" \
#                                        "If you need further information or clarification, do not hesitate to write via email to:\n" \
#                                        "f.barile@maastrichtuniversity.nl. \n" \
#                                        "Thanks in advance for your kind cooperation."

#################### SESSION ROUTES  ############################

SESSION_ROUTE = dict()
SESSION_ROUTE[1] = "session_one"
SESSION_ROUTE[2] = "session_two"
SESSION_ROUTE[3] = "session_three"


#################### STATUSES AND VIEWS  ############################

# SESSION_1_STATUSES = (
#     'INSERT_EMAIL_NICK',
#     'INSERT_EMAIL_NICK_FRIEND',
#     'INSERT_AGE_GENDER',
#     'INSERT_SELF_FFM',
#     'INSERT_SELF_ROCI',
#     'END_1'
# )
#
# SESSION_2_STATUSES = (
#     'START_SESSION_2',
#     'INSERT_FRIEND_FFM',
#     'INSERT_FRIEND_ROCI',
#     'EVALUATE_SONGS_INDIVIDUAL',
#     'END_2'
# )
#
# SESSION_3_STATUSES = (
#     'START_SESSION_3',
#     'EVALUATE_SONGS_GROUP_FRIEND',
#     'EVALUATE_SONGS_GROUP_STRANGER',
#     'END_3'
# )

SESSION_1_STATUSES = (
    'START_SESSION_1',
    'INSERT_EMAIL_NICK',
    'INSERT_EMAIL_NICK_FRIEND',
    'INSERT_AGE_GENDER',
    'INSERT_SELF_FFM',
    'INSERT_SELF_ROCI',
    'EVALUATE_SONGS_INDIVIDUAL',
    'END_1'
)

SESSION_2_STATUSES = (
    'START_SESSION_2',
    'INSERT_FRIEND_FFM',
    'INSERT_FRIEND_ROCI',
    'EVALUATE_SONGS_GROUP_FRIEND',
    'EVALUATE_SONGS_GROUP_STRANGER',
    'END_2'
)

STATUSES = dict()
STATUSES[1] = SESSION_1_STATUSES
STATUSES[2] = SESSION_2_STATUSES
# STATUSES[3] = SESSION_3_STATUSES

PERCENTAGE_COMP = dict()
PERCENTAGE_COMP['START_SESSION_1'] = 100 * (0 / (len(SESSION_1_STATUSES)-1))
PERCENTAGE_COMP['INSERT_EMAIL_NICK'] = 100 * (1 / (len(SESSION_1_STATUSES)-1))
PERCENTAGE_COMP['INSERT_EMAIL_NICK_FRIEND'] = 100 * (2 / (len(SESSION_1_STATUSES)-1))
PERCENTAGE_COMP['INSERT_AGE_GENDER'] = 100 * (3 / (len(SESSION_1_STATUSES)-1))
PERCENTAGE_COMP['INSERT_SELF_FFM'] = 100 * (4 / (len(SESSION_1_STATUSES)-1))
PERCENTAGE_COMP['INSERT_SELF_ROCI'] = 100 * (5 / (len(SESSION_1_STATUSES)-1))
PERCENTAGE_COMP['EVALUATE_SONGS_INDIVIDUAL'] = 100 * (6 / (len(SESSION_1_STATUSES)-1))
PERCENTAGE_COMP['END_1'] = 100 * (7 / (len(SESSION_1_STATUSES)-1))
PERCENTAGE_COMP['START_SESSION_2'] = 100 * (0 / (len(SESSION_2_STATUSES)-1))
PERCENTAGE_COMP['INSERT_FRIEND_FFM'] = 100 * (1 / (len(SESSION_2_STATUSES)-1))
PERCENTAGE_COMP['INSERT_FRIEND_ROCI'] = 100 * (2 / (len(SESSION_2_STATUSES)-1))
PERCENTAGE_COMP['EVALUATE_SONGS_GROUP_FRIEND'] = 100 * (3 / (len(SESSION_2_STATUSES)-1))
PERCENTAGE_COMP['EVALUATE_SONGS_GROUP_STRANGER'] = 100 * (4 / (len(SESSION_2_STATUSES)-1))
PERCENTAGE_COMP['END_2'] = 100 * (5 / (len(SESSION_2_STATUSES)-1))

CURRENT_VIEW_DICT = dict()
CURRENT_VIEW_DICT['START_SESSION_1'] = "start_session_one.html"
CURRENT_VIEW_DICT['INSERT_EMAIL_NICK'] = "insert_email_nick.html"
CURRENT_VIEW_DICT['INSERT_EMAIL_NICK_FRIEND'] = "insert_email_nick_friend.html"
CURRENT_VIEW_DICT['INSERT_AGE_GENDER'] = "insert_age_gender.html"
CURRENT_VIEW_DICT['INSERT_SELF_FFM'] = "insert_ffm.html"
CURRENT_VIEW_DICT['INSERT_SELF_ROCI'] = "insert_roci.html"
CURRENT_VIEW_DICT['END_1'] = "end_session_one.html"

CURRENT_VIEW_DICT['START_SESSION_2'] = "start_session_two.html"
CURRENT_VIEW_DICT['INSERT_FRIEND_FFM'] = "insert_ffm.html"
CURRENT_VIEW_DICT['INSERT_FRIEND_ROCI'] = "insert_roci.html"
CURRENT_VIEW_DICT['EVALUATE_SONGS_INDIVIDUAL'] = "individual_song_eval.html"
CURRENT_VIEW_DICT['END_2'] = "end_session_two.html"
CURRENT_VIEW_DICT['START_SESSION_3'] = "start_session_three.html"
CURRENT_VIEW_DICT['EVALUATE_SONGS_GROUP_FRIEND'] = "individual_song_group_eval.html"
CURRENT_VIEW_DICT['EVALUATE_SONGS_GROUP_STRANGER'] = "individual_song_group_eval.html"
CURRENT_VIEW_DICT['END_3'] = "end_session_three.html"

ERROR_VIEW_DICT = dict()
ERROR_VIEW_DICT['INVALID_USER'] = "login.html"
ERROR_VIEW_DICT['NO_ADMIN_USER'] = "error_no_admin.html"
ERROR_VIEW_DICT['NO_USER'] = "error_no_user.html"
ERROR_VIEW_DICT['INCOMPLETE_USER'] = "error_incomplete_user.html"

ADMIN_VIEW_DICT = dict()
ADMIN_VIEW_DICT['PROCESS_COMPLETED'] = "process_completed.html"
ADMIN_VIEW_DICT['ADMIN_DASHBOARD'] = "admin_dashboard.html"
ADMIN_VIEW_DICT['ADMIN_STATS'] = "admin_statistics.html"


################### REQUIRED PARAMETERS FOR STATUSES ##################

REQUIRED_PARAMETERS = dict()
REQUIRED_PARAMETERS['START_SESSION_1'] = ()
REQUIRED_PARAMETERS['INSERT_EMAIL_NICK'] = ('email', 'nickname', 'pronoun')
REQUIRED_PARAMETERS['INSERT_EMAIL_NICK_FRIEND'] = ('friend_email', 'friend_nickname', 'friend_pronoun')
REQUIRED_PARAMETERS['INSERT_AGE_GENDER'] = ('age', 'gender')
REQUIRED_PARAMETERS['INSERT_SELF_FFM'] = ('agreeableness', 'agreeableness_swap', 'conscentiousness',
                                          'conscentiousness_swap', 'extraversion', 'extraversion_swap',
                                          'emotional_stability', 'emotional_stability_swap', 'openess', 'openess_swap',
                                          'attention_check', 'attention_check_swap')
REQUIRED_PARAMETERS['INSERT_SELF_ROCI'] = ("question_" + str(i) for i in list(range(1, 29)))

REQUIRED_PARAMETERS['START_SESSION_2'] = ()
REQUIRED_PARAMETERS['INSERT_FRIEND_FFM'] = ('agreeableness', 'agreeableness_swap', 'conscentiousness',
                                          'conscentiousness_swap', 'extraversion', 'extraversion_swap',
                                          'emotional_stability', 'emotional_stability_swap', 'openess', 'openess_swap')
REQUIRED_PARAMETERS['INSERT_FRIEND_ROCI'] = ("question_" + str(i) for i in list(range(1, 29)))
# REQUIRED_PARAMETERS['EVALUATE_SONGS_INDIVIDUAL'] = list("SONG_"+ str(i) for i in list(range(3*TRACK_TO_SELECT))) +\
#                                                    list("SONG_" + str(i) + "_SONG_ID" for i in list(range(3 * TRACK_TO_SELECT)))
REQUIRED_PARAMETERS['EVALUATE_SONGS_INDIVIDUAL'] = list("SONG_"+ str(i) for i in list(range(TRACK_NUMBER))) +\
                                                   list("SONG_" + str(i) + "_SONG_ID" for i in list(range(TRACK_NUMBER)))

REQUIRED_PARAMETERS['START_SESSION_3'] = ()
# REQUIRED_PARAMETERS['EVALUATE_SONGS_GROUP_FRIEND'] = list("SONG_"+ str(i) for i in list(range(2*TRACK_TO_SELECT))) +\
#                                                    list("SONG_" + str(i) + "_SONG_ID" for i in list(range(2 * TRACK_TO_SELECT)))
# REQUIRED_PARAMETERS['EVALUATE_SONGS_GROUP_STRANGER'] = list("SONG_"+ str(i) for i in list(range(2*TRACK_TO_SELECT))) +\
#                                                    list("SONG_" + str(i) + "_SONG_ID" for i in list(range(2 * TRACK_TO_SELECT)))
REQUIRED_PARAMETERS['EVALUATE_SONGS_GROUP_FRIEND'] = list("SONG_"+ str(i) for i in list(range(TRACK_NUMBER))) +\
                                                   list("SONG_" + str(i) + "_SONG_ID" for i in list(range(TRACK_NUMBER)))
REQUIRED_PARAMETERS['EVALUATE_SONGS_GROUP_STRANGER'] = list("SONG_"+ str(i) for i in list(range(TRACK_NUMBER))) +\
                                                   list("SONG_" + str(i) + "_SONG_ID" for i in list(range(TRACK_NUMBER)))

################### GENDER NEUTRAL NICKNAMES ##################

STRANGERS_NICKNAMES = ['Alex','Billy','Charlie','Darcy','Eddie',
                       'Freddy','Gale','Jackie','Jess','Kris',
                       'Robin','Sam','Sandy','Taylor','Tony',
                       'Val','Vic','Willie']


################### PERSONALITY SLIDER TEXTS ##################

PRONOUNS = dict()

PRONOUNS[1]= {
    'SUBJECT' : 'he',
    'OBJECT' : 'him',
    'POSSESSIVE_ADJ' : 'his',
    'POSSESSIVE' : 'his',
    'REFLEXIVE' : 'himself',
    'TO_BE_CON' : 'is',
    'TO_HAVE_CON' : 'has',
    'TO_CARRY_CON' : 'carries',
    'TO_WORRY_CON' : 'worries',
    'TO_TRY_CON' : 'tries',
    'VERB_CON' : 's',
    'IRR_VERB_CON' : 'es'
}

PRONOUNS[2]= {
    'SUBJECT' : 'she',
    'OBJECT' : 'her',
    'POSSESSIVE_ADJ' : 'her',
    'POSSESSIVE' : 'hers',
    'REFLEXIVE' : 'herself',
    'TO_BE_CON' : 'is',
    'TO_HAVE_CON' : 'has',
    'TO_CARRY_CON' : 'carries',
    'TO_WORRY_CON' : 'worries',
    'TO_TRY_CON' : 'tries',
    'VERB_CON' : 's',
    'IRR_VERB_CON' : 'es'
}

PRONOUNS[3]= {
    'SUBJECT' : 'they',
    'OBJECT' : 'them',
    'POSSESSIVE_ADJ' : 'their',
    'POSSESSIVE' : 'theirs',
    'REFLEXIVE' : 'themselves',
    'TO_BE_CON' : 'are',
    'TO_HAVE_CON' : 'have',
    'TO_CARRY_CON' : 'carry',
    'TO_WORRY_CON' : 'worry',
    'TO_TRY_CON' : 'try',
    'VERB_CON' : '',
    'IRR_VERB_CON' : ''
}

AGREEABLENESS_FFM_DICT = dict()
AGREEABLENESS_FFM_DICT['INPUT_ID'] = 'agreeableness'
AGREEABLENESS_FFM_DICT['LOW_STORY'] = '<Nickname> <to_have_con> a sharp tongue and cut<verb_con> others to pieces. ' \
                                      '<Subject> suspect<verb_con> hidden motives in people. <Subject> hold<verb_con> grudges and get<verb_con> back ' \
                                      'at others. ' \
                                      '<Subject> insult<verb_con> and contradict<verb_con> people, believing <subject> <to_be_con> better than them. ' \
                                      '<Subject> make<verb_con> demands on others, and <to_be_con> out for <possessive_adj> own personal gain. ' \
                                      '<Nickname> tend<verb_con> to be calm and quite like<verb_con> exploring new ideas.'
AGREEABLENESS_FFM_DICT['HIGH_STORY'] = '<Nickname> <to_have_con> a good word for everyone, believing that they have good ' \
                                       'intentions. <Subject> respect<verb_con> others and accept<verb_con> people as they are. ' \
                                       '<Subject> make<verb_con> people feel at ease. <Subject> <to_be_con> concerned about others, and trust<verb_con> ' \
                                       'what they say. <Subject> sympathize<verb_con> with others’ feelings, and treat<verb_con> everyone ' \
                                       'equally. <Subject> <to_be_con> easy to satisfy. <Nickname> tend<verb_con> to be quite anxious'

CONSCENTIOUSNESS_FFM_DICT = dict()
CONSCENTIOUSNESS_FFM_DICT['INPUT_ID'] = 'conscentiousness'
CONSCENTIOUSNESS_FFM_DICT['LOW_STORY'] = '<Nickname> procrastinate<verb_con> and waste<verb_con> <possessive_adj> time. <Subject> find<verb_con> it difficult to get down' \
                                         'to work. <Subject> do<irr_verb_con> just enough work to get by and often do<irr_verb_con>n’t see things ' \
                                         'through, leaving them unfinished. <Subject> shirk<verb_con> <possessive_adj> duties and mess<irr_verb_con> things up. ' \
                                         '<Subject> do<irr_verb_con>n’t put <possessive_adj> mind on the task at hand and need<verb_con> a push to get started. ' \
                                         '<Nickname> tend<verb_con> to enjoy talking with people.'
CONSCENTIOUSNESS_FFM_DICT['HIGH_STORY'] = '<Nickname> <to_be_con> always prepared. <Subject> get<verb_con> tasks done right away, paying attention' \
                                          ' to detail. <Subject> make<verb_con> plans and stick<verb_con> to them and <to_carry_con> them out. ' \
                                          '<Subject> complet<irr_verb_con> tasks successfully, doing things according to a plan. ' \
                                          '<Subject> <to_be_con> exacting in <possessive_adj> work; <subject> finish<irr_verb_con> what he start<verb_con>. ' \
                                          '<Nickname> <to_be_con> quite a nice person, tend<verb_con> to enjoy talking with people, ' \
                                          'and quite like<verb_con> exploring new ideas.'

EXTRAVERSION_FFM_DICT = dict()
EXTRAVERSION_FFM_DICT['INPUT_ID'] = 'extraversion'
EXTRAVERSION_FFM_DICT['LOW_STORY'] = '<Nickname> <to_have_con> little to say to others, preferring to stay in the background. ' \
                                     '<Subject> would describe <possessive_adj> life experiences as somewhat dull. ' \
                                     '<Subject> do<irr_verb_con>n’t like drawing attention to <reflexive>, and do<irr_verb_con>n’t talk a lot. ' \
                                     '<Subject> avoid<verb_con> contact with others and <to_be_con> hard to get to know. ' \
                                     '<Subject> retreat<verb_con> from others, finding it difficult to approach them. ' \
                                     '<Subject> keep<verb_con> people at a distance. <Nickname> <to_be_con> quite a nice person.'
EXTRAVERSION_FFM_DICT['HIGH_STORY'] = '<Nickname> feel<verb_con> comfortable around people and make<verb_con> friends easily. ' \
                                      '<Subject> <to_be_con> skilled in handling social situations, and <to_be_con> the life and soul of ' \
                                      'the party. <Subject> know<verb_con> how to start conversations and easily captivate<verb_con> ' \
                                      '<possessive_adj> audience. <Subject> warm<verb_con> up quickly to others, and like<verb_con> talking to a ' \
                                      'lot of different people at parties. <Subject> do<irr_verb_con>n’t mind being the centre ' \
                                      'of attention and cheer<verb_con> people up. <Nickname> can sometimes be insensitive.'

EMOTIONAL_STABILITY_FFM_DICT = dict()
EMOTIONAL_STABILITY_FFM_DICT['INPUT_ID'] = 'emotional_stability'
EMOTIONAL_STABILITY_FFM_DICT['LOW_STORY'] = '<Nickname> often feel<verb_con> sad, and dislike<verb_con> the way <subject> <to_be_con>. <Subject> <to_be_con> often down' \
                                            ' in the dumps and suffer<verb_con> from frequent mood swings. <Subject> <to_be_con> often ' \
                                            'filled with doubts about things and <to_be_con> easily threatened. ' \
                                            '<Subject> get<verb_con> stressed out easily, fearing the worst. ' \
                                            '<Subject> panic<verb_con> easily and <to_worry_con> about things. ' \
                                            '<Nickname> <to_be_con> quite a nice person who tend<verb_con> to enjoy talking with people' \
                                            ' and tend<verb_con> to do <possessive_adj> work.'
EMOTIONAL_STABILITY_FFM_DICT['HIGH_STORY'] = '<Nickname> seldom feel<verb_con> sad and <to_be_con> comfortable with <reflexive>. ' \
                                             '<Subject> rarely get<verb_con> irritated, <to_be_con> not easily bothered by things and <subject>' \
                                             ' <to_be_con> relaxed most of the time. <Subject> <to_be_con> not easily frustrated and seldom' \
                                             ' get<verb_con> angry with <reflexive>. <Subject> remain<verb_con> calm under pressure and rarely' \
                                             ' lose<verb_con> <possessive_adj> composure.'

OPENESS_FFM_DICT = dict()
OPENESS_FFM_DICT['INPUT_ID'] = 'openess'
OPENESS_FFM_DICT['LOW_STORY'] = '<Nickname> <to_be_con> not interested in abstract ideas, as <subject> <to_have_con> difficulty understanding' \
                                ' them. <Subject> do<irr_verb_con> not like art, and dislike<verb_con> going to art galleries. ' \
                                '<Subject> avoids philosophical discussions. <Subject> tend<verb_con> to vote for conservative political' \
                                ' candidates. <Subject> do<irr_verb_con> not like poetry and rarely look<verb_con> for a deeper meaning in ' \
                                'things. <Subject> believe<verb_con> that too much tax money go<irr_verb_con> to supporting artists. ' \
                                '<Subject> <to_be_con> not interested in theoretical discussions. <Nickname> <to_be_con> quite a nice person, ' \
                                'and tend<verb_con> to enjoy talking with people'
OPENESS_FFM_DICT['HIGH_STORY'] = '<Nickname> believe<verb_con> in the importance of art and <to_have_con> a vivid imagination. ' \
                                 '<Subject> tend<verb_con> to vote for liberal political candidates. ' \
                                 '<Subject> enjoy<verb_con> hearing new ideas and thinking about things. ' \
                                 '<Subject> enjoy<verb_con> wild flights of fantasy, getting excited by new ideas.'

ATTENTION_CHECK_DICT = dict()
ATTENTION_CHECK_DICT['INPUT_ID'] = 'attention_check'
ATTENTION_CHECK_DICT['LOW_STORY'] = 'This is an attention check. Please, move the slider to the right.'
ATTENTION_CHECK_DICT['HIGH_STORY'] = 'This is an attention check. Please, move the slider to the right.'

FFM_STORIES = [
    AGREEABLENESS_FFM_DICT,
    CONSCENTIOUSNESS_FFM_DICT,
    EXTRAVERSION_FFM_DICT,
    EMOTIONAL_STABILITY_FFM_DICT,
    OPENESS_FFM_DICT,
    ATTENTION_CHECK_DICT
]

FFM_INSTRUCTION = dict()
FFM_INSTRUCTION[1] = "In each of the next pages, you will be presented with two stories, describing two people.<br>" \
               "Read both carefully, and then move the slider towards the story you feel more similar to you.<br>" \
               "If you move the slider all the way to one of the stories, it means that you are exactly like " \
               "the person described in it.<br>" \
               "If you feel only a bit like them, move the slider less far."
FFM_INSTRUCTION[2] = "In each of the next pages, you will be presented with two stories, describing two people.<br>" \
               "Read both carefully, and then move the slider towards the story you feel more similar to your friend" \
                     " <Nickname>.<br>" \
               "If you move the slider all the way to one of the stories, it means that your friend <Nickname> is" \
                     " exactly like the person described in it.<br>" \
               "If you feel that <Nickname> is only a bit like them, move the slider less far."

FFM_INSTRUCTION_SHORT = dict()
FFM_INSTRUCTION_SHORT[1] = "Please, read carefully the stories below and then move the slider towards the story you" \
                           " feel more similar to you.<br>" \
                           "If you move the slider all the way to one of the stories, it means that you are exactly" \
                           " like the person described in it.<br>" \
                           "If you feel only a bit like them, move the slider less far."
FFM_INSTRUCTION_SHORT[2] = "Please, read carefully the stories below and then move the slider towards the story you " \
                           "feel more similar to your friend <Nickname>.<br>" \
                           "If you move the slider all the way to one of the stories, it means that your friend " \
                           "<Nickname> is exactly like the person described in it.<br>" \
                           "If you feel that <Nickname> is only a bit like them, move the slider less far."

FFM_TITLE = dict()
FFM_TITLE[1] = "Evaluate your personality"
FFM_TITLE[2] = "Evaluate the personality of your friend <Nickname>"


# ################### PERSONALITY SLIDER TEXTS ##################
#
# AGREEABLENESS_FFM_DICT = dict()
# AGREEABLENESS_FFM_DICT['INPUT_ID'] = 'agreeableness'
# AGREEABLENESS_FFM_DICT['LOW_STORY'] = '<Nickname> has a sharp tongue and cuts others to pieces. ' \
#                                       'He suspects hidden motives in people. He holds grudges and gets back ' \
#                                       'at others. ' \
#                                       'He insults and contradicts people, believing he is better than them. ' \
#                                       'He makes demands on others, and is out for his own personal gain.' \
#                                       '<Nickname> tends to be calm and quite likes exploring new ideas'
# AGREEABLENESS_FFM_DICT['HIGH_STORY'] = '<Nickname> has a good word for everyone, believing that they have good ' \
#                                        'intentions. He respects others and accepts people as they are. ' \
#                                        'He makes people feel at ease. He is concerned about others, and trusts ' \
#                                        'what they say. He sympathizes with others’ feelings, and treats everyone ' \
#                                        'equally. He is easy to satisfy. Charlie tends to be quite anxious'
#
# CONSCENTIOUSNESS_FFM_DICT = dict()
# CONSCENTIOUSNESS_FFM_DICT['INPUT_ID'] = 'conscentiousness'
# CONSCENTIOUSNESS_FFM_DICT['LOW_STORY'] = '<Nickname> procrastinates and wastes his time. He finds it difficult to get down' \
#                                          'to work. He does just enough work to get by and often doesn’t see things ' \
#                                          'through, leaving them unfinished. He shirks his duties and messes things up. ' \
#                                          'He doesn’t put his mind on the task at hand and needs a push to get started. ' \
#                                          '<Nickname> tends to enjoy talking with people'
# CONSCENTIOUSNESS_FFM_DICT['HIGH_STORY'] = '<Nickname> is always prepared. He gets tasks done right away, paying attention' \
#                                           ' to detail. He makes plans and sticks to them and carries them out. ' \
#                                           'He completes tasks successfully, doing things according to a plan. ' \
#                                           'He is exacting in his work; he finishes what he starts. ' \
#                                           '<Nickname> is quite a nice person, tends to enjoy talking with people, ' \
#                                           'and quite likes exploring new ideas'
#
# EXTRAVERSION_FFM_DICT = dict()
# EXTRAVERSION_FFM_DICT['INPUT_ID'] = 'extraversion'
# EXTRAVERSION_FFM_DICT['LOW_STORY'] = '<Nickname> has little to say to others, preferring to stay in the background. ' \
#                                      'He would describe his life experiences as somewhat dull. ' \
#                                      'He doesn’t like drawing attention to himself, and doesn’t talk a lot. ' \
#                                      'He avoids contact with others and is hard to get to know. ' \
#                                      'He retreats from others, finding it difficult to approach them. ' \
#                                      'He keeps people at a distance. <Nickname> is quite a nice person'
# EXTRAVERSION_FFM_DICT['HIGH_STORY'] = '<Nickname> feels comfortable around people and makes friends easily. ' \
#                                       'He is skilled in handling social situations, and is the life and soul of ' \
#                                       'the party. He knows how to start conversations and easily captivates ' \
#                                       'his audience. He warms up quickly to others, and likes talking to a ' \
#                                       'lot of different people at parties. He doesn’t mind being the centre ' \
#                                       'of attention and cheers people up. <Nickname> can sometimes be insensitive'
#
# EMOTIONAL_STABILITY_FFM_DICT = dict()
# EMOTIONAL_STABILITY_FFM_DICT['INPUT_ID'] = 'emotional_stability'
# EMOTIONAL_STABILITY_FFM_DICT['LOW_STORY'] = '<Nickname> often feels sad, and dislikes the way he is. He is often down' \
#                                             ' in the dumps and suffers from frequent mood swings. He is often ' \
#                                             'filled with doubts about things and is easily threatened. ' \
#                                             'He gets stressed out easily, fearing the worst. ' \
#                                             'He panics easily and worries about things. ' \
#                                             '<Nickname> is quite a nice person who tends to enjoy talking with people' \
#                                             ' and tends to do his work'
# EMOTIONAL_STABILITY_FFM_DICT['HIGH_STORY'] = '<Nickname> seldom feels sad and is comfortable with himself. ' \
#                                              'He rarely gets irritated, is not easily bothered by things and he' \
#                                              ' is relaxed most of the time. He is not easily frustrated and seldom' \
#                                              ' gets angry with himself. He remains calm under pressure and rarely' \
#                                              ' loses his composure'
#
# OPENESS_FFM_DICT = dict()
# OPENESS_FFM_DICT['INPUT_ID'] = 'openess'
# OPENESS_FFM_DICT['LOW_STORY'] = '<Nickname> is not interested in abstract ideas, as he has difficulty understanding' \
#                                 ' them. He does not like art, and dislikes going to art galleries. ' \
#                                 'He avoids philosophical discussions. He tends to vote for conservative political' \
#                                 ' candidates. He does not like poetry and rarely looks for a deeper meaning in ' \
#                                 'things. He believes that too much tax money goes to supporting artists. ' \
#                                 'He is not interested in theoretical discussions. <Nickname> is quite a nice person, ' \
#                                 'and tends to enjoy talking with people'
# OPENESS_FFM_DICT['HIGH_STORY'] = '<Nickname> believes in the importance of art and has a vivid imagination. ' \
#                                  'He tends to vote for liberal political candidates. ' \
#                                  'He enjoys hearing new ideas and thinking about things. ' \
#                                  'He enjoys wild flights of fantasy, getting excited by new ideas'
#
# ATTENTION_CHECK_DICT = dict()
# ATTENTION_CHECK_DICT['INPUT_ID'] = 'attention_check'
# ATTENTION_CHECK_DICT['LOW_STORY'] = 'THIS IS AN ATTENTION CHECK. PLEASE MOVE THE SLIDER ON THE RIGHT'
# ATTENTION_CHECK_DICT['HIGH_STORY'] = 'THIS IS AN ATTENTION CHECK. PLEASE MOVE THE SLIDER ON THE RIGHT'
#
# FFM_STORIES = [
#     AGREEABLENESS_FFM_DICT,
#     CONSCENTIOUSNESS_FFM_DICT,
#     EXTRAVERSION_FFM_DICT,
#     EMOTIONAL_STABILITY_FFM_DICT,
#     OPENESS_FFM_DICT,
#     ATTENTION_CHECK_DICT
# ]
#
# FFM_INSTRUCTION = dict()
# FFM_INSTRUCTION[1] = "In each of the next pages, you will be presented with two stories, describing two people.<br>" \
#                "Read both carefully, and then move the slider towards the story you feel more similar to you.<br>" \
#                "If you move the slider all the way to one of the stories, it means that you are exactly like " \
#                "the person described in it.<br>" \
#                "If you feel only a bit like them, move the slider less far."
# FFM_INSTRUCTION[2] = "In each of the next pages, you will be presented with two stories, describing two people.<br>" \
#                "Read both carefully, and then move the slider towards the story you feel more similar to your friend" \
#                      " <Nickname>.<br>" \
#                "If you move the slider all the way to one of the stories, it means that your friend <Nickname> is" \
#                      " exactly like the person described in it.<br>" \
#                "If you feel that <Nickname> is only a bit like them, move the slider less far."
#
# FFM_INSTRUCTION_SHORT = dict()
# FFM_INSTRUCTION_SHORT[1] = "Please, read carefully the stories below and then move the slider towards the story you" \
#                            " feel more similar to you.<br>" \
#                            "If you move the slider all the way to one of the stories, it means that you are exactly" \
#                            " like the person described in it.<br>" \
#                            "If you feel only a bit like them, move the slider less far."
# FFM_INSTRUCTION_SHORT[2] = "Please, read carefully the stories below and then move the slider towards the story you " \
#                            "feel more similar to your friend <Nickname>.<br>" \
#                            "If you move the slider all the way to one of the stories, it means that your friend " \
#                            "<Nickname> is exactly like the person described in it.<br>" \
#                            "If you feel that <Nickname> is only a bit like them, move the slider less far."
#
# FFM_TITLE = dict()
# FFM_TITLE[1] = "Evaluate your personality"
# FFM_TITLE[2] = "Evaluate the personality of your friend <Nickname>"

################### ROCI II TEXTS ##################

ROCI_TITLE = dict()
ROCI_TITLE[1] = "Evaluate your conflict resolution style"
ROCI_TITLE[2] = "Evaluate the conflict resolution style of your friend <Nickname>"

ROCI_INSTRUCTIONS = dict()
ROCI_INSTRUCTIONS[1] = "Please check the appropriate box after each statement, to indicate how you handle disagreement" \
                       " or conflict with peers.<br>" \
                       "Try to recall as many recent conflict situations as possible in ranking these statements."

ROCI_INSTRUCTIONS[2] = "Please check the appropriate box after each statement, to indicate how your friend <Nickname> " \
                       "handle disagreement or conflict with peers.<br>" \
                       "Try to recall as many recent conflict situations as possible in ranking these statements."


ROCI_INSTRUCTIONS_SHORT = dict()
ROCI_INSTRUCTIONS_SHORT[1] = "Please check the appropriate box, to indicate how you handle disagreement" \
                       " or conflict with peers.<br>"

ROCI_INSTRUCTIONS_SHORT[2] = "Please check the appropriate box, to indicate how your friend <Nickname> " \
                       "handle disagreement or conflict with peers.<br>"

ROCI_QUESTIONS_SELF = dict()

ROCI_QUESTIONS_SELF[1] = "I try to investigate an issue with my peers to find a solution acceptable to us."
ROCI_QUESTIONS_SELF[2] = "I generally try to satisfy the needs of my peers."
ROCI_QUESTIONS_SELF[3] = "I attempt to avoid being \"put on the spot\" and try to keep my conflict with my peers to " \
                         "myself."
ROCI_QUESTIONS_SELF[4] = "I try to integrate my ideas with those of my peers to come up with a decision jointly."
ROCI_QUESTIONS_SELF[5] = "I try to work with my peers to find solution to a problem that satisfies our expectations."
ROCI_QUESTIONS_SELF[6] = "I usually avoid open discussion of my differences with my peers."
ROCI_QUESTIONS_SELF[7] = "I try to find a middle course to resolve an impasse."
ROCI_QUESTIONS_SELF[8] = "I use my influence to get my ideas accepted."
ROCI_QUESTIONS_SELF[9] = "I use my authority to make a decision in my favor."
ROCI_QUESTIONS_SELF[10] = "I usually accommodate the wishes of my peers."
ROCI_QUESTIONS_SELF[11] = "I give in to the wishes of my peers."
ROCI_QUESTIONS_SELF[12] = "I exchange accurate information with my peers to solve a problem together."
ROCI_QUESTIONS_SELF[13] = "I usually allow concessions to my peers."
ROCI_QUESTIONS_SELF[14] = "I usually propose a middle ground for breaking deadlocks."
ROCI_QUESTIONS_SELF[15] = "I negotiate with my peers so that a compromise can be reached."
ROCI_QUESTIONS_SELF[16] = "I try to stay away from disagreement with my peers."
ROCI_QUESTIONS_SELF[17] = "I avoid an encounter with my peers."
ROCI_QUESTIONS_SELF[18] = "I use my expertise to make a decision in my favor."
ROCI_QUESTIONS_SELF[19] = "I often go along with the suggestions of my peers."
ROCI_QUESTIONS_SELF[20] = "I use \"give and take\" so that a compromise can be made."
ROCI_QUESTIONS_SELF[21] = "I am generally firm in pursuing my side of the issue."
ROCI_QUESTIONS_SELF[22] = "I try to bring all our concerns out in the open so that the issues can be resolved in the" \
                     " best possible way."
ROCI_QUESTIONS_SELF[23] = "I collaborate with my peers to come up with decisions acceptable to us."
ROCI_QUESTIONS_SELF[24] = "I try to satisfy the expectations of my peers."
ROCI_QUESTIONS_SELF[25] = "I sometimes use my power to win a competitive situation."
ROCI_QUESTIONS_SELF[26] = "I try to keep my disagreement with my peers to myself in order to avoid hard feelings."
ROCI_QUESTIONS_SELF[27] = "I try to avoid unpleasant exchanges with my peers."
ROCI_QUESTIONS_SELF[28] = "I try to work with my peers for a proper understanding of a problem."
ROCI_QUESTIONS_SELF[29] = "This is an attention check. Please, select \"Strongly Agree\"."

ROCI_QUESTIONS_PEER = dict()

ROCI_QUESTIONS_PEER[1] = "<Nickname> <to_try_con> to investigate an issue with <possessive_adj> peers to find a solution acceptable to " \
                         "them."
ROCI_QUESTIONS_PEER[2] = "<Nickname> generally <to_try_con> to satisfy the needs of <possessive_adj> peers."
ROCI_QUESTIONS_PEER[3] = "<Nickname> attempt<verb_con> to avoid being \"put on the spot\" and <to_try_con> to keep <possessive_adj> conflict " \
                         "with <possessive_adj> peers to <reflexive>."
ROCI_QUESTIONS_PEER[4] = "<Nickname> <to_try_con> to integrate <possessive_adj> ideas with those of <possessive_adj> peers to come up with a " \
                         "decision jointly."
ROCI_QUESTIONS_PEER[5] = "<Nickname> <to_try_con> to work with <possessive_adj> peers to find solution to a problem that satisfies " \
                         "their expectations."
ROCI_QUESTIONS_PEER[6] = "<Nickname> usually avoid<verb_con> open discussion of <possessive_adj> differences with <possessive_adj> peers."
ROCI_QUESTIONS_PEER[7] = "<Nickname> <to_try_con> to find a middle course to resolve an impasse."
ROCI_QUESTIONS_PEER[8] = "<Nickname> use<verb_con> <possessive_adj> influence to get <possessive_adj> ideas accepted."
ROCI_QUESTIONS_PEER[9] = "<Nickname> use<verb_con> <possessive_adj> authority to make a decision in <possessive_adj> favor."
ROCI_QUESTIONS_PEER[10] = "<Nickname> usually accommodate<verb_con> the wishes of <possessive_adj> peers."
ROCI_QUESTIONS_PEER[11] = "<Nickname> give<verb_con> in to the wishes of <possessive_adj> peers."
ROCI_QUESTIONS_PEER[12] = "<Nickname> exchange<verb_con> accurate information with <possessive_adj> peers to solve a problem together."
ROCI_QUESTIONS_PEER[13] = "<Nickname> usually allow<verb_con> concessions to <possessive_adj> peers."
ROCI_QUESTIONS_PEER[14] = "<Nickname> usually propose<verb_con> a middle ground for breaking deadlocks."
ROCI_QUESTIONS_PEER[15] = "<Nickname> negotiate<verb_con> with <possessive_adj> peers so that a compromise can be reached."
ROCI_QUESTIONS_PEER[16] = "<Nickname> <to_try_con> to stay away from disagreement with <possessive_adj> peers."
ROCI_QUESTIONS_PEER[17] = "<Nickname> avoid<verb_con> an encounter with <possessive_adj> peers."
ROCI_QUESTIONS_PEER[18] = "<Nickname> use<verb_con> <possessive_adj> expertise to make a decision in <possessive_adj> favor."
ROCI_QUESTIONS_PEER[19] = "<Nickname> often go<irr_verb_con> along with the suggestions of <possessive_adj> peers."
ROCI_QUESTIONS_PEER[20] = "<Nickname> use<verb_con> \"give and take\" so that a compromise can be made."
ROCI_QUESTIONS_PEER[21] = "<Nickname> <to_be_con> generally firm in pursuing <possessive_adj> side of the issue."
ROCI_QUESTIONS_PEER[22] = "<Nickname> <to_try_con> to bring all their concerns out in the open so that the issues can be " \
                          "resolved in the best possible way."
ROCI_QUESTIONS_PEER[23] = "<Nickname> collaborate<verb_con> with <possessive_adj> peers to come up with decisions acceptable to them."
ROCI_QUESTIONS_PEER[24] = "<Nickname> <to_try_con> to satisfy the expectations of <possessive_adj> peers."
ROCI_QUESTIONS_PEER[25] = "<Nickname> sometimes use<verb_con> <possessive_adj> power to win a competitive situation."
ROCI_QUESTIONS_PEER[26] = "<Nickname> <to_try_con> to keep <possessive_adj> disagreement with <possessive_adj> peers to <reflexive> in" \
                          " order to avoid hard feelings."
ROCI_QUESTIONS_PEER[27] = "<Nickname> <to_try_con> to avoid unpleasant exchanges with <possessive_adj> peers."
ROCI_QUESTIONS_PEER[28] = "<Nickname> <to_try_con> to work with <possessive_adj> peers for a proper understanding of a problem."
ROCI_QUESTIONS_PEER[29] = "This is an attention check. Please, select \"Strongly Agree\"."

################### SONG EVALUATIONS TEXTS ##################

IND_EVAL_INSTRUCTIONS = "You have to make a car journey of about one hour. " \
                              "In this scenario, you are travelling alone. " \
                              "How much would you like to listen to the following song during the trip?"
IND_EVAL_INSTRUCTIONS_SHORT = "You have to make a car journey of about one hour. " \
                              "In this scenario, you are travelling alone. " \
                              "How much would you like to listen to the following song during the trip?"
IND_EVAL_TITLE = "Evaluate songs for a car trip"

GROUP_EVAL_INSTRUCTIONS = dict()
GROUP_EVAL_INSTRUCTIONS['friend'] = "You have to make a car journey of about one hour. " \
                                    "In this scenario, your friend " \
                                    "<Nickname_peer> should reach the same destination, " \
                                    "hence you proposed to share the trip and the costs. " \
                                    "The following 15 songs have been rated by both of you. " \
                                    "In the next pages, you will see the songs, " \
                                    "together with the evaluations performed by you and your friend. " \
                                    "You will be asked to evaluate how much would you like to listen to " \
                                    "each of these songs during your trip together."
GROUP_EVAL_INSTRUCTIONS['stranger'] = "You have to make a car journey of about one hour. In this scenario, " \
                                      "you posted your trip in an application for car sharing. " \
                                      "<Nickname_peer> and you agreed to share the trip " \
                                      "(in the car it's just you two). " \
                                      "The following 15 songs have been rated by both of you. " \
                                      "In the next pages, you will see the songs, " \
                                      "together with the evaluations performed by you and " \
                                      "your travelling companion. " \
                                      "You will be asked to evaluate how much would you like to listen to" \
                                      " each of these songs during your trip together."

GROUP_EVAL_INSTRUCTIONS_SHORT = dict()
GROUP_EVAL_INSTRUCTIONS_SHORT['friend'] = "You have to make a car journey of about one hour with your friend <Nickname_peer>. " \
                                          "How much would you like to listen to the following song during the trip?"
GROUP_EVAL_INSTRUCTIONS_SHORT['stranger'] = "You have to make a car journey of about one hour with <Nickname_peer>. " \
                                            "How much would you like to listen to the following song during the trip?"

GROUP_EVAL_TITLE = dict()
GROUP_EVAL_TITLE['friend'] = "Evaluate songs for a shared car trip with your friend <Nickname_peer>"
GROUP_EVAL_TITLE['stranger'] = "Evaluate songs for a shared car trip with <Nickname_peer>"
GROUP_SELF_EVAL_MSG = "Your evaluation"
GROUP_PEER_EVAL_MSG = "<Nickname_peer>'s evaluation"




TOP_TRACK_ID_LIST = ['3k79jB4aGmMDUQzEwa46Rz',
 '1BxfuPKGuaTgP7aM0Bbdwr',
 '3qQbCzHBycnDpGskqOWY0E',
 '7ro0hRteUMfnOioTFI5TG1',
 '4DHcnVTT87F0zZhRPYmZ3B',
 '2UW7JaomAMuX9pZrjVpHAU',
 '6pD0ufEQq0xdHSsRbg9LBK',
 '1odExI7RdWc4BT515LTAwj',
 '4Dvkj6JhhA12EX05fT7y2e',
 '1Qrg8KqiBpW07V7PNxwwwL',
 '7FbrGaHYVDmfr7KoLIZnQ7',
 '4eMKD8MRroxCqugpsxCCNb',
 '7mXuWTczZNxG5EDcjFEuJR',
 '2FDTHlrBguDzQkp7PVj16Q',
 '7ABLbnD53cQK00mhcaOUVG',
 '6XSqqQIy7Lm7SnwxS4NrGx',
 '1UMm1Qs3u59Wvk53zBUE8r',
 '5AqiaZwhmC6dIbgWrD5SzV',
 '3Ua0m0YmEjrMi9XErKcNiR',
 '5XeFesFbtLpXzIVDNQP22n',
 '1s7oOCT8vauUh01PbJD6ps',
 '368eeEO3Y2uZUQ6S5oIjcu',
 '4rXLjWdF2ZZpXCVTfWcshS',
 '0DWdj2oZMBFSzRsi2Cvfzf',
 '0RiRZpuVRbi7oqRdSMwhQY',
 '2NFadq6pUeiVEihLvUlOSr',
 '1daDRI9ahBonbWD8YcxOIB',
 '7K3BhSpAxZBznislvUMVtn',
 '2dHHgzDwk4BJdRwy9uXhTO',
 '7bPp2NmpmyhLJ7zWazAXMu',
 '0V3wPSX9ygBnCm8psDIegu',
 '1haJsMtoBhHfvuM7XWuT3W',
 '1Hs1uUl8o2VtDp1DABFq0O',
 '1u8c2t2Cy7UBoG4ArRcF5g',
 '7KA4W4McWYRpgf0fWsJZWB',
 '4uUG5RXrOk84mYEfFvj3cK',
 '6WzRpISELf3YglGAh7TXcG',
 '4fYte8ZvTK14NEhAOZocBi',
 '0ug5NqcwcFR2xrfTkc7k8e',
 '2LBqCSwhJGcFQeTHMVGwy3',
 '4W4fNrZYkobj539TOWsLO2',
 '4daEMLSZCgZ2Mt7gNm2SRa',
 '4JdSXF2p71cr8uCY3UiJM0',
 '3RA55zrRkyPK8Fd86hrMy8',
 '7MXVkk9YMctZqd1Srtv4MB',
 '7jtQIBanIiJOMS6RyCx6jZ',
 '0fABszUFNbNq9IW503Gj8v',
 '3BKD1PwArikchz2Zrlp1qi',
 '609E1JCInJncactoMmkDon',
 '4PA1wK0leCjmRZlP5dQ8Lv',
 '2SOvWt6igzXViIjIiWNWEP',
 '3tt9i3Hhzq84dPS8H7iSiJ',
 '741UUVE2kuITl0c6zuqqbO',
 '5rurggqwwudn9clMdcchxT',
 '3sqrvkNC6IPTIXvvbx9Arw',
 '4R2kfaDFhslZEMJqAFNpdd',
 '26b3oVLrRUaaybJulow9kz',
 '1vYXt7VSjH9JIM5oRRo7vA',
 '6AQbmUe0Qwf5PZnt4HmTXv',
 '5IAESfJjmOYu7cHyX557kz',
 '0JmnkIqdlnUzPaf8sqBRs3',
 '0VjIjW4GlUZAMYd2vXMi3b',
 '5JdLUE9D743ob2RtgmVpVx',
 '3AJwUDP919kvQ9QcozQPxg',
 '1Y3LN4zO1Edc2EluIoSPJN',
 '5odlY52u43F5BjByhxg7wg',
 '7KokYm8cMIXCsGVmUvKtqf',
 '0dS2u2UFd88TIzDDaZDLvS',
 '2tTmW7RDtMQtBk7m2rYeSw',
 '3USxtqRwSYz57Ewm6wWRMp',
 '1mea3bSkSGXuIRvnydlB5b',
 '7qEHsqek33rTcFNT9PFqLf',
 '4FAKtPVycI4DxoOHC01YqD',
 '1zsPaEkglFvxjAhrM8yhpr',
 '505v13epFXodT9fVAJ6h8k',
 '2iVgM5C7m1G4CJGbms301G',
 '6T7FXSuXykeGktMLGp8WgE',
 '2QjOHCTQ1Jl3zawyYOpxh6',
 '1oWkcc7hQdVYPQMyQ6AFov',
 '6Ec5LeRzkisa5KJtwLfOoW',
 '0NZPBYD5qbEWRs3PrGiRkT',
 '6Sq7ltF9Qa7SNFBsV5Cogx',
 '7yq4Qj7cqayVTp3FF9CWbm',
 '23RoR84KodL5HWvUTneQ1w',
 '1DmW5Ep6ywYwxc2HMT5BG6',
 '6GGtHZgBycCgGBUhZo81xe',
 '1Lo0QY9cvc8sUB2vnIOxDT',
 '5Odq8ohlgIbQKMZivbWkEo',
 '567e29TDzLwZwfDuEpGTwo',
 '3oNnzH6hmqIGIhJ1NcHlrh',
 '0cNSq9T5l8gZnpY14rsTR2',
 '41bmnQZoDMQdDh5zyomtW7',
 '0PB0O24JqAuNdOAFVJljMS',
 '3kf0WdFOalKWBkCCLJo4mA',
 '1VvoSJiPG9dFsDQjTkACvG',
 '2Hc1LaV6bzFil3dE71eORA',
 '4nrPB8O7Y7wsOCJdgXkthe',
 '2Hh3ETdQKrmSI3QS0hme7g',
 '1R0a2iXumgCiFb7HEZ7gUE',
 '1FEiijYPJtyswChfcpv3p0',
 '561jH07mF1jHuk7KlaeF0s',
 '4iZ4pt7kvcaH6Yo8UoZ4s2',
 '6f8wbdo8KU5ETWJA7lapgS',
 '7j4OmvkjRz0PrjFADlHfQx',
 '2eAvDnpXP5W0cVtiI0PUxV',
 '2HbKqm4o0w5wEeEFXm2sD4',
 '51FvjPEGKq2zByeeEQ43V9',
 '2VzCjpKvPB1l1tqLndtAQa',
 '1dGr1c8CrMLDpV6mPbImSI',
 '3fDTzkvrOo5xQIO480Qmsb',
 '5NhLA2P7AiV3cloVmwtwLS',
 '26cvTWJq2E1QqN4jyH2OTU',
 '6JIC3hbC28JZKZ8AlAqX8h',
 '6UelLqGlWMcVH1E5c4H7lY',
 '4Ls53fBNVfaXTROBi6X8Hw',
 '5w40ZYhbBMAlHYNDaVJIUu',
 '1MB8kTH7VKvAMfL9SHgJmG',
 '73RbfOTJIjHzi2pcVHjeHM',
 '5eTaQYBE1yrActixMAeLcZ',
 '68Dni7IE4VyPkTOH9mRWHr',
 '54ipXppHLA8U4yqpOFTUhr',
 '2CeKVsFFXG4QzA415QygGb',
 '0u2P5u6lvoDfwTYjAADbn4',
 '46hzNOUOAlivuCZZ0wE3zi',
 '0tgVpDi06FyKpA1z0VMD4v',
 '5PLqXnvHH7Gh6CcfiUEr7e',
 '4uqJelb9THHmJ3OCohg4ZJ',
 '4RvWPyQ5RL0ao9LPZeSouE',
 '6Um358vY92UBv5DloTRX9L',
 '2a1o6ZejUi8U3wzzOtCOYw',
 '2uhw2oYbugGJbn10wipNX5',
 '50x1Ic8CaXkYNvjmxe3WXy',
 '5wG3HvLhF6Y5KTGlK0IW3J',
 '3hUxzQpSfdDqwM3ZTFQY0K',
 '58ge6dfP91o9oXMzq3XkIS',
 '22skzmqfdWrjJylampe0kt',
 '5g7sDjBhZ4I3gcFIpkrLuI',
 '5O2P9iiztwhomNh8xkR9lJ',
 '1xK59OXxi2TAAAbmZK0kBL',
 '0pqnGHJpmpxLKifKRmU6WP',
 '0PZ04XgQ14FmKZBg3Gxlhr',
 '0ll8uFnc0nANY35E0Lfxvg',
 '7MVIfkyzuUmQ716j8U7yGR',
 '7lQ8MOhq6IN2w8EYcFNSUk',
 '4uOBL4DDWWVx4RhYKlPbPC',
 '6dgUya35uo964z7GZXM07g',
 '39MK3d3fonIP8Mz9oHCTBB',
 '228BxWXUYQPJrJYHDLOHkj',
 '7sliFe6W30tPBPh6dvZsIH',
 '0U9CZWq6umZsN432nh3WWT',
 '0B7wvvmu9EISAwZnOpjhNI',
 '3k3NWokhRRkEPhCzPmV8TW',
 '0cqRj7pUJDkTCEsJkx8snD',
 '25OeKzcqakFPaJlXHPE5lm',
 '65FftemJ1DbbZ45DUfHJXE',
 '0eFMbKCRw8KByXyWBw8WO7',
 '6TBzRwnX2oYd8aOrOuyK1p',
 '7ovUcF5uHTBRzUpB6ZOmvt',
 '76OGwb5RA9h4FxQPT33ekc',
 '6I3mqTwhRpn34SLVafSH7G',
 '5IgjP7X4th6nMNDh4akUHb',
 '2tpWsVSb9UEmDRxAl1zhX1',
 '3tiJUOfAEqIrLFRQgGgdoY',
 '28BSTgZH1ckI8Xfy8LXaRz',
 '3p7XQpdt8Dr6oMXSvRZ9bg',
 '1zv3WFUbZ5vPxFq9I2jAU1',
 '4hKLzFvNwHF6dPosGT30ed',
 '0JXXNGljqupsJaZsgSbMZV',
 '1JSTJqkT5qHq8MDJnJbRE1',
 '0EhuGnOS6fTc5l5UNtDEH2',
 '5FVd6KXrgO9B3JPmC8OPst',
 '5gDWsRxpJ2lZAffh5p7K0w',
 '086myS9r57YsLbJpU0TgK9',
 '3HOKxuTDmNVmIlCIpBiD8m',
 '37F0uwRSrdzkBiuj0D5UHI',
 '3AVrVz5rK8Hrqo9YGiVGN5',
 '7qiZfU4dY1lWllzX7mPBI3',
 '2LawezPeJhN4AWuSB0GtAU',
 '3E7dfMvvCLUddWissuqMwr',
 '6YC5ibtCMyXU1RQ1LkQLIn',
 '3hRV0jL3vUpRrcy398teAU',
 '5QW9K4A1gMnIi94YUxtsfM',
 '0IKeDy5bT9G0bA7ZixRT4A',
 '2qxmye6gAegTMjLKEBoR3d',
 '1IHWl5LamUGEuP4ozKQSXZ',
 '0otRX6Z89qKkHkQ9OqJpKt',
 '5CZ40GBx1sQ9agT82CLQCT',
 '5QO79kh1waicV47BqGRL3g',
 '0hDE81j4N2DPLbEY4tiCDs',
 '1u9oZzM8CTeCMXsdTXaOtY',
 '7BqBn9nzAq8spo5e7cZ0dJ',
 '3F5CgOj3wFlRv51JsHbxhe',
 '1zi7xx7UVEFkmKfv06H8x0',
 '3PH1nUysW7ybo3Yu8sqlPN',
 '1vvcEHQdaUTvWt0EIUYcFK',
 '5qaEfEh1AtSdrdrByCP7qR',
 '11xC6P3iKYpFThT6Ce1KdG',
 '3xKsf9qdS1CyvXSMEid6g8',
 '6HU7h9RYOaPRFeh0R3UeAr',
 '0CYTGMBYkwUxrj1MWDLrC5']

######################## INSTRUMENTS KEYS

PERSONALITY_INSTRUMENTS = ['FFM', 'ROCI']
PERSONALITY_TRAITS = dict()
PERSONALITY_TRAITS['FFM'] = ['AGR','CON','EXT','EMO','OPE']
PERSONALITY_TRAITS['ROCI'] = ['INT','OBL','DOM','AVO','COM']
PERSONALITY_INSTRUMENT_MIN_VALUE = dict()
PERSONALITY_INSTRUMENT_MAX_VALUE = dict()
PERSONALITY_INSTRUMENT_MIN_VALUE['FFM'] = 18
PERSONALITY_INSTRUMENT_MAX_VALUE['FFM'] = 162
PERSONALITY_INSTRUMENT_MIN_VALUE['ROCI'] = 1
PERSONALITY_INSTRUMENT_MAX_VALUE['ROCI'] = 5