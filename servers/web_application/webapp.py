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
from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import LoginManager, login_required, login_user, logout_user
from urllib.parse import quote

from flask_sqlalchemy import SQLAlchemy

### Setting up the Flask App, Login Manager, and Database
app = Flask(__name__, template_folder="templates")

login_manager = LoginManager()
login_manager.init_app(app)

### Connect to the database
DB_URI = "mysql+pymysql://root:Password-123%21@mariadb:3306/accounts"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)
# engine = sql.create_engine(URI, echo=True)

### The user class which creates a user object
class accounts(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(200))

    def __repr__(self):
        return f"<Username: {self.username} Password: {self.password}"


### The Flask Apps Code

@app.route('/database')
def databasefucn():
    users = accounts.query.filter_by(username='admin').first()
    return users.username

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
            return redirect(url_for('landingPage'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/landingPage')
@login_required
def landingPage():
    return "Congrats! You logged in sucessfully"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')