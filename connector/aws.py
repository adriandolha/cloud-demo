import json

from connector.service import ConnectorService


def response(message, status_code):
    return {
        'statusCode': str(status_code),
        'body': json.dumps(message)
    }


def add(event, context=None):
    print(event)
    print(context)
    return response(ConnectorService().add(json.loads(event['body'])), 200)
