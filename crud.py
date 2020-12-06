import requests
import pymysql
from dotenv import load_dotenv
import os
from json import dumps
from flask_bcrypt import Bcrypt

load_dotenv()

host_db = os.getenv("host_db")
user_db = os.getenv("user_db")
password_db = os.getenv("password_db")
schema_db = os.getenv("schema_db")

db_conn_write = pymysql.connect(host_db, user_db, password_db,
                                schema_db, cursorclass=pymysql.cursors.DictCursor)

db_cursor = db_conn_write.cursor()

from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/users/register')
def registerUser():
    query_data = 'select * from users'
    db_cursor.execute(query_data)
    all_users = db_cursor.fetchall()
    return dumps(all_users)

@app.route('/users/fetchAll')
def fetchAllUsers():
    query_data = 'select * from users'
    db_cursor.execute(query_data)
    all_users = db_cursor.fetchall()
    return dumps(all_users)

app.run()