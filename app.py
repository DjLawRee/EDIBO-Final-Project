from flask import Flask
from werkzeug.security import generate_password_hash , check_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


app=Flask(__name__)

@app.route("/")
def home():
    return "Here we Go test!"


