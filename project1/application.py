import os

from flask import Flask, session, redirect
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


def renderPage(pageName, **args):
    args['username'] = session.get('username', None)
    return render_template(pageName, **args)


@app.route("/")
def index():
    return "Project 1: TODO"


@app.route("/login", methods=['get'])
def loginGet(errMsg=None):
    return renderPage('login.html', errMsg=errMsg)


@app.route('/login', methods=['post'])
def loginPost():
    name = request.form.get('name')
    results = db.getUserDetails(name)
    if results.rowcount == 1 and request.form.get('password') == results.fetchone()['password']:
        session['username'] = name
        return renderPage('landing.html')
    else:
        return loginGet('Invalid username or password.')


@app.route("/logout")
def logOut():
    session.pop('username', None)
    return renderPage('logout.html')


@app.route('/register', methods=['get'])
def registerGet():
    return renderPage('register.html')


@app.route('/register', methods=['post'])
def registerPost():
    registerPage = 'register.html'
    
    name = request.form.get('name')
    password = request.form.get('password')
    
    # check username is valid
    if not name:
        return renderPage(registerPage, errMsg="Invalid user name.")
    # check if user name already exists
    elif db.getUserDetails(name).rowcount != 0:        
        return renderPage(registerPage, errMsg="User name already exists.  Please choose another.")
    # check password is valid
    elif not password:
        return renderPage(registerPage, errMsg="Invalid Password")
    else:
        # create user in database
        if db.addUser(name, password):
            return renderPage('registrationComplete.html')
        else:
            return renderPage(registerPage, errMsg="User name already exists.  Please choose another. ")


@app.route('/booksearch', methods=['get', 'post'])
def booksearch():
    params = {}
    for fieldName in ['author', 'title', 'isbn']:
        value = request.form.get(fieldName)
        if value:
            params[fieldName] = value
    results = db.searchForBooks(**params)
    return renderPage('booksearch.html', results=results)
    
        
@app.route('/books/<string:isbn>')
def bookInfo(isbn):
    results = db.getBookDetails(isbn)
    return  renderPage('bookInfo.html', results=results )


app.run()