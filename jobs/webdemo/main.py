'''Search for job postings demonstration

@author Hideki Ikeda
@created Apr 21, 2015
'''

from collections import defaultdict
import json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask(__name__)
app.config.from_pyfile('democonfig.py')


class FormData(object):
    nextid = 0
    datadict = {}

    @classmethod
    def factory(cls, *args):
        '''
        FormData factory class method
        Args: skill, keyword, zipcode, age 
        '''
        formdata = FormData(*args)
        dataid = cls.nextid
        cls.nextid += 1
        cls.datadict[dataid] = formdata
        return dataid

    @classmethod
    def getData(cls, dataid):
        return cls.datadict.get(dataid)

    @classmethod
    def deleteData(cls, dataid):
        if dataid in cls.datadict:
            del cls.datadict[dataid]
        
    def __init__(self, skill=None, keyword=None, zipcode=None, age=None):
        feeder = cb(skill, keyword, zipcode, age)
        city_pos_dict = defaultdict(int)
        for raw_data in feeder:
            data = json.loads(raw_data)
            city_pos_dict[data['location'].lower()] += 1
            print '{} {} {}'.format(data['location'], data['postdate'], data['title'])
        self._entries = [{'city':city, 'n_pos':city_pos_dict[city]} for city in city_pos_dict]
        # TODO feeder

        if skill is None:
            skill = ''
        if keyword is None:
            keyword = ''
        self._keywords = {'skill':skill, 'keyword':keyword,
                'zipcode':zipcode, 'age':age}

    def get_entries(self):
        return self._entries

    def get_keywords(self):
        return self._keywords


cb = None

def set_callback(callback):
    global cb
    cb = callback


def start():
    app.run()


@app.route('/')
def show_entries():
    formdata = None
    if 'formdata' in session:
        dataid = session['formdata']
        formdata = FormData.getData(dataid)

    if formdata:
        ent = formdata.get_entries()
        swords = formdata.get_keywords()
    else:
        ent = [{'n_pos':0, 'city':'chelmsford, ma'}]
        swords = {'skill':'', 'keyword':'', 'zipcode':'', 'age':''}
    return render_template('search.html',
            entries=ent, searchwords=swords)

@app.route('/search_jobs', methods=['POST'])
def search_jobs():
    if ((request.form['skill']=='' and request.form['keyword']=='')
            or request.form['zipcode']==''
            or request.form['age']==''):
        flash('Please enter all fields')
    else:
        try:
            skill_ = request.form['skill']
            if skill_ == '':
                skill_ = None
            key_ = request.form['keyword']
            if key_ == '':
                key_ = None
            zip_ = request.form['zipcode']
            age_ = int(request.form['age'])

            dataid = FormData.factory(skill_, key_, zip_, age_)
            formdata = FormData.getData(dataid)

            if 'formdata' in session:
                FormData.deleteData(session['formdata'])
            session['formdata'] = dataid
        except ValueError:
            flash('Age must be a number')

    return redirect(url_for('show_entries'))


if __name__=='__main__':
    start()
