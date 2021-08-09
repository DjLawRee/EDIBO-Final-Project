import os


from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, login_required
from flask_mail import Mail, Message
from PIL import Image

import user_controll
import picture_controll






# Configure application
app = Flask(__name__)
app.config.from_object(__name__)

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
app.config['MAIL_USERNAME'] = 'email login'
app.config['MAIL_PASSWORD'] = 'email password'
app.config['MAIL_DEFAULT_SENDER'] = 'default sender'
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

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/forgot")
def forgot():

    msg = Message("Hello",
                  recipients=["test email"])
    
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        
        # Ensure username exists and password is correct
        if not user_controll.check_if_user_exists(
            request.form.get('username')
        ) or not check_password_hash(user_controll.get_user_password(
            request.form.get('username')
        ), request.form.get("password")):
            print(user_controll.get_user_password(request.form.get('username')))
            print(request.form.get("password"))
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        
        session["user_id"] = user_controll.get_user_data(request.form.get('username')).get('Id')
        print("session id" ,session["user_id"])
        return redirect("/user-home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register",methods=["GET", "POST"])
def register():
    session.clear()
    
    if request.method == "POST":
        if not request.form.get('username'):
            return apology("must provide valid username")
        if request.form.get('password')!=request.form.get('password2'):
            return apology("Passwords do not match")
        if user_controll.get_user_data(request.form.get('username')):
            return apology('username already exists')

        psw = generate_password_hash(request.form.get("password"),method='pbkdf2:sha256', salt_length=8)
        user_controll.register_user(request.form.get('username'),psw)

        session["user_id"] = user_controll.get_user_data(request.form.get('username')).get('Id')
        print(session['user_id'])
        return redirect("/")

    else :
        return render_template("register.html")
    
@app.route("/user-home",methods=["GET","POST"])
@login_required
def user_home():
    user_data=user_controll.get_user_data_by_id(session['user_id'])
    user_name=user_data.get('user_name')
    user_images=picture_controll.get_user_pictures(session['user_id'])
    
    return render_template("/user-home.html",user_name=user_name,user_images=user_images)
   
         

@app.route("/upload_picture",methods=['POST'])
@login_required
def upload_picture():
    image=request.files['image']
    image_name=request.form.get("image_name")
    
    if not image:
        return apology("no picture selected")
    user_id=session["user_id"]
    picture_controll.upload_image(image,user_id,image_name)
    return redirect("/user-home")
    


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

