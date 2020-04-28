import json
import boto3

# Get the service resource
sqs = boto3.resource('sqs')

def read_message():
    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='storeCurrencyData')
    
    # Set basic message_body value
    message_body = 'Start stream:'
    
    # Process messages by printing out body and optional author name
    for message in queue.receive_messages(MessageAttributeNames=['Author']):
        # Get the custom author message attribute if it was set
        author_text = ''
        if message.message_attributes is not None:
            author_name = message.message_attributes.get('Author').get('StringValue')
            if author_name:
                author_text = ' ({0})'.format(author_name)
    
        # Print out the body and author (if set)
        print('Hello, {0}!{1}'.format(message.body, author_text))
        
        # Save message body to return variable
        message_body = message.body
    
        # Let the queue know that the message is processed
        message.delete()
        
    return message_body
        
def send_sqs(message):
    # Get the service resource
    sqs = boto3.resource('sqs')
    
    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='storeCurrencyData')
    
    # Create a new message
    response = queue.send_message(MessageBody=message, MessageAttributes={
        'Author': {
            'StringValue': 'Benjanimm',
            'DataType': 'String'
        }
    })

def lambda_handler(event, context):
    # TODO implement
    previous_message_body = read_message()
    event_message_body = event['Records'][0]['body']
    combined_message_bodies = previous_message_body + '\n' + event_message_body
    send_sqs(combined_message_bodies)
    return {
        'statusCode': 200,
        'body': 'Function executed successfully!'
    }
