import json
import boto3


client = boto3.client('lex-runtime')

def lambda_handler(event, context):
    
    lastUserMessage = event['messages'];
    botMessage = "Ask me something!!";
    dummy="I'm still under development. Please come back later."
    user ='test'
   
    if lastUserMessage is None or len(lastUserMessage) < 1:
        return {
            'statusCode': 200,
            'body': json.dumps(botMessage)
        }
     
    response = client.post_text(botName='DinningConcierge',
        botAlias='Dining',
        userId=user,
        inputText=lastUserMessage)
    
    if response['message'] is not None or len(response['message']) > 0:
        lastUserMessage = response['message']   
    
    return {
        'statusCode': 200,
        'body': json.dumps(lastUserMessage)
    }
