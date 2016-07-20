#  Changes to migrate JobPostFeeder to Python 3.x


## jobs.py
## jobfeeder/jobfeed.py
## webdemo/handler.py
## webdemo/model.py
* #### 	fix print commands -- print is a function in Python 3.x


## jobfeeder/dice.py
* #### 	fix print commands -- print is a function in Python 3.x
* ####	fix urllib usage -- now urllib package is split into urllib.request, urllib.parse, and urllib.error
* ####	fix use of basestring -- this type does not exist in Python 3.x
* ####	fix definition of iterator -- now use \_\_iter\_\_() not iter()
* ####	fix loading of JSON response


## webdemo/app.py
* ####	fix the import of Flask extensions -- new package structure


## webdemo/democonfig.py
* ####	add SQLALCHEMY_TRACK_MODIFICATIONS definition to suppress annoying warning
* ####	print a couple of logging lines (commented out)


## changes.md (this file)
* ####	list of changes made to migrate to Python 3.x


## .gitignore
* #### 	ignore webdemo/migrations folder -- not sure it is ever used

