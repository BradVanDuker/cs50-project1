import os

from flask import Flask, session
from flask_session import Session
from flask.templating import render_template
from flask import request
from dataStore import DataStore


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
db = DataStore(os.getenv("DATABASE_URL"))


@app.route("/")
def index():
    return "Project 1: TODO"


@app.route("/login", methods=['get'])
def loginGet(errMsg=None):
    return render_template('login.html', errMsg=errMsg)


@app.route('/login', methods=['post'])
def loginPost():
    name = request.form.get('name')
    results = db.getUserDetails(name)
    if results.rowcount == 1 and request.form.get('password') == results.fetchone()['password']:
        return render_template('landing.html')
    else:
        return loginGet('Invalid username or password.')


@app.route("/logout")
def logOut():
    return render_template('logout.html')


@app.route('/register', methods=['get'])
def registerGet():
    return render_template('register.html')


@app.route('/register', methods=['post'])
def registerPost():
    registerPage = 'register.html'
    
    name = request.form.get('name')
    password = request.form.get('password')
    
    # check username is valid
    if not name:
        return render_template(registerPage, errMsg="Invalid user name.")
    # check if user name already exists
    elif db.getUserDetails(name).rowcount != 0:        
        return render_template(registerPage, errMsg="User name already exists.  Please choose another.")
    # check password is valid
    elif not password:
        return render_template(registerPage, errMsg="Invalid Password")
    else:
        # create user in database
        if db.addUser(name, password):
            return render_template('registrationComplete.html')
        else:
            return render_template(registerPage, errMsg="User name already exists.  Please choose another. ")
    
        
app.run()