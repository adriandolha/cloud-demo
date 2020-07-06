import logging
import uuid

import covid19_symptoms
from covid19_symptoms.serializers import to_json, from_json

LOGGER = logging.getLogger('symptoms')


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
    LOGGER.info(f'event = {event}')
    LOGGER.info(f'context={context}')
    data = app_context().symptom_service.save(from_json(event['body']))
    return response({"status_code": '200', 'body': to_json(data)})


def get(event, context=None):
    LOGGER.info(f'event = {event}')
    LOGGER.info(f'context={context}')
    query_params = event.get('queryStringParameters')
    id = None
    if query_params is not None and query_params.get('id') is not None:
        id = query_params['id']
    result = app_context().symptom_service.get(id)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


def app_context():
    return covid19_symptoms.AppContext()