import json

from connector.metadata.app import MetadataService
from connector.metadata.model import Metadata


def response(message, status_code):
    return {
        'statusCode': str(status_code),
        'body': json.dumps(message)
    }


def create_metadata(event, context=None):
    print(event)
    print(context)
    body = json.loads(event['body'])
    return response(MetadataService().add(Metadata(**body)), 200)
