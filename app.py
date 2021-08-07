import os


from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import user_controll



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")


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


@app.route("/test")
def test():
    return render_template("test.html")

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
        return redirect("/")

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

