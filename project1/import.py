'''
Created on Aug 21, 2019

@author: Brad
'''

def populateBooks(connectionStr, fileLocation):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker
    import csv
    
    engine = create_engine(connectionStr)
    db = scoped_session(sessionmaker(bind=engine))
    
    with open(fileLocation) as f:
        reader = csv.reader(f) # skip title row
        next(reader)
        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year);", \
                       {'isbn':isbn, 'title':title, 'author':author, 'year':year})
            #print(f'row added for {title}')
        db.commit()
            
    

import sys
if __name__ == '__main__':
    print(sys.argv[1])
    print (sys.argv[2])
    #populateBooks(sys.argv[1], sys.argv[2])