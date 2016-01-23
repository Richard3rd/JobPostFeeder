'''Search for job postings demonstration

@author Hideki Ikeda
@created Apr 21, 2015
'''

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask(__name__)
app.config.from_pyfile('democonfig.py')


class FormData(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self._entries = []
        self._keywords = {'skill':'', 'keyword':'', 'zipcode':'', 'age':''}

    def set_entry(self, city_pos):
        self._entries = city_pos

    def get_entries(self):
        entries = []
        for city, n_pos in self._entries:
            entries.append( {'city':city, 'n_pos':n_pos} )
        return entries

    def set_keywords(self, skill=None, keyword=None, zipcode=None, age=None):
        if skill is None:
            skill = ''
        if keyword is None:
            keyword = ''
        self._keywords = {'skill':skill, 'keyword':keyword,
                'zipcode':zipcode, 'age':age}

    def get_keywords(self):
        return self._keywords

formdata = FormData()


def test_callback(skill=None, keyword=None, zipcode=None, age=None):
    return [('Chelmsford', 0)]

cb = test_callback

def set_callback(callback):
    global cb
    cb = callback


def start():
    app.run()


@app.route('/')
def show_entries():
    return render_template('layout.html',
            entries=formdata.get_entries(),
            searchwords=formdata.get_keywords())

@app.route('/search_jobs', methods=['POST'])
def search_jobs():
    global entries
    if ((request.form['skill']=='' and request.form['keyword']=='')
            or request.form['zipcode']==''
            or request.form['age']==''):
        formdata.reset()
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

            city_pos = cb(
                    skill = skill_,
                    keyword = key_,
                    zipcode = zip_,
                    age = age_ )
            formdata.set_entry(city_pos)

            formdata.set_keywords(skill_, key_, zip_, age_)
        except ValueError:
            flash('Age must be a number')

    return redirect(url_for('show_entries'))


if __name__=='__main__':
    start()
