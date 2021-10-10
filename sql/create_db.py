import sqlite3
import os

conn = sqlite3.connect(os.path.dirname(os.getcwd()) + '/profiles.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   username TEXT PRIMARY KEY,
   easy INT,
   medium INT,
   hard INT,
   count_all INT,
   recent_submission TEXT);
""")
conn.commit()
cur.close()
