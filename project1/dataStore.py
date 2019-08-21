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
    db = None
    
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


    def __init__(self, connectionString):
        '''
        Constructor
        '''
        engine = create_engine(connectionString)
        self.db = scoped_session(sessionmaker(bind=engine))
        