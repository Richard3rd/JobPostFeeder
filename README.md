# JobPostFeeder

Retrieve job postings from Dice.com and show as JSON objects.

### How to run
On Linux, go to the jobs directory and run `./jobs.py`  
ex)  
``$ ./jobs.py -k "big data" -z 02140 -a 7 -S age -D -n``
  
On Windows,  
``>python jobs.py -k "big data" -z 02140 -a 7 -S age -D -n``
  
If it complains that you don't have BeautifulSoup, run
``pip install -r requirements.txt``
  
### Command line options
* `-h, --help`  
   show the help messagne and quit  
* `-k KEYWORD [KEYWORD ...], --keyword KEYWORD [KEYWORD ...]`  
  specify search keywords for job description  
* `-s SKILL [SKILL ...], -skill SKILL [SKILL ...]`  
  specify search text for the jobs skill property  
* `-z ZIPCODE, --zipcode ZIPCODE`  
  specify a zipcode as the center of 40 mile radius  
* `-a AGE, -- age AGE`  
  specify a posting age (a.k.a. days back)  
* `-S {age,jobtitle,company,location}, --sort {age,jobtitle company,location}`  
  specify a sort key  
* `-D, --descending`  
  sort in descending order; without this, sort in scending order  
* `-n, --no_description`  
  don't get detail job description; return the URL instead  
* `-d, --direct`  
  return direct hire jobs only.  
