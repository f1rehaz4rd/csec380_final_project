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
@app.route('/upload', methods=['GET', 'POST'])
def testUpload():

    return "This is the test upload page"

@app.route('/token')
def testToken():
    """
    This is a test function that will be removed after development of the app.
    """
    return "User Session: " + session.get('username') + "\nsession: " + str(session.get('token'))

@app.route('/')
def main():
    return redirect(url_for('login'))

def loginValidate(name, password):
    """
    Validates a users log in request by checking the
    database.
    """
    user = users.query.filter_by(username=name).first()
    if user is not None:
        if password == user.password:
            return True

    return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles the login page logic 
    and authentication.
    """
    error = None
    if 'username' in session:
        return redirect(url_for('home'))

    # Checks validates login request.
    if request.method == 'POST':
        if loginValidate(request.form['username'].strip(), request.form['password']):
            session['username'] = request.form['username'].strip()
            session['token'] = secrets.token_urlsafe(32)   
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'

    # If there is no log in request it will send the user
    # the login page.
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    
    # Impliment Token into the database so that I can check
    if 'token' in session:
        session.pop('token')

    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    This is the landing page that you get to after log in.

    During the second part of the project this will be replaced
    with all the videos and profile settings. 
    """
    if request.method == "POST":
        return redirect(url_for('logout'))

    if 'token' in session:
        return render_template('home.html', username=session.get('username'))
    
    return "You are not logged in, please log in to view the page."

if __name__ == '__main__':
    """
    This starts the server up on port 80
    """
    app.run(debug=True,host='0.0.0.0', port=80)