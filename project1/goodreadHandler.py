'''
Created on Aug 30, 2019

@author: Brad
'''

import requests
from go import getCreds
import sys
import datetime

class GoodreadHandler(object):    
    '''
    classdocs
    '''

    _key = None
    _lastAccessTime = None
    _baseURL = 'https://www.goodreads.com/'


    def __init__(self):
        creds = getCreds(sys.argv[1], "goodreads")
        GoodreadHandler._key = creds['key']
        
    
    @classmethod
    def _isOldEnough(self):
        if GoodreadHandler._lastAccessTime is None:
            return True
        if GoodreadHandler._lastAccessTime - datetime.datetime.now() < datetime.timedelta(seconds=1):
            return False
        return True
    
    
    def getBookRating(self, isbn):
        if not GoodreadHandler._isOldEnough():
            raise Exception("API request made too soon.  Wait at least one minute between requests.")
        
        response = requests.get(self._baseURL + 'book/review_counts.json', params={"key": GoodreadHandler._key, "isbns":isbn})
        if response.status_code != 200:
            raise Exception("Goodbooks API unavailable")
        
        data = response.json()['books'][0]
        print(data)
        return (data['ratings_count'], data['average_rating'])