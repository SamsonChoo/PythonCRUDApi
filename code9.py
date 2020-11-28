import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

host_db = os.getenv("host_db")
user_db = os.getenv("user_db")
password_db = os.getenv("password_db")
schema_db = os.getenv("schema_db")

db_conn_write = pymysql.connect(host_db, user_db, password_db,
                                schema_db, cursorclass=pymysql.cursors.DictCursor)

db_cursor = db_conn_write.cursor()

try:
    query_data = 'select * from users'
    db_cursor.execute(query_data)
    print(db_cursor.fetchall())
except:
    pass