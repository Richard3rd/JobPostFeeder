'''Job search feeder

@author Hideki Ikeda
@created Apr 19, 2015
'''


__title__ = 'jobfeeder'
__version__ = '0.0.1'
__author__ = 'Hideki Ikeda'
__licence__ = 'Apache License Version 2.0'
__copyright__ = 'Copyright 2015 Hideki Ikeda'


from consts import idx_company
from consts import idx_postdate
from consts import idx_title
from consts import idx_location
from consts import idx_description
from consts import idx_posturl
from jobfeed import JobFeeder


__all__ = [
            'idx_company',
            'idx_postdate',
            'idx_title',
            'idx_location',
            'idx_description',
            'JobFeeder'
          ]
