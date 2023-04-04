import os

#################### GENERAL CONFIG TO SET UP IN ENVIRONMENTAL VARIABLES ############################

# This are Spotify API Credentials! Create another spotify account create an application!
client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

HOST = os.environ['HOST']
PORT =  os.environ['PORT']
main_page_uri = "http://"+HOST+":"+PORT

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
ADMIN_USER_ID_LIST = (os.environ['SUPER_ADMIN'],)

#################### EMAIL TEXT  ############################

PARTICIPATION_EMAIL_TEXT = "We will conduct a user study evaluating the satisfaction related on listening to different " \
                           "songs in different contexts, alone or in a group. For the participation, it is necessary that " \
                           "you are a regular user of the Spotify app.\n" \
                           "The experiment is composed by three sessions, scheduled in the next 3 weeks: the first session" \
                           " should take approx. 20 min, the second session 25 min and the third 5 minutes. You will be" \
                           " asked to register on our web application using your Spotify account and to indicate the" \
                           " email address and the nickname of a second person who can perform the experiment with you" \
                           " (each one will carry out the experiment individually). Such person should be somebody with" \
                           " whom you have a close relationship (e.g., your partner or a close friend) and a regular user" \
                           " of the Spotify app.\n" \
                           "We will use your email address to notify the start of sessions 2 and 3," \
                           " and to provide the link on which to connect to perform the sessions. You will be able to" \
                           " withdraw from the study in any moment. After the end of the last session, you will have 30" \
                           " days to ask for deleting your data; after that, we will delete all the email addresses, and" \
                           " all the provided data will be stored anonymously. Among the participants, we will extract" \
                           " one winner for an Amazon voucher worth 20 euros.\n" \
                           "Please use the following link to start the session 1: http://localhost:5000/consent_form \n" \
                           "If you need further information or clarification, do not hesitate to write via email to:\n" \
                           "f.barile@maastrichtuniversity.nl. \n" \
                           "Thanks in advance for your kind cooperation."

INVITATION_EMAIL_TEXT = "You have been invited by your friend <EmailFriend> to participate in our study user study " \
                        "evaluating the satisfaction related on listening to different " \
                        "songs in different contexts, alone or in a group. For the participation, it is necessary that " \
                        "you are a regular user of the Spotify app.\n" \
                        "The experiment is composed by three sessions, scheduled in the next 3 weeks: the first session" \
                        " should take approx. 20 min, the second session 25 min and the third 5 minutes. You will be" \
                        " asked to register on our web application using your Spotify account." \
                        "We will use your email address to notify the start of sessions 2 and 3," \
                        " and to provide the link on which to connect to perform the sessions. You will be able to" \
                        " withdraw from the study in any moment. After the end of the last session, you will have 30" \
                        " days to ask for deleting your data; after that, we will delete all the email addresses, and" \
                        " all the provided data will be stored anonymously. Among the participants, we will extract" \
                        " one winner for an Amazon voucher worth 20 euros.\n" \
                        "Please use the following link to start the session 1: http://localhost:5000/consent_form_invited \n" \
                        "If you need further information or clarification, do not hesitate to write via email to:\n" \
                        "f.barile@maastrichtuniversity.nl. \n" \
                        "Thanks in advance for your kind cooperation."

#################### SESSION ROUTES  ############################

SESSION_ROUTE = dict()
SESSION_ROUTE[1] = "session_one"
SESSION_ROUTE[2] = "session_two"
SESSION_ROUTE[3] = "session_three"

SESSION_1_STATUSES = (
    'INSERT_EMAIL_NICK',
    'INSERT_EMAIL_NICK_FRIEND',
    'INSERT_AGE_GENDER',
    'INSERT_SELF_FFM',
    'INSERT_SELF_ROCI',
    'END_1'
)

#################### STATUSES AND VIEWS  ############################

SESSION_2_STATUSES = (
    'START_SESSION_2',
    'INSERT_FRIEND_FFM',
    'INSERT_FRIEND_ROCI',
    'EVALUATE_SONGS_INDIVIDUAL',
    'END_2'
)

SESSION_3_STATUSES = (
    'START_SESSION_3',
    'EVALUATE_SONGS_GROUP_FRIEND',
    'EVALUATE_SONGS_GROUP_STRANGER',
    'END_3'
)

STATUSES = dict()
STATUSES[1] = SESSION_1_STATUSES
STATUSES[2] = SESSION_2_STATUSES
STATUSES[3] = SESSION_3_STATUSES

CURRENT_VIEW_DICT = dict()
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
ERROR_VIEW_DICT['INVALID_USER'] = "invalid_user.html"
ERROR_VIEW_DICT['NO_ADMIN_USER'] = "no_admin_user.html"

ADMIN_VIEW_DICT = dict()
ADMIN_VIEW_DICT['PROCESS_COMPLETED'] = "process_completed.html"
ADMIN_VIEW_DICT['ADMIN_DASHBOARD'] = "admin_dashboard.html"

################### REQUIRED PARAMETERS FOR STATUSES ##################

REQUIRED_PARAMETERS = dict()
REQUIRED_PARAMETERS['INSERT_EMAIL_NICK'] = ('email', 'nickname')
REQUIRED_PARAMETERS['INSERT_EMAIL_NICK_FRIEND'] = ('friend_email', 'friend_nickname')
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
REQUIRED_PARAMETERS['EVALUATE_SONGS_INDIVIDUAL'] = list("SONG_"+ str(i) for i in list(range(3*TRACK_TO_SELECT))) +\
                                                   list("SONG_" + str(i) + "_SONG_ID" for i in list(range(3 * TRACK_TO_SELECT)))

REQUIRED_PARAMETERS['START_SESSION_3'] = ()
REQUIRED_PARAMETERS['EVALUATE_SONGS_GROUP_FRIEND'] = list("SONG_"+ str(i) for i in list(range(2*TRACK_TO_SELECT))) +\
                                                   list("SONG_" + str(i) + "_SONG_ID" for i in list(range(2 * TRACK_TO_SELECT)))
REQUIRED_PARAMETERS['EVALUATE_SONGS_GROUP_STRANGER'] = list("SONG_"+ str(i) for i in list(range(2*TRACK_TO_SELECT))) +\
                                                   list("SONG_" + str(i) + "_SONG_ID" for i in list(range(2 * TRACK_TO_SELECT)))

################### GENDER NEUTRAL NICKNAMES ##################

STRANGERS_NICKNAMES = ['Alex','Billy','Charlie','Darcy','Eddie',
                       'Freddy','Gale','Jackie','Jess','Kris',
                       'Robin','Sam','Sandy','Taylor','Tony',
                       'Val','Vic','Willie']

################### PERSONALITY SLIDER TEXTS ##################

AGREEABLENESS_FFM_DICT = dict()
AGREEABLENESS_FFM_DICT['INPUT_ID'] = 'agreeableness'
AGREEABLENESS_FFM_DICT['LOW_STORY'] = '<Nickname> has a sharp tongue and cuts others to pieces. ' \
                                      'He suspects hidden motives in people. He holds grudges and gets back ' \
                                      'at others. ' \
                                      'He insults and contradicts people, believing he is better than them. ' \
                                      'He makes demands on others, and is out for his own personal gain.' \
                                      '<Nickname> tends to be calm and quite likes exploring new ideas'
AGREEABLENESS_FFM_DICT['HIGH_STORY'] = '<Nickname> has a good word for everyone, believing that they have good ' \
                                       'intentions. He respects others and accepts people as they are. ' \
                                       'He makes people feel at ease. He is concerned about others, and trusts ' \
                                       'what they say. He sympathizes with others’ feelings, and treats everyone ' \
                                       'equally. He is easy to satisfy. Charlie tends to be quite anxious'

CONSCENTIOUSNESS_FFM_DICT = dict()
CONSCENTIOUSNESS_FFM_DICT['INPUT_ID'] = 'conscentiousness'
CONSCENTIOUSNESS_FFM_DICT['LOW_STORY'] = '<Nickname> procrastinates and wastes his time. He finds it difficult to get down' \
                                         'to work. He does just enough work to get by and often doesn’t see things ' \
                                         'through, leaving them unfinished. He shirks his duties and messes things up. ' \
                                         'He doesn’t put his mind on the task at hand and needs a push to get started. ' \
                                         '<Nickname> tends to enjoy talking with people'
CONSCENTIOUSNESS_FFM_DICT['HIGH_STORY'] = '<Nickname> is always prepared. He gets tasks done right away, paying attention' \
                                          ' to detail. He makes plans and sticks to them and carries them out. ' \
                                          'He completes tasks successfully, doing things according to a plan. ' \
                                          'He is exacting in his work; he finishes what he starts. ' \
                                          'Josh is quite a nice person, tends to enjoy talking with people, ' \
                                          'and quite likes exploring new ideas'

EXTRAVERSION_FFM_DICT = dict()
EXTRAVERSION_FFM_DICT['INPUT_ID'] = 'extraversion'
EXTRAVERSION_FFM_DICT['LOW_STORY'] = '<Nickname> has little to say to others, preferring to stay in the background. ' \
                                     'He would describe his life experiences as somewhat dull. ' \
                                     'He doesn’t like drawing attention to himself, and doesn’t talk a lot. ' \
                                     'He avoids contact with others and is hard to get to know. ' \
                                     'He retreats from others, finding it difficult to approach them. ' \
                                     'He keeps people at a distance. <Nickname> is quite a nice person'
EXTRAVERSION_FFM_DICT['HIGH_STORY'] = '<Nickname> feels comfortable around people and makes friends easily. ' \
                                      'He is skilled in handling social situations, and is the life and soul of ' \
                                      'the party. He knows how to start conversations and easily captivates ' \
                                      'his audience. He warms up quickly to others, and likes talking to a ' \
                                      'lot of different people at parties. He doesn’t mind being the centre ' \
                                      'of attention and cheers people up. <Nickname> can sometimes be insensitive'

EMOTIONAL_STABILITY_FFM_DICT = dict()
EMOTIONAL_STABILITY_FFM_DICT['INPUT_ID'] = 'emotional_stability'
EMOTIONAL_STABILITY_FFM_DICT['LOW_STORY'] = '<Nickname> often feels sad, and dislikes the way he is. He is often down' \
                                            ' in the dumps and suffers from frequent mood swings. He is often ' \
                                            'filled with doubts about things and is easily threatened. ' \
                                            'He gets stressed out easily, fearing the worst. ' \
                                            'He panics easily and worries about things. ' \
                                            '<Nickname> is quite a nice person who tends to enjoy talking with people' \
                                            ' and tends to do his work'
EMOTIONAL_STABILITY_FFM_DICT['HIGH_STORY'] = '<Nickname> seldom feels sad and is comfortable with himself. ' \
                                             'He rarely gets irritated, is not easily bothered by things and he' \
                                             ' is relaxed most of the time. He is not easily frustrated and seldom' \
                                             ' gets angry with himself. He remains calm under pressure and rarely' \
                                             ' loses his composure'

OPENESS_FFM_DICT = dict()
OPENESS_FFM_DICT['INPUT_ID'] = 'openess'
OPENESS_FFM_DICT['LOW_STORY'] = '<Nickname> is not interested in abstract ideas, as he has difficulty understanding' \
                                ' them. He does not like art, and dislikes going to art galleries. ' \
                                'He avoids philosophical discussions. He tends to vote for conservative political' \
                                ' candidates. He does not like poetry and rarely looks for a deeper meaning in ' \
                                'things. He believes that too much tax money goes to supporting artists. ' \
                                'He is not interested in theoretical discussions. <Nickname> is quite a nice person, ' \
                                'and tends to enjoy talking with people'
OPENESS_FFM_DICT['HIGH_STORY'] = '<Nickname> believes in the importance of art and has a vivid imagination. ' \
                                 'He tends to vote for liberal political candidates. ' \
                                 'He enjoys hearing new ideas and thinking about things. ' \
                                 'He enjoys wild flights of fantasy, getting excited by new ideas'

ATTENTION_CHECK_DICT = dict()
ATTENTION_CHECK_DICT['INPUT_ID'] = 'attention_check'
ATTENTION_CHECK_DICT['LOW_STORY'] = 'THIS IS AN ATTENTION CHECK. PLEASE MOVE THE SLIDER ON THE RIGHT'
ATTENTION_CHECK_DICT['HIGH_STORY'] = 'THIS IS AN ATTENTION CHECK. PLEASE MOVE THE SLIDER ON THE RIGHT'

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
ROCI_QUESTIONS_SELF[29] = "THIS IS AN ATTENTION CHECK! PLEASE SELECT \"Strongly Agree\"."

ROCI_QUESTIONS_PEER = dict()

ROCI_QUESTIONS_PEER[1] = "<Nickname> tries to investigate an issue with his/her peers to find a solution acceptable to " \
                         "them."
ROCI_QUESTIONS_PEER[2] = "<Nickname> generally tries to satisfy the needs of his/her peers."
ROCI_QUESTIONS_PEER[3] = "<Nickname> attempts to avoid being \"put on the spot\" and tries to keep his/her conflict " \
                         "with his/her peers to himself/herself."
ROCI_QUESTIONS_PEER[4] = "<Nickname> tries to integrate his/her ideas with those of his/her peers to come up with a " \
                         "decision jointly."
ROCI_QUESTIONS_PEER[5] = "<Nickname> tries to work with his/her peers to find solution to a problem that satisfies " \
                         "their expectations."
ROCI_QUESTIONS_PEER[6] = "<Nickname> usually avoids open discussion of his/her differences with his/her peers."
ROCI_QUESTIONS_PEER[7] = "<Nickname> tries to find a middle course to resolve an impasse."
ROCI_QUESTIONS_PEER[8] = "<Nickname> uses his/her influence to get his/her ideas accepted."
ROCI_QUESTIONS_PEER[9] = "<Nickname> uses his/her authority to make a decision in his/her favor."
ROCI_QUESTIONS_PEER[10] = "<Nickname> usually accommodates the wishes of his/her peers."
ROCI_QUESTIONS_PEER[11] = "<Nickname> gives in to the wishes of his/her peers."
ROCI_QUESTIONS_PEER[12] = "<Nickname> exchanges accurate information with his/her peers to solve a problem together."
ROCI_QUESTIONS_PEER[13] = "<Nickname> usually allows concessions to his/her peers."
ROCI_QUESTIONS_PEER[14] = "<Nickname> usually proposes a middle ground for breaking deadlocks."
ROCI_QUESTIONS_PEER[15] = "<Nickname> negotiates with his/her peers so that a compromise can be reached."
ROCI_QUESTIONS_PEER[16] = "<Nickname> tries to stay away from disagreement with his/her peers."
ROCI_QUESTIONS_PEER[17] = "<Nickname> avoids an encounter with his/her peers."
ROCI_QUESTIONS_PEER[18] = "<Nickname> uses his/her expertise to make a decision in his/her favor."
ROCI_QUESTIONS_PEER[19] = "<Nickname> often goes along with the suggestions of his/her peers."
ROCI_QUESTIONS_PEER[20] = "<Nickname> uses \"give and take\" so that a compromise can be made."
ROCI_QUESTIONS_PEER[21] = "<Nickname> is generally firm in pursuing his/her side of the issue."
ROCI_QUESTIONS_PEER[22] = "<Nickname> tries to bring all their concerns out in the open so that the issues can be " \
                          "resolved in the best possible way."
ROCI_QUESTIONS_PEER[23] = "<Nickname> collaborates with his/her peers to come up with decisions acceptable to them."
ROCI_QUESTIONS_PEER[24] = "<Nickname> tries to satisfy the expectations of his/her peers."
ROCI_QUESTIONS_PEER[25] = "<Nickname> sometimes uses his/her power to win a competitive situation."
ROCI_QUESTIONS_PEER[26] = "<Nickname> tries to keep his/her disagreement with his/her peers to himself/herself in" \
                          " order to avoid hard feelings."
ROCI_QUESTIONS_PEER[27] = "<Nickname> tries to avoid unpleasant exchanges with his/her peers."
ROCI_QUESTIONS_PEER[28] = "<Nickname> tries to work with his/her peers for a proper understanding of a problem."
ROCI_QUESTIONS_PEER[29] = "THIS IS AN ATTENTION CHECK! PLEASE SELECT \"Strongly Agree\"."

################### SONG EVALUATIONS TEXTS ##################

IND_EVAL_INSTRUCTIONS = "You have to make a car journey of about one hour. How much would you like to listen to one of these songs during the trip?"
IND_EVAL_INSTRUCTIONS_SHORT = "You have to make a car journey of about one hour. How much would you like to listen to the following song during the trip?"
IND_EVAL_TITLE = "Evaluate songs for a car trip"

GROUP_EVAL_INSTRUCTIONS = dict()
GROUP_EVAL_INSTRUCTIONS['friend'] = "You have to make a car journey of about one hour. In this scenario, your friend " \
                                    "<Nickname> should reach the same destination, hence you proposed to share the trip and the costs. " \
                                    "The following 10 songs have been obtained by analyzing your Spotify account and the one of your travelling companion. " \
                                    "In the next pages, you will see the selected songs, together with the evaluations performed by you and your travelling companion." \
                                    "How much would you like to listen to one of these songs during your trip together?"
GROUP_EVAL_INSTRUCTIONS['stranger'] = "You have to make a car journey of about one hour. In this scenario, you posted your trip in an application for car sharing. " \
                                      "<Nickname> and you agreed to share the trip (in the car it's just you two). " \
                                      "The following 10 songs have been obtained by analyzing your Spotify account and the one of your travelling companion. " \
                                      "Below, you can see the selected songs, together with the evaluations performed by you and your travelling companion." \
                                      "In the next pages, you will see the selected songs, together with the evaluations performed by you and your travelling companion." \
                                      "How much would you like to listen to one of these songs during your trip together?"

GROUP_EVAL_INSTRUCTIONS_SHORT = dict()
GROUP_EVAL_INSTRUCTIONS_SHORT['friend'] = "You have to make a car journey of about one hour with your friend <Nickname>." \
                                          "How much would you like to listen the following song during the trip?"
GROUP_EVAL_INSTRUCTIONS_SHORT['stranger'] = "You have to make a car journey of about one hour with <Nickname>." \
                                            " How much would you like to listen the following song during the trip?"

GROUP_EVAL_TITLE = dict()
GROUP_EVAL_TITLE['friend'] = "Evaluate songs for a car shared car trip with your friend <Nickname>"
GROUP_EVAL_TITLE['stranger'] = "Evaluate songs for a car shared car trip with <Nickname>"
GROUP_SELF_EVAL_MSG = "Your evaluation"
GROUP_PEER_EVAL_MSG = "<Nickname>'s evaluation"