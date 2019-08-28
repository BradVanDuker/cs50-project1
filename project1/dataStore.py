'''
Created on Aug 20, 2019

@author: Brad
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import InvalidRequestError


class DataStore(object):
    '''
    classdocs
    '''
    
    
    def getUserDetails(self, name):
        return self.db.execute("SELECT * FROM users WHERE user_name = :name", {'name':name})
    
    
    def addUser(self, name, password, **params):
        params['user_name'] = name
        params['password'] = password
        try:
            front = "INSERT INTO users ("
            back = " VALUES ("
            for colName in params.keys():
                front += colName + ', '
                back += ':' + colName + ', '
            strings_ = [front, back]
            for i in range(0, len(strings_)):
                str_ = strings_[i]
                str_ = str_[:-2] # chop off trailing , and space
                str_ += ')'
                strings_[i] = str_
            finalString = strings_[0] + strings_[1] + ';'
            self.db.execute(finalString, params)
            self.db.commit()
            return True
        except InvalidRequestError:
            return False
            
    
    
    def deleteUser(self, name):
        pass


    def searchForBooks(self, author=None, title=None, isbn=None):
        if not (author or title or isbn):
            return []
        
        searchStr = 'SELECT * from books WHERE '
        concator = ' AND '
        params = {'author':author, 'title':title, 'isbn':isbn}
        inputsToBeEscaped = {}
        for fieldName, value in params.items():
            if value:
                searchStr += f"{fieldName} ILIKE :{fieldName}" + concator
                inputsToBeEscaped[fieldName] = '%' + value + '%'
        searchStr = searchStr.rstrip(concator) + ';'
        results = self.db.execute(searchStr, inputsToBeEscaped) 
        return results
    
    
    def getBookDetails(self, isbn):
        searchStr = 'Select * FROM books WHERE isbn=:isbn'
        return self.db.execute(searchStr, {'isbn':isbn}).first()
    
    
    def saveReview(self, userId, isbn, rating, reviewText):
        bookId = self.searchForBooks(isbn=isbn).first()['id']
        sqlStr = 'INSERT INTO reviews (book_id, user_id, rating, entry) VALUES '
        sqlStr += '(:bookId, :userId, :rating, :reviewText);'
        self.db.execute(sqlStr, {'bookId':bookId, 'userId':userId, 'rating':rating, 'reviewText':reviewText})
        self.db.commit()
    
    
    def getReviews(self, isbn):
        bookDetails = self.getBookDetails(isbn)
        sqlStr = """SELECT reviews.user_id, reviews.rating, reviews.entry, reviews.creation_date 
        FROM reviews WHERE reviews.book_id=:book_id"""
        return self.db.execute(sqlStr, {'book_id':bookDetails['id']}).fetchall()


    def __init__(self, connectionString):
        '''
        Constructor
        '''
        engine = create_engine(connectionString)
        self.db = scoped_session(sessionmaker(bind=engine))