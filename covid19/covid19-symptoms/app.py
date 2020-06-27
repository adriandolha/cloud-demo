import logging
import os
import uuid

from flask import Flask, request

import covid19_symptoms
from covid19_symptoms.serializers import to_json, from_json

app = Flask('C19')
LOGGER = logging.getLogger('c19')


def response(api_response):
    return app.response_class(response=api_response['body'], status=api_response['status_code'])


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


@app.route('/symptoms/health', methods=['GET'])
def health():
    LOGGER.info('Checking system health...')
    return response({'body': 'all_good', 'status_code': '200'})


@app.route('/symptoms/<id>', methods=['GET'])
def get(id):
    LOGGER.debug('Get all data...')
    result = app_context().symptom_service.get(id)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@app.route('/symptoms', methods=['GET'])
def get_all():
    LOGGER.debug('Get all data...')
    result = app_context().symptom_service.get()
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@app.route('/symptoms', methods=['POST'])
def save():
    LOGGER.info('Adding data...')
    _request = from_json(request.data.decode('utf-8'))
    result = app_context().symptom_service.save(_request)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


def app_context():
    return covid19_symptoms.AppContext()


if __name__ == 'app' and os.getenv('env') != 'test':
    covid19_symptoms.create_app()
    LOGGER = logging.getLogger('c19')
