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

from random import choice


def load_current_session():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
        select current_session from session_info
        where id = 1
        """)

    result = cur.fetchone()
    print('Executed the query')
    db.close()

    return result[0]


def init_session_info():
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO session_info (id, current_session) VALUES (1,1)
        """)
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur


def update_current_session(new_current_session):
    db = db_utils.create_connection_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE session_info 
        SET current_session = %s 
        WHERE id = 1
        """, (new_current_session,))
    db.commit()
    print('Executed the query')
    db.close()
    print('Closed the dao!')
    return cur

