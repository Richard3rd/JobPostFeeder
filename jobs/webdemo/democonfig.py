'''Search for job postings demonstration

@author Hideki Ikeda
@created Apr 21, 2015
'''

import os

DEBUG=True
SECRET_KEY='development key'
APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/jobs.db'.format(APPLICATION_DIR)
