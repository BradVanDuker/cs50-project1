import os

from flask import Flask, session, redirect, make_response
from flask_session import Session
from flask.templating import render_template
from flask import request
from dataStore import DataStore
from sqlalchemy.exc import IntegrityError
from goodreadHandler import GoodreadHandler


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

goodread = GoodreadHandler()

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
    if results.rowcount == 1:
        r = results.first()
        if request.form.get('password') == r['password']:
            print(results)
            session['username'] = name
            session['userId'] = r['id']
            return redirect('booksearch')
    return loginGet('Invalid username or password.')


@app.route("/logout")
def logOut():
    session.pop('username', None)
    session.pop('userId', None)
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


@app.route('/books/<string:isbn>', methods=['get'])
def bookInfo(isbn):
    details = db.getBookDetails(isbn)
    #results = {key:value for key, value in details.items()}
    reviews = db.getReviews(isbn)
    cannotSubmit = False
    for r in reviews:
        if r['user_id'] == session['userId']:
            cannotSubmit = True
            break
    try:
        gr = goodread.getBookRating(isbn)
    except Exception as e:
        gr = None
        
    return  renderPage('bookInfo.html', results=details, reviews=reviews, cannotSubmit=cannotSubmit, goodreads=gr)


@app.route('/submitReview', methods=['post'])
def bookReviewSubmission():
    try:
        params = {pName:request.form.get(pName) for pName in ['reviewText', 'rating', 'isbn']}
        params['userId'] = session['userId']
        db.saveReview(**params)
        return renderPage('submissionSuccess.html')
    except IntegrityError as e:
        if str(e).lower().find("duplicate") > -1:
            errMsg = "Oops!  You may only submit one review per book."
        else:
            errMsg = "You must supply all required information before we can save your review."
    except Exception as e:
        errMsg = str(e)
    return renderPage('template.html', errMsg=errMsg) 


@app.route('/api/<string:isbn>')
def api_isbn(isbn):
    status = 200
    try:
        details = db.getBookDetails(isbn)
        if details:
            details = {k:v for k, v in details.items()}
            details.pop('id')
            try:
                reviews = goodread.getBookRating(isbn)
                details['review_count'] = reviews[0]
                details['average_score'] = reviews[1]
            except Exception:
                details['review_count'] = None
                details['average_score'] = None
        else:
            details = ""
            status = 404
    except Exception:
        details = ""
        status = 404
    response = make_response(details)
    response.status_code = status
    return response



app.run()