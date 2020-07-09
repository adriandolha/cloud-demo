import logging
import os
import sys
import uuid

from flask import Flask, request

import lorem_ipsum
from lorem_ipsum.serializers import to_json, from_json

app = Flask('lorem-ipsum')
LOGGER = logging.getLogger('lorem-ipsum')


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


@app.route('/books/health', methods=['GET'])
def health():
    LOGGER.info('Checking system health...')
    return response({'body': 'all_good', 'status_code': '200'})


@app.route('/books/metrics', methods=['GET'])
def metrics():
    LOGGER.info('Metrics...')
    metrics = {}
    try:
        metrics = to_json(app_context().metrics_service.metrics())
    except:
        e = sys.exc_info()[0]
        LOGGER.exception('Could not get metrics...')
        print(e)
    return response({'body': metrics, 'status_code': '200'})


@app.route('/books/<id>', methods=['GET'])
def get(id):
    LOGGER.debug('Get all data...')
    result = app_context().book_service.get(id)
    return response({"status_code": '200', 'body': to_json(result)})


@app.route('/books', methods=['GET'])
def get_all():
    LOGGER.debug('Get all data...')
    _limit = int(request.args.get('limit', 1))
    result = app_context().book_service.get_all(limit=_limit)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@app.route('/books', methods=['POST'])
def save():
    LOGGER.info('Adding data...')
    _request = from_json(request.data.decode('utf-8'))
    result = app_context().book_service.save(_request)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


def app_context():
    return lorem_ipsum.AppContext()


print(f'Name is {__name__}')
if __name__ == 'app' and os.getenv('env') != 'test':
    lorem_ipsum.create_app()
    LOGGER = logging.getLogger('lorem-ipsum')
