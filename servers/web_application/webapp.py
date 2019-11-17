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
import requests as getVideo

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
    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(200))
    session_token = db.Column(db.String(200))

    def __repr__(self):
        return f"<Username: {self.username} Password: {self.password}"

### Class for the video metadata
class videos(db.Model):
    title = db.Column(db.String(100), primary_key=True)
    filename = db.Column(db.String(50))
    filetype = db.Column(db.String(5))
    path = db.Column(db.String(100))
    url = db.Column(db.String(100))
    username = db.Column(db.String(30))

    def __repr__(self):
        return f"<Filename: {self.filename} Path: {self.path}"


### Helper Functions
def authorize():
    """
    Verifies if the user is logged in.
    """
    if 'token' in session:
        user = users.query.filter_by(username=session.get('username')).first()
        if session.get('token') == user.session_token:
            return True

    return False

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

def loginValidate(name, password):
    """
    Validates a users log in request by checking the
    database.
    """
    user = users.query.filter_by(username=name).first()
    if user is not None:
        if password == user.password:
            # Creates the session data
            session['username'] = request.form['username'].strip()
            session['token'] = secrets.token_urlsafe(32)  
            # Addes session data to the database
            user.session_token = session.get('token')
            db.session.commit()
            return True

    return False

### The Flask Apps Code
@app.route('/display/<filename>')
def uploaded_file(filename):

    if not authorize():
        return redirect(url_for('login'))        

    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    """
    Handles uplaoding a video.
    TODO:
        Add file already exists checking
    """

    if not authorize():
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        
        # Need to add extension verificaiton 
        if file and allowed_file(file.filename) and \
                file.filename != '' and request.form['title'] != '':
            
            try:
                # Save the file to the server
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Save the metadata to the database
                url= "http://localhost:80/display/" + filename

                # NEED TO SANITIZE THE TITLE INPUT

                video = videos(title=request.form['title'],filename=filename, filetype=filename.split('.')[1],\
                    path=app.config['UPLOAD_FOLDER'], url=url, username=session.get('username'))
                db.session.add(video)
                db.session.commit()

                return redirect(url_for('home'))
            except:
                return redirect(request.url)


        elif request.form['videourl'] is not None: # If it is a link that was submited and not a video
            upload_url = request.form['videourl']

            try:
                req = getVideo.get(upload_url, allow_redirects=True)

                filename = upload_url.split('/')
                filename = filename[len(filename) - 1]
                filename = secure_filename(filename) # Secures the filename
                # Saves the file to the server
                fd = open(app.config['UPLOAD_FOLDER'] + filename, "wb")
                fd.write(req.content)
                fd.close()

                url= "http://localhost:80/display/" + filename

                video = videos(title=request.form['title'],filename=filename, filetype=filename.split('.')[1],\
                    path=app.config['UPLOAD_FOLDER'], url=url, username=session.get('username'))
                db.session.add(video)
                db.session.commit()

                return redirect(url_for('home'))
            except:
                print("Oh no REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
                return redirect(url_for('testToken'))
        
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
            # NOTE: Sets the session information in the loginValidate function
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
        if request.form['submit_button'] == 'logout':
            return redirect(url_for('logout'))
        elif request.form['submit_button'] == 'account':
            pass
        elif request.form['submit_button'] == 'upload':
            return redirect(url_for('upload_video'))
        

    video_list = get_uploads()
    
    return render_template('home.html', username=session.get('username'), len=len(video_list), display=video_list)

if __name__ == '__main__':
    """
    This starts the server up on port 80
    """
    app.run(debug=True,host='0.0.0.0', port=80)