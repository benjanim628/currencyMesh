import time
import requests
import boto3
import json
from datetime import datetime

def get_currencies_dict():
    # Use a proxy server to stop local ip from being blacklisted
    proxies = {'http': '45.33.90.184:8080'}
    response = requests.get('https://www.freeforexapi.com/api/live?pairs=EURGBP,GBPUSD,USDZAR', proxies=proxies)
    currencies_dict = json.loads(response.text)
    print(currencies_dict)

    return currencies_dict

# Get the service resource.
dynamodb = boto3.resource(
'dynamodb',
aws_access_key_id='my access key',
aws_secret_access_key='my secret key',
region_name='my server region'
)

def create_table():
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='exchangeRates',
        KeySchema=[
            {
                'AttributeName': 'base_symbol',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'timestamp_rounded',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'base_symbol',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'timestamp_rounded',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='exchangeRates')

    # Print out some data about the table.
    print(table.item_count)

def delete_table():
    # Instantiate a table resource object
    table = dynamodb.Table('exchangeRates')

    table.delete()

def put_items():
    # Instantiate a table resource object
    table = dynamodb.Table('exchangeRates')

    # Get currency values
    currencies_dict = get_currencies_dict()
    EURGBP = currencies_dict['rates']['EURGBP']['rate']
    GBPUSD = currencies_dict['rates']['GBPUSD']['rate']
    USDZAR = currencies_dict['rates']['USDZAR']['rate']

    # Get timestamp values
    EURGBP_timestamp = currencies_dict['rates']['EURGBP']['timestamp']
    GBPUSD_timestamp = currencies_dict['rates']['GBPUSD']['timestamp']
    USDZAR_timestamp = currencies_dict['rates']['USDZAR']['timestamp']
    up_nearest_60 = ((EURGBP_timestamp+60-1)//60)*60

    table.put_item(
        Item={
            'base_symbol': 'EURGBP',
            'timestamp': str(EURGBP_timestamp),
            'timestamp_rounded': str(up_nearest_60),
            'date': str(datetime.today()),
            'value': str(EURGBP),
        }
    )

    table.put_item(
        Item={
            'base_symbol': 'GBPUSD',
            'timestamp': str(GBPUSD_timestamp),
            'timestamp_rounded': str(up_nearest_60),
            'date': str(datetime.today()),
            'value': str(GBPUSD),
        }
    )

    table.put_item(
        Item={
            'base_symbol': 'USDZAR',
            'timestamp': str(USDZAR_timestamp),
            'timestamp_rounded': str(up_nearest_60),
            'date': str(datetime.today()),
            'value': str(USDZAR),
        }
    )

def put_items_loop(repetitions):
    for i in range(repetitions):
        put_items()
        time.sleep(30)

def table_scan():
    # Instantiate a table resource object
    table = dynamodb.Table('exchangeRates')

    response = table.scan()
    items = response['Items']
    print(items)

delete_table()
time.sleep(10)
create_table()
put_items_loop(12)
print('Successfully retrieved currency values!')