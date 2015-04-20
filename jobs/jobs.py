#!/usr/bin/env python

'''Search for job postings

@author Hideki Ikeda
@created Apr 19, 2015

Command line options:
    -h, --help        show the help messagne and quit
    -k KEYWORD [KEYWORD ...], --keyword KEYWORD [KEYWORD ...]
                      specify search keywords for job description
    -s SKILL [SKILL ...], -skill SKILL [SKILL ...]
                      specify search text for the jobs skill property
    -z ZIPCODE, --zipcode ZIPCODE
                      specify a zipcode as the center of 40 mile radius
    -a AGE, -- age AGE
                      specify a posting age (a.k.a. days back)
    -S {age,jobtitle,company,location}, --sort {age,jobtitle company,location}
                      specify a sort key
    -D, --descending  sort in descending order; without this, sort in scending
                      order
    -n, --no_description
                      don't get detail job description; return the URL instead
    -d, --direct      return direct hire jobs only.
'''

import argparse

from jobfeeder import JobFeeder
from jobfeeder import idx_company
from jobfeeder import idx_postdate
from jobfeeder import idx_title
from jobfeeder import idx_location
from jobfeeder import idx_description


if __name__=='__main__':
    parser = argparse.ArgumentParser(
            description='Search for job posting and show them in the JSON format',
            epilog='ex) jobs.py -s c++ java -k "big data" -z 02140 -a 14 -S age -D')
    parser.add_argument('-k', '--keyword', nargs='+',
            help='specify search keywords for job description')
    parser.add_argument('-s', '--skill', nargs='+',
            help='specify search text for the jobs skill property')
    parser.add_argument('-z', '--zipcode', 
            help='specify a zipcode as the center of 40 mile redius')
    parser.add_argument('-a', '--age', type=int,
            help='specify a posting age (a.k.a. days back)')
    parser.add_argument('-S', '--sort',
            choices=['age', 'jobtitle', 'company', 'location'],
            help='specify a sort key')
    parser.add_argument('-D', '--descending', action='store_true',
            help='sort in descending order; without this, sort in ascending order')
    parser.add_argument('-n', '--no_description', action='store_true',
            help="don't get detailed job description; return the URL instead")
    parser.add_argument('-d', '--direct', action='store_true',
            help='return direct hire jobs only.')

    args = parser.parse_args()
    feeder = JobFeeder(direct=args.direct, skill=args.skill,
                       zipcode=args.zipcode, text=args.keyword,
                       age=args.age, sort=args.sort, sd=args.descending,
                       description=not args.no_description)

    for post in feeder:
        print post
