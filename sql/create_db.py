from sql.update_sql import connect_to_db

conn = connect_to_db()
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
