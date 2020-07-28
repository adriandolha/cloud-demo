import logging
import os
import sys
import uuid

import gevent_psycopg2
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
    fields = request.args.get('fields')
    if fields is None:
        fields = []

    LOGGER.info('Metrics...')
    metrics = {}
    try:
        metrics = to_json(app_context().metrics_service.metrics(fields.split(',')))
    except:
        e = sys.exc_info()[0]
        LOGGER.exception('Could not get metrics...')
        print(e)
    return response({'body': metrics, 'status_code': '200'})


@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    LOGGER.debug('Get all data...')
    result = app_context().book_service.get(id)
    return response({"status_code": '200', 'body': to_json(result)})


@app.route('/books', methods=['GET'])
def get_all_books():
    LOGGER.debug(app.config)

    LOGGER.debug('Get all data...')
    LOGGER.debug(request.headers)
    _limit = int(request.args.get('limit', 1))
    result = app_context().book_service.get_all(limit=_limit)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@app.route('/books', methods=['POST'])
def save_book():
    LOGGER.info('Adding data...')
    _request = from_json(request.data.decode('utf-8'))
    result = app_context().book_service.save(_request)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@app.route('/config', methods=['GET'])
def get_config():
    public_config = {k: v for (k, v) in app_context().config.items() if 'password' not in k}
    return response({"status_code": '200', 'body': to_json(public_config)})


@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    LOGGER.debug('Get user...')
    result = app_context().user_service.get(username)
    return response({"status_code": '200', 'body': to_json(result)})


@app.route('/users', methods=['GET'])
def get_all_users():
    LOGGER.debug('Get all users...')
    LOGGER.debug(request.headers)
    _limit = int(request.args.get('limit', 1))
    result = app_context().user_service.get_all(limit=_limit)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@app.route('/users/validate', methods=['POST'])
def validate_user():
    LOGGER.info('Validating user...')
    _request = from_json(request.data.decode('utf-8'))
    result = app_context().user_service.validate(_request)
    return response({"status_code": '200', 'body': to_json(result)})


def app_context():
    return lorem_ipsum.AppContext()


print(f'Name is {__name__}')


def prepare_orm_for_gevent():
    """
    In order to make psycopg2 work with gevent, we need to apply this patch, otherwise all worker connections will use
    only one connection which might cause serious issues in production.
    Also, the patch needs to be applied before creating the db engine.
    """
    gevent_psycopg2.monkey_patch()


if __name__ == "__main__" or __name__ == 'app' and os.getenv('env') != 'test':
    prepare_orm_for_gevent()
    lorem_ipsum.create_app()
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.debug(app.config)
