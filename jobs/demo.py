#!/usr/bin/env python

'''Job search feeder demonstration

@author Hideki Ikeda
@created Apr 21, 2015
'''

from collections import defaultdict
import json
from jobfeeder import JobFeeder
from webdemo import set_callback, start


def search_callback(skill=None, keyword=None, zipcode=None, age=None):
    feeder = JobFeeder(skill=skill, text=keyword, zipcode=zipcode, age=age,
            sort='age', sd=True, description=False)
    city_pos_dict = defaultdict(int)
    for raw_data in feeder:
        data = json.loads(raw_data)
        city_pos_dict[data['location'].lower()] += 1
        print '{} {} {}'.format(data['location'], data['postdate'], data['title'])

    city_pos = [(city, city_pos_dict[city]) for city in city_pos_dict]
    return city_pos


if __name__=='__main__':
    set_callback(search_callback)
    start()
