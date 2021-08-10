from flask import Flask 
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from mysql.connector import cursor
import mysql.connector


# Configure application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '9491628bb0b13ce0c676dfde280ba321'
db=mysql.connector.connect(user='root',password='MyNewPass',
                        host='127.0.0.1',
                        database='instaclone')
cursor=db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS `users` (`Id` int NOT NULL AUTO_INCREMENT, `user_name` varchar(100) NOT NULL,`password_hash` text NOT NULL, `email` varchar(100) NOT NULL,`reg_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (`Id`)) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
db.commit()
cursor.close()  

from Instaclone import routes
from Instaclone.helpers import apology
from flask_mail import Mail




# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"]="temp_upload"
app.config["ALLOWED_EXTENSIONS"] = ["png","jpg","jpeg","gif"]



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Flask-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'edibo.final@gmail.com'
app.config['MAIL_PASSWORD'] = 'laurisedas123'
app.config['MAIL_DEFAULT_SENDER'] = 'edibo.final@gmail.com'
app.config['MAIL_MAX_EMAILS'] = 3
app.config['MAIL_SUPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

