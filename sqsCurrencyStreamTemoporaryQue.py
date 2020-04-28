import requests
import boto3
from datetime import datetime

def get_latest_currency(base_list, symbols_list):
    
    ## api generic info:
    latest_url = 'http://data.fixer.io/api/latest'
    api_key = '?access_key=831d2e7d8cad1c85a9fda5a834cdcf64'
    currency_pairs = {}

    ## create currency request:
    base_string = ''
    symbols_string = ''
    for value in base_list:
        base_string += value +','
    for value in symbols_list:
        symbols_string += value +','
    historical_request_text = requests.get(latest_url + api_key + '&symbols=' + symbols_string + ',' + base_string).text

    ## calculate base value:
    for i in range(len(base_list)):

        #currency_pairs = {} # new dict to store results in

        if(base_list[i]=='EUR'):
            base_value = 1
        else:
            start = historical_request_text.find(base_list[i]) + 5
            end = start + 5
            base_value = float(historical_request_text[start:end])
        
        ## calculate symbol value for current base:
        for j in range(len(symbols_list)):
            if(symbols_list[j]=='EUR'):
                symbol_value = 1
            else:
                start = historical_request_text.find(symbols_list[j]) + 5
                end = start + 5
                symbol_value = float(historical_request_text[start:end])

            ## calculate symbol:base value:
            symbolbase_value = symbol_value/base_value
            # print(symbols_list[j] + ':' + base_list[i] + '=' + str(symbolbase_value))
            if (i == 0):
                currency_pairs[symbols_list[j]] = {base_list[i]:symbolbase_value}
            else:
                # currency_pairs['ZAR'].update({base_list[i]:symbolbase_value})
                currency_pairs[symbols_list[j]][base_list[i]] = symbolbase_value
            j += 1
        i += 1

    return currency_pairs

def send_sqs(message):
    # Get the service resource
    sqs = boto3.resource('sqs')
    
    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='temporaryHoldingQue')
    
    # Create a new message
    response = queue.send_message(MessageBody=message, MessageAttributes={
        'Author': {
            'StringValue': 'Daniel',
            'DataType': 'String'
        }
    })
    
    # The response is NOT a resource, but gives you a message ID and MD5
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))

def lambda_handler(event, context):
    get_latest_currency_return_dict = get_latest_currency(['EUR'], ['ZAR'])
    base_1 = get_latest_currency_return_dict['ZAR']['EUR']
    print(base_1)
    message = 'Currency value is: ' + str(base_1) + ' Time is: ' + str(datetime.today())
    send_sqs(message)

    return 'SQS successfully sent!'

