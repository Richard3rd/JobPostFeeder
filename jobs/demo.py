#!/usr/bin/env python

'''Job search feeder demonstration

@author Hideki Ikeda
@created Apr 21, 2015
'''

from jobfeeder import JobFeeder
from webdemo import set_callback, start


def search_callback(skill=None, keyword=None, zipcode=None, age=None):
    return JobFeeder(skill=skill, text=keyword, zipcode=zipcode, age=age,
            sort='age', sd=True, description=False)


if __name__=='__main__':
    set_callback(search_callback)
    start()
