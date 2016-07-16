'''Search for job postings demonstration
Data model module

@author Hideki Ikeda
@created Feb 16, 2016
'''

import datetime
from collections import defaultdict
import json

from sqlalchemy import func, desc

from app import db

cb = None

def set_callback(callback):
    global cb
    cb = callback


class Session(db.Model):
    sessionID = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.String(100))
    keywords = db.Column(db.String(100))
    zipcode = db.Column(db.String(10))
    postage = db.Column(db.Integer)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    access_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    postdata = db.relationship('PostData', backref='session', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Session: skills={}, keywords={}, zip={}, age={}>'.format(
                self.skills, self.keywords, self.zipcode, self.postage)


class PostData(db.Model):
    postID = db.Column(db.Integer, primary_key=True)
    sessionID = db.Column(db.Integer, db.ForeignKey('session.sessionID'))
    postDate = db.Column(db.DateTime)
    title = db.Column(db.String(128))
    company = db.Column(db.String(64))
    location = db.Column(db.String(32))
    postURL = db.Column(db.String(64))

    def __init__(self, *args, **kwargs):
        super(PostData, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<PostData: postID={}, sessionID={}>'.format(self.postID,
                self.sessionID)


class FormData(object):
    @classmethod
    def factory(cls, skill, keyword, zipcode, age):
        '''
        FormData factory class method
        Args: skill, keyword, zipcode, age 
        '''
        feeder = cb(skill, keyword, zipcode, age)

        if skill is None:
            skill = ''
        if keyword is None:
            keyword = ''
        newsession = Session(skills=skill, keywords=keyword, zipcode=zipcode,
                postage=age)
        db.session.add(newsession)
        db.session.commit()

        sessionID = newsession.sessionID

        for raw_data in feeder:
            data = json.loads(raw_data)
            newPost = PostData(sessionID=sessionID, title=data['title'],
                    postDate=datetime.datetime.strptime(data['postdate'], '%Y-%m-%d'),
                    company=data['company'], location=data['location'],
                    postURL=data['posturl'])
            db.session.add(newPost)
            print ('{} {} {}'.format(data['location'], data['postdate'], data['title']))
        db.session.commit()

        return sessionID


    @classmethod
    def getData(cls, dataid):
        if not Session.query.filter(Session.sessionID==dataid).first():
            return None
        return FormData(dataid)

    def __init__(self, dataID):
        self._dataID = dataID
        sess = Session.query.filter(Session.sessionID==dataID).first()
        self._keywords = {'skill':sess.skills, 'keyword':sess.keywords,
                'zipcode':sess.zipcode, 'age':sess.postage}
        sess.access_timestamp = datetime.datetime.now()
        db.session.add(sess)
        db.session.commit()

        city_pos_dict = defaultdict(int)
        postdata = (db.session
                .query(PostData.location, func.count(PostData.postID))
                .filter(PostData.sessionID==dataID)
                .group_by(PostData.location)
                .order_by(PostData.location) )
        self._entries = [{'city':d[0], 'n_pos':d[1]} for d in postdata]

    def get_entries(self):
        return self._entries

    def get_keywords(self):
        return self._keywords

    def get_post_in_city(self, city):
        raw_data = (PostData.query
                .filter(PostData.sessionID==self._dataID)
                .filter(PostData.location==self._entries[city]['city'])
                .order_by(desc(PostData.postDate))
                .all())
        data = [ {'postDate':d.postDate.strftime("%x"), 'title':d.title, 'company':d.company,
            'postURL':d.postURL} for d in raw_data]
        return data
