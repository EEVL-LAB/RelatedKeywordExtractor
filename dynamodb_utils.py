import json
import boto3
import datetime
from boto3.dynamodb.conditions import Key


async def read_secret():
    with open('secret.json', 'r') as f:
        secret = json.load(f)
        return secret


async def load_table(secret: dict):
    dynamodb = boto3.resource(
        'dynamodb', 
        region_name='ap-northeast-2',
        aws_access_key_id=secret.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=secret.get("AWS_SECRET_ACCESS_KEY")
    )
    return dynamodb.Table('ScrapingData')


async def retrieve_documents(table, target_keyword):
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=5)
    previous = (today - delta).strftime("%Y-%m-%d")
    today = today.strftime("%Y-%m-%d")
    
    query = {
        "IndexName": 'TargetKeyword-Date-index',
        "KeyConditionExpression": Key("TargetKeyword").eq(target_keyword) & Key('Date').between(previous, today)
    }
    documents = table.query(**query)
    return [
        document.get("CotentPlainText") for document in documents.get("Items")
    ]
