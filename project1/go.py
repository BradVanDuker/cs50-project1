'''
Created on Aug 18, 2019

@author: Brad
'''

import os
import yaml
from runpy import run_module
import sys


def getCreds(credFileLocation, filename):
    credFileLocation
    with open(credFileLocation + '\\' + filename, mode='r') as credFile:
        contents = yaml.safe_load(credFile)
    return contents


if __name__ == '__main__':
    creds = getCreds(sys.argv[1], 'project1')
    os.environ['DATABASE_URL'] = creds['URI']
    os.environ['FLASK_APP'] = 'application.py'
    os.environ['FLASK_DEBUG'] = '1'
    
    run_module('application', run_name='application')

    print('Done')