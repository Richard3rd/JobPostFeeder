'''Search for job postings demonstration

@author Hideki Ikeda
@created Apr 21, 2015
'''

from app import app, db
import model
import handler

def start():
    app.run()


if __name__=='__main__':
    start()
