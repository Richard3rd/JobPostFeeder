'''Search for job postings demonstration

@author Hideki Ikeda
@created Apr 21, 2015
'''

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask(__name__)
app.config.from_pyfile('democonfig.py')


entries = [ {'city':'Chelmsford', 'n_pos':0} ]
def test_callback(skill=None, keyword=None, zipcode=None, age=None):
    if entries[0]['city'] == 'Chelmsford':
        return [('Boston', 32)]
    else:
        return [('Chelmsford', 0)]

cb = test_callback

def set_callback(callback):
    global cb
    cb = callback


def start():
    app.run()


@app.route('/')
def show_entries():
    return render_template('layout.html', entries=entries)

@app.route('/search_jobs', methods=['POST'])
def search_jobs():
    global entries
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
            age_int = int(request.form['age'])

            city_pos = cb(
                    skill = skill_,
                    keyword = key_,
                    zipcode = request.form['zipcode'],
                    age = age_int )

            entries = []
            for city, n_pos in city_pos:
                entries.append( {'city':city, 'n_pos':n_pos} )
        except ValueError:
            flash('Age must be a number')

    return redirect(url_for('show_entries'))


if __name__=='__main__':
    start()
