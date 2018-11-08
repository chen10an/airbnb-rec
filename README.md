# airbnb-rec
A web app that recommends airbnb listings based on custom heuristics. This project is developed by Duke Computer Science students for COMPSCI 316.

## Production Data
### Airbnb data
The production dataset may be downloaded from the website http://insideairbnb.com/get-the-data.html under New York City, New York, United States. The datasets needed are listings.csv and calendar.csv. Both of these files should be converted to .xlsx files.

The data from listings.xlsx can be extracted and inserted into the database using the code in listingInsert.py (simply run the command 'python listingInsert.py' on the command line). The same can be done with the data from calendar.xlsx using the code in calendarInsert.py.

Note that this will not work on a computer without access to the database we are using.

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



