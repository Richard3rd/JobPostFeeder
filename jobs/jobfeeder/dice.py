'''Dice job search feeder

@author Hideki Ikeda
@created Apr 17, 2015
'''

import urllib
import json
import urllib
from bs4 import BeautifulSoup

from consts import idx_company
from consts import idx_postdate
from consts import idx_title
from consts import idx_location
from consts import idx_description
from consts import idx_posturl

host_url='http://service.dice.com'
base_url=host_url+'/api/rest/jobsearch/v1/simple.json'
direct_url='direct=1'
areacode_url='areacode={}'
country_url='country={}'
state_url='state={}'
skill_url='skill={}'
city_url='city={}'
text_url='text={}'
ip_url='ip={}'
age_url='age={}'
diceid_url='diceid={}'
sort_url='sort={}'
sd_url='sd={}'

def _list_arg_to_string(l_str):
    '''
    Concatenates strings in a list into a string.
    If a string in the list contains spaces, the string will be embraced with
    double quote.
    '''
    l = [l_str] if isinstance(l_str, basestring) else l_str
    return ' '.join([urllib.quote(s if s.find(' ')==-1 else '"'+s+'"') for s in l])


class DiceFeeder(object):
    '''Feed job postings from Dice.

    Works as a generator. Returns a job posting one by one.
    Arguments:
        direct - (optional) if the value of this parameter is True then jobs
            returned will be direct hire; default False
        areacode - (optional) specify the jobs area code
        country - (optional) specify the jobs ISO 3166 country code
        state - (optional) specify the jobs United States Post Office
            state code
        skill - (optional) list of search text for the jobs skill property
        city - (optional) specify the jobs United States Post Office ZipCode
            as the center of 40 mile radius
        text - (optional) list of search text for the jobs entire body
        ip - (optional) specify an IP address that will be used to look up
            a geocode which will be used in the search
        age - (optional) specify a posting age (a.k.a. days back)
        diceid - (optional) specify a Dice customer ID to find only jobs
            from that company
        sort - (optional) specify a sort paremeter;
            'age', 'jobtitle', 'company', or 'location'
        sd - (optional) sort direction; if False is ASCENDING (default)
            if True is DESCENDING
            Ignored if sort is not set.
        description - (optional) if True, returns the description.
            if False, return the url to the job posting. Default True
    '''
    def __init__(self,
            direct = False,
            areacode = None,
            country = None,
            state = None,
            skill = None,
            city = None,
            text = None,
            ip = None,
            age = None,
            diceid = None,
            sort = None,
            sd = False,
            description = True
            ):
        self._description = description
        params = []
        if direct:
            params.append(direct_url.format(1))

        if areacode is not None:
            params.append(apreacode_url.format(urllib.quote(areacode)))

        if country is not None:
            params.append(country_url.format(urllib.quote(country)))

        if state is not None:
            params.append(state_url.format(urllib.quote(state)))

        if skill is not None:
            params.append(skill_url.format(_list_arg_to_string(skill)))

        if city is not None:
            params.append(city_url.format(urllib.quote(city)))

        if text is not None:
            params.append(text_url.format(_list_arg_to_string(text)))

        if ip is not None:
            params.append(ip_url.format(urllib.quote(ip)))

        if age is not None:
            params.append(age_url.format(age))

        if diceid is not None:
            params.append(diceid_url.format(urllib.quote(diceid)))

        if sort is not None:
            if sort=='age':
                n = 1
            elif sort=='jobtitle':
                n = 2
            elif sort=='company':
                n = 3
            elif sort=='location':
                n = 4
            else:
                raise ValueError('sort parameter must be "age", "jobtitle", "company" or "location"')
            params.append(sort_url.format(n))
            params.append(sd_url.format('d' if sd else 'a'))

        self._base_url = base_url
        if len(params) > 0:
            self._base_url += '?' + '&'.join(params)
        self._next_url = self._base_url
        self._load_next()
        self._count=self._top_json['count']
        self._next_doc = 0

    def _load_next(self):
        f_dice = urllib.urlopen(self._next_url)
        self._top_json = json.load(f_dice)
        f_dice.close()

        if 'nextUrl' in self._top_json:
            self._next_url = host_url + self._top_json['nextUrl']
        else:
            self._next_url = None
        self._first_doc = self._top_json['firstDocument']
        self._last_doc = self._top_json['lastDocument']

    def __iter__(self):
        return self

    def next(self):
        if self._next_doc == self._count:
            raise StopIteration
        if self._next_doc == self._last_doc:
            self._load_next()
        j_job = self._top_json['resultItemList'][self._next_doc - self._first_doc]
        a_job = { idx_company : j_job['company'],
                idx_postdate : j_job['date'],
                idx_title : j_job['jobTitle'],
                idx_location : j_job['location'],
                idx_description : self._get_description(j_job['detailUrl']),
                idx_posturl : j_job['detailUrl'] }
        self._next_doc += 1

        return json.dumps(a_job)

    def count(self):
        return self._count

    def _get_description(self, url):
        '''Get job description from a Dice url'''
        if self._description:
            try:
                page = urllib.urlopen(url)
                post = BeautifulSoup(page)
                page.close()
                description = post.body.find(property='description')['content']
            except TypeError:
                description = 'Description not available: ' + url
        else:
            description = url
        return description


if __name__=='__main__':
    feeder=DiceFeeder(text='hadoop', city='01886', age=21, sort='age', sd=True)
    print feeder._next_url
    print feeder._count
    for i, post in enumerate(feeder):
        print i, post
        if i == 9:
            break
