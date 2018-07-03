import json

from connector.metadata.app import ConnectorService


def response(message, status_code):
    return {
        'statusCode': str(status_code),
        'body': json.dumps(message)
    }


def create_connector(event, context=None):
    print(event)
    print(context)
    return response(ConnectorService().add(json.loads(event['body'])), 200)
