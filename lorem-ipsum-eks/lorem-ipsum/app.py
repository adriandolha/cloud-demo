import json
import logging
import os
import time

import sys
import uuid

import gevent_psycopg2
from flask import Flask, request
from flask import g
import lorem_ipsum
from lorem_ipsum.serializers import to_json, from_json
from prometheus_flask_exporter import PrometheusMetrics

app = Flask('lorem-ipsum')

LOGGER = logging.getLogger('lorem-ipsum')
from prometheus_client import make_wsgi_app, start_http_server, REGISTRY, Metric
from wsgiref.simple_server import make_server
from prometheus_client import CollectorRegistry, generate_latest, multiprocess


def response(api_response):
    return app.response_class(response=api_response['body'], status=api_response['status_code'])


def requires_role(roles: list):
    def requires_role_decorator(function):
        def wrapper(*args, **kwargs):
            LOGGER.debug(request.headers)
            user_service = app_context().user_service
            payload = user_service.decode_auth_token(request.headers['X-Token-String'])
            LOGGER.debug(payload)
            user_roles = payload.get('roles', [])
            LOGGER.debug(user_roles)
            if not set(roles).issubset(user_roles):
                return response({'body': to_json('Forbidden.'), 'status_code': '403'})
            _result = function(*args, **kwargs)
            return _result

        return wrapper

    return requires_role_decorator


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
        fields = ''
    LOGGER.info('Metrics...')
    return response({'body': raw_metrics(fields), 'status_code': '200'})


def raw_metrics(fields=''):
    LOGGER.info('Metrics...')
    _metrics = {}
    try:
        _metrics = to_json(lorem_ipsum.create_app_context().metrics_service.metrics(fields.split(',')))
    except:
        e = sys.exc_info()[0]
        LOGGER.exception('Could not get metrics...')
        print(e)
    return _metrics


@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    LOGGER.debug('Get all data...')
    result = app_context().book_service.get(id)
    return response({"status_code": '200', 'body': to_json(result)})


@app.route('/books', methods=['GET'])
def get_all_books():
    LOGGER.debug('Get all data...')
    _limit = int(request.args.get('limit', 1))
    result = app_context().book_service.get_all(limit=_limit)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@app.route('/books', methods=['POST'])
@requires_role(['admin'])
def save_book():
    LOGGER.info('Adding data...')
    _request = from_json(request.data.decode('utf-8'))
    result = app_context().book_service.save(_request)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@app.route('/config', methods=['GET'])
def get_config():
    LOGGER.debug(app.config)
    LOGGER.debug(request.headers)
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
    if 'app_context' not in g:
        g.app_context = lorem_ipsum.AppContext()
    return g.app_context


print(f'Name is {__name__}')


def prepare_orm_for_gevent():
    """
    In order to make psycopg2 work with gevent, we need to apply this patch, otherwise all worker connections will use
    only one connection which might cause serious issues in production.
    Also, the patch needs to be applied before creating the db engine.
    """
    gevent_psycopg2.monkey_patch()


class JsonCollector(object):
    def __init__(self):
        pass

    def collect(self):
        _raw_metrics = raw_metrics()
        LOGGER.debug(_raw_metrics)
        _metrics = json.loads(_raw_metrics)
        # Convert requests and duration to a summary in seconds
        _metric = Metric('lorem_ipsum_metric',
                         'Requests time taken in seconds', 'summary')
        _metric.add_sample('lorem_ipsum_connection_pool_maxconn',
                           value=_metrics['connection_pool.maxconn'], labels={})
        _metric.add_sample('lorem_ipsum_connection_pool_usedconn',
                           value=_metrics['connection_pool.usedconn'], labels={})
        _metric.add_sample('lorem_ipsum_connection_pool_rusedconn',
                           value=_metrics['connection_pool.rusedconn'], labels={})
        _metric.add_sample('lorem_ipsum_connection_pool_size',
                           value=_metrics['connection_pool.size'], labels={})
        _metric.add_sample('lorem_ipsum_thread_count',
                           value=_metrics['thread_count'], labels={})
        yield _metric


def start_prometheus_metrics():
    start_http_server(int('8082'))
    REGISTRY.register(JsonCollector())
    while True:
        time.sleep(1)


if __name__ == "__main__" or __name__ == 'app' and os.getenv('env') != 'test':
    prepare_orm_for_gevent()
    lorem_ipsum.create_app()
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.debug(app.config)
    _prometheus_metrics = PrometheusMetrics(app=None)
    _prometheus_metrics.init_app(app)
    REGISTRY.register(JsonCollector())
    # start_prometheus_metrics()
