import sqlite3
from query.getUserProfile import getprofile

DB_NAME = 'profiles.db'


def get_top_10(sort_key: str) -> list:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users ORDER BY {} DESC LIMIT 10'.format(sort_key))
    data = cur.fetchall()
    cur.close()
    return data


def update_user(user_data: tuple) -> None:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    update_query = 'INSERT OR REPLACE INTO users VALUES(?, ?, ?, ?, ?, ?);'
    cur.execute(update_query, user_data)
    conn.commit()
    cur.close()


def update_all_users() -> None:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    update_query = 'INSERT OR REPLACE INTO users VALUES(?, ?, ?, ?, ?, ?);'
    for profile in data:
        cur.execute(update_query, getprofile(profile[0]))
    conn.commit()
    cur.close()
