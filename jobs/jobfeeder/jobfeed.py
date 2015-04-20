'''Job search feeder

@author Hideki Ikeda
@created Apr 17, 2015
'''

from dice import DiceFeeder

from consts import idx_company
from consts import idx_postdate
from consts import idx_title
from consts import idx_location
from consts import idx_description


class JobFeeder(object):
    '''Feed job postings from Dice.

    This module works as a generator and returns job postings in the JSON
    format.
    Arguments:
        direct: if True then jobs returned will be direct hire; default False
        skill: list of search text for the jobs skill property
        zipcode: specify the jobs United States Post Office ZipCode
            as the center of 40 mile radius
        text: list of search text for the jobs entire body
        age: specify a posting age (a.k.a. days back)
        sort: specify a sort paremeter;
            'age', 'jobtitle', 'company', or 'location'
        sd: sort direction; if False is ASCENDING (default)
            if True is DESCENDING
            Ignored if sort is not set.
        description: if True, returns the description.
            if False, return the url to the job posting. Default True
    '''

    def __init__(self,
                 direct=False, skill=None, zipcode=None, text=None,
                 age=None, sort=None, sd=False, description=True):
        self._dice_feeder = DiceFeeder(
                direct=direct, skill=skill, city=zipcode, text=text, age=age,
                sort=sort, sd=sd, description=description);

    def count(self):
        '''returns the number of job postings'''
        return self._dice_feeder.count()

    def __iter__(self):
        return self._dice_feeder;


if __name__=='__main__':
    feeder=JobFeeder(text='hadoop', zipcode='02140', age=21, sort='age', sd=True)
    for post in feeder:
        print post

