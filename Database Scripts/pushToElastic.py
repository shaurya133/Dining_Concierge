import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.vendored import requests


def lambda_handler(event, context):
    # TODO implement
    putRequests()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('yelp-restaurants')

def putRequests():
    resp = table.scan()
    i = 1
    url='https://search-sygo-domain-mf7q4d6yb655bv3ug7p6j7r23u.us-east-1.es.amazonaws.com/restaurants/restaurant'
    while True:
        #print(len(resp['Items']))
        for item in resp['Items']:
            body = {"RestaurantID": item['insertedAtTimestamp'], "Cuisine": item['cuisine']}
            r = requests.post(url, data=json.dumps(body).encode("utf-8"), headers=headers)
            #print(r)
            i += 1
            #break;
        if 'LastEvaluatedKey' in resp:
            resp = table.scan(
                ExclusiveStartKey=resp['LastEvaluatedKey']
            )
            #break;
        else:
            break;
    print(i)
