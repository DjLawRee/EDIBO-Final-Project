from Instaclone import db, app, mail
from flask_mail import  Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.helpers import url_for

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

def get_user_data_by_email(email):
    cursor=db.cursor(dictionary=True)
    query=("SELECT * FROM users WHERE email = %s ")
    cursor.execute(query,(email,))
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

def get_user_password_by_email(email):
    cursor=db.cursor(dictionary=True)
    query=("SELECT password_hash FROM users WHERE email = %s ")
    cursor.execute(query,(email,))
    result=cursor.fetchone()
    password = result.get("password_hash")
    print(password)
    return password

def get_user_id_by_email(email):
    cursor=db.cursor(dictionary=True)
    query=("SELECT Id FROM users WHERE email = %s ")
    cursor.execute(query,(email,))
    result = cursor.fetchone()
    id = result.get("Id")
    print(id)
    return id

def register_user(user_name,password,email):
    cursor=db.cursor()
    values=[user_name,password,email]
    query=("INSERT INTO users (user_name,password_hash,email) VALUES(%s,%s,%s)")
    cursor.execute(query,values)
    db.commit()
    cursor.close()



def send_reset_email(email):
    id = get_user_id_by_email(email)
    token = get_reset_token(id)
    msg = Message('Password Reset Request',
                  recipients=[email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def get_reset_token(id, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': id}).decode('utf-8')


def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return get_user_data_by_id(user_id)




def reset_password(hashed_password , user_id):
    cursor=db.cursor()
    sql=("UPDATE users SET password_hash = %s   WHERE Id = %s ")
    values=[hashed_password , user_id]
    cursor.execute(sql,values)
    db.commit
    cursor.close()



