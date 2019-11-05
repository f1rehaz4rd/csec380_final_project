"""
@filename: webapp.py

@Description:
This is a simple flask app that is intented to be a video
hosting and sharing website. It will allow users to login
and view others video uploads.

@Author: Jon Bauer (JonBauer123)
@Contributors: 
"""
# https://scotch.io/tutorials/authentication-and-authorization-with-flask-login

### Python Imports
from flask import Flask, render_template, redirect, url_for, request, abort, session
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

import secrets

### Setting up the Flask App, Session Manager, and Database
app = Flask(__name__, template_folder="templates")

### Initialize the Session
app.secret_key = secrets.token_bytes(32)
app.config['SESSION_TYPE'] = 'filesystem'

sess = Session()
sess.init_app(app)

### Connect to the database
DB_URI = "mysql+pymysql://root:Password-123%21@mariadb:3306/accounts"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)

### The users class which creates a user object
class users(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(200))

    def __repr__(self):
        return f"<Username: {self.username} Password: {self.password}"


### The Flask Apps Code
@app.route('/database')
def databasefunc():
    """
    Function testing database access with SQLAlchemy

    It will output the username and password that is in the database
    """
    user = users.query.filter_by(username='admin').first()
    return user.username + " " + user.password

@app.route('/session')
def sessionTest():
    """
    Function for testing the implementation of a session
    per user log in.

    It will out the session data to verify that it is saved
    properly.
    """
    session['test'] = '12345'
    return session.get('test')

@app.route('/')
def main():
    return redirect(url_for('login'))

def loginValidate():
    """
    Validates a users log in request.
    """
    return request.form['username'] == "admin" \
        or request.form['password'] == "admin"


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles the login page logic 
    and authentication.
    """
    error = None

    # Checks validates login request.
    if request.method == 'POST':
        if loginValidate():
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'

    # If there is no log in request it will send the user
    # the login page.
    return render_template('login.html', error=error)

@app.route('/home')
def home():
    """
    This is the landing page that you get to after log in.

    During the second part of the project this will be replaced
    with all the videos and profile settings. 
    """
    return "Congrats! You logged in sucessfully"

if __name__ == '__main__':
    """
    This starts the server up on port 80
    """
    app.run(debug=True,host='0.0.0.0', port=80)