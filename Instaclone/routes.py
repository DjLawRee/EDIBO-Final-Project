from flask import redirect, render_template, request, session, flash
from flask.helpers import url_for
from werkzeug.security import check_password_hash, generate_password_hash
from Instaclone.helpers import apology, login_required
from flask_mail import  Message
from Instaclone import app, mail, db
import Instaclone.picture_controll
import Instaclone.user_controll



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return render_template("reset_token.html")



@app.route("/forgot", methods=["GET", "POST"])
def forgot():

    if request.method == "POST":
        if not Instaclone.user_controll.get_user_data_by_email(request.form.get('email')):
            return apology("Email doesn't exist")

        email = request.form.get('email')
        # msg = Message("Remember Password",
        #             recipients=[email])

        # password = Instaclone.user_controll.get_user_password_by_email(email)
        # testing = "<b>Testing body</b>"
        # msg.body = password
        # msg.html = testing
        # mail.send(msg)
        
  
        Instaclone.user_controll.send_reset_email(email)
        return redirect(url_for('login'))

    else:
        return render_template("reset_request.html")

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
        if not Instaclone.user_controll.check_if_user_exists(
            request.form.get('username')
        ) or not check_password_hash(Instaclone.user_controll.get_user_password(
            request.form.get('username')
        ), request.form.get("password")):
            print(Instaclone.user_controll.get_user_password(request.form.get('username')))
            print(request.form.get("password"))
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        
        session["user_id"] = Instaclone.user_controll.get_user_data(request.form.get('username')).get('Id')
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
        if Instaclone.user_controll.get_user_data(request.form.get('username')):
            return apology('Username already exists')
        if Instaclone.user_controll.get_user_data_by_email(request.form.get('email')):
            return apology('Email already exists')

        psw = generate_password_hash(request.form.get("password"),method='pbkdf2:sha256', salt_length=8)
        Instaclone.user_controll.register_user(request.form.get('username'),psw,request.form.get('email'))

        session["user_id"] = Instaclone.user_controll.get_user_data(request.form.get('username')).get('Id')
        print(session['user_id'])
        return redirect("/")

    else :
        return render_template("register.html")
    
@app.route("/user-home",methods=["GET","POST"])
@login_required
def user_home():
    user_data=Instaclone.user_controll.get_user_data_by_id(session['user_id'])
    user_name=user_data.get('user_name')
    user_images=Instaclone.picture_controll.get_user_pictures(session['user_id'])
    
    return render_template("/user-home.html",user_name=user_name,user_images=user_images)
   
         

@app.route("/upload_picture",methods=['POST'])
@login_required
def upload_picture():
    image=request.files['image']
    image_name=request.form.get("image_name")
    
    if not image:
        return apology("no picture selected")
    user_id=session["user_id"]
    Instaclone.picture_controll.upload_image(image,user_id,image_name)
    return redirect("/user-home")
    


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/reset/<token>", methods=['GET', 'POST'])
def reset_token(token):
    
    user = Instaclone.user_controll.verify_reset_token(token)
    if user is None:
        return apology('That is an invalid or expired token')
    print("works till here")
    if request.method == "POST":
        print("works after here")
        # if not request.form.get('username'):
        #     return apology("must provide valid username")
        # if request.form.get('password')!=request.form.get('password2'):
        #     return apology("Passwords do not match")
        # if Instaclone.user_controll.get_user_data(request.form.get('username')):
        #     return apology('Username already exists')

        # hashed_password = generate_password_hash(request.form.get("password"),method='pbkdf2:sha256', salt_length=8)
        
        # # Update pass to new one ???
        # user.password = hashed_password
        

        # session["user_id"] = Instaclone.user_controll.get_user_data(request.form.get('username')).get('Id')
        # print(session['user_id'])
        # db.session.commit()
        

        # print("Success\n")
        # print("Success\n")
        # print("Success\n")
        # print("Success\n")
        # print("Success\n")
        return redirect(url_for('login'))
    return render_template('reset_token.html')


@app.route("/reset", methods=['POST'])
def reset():
    if request.method == "POST":
        if request.form.get('password')!=request.form.get('password2'):
            return apology("Passwords do not match")
        hashed_password = generate_password_hash(request.form.get("password"),method='pbkdf2:sha256', salt_length=8)

        return redirect(url_for('login'))

    return redirect(url_for('forget'))
