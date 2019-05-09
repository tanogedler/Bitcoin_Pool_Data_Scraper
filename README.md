# Bitcoin Pool Data Scraper
Scraper of Bitcoin transaction data, as hashrate and profit in terms of BTC


Here we have a Python script that collects from several mining pools the data about hashrate and profit. The profit is the actual profit in terms of BTC. 


Any data from the available APIs can be easily added to the script, and other pools as well. Feel free to use this, and modify as you like. 


## How it works?

* The script in python dataCapture.py runs forever and grab the mentioned data from the pool every 10 seconds. 
* This data is then stored in csv files in the directory csvdata. (make sure you have this directory under which you are running the script)
* Also, we have here a bash script that takes the last 5 min data, clones it to a new file in the directorty called csvdata_tmp (again make sure there is such csvdata_tmp directory) and loads it to a database.
* The tables in database, are called with same names as the files, (without the csv extension, of course)


## Assumptions

This scraper is intended to run in a Ubuntu server, and from there it sends the data to a phpPMyAdmin database where the data is finally stored.

The shell script can be added as a cron job that runs every 5 minutes

### Last but not lest...

You can use this, as you like, improve it, break it, modify it, or just clone it and use it. 

It would be nice if you let me know any improvement that can be done, so we can learn together.
