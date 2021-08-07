import mysql.connector
from mysql.connector import cursor
from mysql.connector.cursor import MySQLCursor

db=mysql.connector.connect(user='root',password='MyNewPass',
                        host='127.0.0.1',
                        database='instaclone')


def check_if_user_exists(user_name):
    cursor=db.cursor(dictionary=True)
    query=("SELECT Id FROM users WHERE user_name = %s ")
    cursor.execute(query,(user_name,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
    

def get_user_data(user_name):
    cursor=db.cursor(dictionary=True)
    query=("SELECT * FROM users WHERE user_name = %s ")
    cursor.execute(query,(user_name,))
    user_data = cursor.fetchone()
    print(user_data)
    return user_data

def get_user_password(user_name):
    cursor=db.cursor(dictionary=True)
    query=("SELECT password FROM users WHERE user_name = %s ")
    cursor.execute(query,(user_name,))
    result=cursor.fetchone()
    return result[0]

def register_user(user_name,password):
    cursor=db.cursor()
    query=("INSERT INTO users (user_name,password_hash) VALUES(%s,%s)")
    cursor.execute(query,(user_name,),(password,))







