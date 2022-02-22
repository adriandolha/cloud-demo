from authlib.jose import JsonWebKey
from functools import lru_cache

from flask import current_app as app
from flask import Blueprint
from lorem_ipsum.serializers import to_json, from_json
from flask import request
import lorem_ipsum
import logging
import uuid
import sys
import json
from prometheus_client import Metric

books = Blueprint('books', __name__)
users = Blueprint('users', __name__)
from flask import g

LOGGER = logging.getLogger('lorem-ipsum')


def response(api_response):
    return app.response_class(response=api_response['body'], status=api_response['status_code'])


@lru_cache()
def get_jwk():
    LOGGER.debug('Loading jwk from public key...')
    key_data = None
    with open(app_context().config['jwk_public_key_path'], 'rb') as _key_file:
        key_data = _key_file.read()
    LOGGER.debug(key_data)
    key = JsonWebKey.import_key(key_data, {'kty': 'RSA'})
    _jwks = {'keys': [{**key.as_dict(), 'kid': 'demo_key'}]}
    LOGGER.debug(_jwks)
    return _jwks


def requires_permission(permissions: list):
    def requires_permission_decorator(function):
        def wrapper(*args, **kwargs):
            LOGGER.info(f'Authorization...\n{request.headers}')
            user_service = app_context().user_service
            access_token = request.headers.get('X-Token-String')
            if not access_token:
                authorization_header = request.headers.get('Authorization')
                if not authorization_header:
                    return response({'body': to_json('Forbidden.'), 'status_code': '403'})
                access_token = authorization_header.split('Bearer')[1].strip()

            payload = user_service.decode_auth_token(access_token, get_jwk())
            LOGGER.debug(payload)
            user_permissions = payload.get('roles', [])
            payload_scope = payload.get('scope')
            if payload_scope:
                user_permissions = payload_scope.split()
            LOGGER.debug(f'Required: {permissions} Actual: {user_permissions}')
            if not set(permissions).issubset(user_permissions):
                return response({'body': to_json('Forbidden.'), 'status_code': '403'})
            _result = function(*args, **kwargs)
            return _result

        wrapper.__name__ = function.__name__
        return wrapper

    return requires_permission_decorator


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


@books.route('/health', methods=['GET'])
def health():
    LOGGER.debug('Checking system health...')
    return response({'body': 'all_good', 'status_code': '200'})


@books.route('/metrics', methods=['GET'])
def metrics():
    fields = request.args.get('fields')
    if fields is None:
        fields = ''
    LOGGER.debug('Metrics...')
    return response({'body': raw_metrics(fields), 'status_code': '200'})


def raw_metrics(fields=''):
    LOGGER.debug('Metrics...')
    _metrics = {}
    try:
        _metrics = to_json(lorem_ipsum.create_app_context().metrics_service.metrics(fields.split(',')))
    except:
        e = sys.exc_info()[0]
        LOGGER.exception('Could not get metrics...')
        print(e)
    return _metrics


@books.route('/<id>', methods=['GET'])
@requires_permission(['ROLE_ADMIN'])
def get_book(id):
    LOGGER.info('Get all data...')
    result = app_context().book_service.get(id)
    return response({"status_code": '200', 'body': to_json(result)})


@books.route('/', methods=['GET', 'OPTIONS'])
def get_all_books():
    _limit = int(request.args.get('limit', 20))
    _offset = int(request.args.get('offset', 1))
    LOGGER.info(f'Get all data [limit={_limit}, offset=[{_offset}]]...')
    result = app_context().book_service.get_all(limit=_limit, offset=_offset)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@books.route('/random', methods=['GET', 'OPTIONS'])
def random_book():
    no_of_pages = int(request.args.get('no_of_pages', 1))
    LOGGER.info(f'Generate book, no_of_pages=[{no_of_pages}]]...')
    result = app_context().book_service.random(no_of_pages=no_of_pages)
    return response({"status_code": '200', 'body': to_json(result)})


@books.route('/', methods=['POST'])
@requires_permission(['ROLE_ADMIN'])
def save_book():
    LOGGER.info('Adding data...')
    _request = from_json(request.data.decode('utf-8'))
    result = app_context().book_service.save(_request)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@books.route('/config', methods=['GET'])
def get_config():
    LOGGER.info(app.config)
    LOGGER.info(request.headers)
    public_config = {k: v for (k, v) in app_context().config.items() if 'password' not in k}
    return response({"status_code": '200', 'body': to_json(public_config)})


@books.route('/<id>', methods=['DELETE'])
@requires_permission(['ROLE_ADMIN'])
def delete_user(id: str):
    LOGGER.info(f'Delete book {id}...')
    app_context().book_service.delete(id)
    return '', 204


@users.route('/<username>', methods=['GET'])
def get_user(username):
    LOGGER.info('Get user...')
    result = app_context().user_service.get(username)
    return response({"status_code": '200', 'body': to_json(result)})


@users.route('/', methods=['GET'])
def get_all_users():
    LOGGER.info('Get all users...')
    LOGGER.info(request.headers)
    _limit = int(request.args.get('limit', 1))
    result = app_context().user_service.get_all(limit=_limit)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@users.route('/validate', methods=['POST'])
def validate_user():
    LOGGER.info('Validating user...')
    _request = from_json(request.data.decode('utf-8'))
    result = app_context().user_service.validate(_request)
    return response({"status_code": '200', 'body': to_json(result)})


def app_context():
    if 'app_context' not in g:
        g.app_context = lorem_ipsum.create_app_context()
    return g.app_context


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


@books.after_request
def apply_cors(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
