from io import TextIOBase
import mysql.connector
from mysql.connector import cursor
from mysql.connector.cursor import MySQLCursor
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import key

db=mysql.connector.connect(user='root',password='MyNewPass',
                        host='127.0.0.1',
                        database='instaclone')
cursor=db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS `users` (`Id` int NOT NULL AUTO_INCREMENT, `user_name` varchar(100) NOT NULL,`password_hash` text NOT NULL,`reg_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (`Id`)) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
db.commit()
cursor.close()  



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

def get_user_data_by_id(user_id):
    cursor=db.cursor(dictionary=True)
    query=("SELECT * FROM users WHERE Id = %s ")
    cursor.execute(query,(user_id,))
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

def get_reset_token(self, expires_sec=1800):
    s = Serializer(key, expires_sec)
    return s.dumps({'user_id': self.id}.decode('utf-8'))

def verify_reset_token(token):
    s = Serializer(key)
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return User.query.get(user_id)


