import random
import json
import boto3
import decimal
import time
import datetime
#from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr
import requests

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('yelp-restaurants')

def lambda_handler(event, context):
    #print('inside handler')
    #print(event)
    sendMessage()
   
def sendMessage():
    # create a boto3 client
    client = boto3.client('sqs')
    sms_client = boto3.client('sns')
    queues = client.list_queues(QueueNamePrefix='input') # we filter to narrow down the list
    test_queue_url = queues['QueueUrls'][0]
    #print(test_queue_url)
    while True:
        # Receive message from SQS queue
        response = client.receive_message(
        QueueUrl=test_queue_url,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=30,
        WaitTimeSeconds=0
        )
        #print(response)
        if 'Messages' in response: # when the queue is exhausted, the response dict contains no 'Messages' key
            for message in response['Messages']: # 'Messages' is a list
                js = json.loads(message['Body'])
                #print(json.dumps(js,indent=4,sort_keys=True))
                cuisine = js['cuisine']
                email = js['email']
                phone = js['phone']
                count= js['count']
                time= js['time']
                date= js['date']
                url = 'https://search-sygo-domain-mf7q4d6yb655bv3ug7p6j7r23u.us-east-1.es.amazonaws.com/restaurants/restaurant/_search?from=0&&size=1&&q=Cuisine:'+cuisine 
                resp = requests.get(url,headers={"Content-Type": "application/json"}).json()
                n_vals = resp['hits']["total"]['value']
                #idx = random.randint(0,n_vals-1)
                idxList = random.sample(range(0,n_vals-1), 3)
                resNameAdd=''
                for idx in range(len(idxList)):
                    url2 = 'https://search-sygo-domain-mf7q4d6yb655bv3ug7p6j7r23u.us-east-1.es.amazonaws.com/restaurants/restaurant/_search?from='+str(idxList[idx])+'&&size=1&&q=Cuisine:'+cuisine
                    resp = requests.get(url2,headers={"Content-Type": "application/json"}).json()
                    #print(resp)
                    res = resp['hits']['hits'][0]['_source']['RestaurantID']
                    dbRes = table.query(KeyConditionExpression=Key('insertedAtTimestamp').eq(res))
                    addr = str(dbRes['Items'][0]['address'])
                    for char in "'u[]":
                        addr = addr.replace(char,'')
                    resNameAdd += ' '+str(idx+1) +'. '+ dbRes['Items'][0]['name']+", located at "+addr+"."
                #print(resNameAdd)
                client.delete_message(QueueUrl=test_queue_url,ReceiptHandle=message['ReceiptHandle'])
                message = 'Hello! Here are my '+ cuisine +' restaurant suggestions for '+ count +' people, for '+ date+ ' at '+time+ ': '+resNameAdd+' Enjoy your meal!'
                check = sms_client.publish(PhoneNumber=str(phone),Message=message)
                #print(check)
                print(message)
        else:
            print('Queue is now empty')
            break
        
