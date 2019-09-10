# Project 1

# Description
This project uses PostgresSQL, sqlAlchemy, and flask to create a simple book review website.  The site allows users to register, log in, search and view details of books, leave a review, and view a score for the book from goodreads.com.

# Assignment Requirements
* [x] **Registration:** Users should be able to register for your website, providing (at minimum) a username and password.
* [x] **Login:** Users, once registered, should be able to log in to your website with their username and password.
* [x] **Logout:** Logged in users should be able to log out of the site.
* [x] **Import:** Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books
  * [x] In a Python file called import.py separate from your web application, write a program that will take the books and import them into your PostgreSQL database
  * [x] Run this program by running python3 import.py to import the books into your database, and submit this program with the rest of your project code.
* [x] **Search:** Once a user has logged in, they should be taken to a page where they can search for a book. 
  * [x] Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. 
  * [x] After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. 
  * [x] If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
* [x] **Book Page:** When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
* [x] **Review Submission:** On the book page, users should be able to submit a review: 
  * [x] consisting of a rating on a scale of 1 to 5 
  * [x] a text component to the review where the user can write their opinion about a book.
  * [x] Users should not be able to submit multiple reviews for the same book.
* [x] **Goodreads Review Data:** On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
* [x] **API Access:** If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score.  If the requested ISBN number isn’t in your database, your website should return a 404 error.
* [x] You should be using raw SQL commands (as via SQLAlchemy’s execute method) in order to make database queries. You should not use the SQLAlchemy ORM (if familiar with it) for this project.
* [x] In README.md, include a short writeup describing your project, what’s contained in each file, and (optionally) any other additional information the staff should know about your project.
* [x] If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to requirements.txt!

# Dependencies
requests library,
yaml library,
flask,
sqlalchemy

# Other
* The file go.py is used to set environment variables and then run the application.py script.  This saves painful setup and allows the use of an IDE and debugger.
  * go.py requires a folder location for credentials.  The files must be in YAML.  
    * The system requires a file named "project1."  This file should contain credentials for the heroku database connection.  It's pretty much a copy-paste the connection info from the heroku website. 
    * The system requires a file named "goodreads."  This file should contain credentials for the goodreads API
    * This project should contain two templates for credentials.
  * The file location is passed into go.py as the first and only argument.
* Known Issues:
  * The flask server restarts itself when first starting
  * As of this writing there is no favicon.  This will cause return code 404 to sporadically appear in the logs.  This behavior is sporadic and its replication conditions are yet unknown.
* When the api returns a 404 error, the server logs show a 404 error being returned.  However, the browser (firefox) shows a blank screen.  When navigating to a known bad URL, firefox displays a 404 page.  The difference might be that flask is generating an actual response with a code 404, rather than the browser getting no response and displaying a 404 page as a default.  I'm not sure how to test if a 404 error was read by the browser.

# File Description
* static/stylings.css: css file for creating a nice display for content
* templates/template.html: a general purpose web page used as a base for creating other web pages on the site.
* templates/*: flask files for the various web pages on the site
* application.py: python script that contains routing logic and ties everything together
* books.csv: csv format file used to initialize the books table of the database
* dataStore.py:  python file used to interact with the site's database
* go.py:  the main entry point for the system used to set environment variables, get needed credentials, and start the server
* goodreadsHandler.py  python file for interacting with the goodreads API
* goodreads: a YAML file that holds credentials for the goodreads API
* import.py:  python script used to initialize the books table of the database
* project1:  a YAML file that holds credentials used by the server to access the database 
* README.md: file used for describing the project.  Used as the front page for the github repository.
* requirements.txt: contains names of package that are required to be installed before running this software.
* sass\_compile\_to\_static\_folder\_as\_stylings.scss:  SASS file for creating the stylings.css file