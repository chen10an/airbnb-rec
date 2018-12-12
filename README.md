# airbnb-rec
A web app that recommends airbnb listings based on custom heuristics. This project is developed by Duke Computer Science students for COMPSCI 316.

# Running the App

We have deployed our app on Heroku where it can be accessed at 

https://airbnbproduction.herokuapp.com/recommender/

Note: We have deployed our database onto Heroku with the Heroku Postgres add on. Since we have over 1 million rows and the free plan only supports 10,000 rows, we have included instructions for how to create the database locally. 

## Production Data
### Airbnb data

The production dataset may be downloaded from the website http://insideairbnb.com/get-the-data.html under New York City, New York, United States. The datasets needed are listings.csv and calendar.csv. Both of these files should be converted to .xlsx files.

The data from listings.xlsx can be extracted and inserted into the database using the code in listingInsert.py (simply run the command 'python listingInsert.py' on the command line). The same can be done with the data from calendar.xlsx using the code in calendarInsert.py.

Note that this will not work on a computer without access to the database we are using.

Tables for the database may be generated with the creating.sql.

### Yelp data
The production dataset may be queried from `API_HOST = 'https://api.yelp.com'`. Specifically, we are querying yelp business data with the following api parameters (which can be found in `yelp_scrape.py`):

```py
DEFAULT_TERM = 'restaurants'
DEFAULT_LOCATION = 'New York'

NUM_BUSINESSES = 500
SEARCH_LIMIT = 50
offset = 0

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
```

`yelp_scrape.py` queries and stores this business production data in json format. A small sample of this stored data is in `businesses_sample.json` (the full dataset is not included in this repository).

## Python environment
**To replicate the python/conda environment we used, do the following:**

1. Install conda/miniconda
2. Type the following on the command line to import and activate the conda environment:

Mac:

```bash
conda env create -f airbnb-rec-env.yml
source activate airbnb-rec
```

Windows:

```bash
conda env create -f airbnb-rec-env.yml
activate airbnb-rec
```

3. View all of the installed python packages:

```bash
conda list
```


# Creating and Populating the Database Locally:
In the psql shell, create the database airbnb using the command
	CREATE DATABASE airbnb;
Create the tables for the database using the creating.sql file.
You can just copy and paste the commands and run them in the psql shell.
Populate the database tables using the Insert.py files.
Near the top of each Insert.py file is a line
	conn = psycopg2.connect("dbname=airbnb user=username password=password")
Change username and password to be the username and password of the database.
Make sure the Insert.py files are in the same location as the excel spreadsheets and the yelp_businesses_cleaned.pickle file.
First run the listingInsert.py file in the command line using python. Then do the same with calendarInsert.py and businessInsert.py. These may take several minutes to run.


# Connecting Django to the Database
Locate the settings.py file in the django project (located in the folder airbnbrec). 
Scroll down to DATABASES and set the USER and PASSWORD fields to the username and password of the database.
To run our app, use the following command:

```py
python manage.py runserver
```



