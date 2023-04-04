import sys

sys.path.append('../')
import psycopg2
import config


def ping_db():
    try:
        connection = psycopg2.connect(user=config.user,
                                      password=config.password,
                                      host="127.0.0.1",
                                      port="5432",
                                      database=config.database)
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def select_user_id():
    db = psycopg2.connect(user=config.user,
                                  password=config.password,
                                  host=config.host,
                                  port=config.port,
                                  database=config.database)
    query = '''
                SELECT ID FROM users
                WHERE ID != (%s)
                '''
    params = ('messe_',)
    cur = db.cursor()
    cur.execute(query, params)
    print('Executed the query')
    res = cur.fetchall()
    ids = [a[0] for a in res]
    print(ids)
    db.close()


if __name__ == '__main__':
    ping_db()