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
from flask import Flask, render_template, redirect, url_for, request, abort, session, send_from_directory
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.utils import secure_filename

import secrets
import os

### Setting up the Flask App, Session Manager, and Database
app = Flask(__name__, template_folder="templates")

### Initialize the Session
app.secret_key = secrets.token_bytes(32)
app.config['SESSION_TYPE'] = 'filesystem'

sess = Session()
sess.init_app(app)

### Sets up the upload conditions
UPLOAD_FOLDER = '/app/static/videos'
ALLOWED_EXTENSIONS = {'avi', 'flv', 'wmv', 'mov', 'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

### Class for the video metadata
class videos(db.Model):
    filename = db.Column(db.String(100), primary_key=True)
    path = db.Column(db.String(100))
    url = db.Column(db.String(200))
    username = db.Column(db.String(80))

    def __repr__(self):
        return f"<Filename: {self.filename} Path: {self.path}"

### The Flask Apps Code
def authorize():
    """
    Verifies if the user is logged in.
    """
    return 'token' in session

@app.route('/display/<filename>')
def uploaded_file(filename):

    if not authorize():
        return redirect(url_for('login'))        

    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def get_uploads():
    video_list = videos.query.all()

    return video_list

def allowed_file(filename):
    """
    This checks to see if the file is one of the allowed
    file types. If its not it returns false.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if not authorize():
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        # Need to add extension verificaiton 
        if file and allowed_file(file.filename):
            # Save the file to the server
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the metadata to the database
            url= "http://localhost:80/display/" + filename

            video = videos(filename=filename, path=app.config['UPLOAD_FOLDER'], \
                 url=url, username=session.get('username'))
            db.session.add(video)
            db.session.commit()

            return redirect(url_for('uploaded_file', filename=filename))

    return render_template("upload.html")

@app.route('/token')
def testToken():
    """
    This is a test function that will be removed after development of the app.
    """
    if not authorize():
        return redirect(url_for('login'))

    return "User Session: "+session.get('username')+"\nsession:"+str(session.get('token'))

@app.route('/')
def main():
    if authorize():
        return redirect(url_for('home'))

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
    if authorize():
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

    if not authorize():
        return redirect(url_for('login'))

    if 'username' in session:
        session.pop('username')
    
    # Impliment Token into the database so that I can check
    if 'token' in session:
        session.pop('token')

    return redirect(url_for('login'))

@app.route('/uploads')
def uploads_list():
    if not authorize():
        return redirect(url_for('login'))

    video_list = get_uploads()
    return render_template('video_display.html', len=len(video_list), display=video_list)

@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    This is the landing page that you get to after log in.

    During the second part of the project this will be replaced
    with all the videos and profile settings. 
    """
    if not authorize():
        return redirect(url_for('login'))
    
    if request.method == "POST":
        return redirect(url_for('logout'))

    video_list = get_uploads()
    
    return render_template('home.html', username=session.get('username'), len=len(video_list), display=video_list)

if __name__ == '__main__':
    """
    This starts the server up on port 80
    """
    app.run(debug=True,host='0.0.0.0', port=80)