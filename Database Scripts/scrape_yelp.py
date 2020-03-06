#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json

# from botocore.vendored import requests
import requests
from urllib.parse import urljoin
import boto3
from decimal import *
import datetime
from time import sleep
# from elasticSearch import putRequests


# In[2]:


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('yelp-restaurants')

API_KEY = 'hUXr7rBoAynAWO3Z2ZQIZ18hp7ELUA3zx_8VXDQiHbGLTuChAK7WoW7js9mtAUV-9Cy3g_q7KwNGDIWMYp9N3brGisyfrLLAhtJ3YfvpUxNUKTvFQQEWvgtnSetaXnYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Manhattan'
restaurants = {}



# In[4]:


def search(cuisine,offset):
    url_params = {
        'location': 'Manhattan',
        'offset' : offset,
        'limit': 50,
        'term': cuisine + " restaurants",
        'sort_by' : 'rating'
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)


def request(host, path, url_params=None):
    API_KEY = 'hUXr7rBoAynAWO3Z2ZQIZ18hp7ELUA3zx_8VXDQiHbGLTuChAK7WoW7js9mtAUV-9Cy3g_q7KwNGDIWMYp9N3brGisyfrLLAhtJ3YfvpUxNUKTvFQQEWvgtnSetaXnYx'
    # ENDPOINT = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(business_id)
    ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}

    PARAMETERS = url_params
    # Make a request to the Yelp API
    response = requests.get(url = ENDPOINT,
                            params = PARAMETERS,
                            headers = HEADERS)
    # response = requests.get(url = ENDPOINT,params = PARAMETERS,headers = HEADERS)
    rjson = response.json()
    return rjson

def addItems(data, cuisine):
    global restaurants
    with table.batch_writer() as batch:
        for rec in data:
            try:
                if rec["alias"] in restaurants:
                    continue;
                rec["rating"] = Decimal(str(rec["rating"]))
                restaurants[rec["alias"]] = 0
                rec['cuisine'] = cuisine
                rec['insertedAtTimestamp'] = str(datetime.datetime.now())
                rec["coordinates"]["latitude"] = Decimal(str(rec["coordinates"]["latitude"]))
                rec["coordinates"]["longitude"] = Decimal(str(rec["coordinates"]["longitude"]))
                rec['address'] = rec['location']['display_address']
                rec.pop("distance", None)
                rec.pop("location", None)
                rec.pop("transactions", None)
                rec.pop("display_phone", None)
                rec.pop("categories", None)
                if rec["phone"] == "":
                    rec.pop("phone", None)
                if rec["image_url"] == "":
                    rec.pop("image_url", None)
    
                # print(rec)
                batch.put_item(Item=rec)
                sleep(0.001)
            except Exception as e:
                print(e)
                print(rec)


def scrape():
    cuisines = ['italian', 'chinese', 'indian', 'american', 'mexican', 'spanish','greek','latin','Persian']
    for cuisine in cuisines:
        offset = 0
        print('cuisine : ',cuisine)
        while offset<1000:
            js = search(cuisine,offset)
            addItems(js["businesses"], cuisine)
            offset+=50


# In[5]:


scrape()


# In[ ]:




