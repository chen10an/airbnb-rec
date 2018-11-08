# this code is adapted from https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py

# GOAL: scrape NUM_BUSINESSES relevant yelp businesses and store into a json file

import config  # file with private info
import math

import argparse
import json
import pprint
import requests
import sys
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

FILE_PATH = 'businesses.json'  # where to save the queried json

DEFAULT_TERM = 'restaurants'
DEFAULT_LOCATION = 'New York'

NUM_BUSINESSES = 500  # best if this is a multiple of SEARCH_LIMIT
SEARCH_LIMIT = 50  # max 50

offset = 0  # don't change
# results are returned in range 0 to <SEARCH_LIMIT>
# this is incremented to also return results in range offset to <offset+SEARCH_LIMIT>

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# "Using the offset and limit parameters, you can get up to 1000 businesses from this endpoint if there are more than 1000 results.
# If you request a page out of this 1000 business limit, this endpoint will return an error."
# source: https://www.yelp.com/developers/documentation/v3/business_search

# note: not possible to filter by rating (number of stars), so this will have to be done manually later

API_KEY = config.API_KEY


def request(host, path, api_key, url_params=None):
  """Given your API_KEY, send a GET request to the API.
  Args:
    host (str): The domain host of the API.
    path (str): The path of the API after the domain.
    API_KEY (str): Your API Key.
    url_params (dict): An optional set of query parameters in the request.
  Returns:
    dict: The JSON response from the request.
  Raises:
    HTTPError: An error occurs from the HTTP request.
  """
  url_params = url_params or {}
  url = '{0}{1}'.format(host, quote(path.encode('utf8')))
  headers = {
    'Authorization': 'Bearer %s' % api_key,
  }

  # print(u'Querying {0} ...'.format(url))

  response = requests.request('GET', url, headers=headers, params=url_params)

  return response.json()


def search(api_key, term, location):
  """Query the Search API by a search term and location.
  Args:
  term (str): The search term passed to the API.
    location (str): The search location passed to the API.
  Returns:
    dict: The JSON response from the request.
  """
  global offset
  url_params = {
    'term': term.replace(' ', '+'),
    'location': location.replace(' ', '+'),
    'limit': SEARCH_LIMIT,
    'offset': offset
  }
  return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
  """Query the Business API by a business ID.
  Args:
    business_id (str): The ID of the business to query.
  Returns:
    dict: The JSON response from the request.
  """
  business_path = BUSINESS_PATH + business_id

  return request(API_HOST, business_path, api_key)


def query_api(term, location):
  """Queries the API by the input values from the user.
  Args:
    term (str): The search term to query.
    location (str): The location of the business to query.
  """
  response = search(API_KEY, term, location)

  businesses = response.get('businesses')

  if not businesses:
    print(u'No businesses for {0} in {1} found.'.format(term, location))
    return

  print(u'{0} businesses found, querying business info for all results...'.format(len(businesses)))

  response_list = []
  for i in range(len(businesses)):
    business_id = businesses[i]['id']
    response = get_business(API_KEY, business_id)
    response_list.append(response)

  # print(u'Result for business "{0}" found:'.format(business_id))
  return response_list


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
  parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')

  input_values = parser.parse_args()

  try:

    # get all the businesses we want while staying within search limit for each query
    # i.e. query several times to get a number of businesses that exceeds the query limit
    all_response_list = []
    for i in range(math.ceil(NUM_BUSINESSES/SEARCH_LIMIT)):
      all_response_list += query_api(input_values.term, input_values.location)
      global offset
      offset += SEARCH_LIMIT

    # save all businesses into one file
    with open(FILE_PATH, 'w') as fp:  # save all 
      json.dump(all_response_list, fp, indent=2, ensure_ascii=False)

    print("Saved {} businesses in {}!".format(len(all_response_list), FILE_PATH))

  except HTTPError as error:
    sys.exit(
      'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
          error.code,
          error.url,
          error.read(),
      )
    )


if __name__ == '__main__':
  main()
