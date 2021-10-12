import psycopg2
from query.getUserProfile import getprofile

DB_NAME = 'd8dpaa8b7gqpdm'
DB_USER = 'fsdygodmdxeuay'
DB_PASSWORD = '3f67e9fe7e19c35e5c46331d6a3b001c874a29ec85a9dbf49b970a26f87f71b2'
DB_HOST = 'ec2-52-214-178-113.eu-west-1.compute.amazonaws.com'


def connect_to_db():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, host=DB_HOST)


def get_top_10(sort_key: str) -> list:
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users ORDER BY {} DESC LIMIT 10'.format(sort_key))
    data = cur.fetchall()
    cur.close()
    return data


def get_user(username: str) -> tuple:
    conn = connect_to_db()
    cur = conn.cursor()
    get_query = 'SELECT * FROM users WHERE username=%s'
    cur.execute(get_query, (username,))
    data = cur.fetchone()
    if not data:
        raise ValueError('Profile ' + username + ' not on the list')
    return data


def update_user(user_data: tuple) -> None:
    conn = connect_to_db()
    cur = conn.cursor()
    update_query = 'INSERT INTO users (username, easy, medium, hard, count_all, recent_submission) ' \
                   'VALUES(%s, %s, %s, %s, %s, %s) ' \
                   'ON CONFLICT (username) DO UPDATE SET ' \
                   'username = EXCLUDED.username, easy = EXCLUDED.easy, medium = EXCLUDED.medium, ' \
                   'hard = EXCLUDED.hard, count_all = EXCLUDED.count_all, ' \
                   'recent_submission = EXCLUDED.recent_submission;'
    cur.execute(update_query, user_data)
    conn.commit()
    cur.close()


def update_all_users() -> None:
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    update_query = 'INSERT INTO users (username, easy, medium, hard, count_all, recent_submission) ' \
                   'VALUES(%s, %s, %s, %s, %s, %s) ' \
                   'ON CONFLICT (username) DO UPDATE SET ' \
                   'username = EXCLUDED.username, easy = EXCLUDED.easy, medium = EXCLUDED.medium, ' \
                   'hard = EXCLUDED.hard, count_all = EXCLUDED.count_all, ' \
                   'recent_submission = EXCLUDED.recent_submission;'
    for profile in data:
        cur.execute(update_query, getprofile(profile[0]))
    conn.commit()
    cur.close()


def get_all_users() -> list:
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users ORDER BY count_all DESC')
    data = cur.fetchall()
    cur.close()
    return data


def delete_user(username: str) -> None:
    conn = connect_to_db()
    cur = conn.cursor()
    delete_query = 'DELETE FROM users WHERE username=%s'
    cur.execute(delete_query, (username,))
    conn.commit()
    cur.close()
