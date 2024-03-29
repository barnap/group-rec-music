import dao.db_utils as db_utils
from dao import dao_session_info, dao_user
import config
import control
from utils import utils

def drop_database():
    drop_database_query = '''DROP DATABASE IF EXISTS  ''' + config.database + ''';'''
    db = db_utils.create_connection_dbms()
    cur = db.cursor()
    cur.execute(drop_database_query)

    print('Database deleted')
    db.close()

def check_databas_exists():
    exist_db_query = '''select exists(SELECT datname FROM pg_catalog.pg_database WHERE datname = %s );'''
    db = db_utils.create_connection_dbms()
    # cur = db.cursor()
    # cur.execute(drop_database_query)

    cur = db.cursor()
    cur.execute(exist_db_query, (config.database,))

    result = cur.fetchone()
    print('Executed the query')
    print(result[0])
    db.close()

    return result[0]


def create_database():
    # drop_database_query = '''DROP DATABASE IF EXISTS  ''' + config.database + ''';'''

    create_database_query = '''CREATE DATABASE ''' + config.database + '''
            WITH
            OWNER = %s
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1
            IS_TEMPLATE = False;
        '''

    db = db_utils.create_connection_dbms()
    # cur = db.cursor()
    # cur.execute(drop_database_query)

    cur = db.cursor()
    cur.execute(create_database_query, (config.user,))

    print('Database created')
    db.close()


def create_user_table():
    create_user_table_query = '''CREATE TABLE IF NOT EXISTS public.user_app
        (
        id text COLLATE pg_catalog."default" NOT NULL,
        nickname text COLLATE pg_catalog."default",
        email text COLLATE pg_catalog."default",
        friend_id text COLLATE pg_catalog."default",
        friend_nickname text COLLATE pg_catalog."default",
        stranger_id text COLLATE pg_catalog."default",
        stranger_nickname text COLLATE pg_catalog."default",
        gender text COLLATE pg_catalog."default",
        pronoun text COLLATE pg_catalog."default",
        age_group text COLLATE pg_catalog."default",
        friend_pronoun text COLLATE pg_catalog."default",
        spotify_url text COLLATE pg_catalog."default",
        agreableness_self_eval double precision,
        conscentiousness_self_eval double precision,
        extraversion_self_eval double precision,
        emotional_stability_self_eval double precision,
        openess_self_eval double precision,
        agreableness_friend_eval double precision,
        conscentiousness_friend_eval double precision,
        extraversion_friend_eval double precision,
        emotional_stability_friend_eval double precision,
        openess_friend_eval double precision,
        integrating_self_eval double precision,
        obliging_self_eval double precision,
        dominating_self_eval double precision,
        avoiding_self_eval double precision,
        compromising_self_eval double precision,
        integrating_friend_eval double precision,
        obliging_friend_eval double precision,
        dominating_friend_eval double precision,
        avoiding_friend_eval double precision,
        compromising_friend_eval double precision,
        current_state text COLLATE pg_catalog."default",
        is_invited boolean,
        friend_email text COLLATE pg_catalog."default",
        is_user boolean,
        is_admin boolean,
        attention_ffm_self boolean,
        attention_roci_self boolean,
        attention_ffm_peer boolean,
        attention_roci_peer boolean,
        attention_individual boolean,
        attention_group_friend boolean,
        attention_group_stranger boolean,
        CONSTRAINT user_pkey PRIMARY KEY (id)
        )
        
        TABLESPACE pg_default;
        
        ALTER TABLE IF EXISTS public.user_app
        OWNER to ''' + config.user + ''';
    '''

    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute(create_user_table_query)

    db.commit()
    print('User table created')
    db.close()


def create_playlist_table():
    create_plylist_table_query = '''CREATE TABLE IF NOT EXISTS public.playlist_evaluation
        (
            song_id text COLLATE pg_catalog."default" NOT NULL,
            user_id text COLLATE pg_catalog."default" NOT NULL,
            relationship text COLLATE pg_catalog."default" NOT NULL,
            self_eval double precision,
            peer_eval double precision,
            group_self_eval double precision,
            is_original boolean,
            peer_id text COLLATE pg_catalog."default",
            CONSTRAINT playlist_evaluation_pkey PRIMARY KEY (song_id, user_id, relationship)
        )
        
        TABLESPACE pg_default;
        
        ALTER TABLE IF EXISTS public.playlist_evaluation
        OWNER to ''' + config.user + ''';
    '''

    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute(create_plylist_table_query)

    db.commit()
    print('Playlist table created')
    db.close()


def create_session_info_table():
    create_session_info_table_query = '''CREATE TABLE IF NOT EXISTS public.session_info
        (
            id integer NOT NULL DEFAULT 1,
            current_session integer NOT NULL DEFAULT 1,
            CONSTRAINT session_info_pkey PRIMARY KEY (id)
        )
        
        TABLESPACE pg_default;
        
        ALTER TABLE IF EXISTS public.session_info
        OWNER to ''' + config.user + ''';
    '''

    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute(create_session_info_table_query)

    db.commit()
    print('Session info table created')
    db.close()


if __name__ == '__main__':
    # print(dao_user.get_user_email_list())
    # user_email_list = dao_user.get_user_email_list()
    # for email in user_email_list:
    #     utils.send_email_start_session_2(email)

    # dao_session_info.init_session_info()

    if check_databas_exists():
        print("THE DATABASE ALREADY EXISTS")
    else:
        create_database()
        create_user_table()
        create_playlist_table()
        create_session_info_table()
        dao_session_info.init_session_info()
        print("CURRENT SESSION: ", dao_session_info.load_current_session())
