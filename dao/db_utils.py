import sys

import dao.dao_session_info

sys.path.append('../')
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import config

def create_connection_db():
    '''
    Creates connection to the database!
    :return:
    '''
    connection = psycopg2.connect(user=config.user,
                                  password=config.password,
                                  host=config.host,
                                  port=config.port,
                                  database=config.database)
    return connection

def create_connection_dbms():
    '''
    Creates connection to the database!
    :return:
    '''
    # con = psycopg2.connect("user=test password='test'");
    connection = psycopg2.connect(user=config.user,
                                  password=config.password,
                                  host=config.host,
                                  port=config.port)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

    return connection


def get_current_session():
    return dao.dao_session_info.load_current_session()
