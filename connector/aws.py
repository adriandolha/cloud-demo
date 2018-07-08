from connector.api import ConnectorRestApi


def response(api_response):
    return {
        'statusCode': api_response['status_code'],
        'body': api_response['body']
    }


def add(event, context=None):
    return response(ConnectorRestApi().add(event['body']))


def get(event, context=None):
    print(event)
    print(context)
    return response(ConnectorRestApi().get(event['pathParameters'].get('id')))
