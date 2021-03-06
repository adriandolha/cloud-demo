import uuid

from connection.api import ConnectionRestApi


def response(api_response):
    return {
        'statusCode': api_response['status_code'],
        'body': api_response['body']
    }


def api_context(event, context):
    if not event:
        event = {}
    if not context:
        context = {}
    return {
        'user_id': str(uuid.uuid4()),
        'body': event.get('body') or {},
        'path_parameters': event.get('pathParameters') or {}
    }


def add(event, context=None):
    return response(ConnectionRestApi(api_context(event, context)).add())


def get(event, context=None):
    print(event)
    print(context)
    return response(ConnectionRestApi(api_context(event, context)).get())


def list(event, context=None):
    return response(ConnectionRestApi(api_context(event, context)).list())


def delete(event, context=None):
    return response(ConnectionRestApi(api_context(event, context)).delete())