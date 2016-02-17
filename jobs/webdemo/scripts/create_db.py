'''Search for job postings demonstration
Create DB utility

@author Hideki Ikeda
@created Feb 16, 2016
'''

import os, sys
sys.path.append(os.getcwd())
from main import db

if __name__ == '__main__':
    db.create_all()
