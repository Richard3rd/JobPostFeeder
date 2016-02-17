'''Search for job postings demonstration
request handlers

@author Hideki Ikeda
@created Feb 16, 2016
'''

from flask import request, session, redirect, url_for, abort, render_template, flash

from app import app
from model import FormData

# helper functions
def get_current_data():
    '''
    Helper function to get the current FormData in this session
    Args: None
    Return: An FormData object; None if there're no current data
    '''
    formdata = None
    if 'formdata' in session:
        dataid = session['formdata']
        formdata = FormData.getData(dataid)
        if not formdata:
            flash('Session expired')
            del session['formdata']
    return formdata


@app.route('/')
def show_entries():
    formdata = get_current_data()
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

            session['formdata'] = dataid
        except ValueError:
            flash('Age must be a number')

    return redirect(url_for('show_entries'))


@app.route('/list')
def show_jobs():
    city = request.args.get('city')
    if not city:
        flash('No city given')
        return redirect(url_for('show_entries'))
    try:
        city = int(city)
    except ValueError:
        flash('Invalid city specified')
        return redirect(url_for('show_entries'))

    formdata = get_current_data()
    if not formdata:
        return redirect(url_for('show_entries'))

    cities = formdata.get_entries()
    if not cities or city >= len(cities):
        flash('Invalid city specified')
        return redirect(url_for('show_entries'))

    postData = formdata.get_post_in_city(city)
    print postData

    return render_template('list.html', city=cities[city]['city'],
            n_pos=cities[city]['n_pos'], postData=postData)
