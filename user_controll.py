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
    id = result.get("Id")
    print(id)
    if id is not None:
        print("TRUE")
        return True
    else:
        print("FALSE")
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
    query=("SELECT password_hash FROM users WHERE user_name = %s ")
    cursor.execute(query,(user_name,))
    result=cursor.fetchone()
    password = result.get("password_hash")
    print(password)
    return password

def register_user(user_name,password):
    cursor=db.cursor()
    values=[user_name,password]
    query=("INSERT INTO users (user_name,password_hash) VALUES(%s,%s)")
    cursor.execute(query,values)
    db.commit()
    cursor.close()







