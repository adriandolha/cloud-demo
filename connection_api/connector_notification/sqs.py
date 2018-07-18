import boto3

sqs = boto3.client('sqs')

queue_url = 'https://sqs.us-east-1.amazonaws.com/856816586042/connection_dev_myapp'


def publish(event):
    sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Author': {
                'DataType': 'String',
                'StringValue': 'Adrian Dolha'
            }
        },
        MessageBody=event
    )


def receive():
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    if response:
        if 'Messages' in response:
            return response['Messages']
        else:
            return [response]
    return None


def delete(message, logger=None):
    if message and 'ReceiptHandle' in message:
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
    else:
        print('Could not delete ')
        print(message)
