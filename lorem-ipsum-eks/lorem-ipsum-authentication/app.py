import logging
import os
import sys
import threading
import uuid
from authlib.jose import JsonWebKey
from authlib.jose import JWK_ALGORITHMS
from authlib.jose import jwt
from flask import Flask, request, g
import json
import gevent_psycopg2
import lorem_ipsum_auth
from lorem_ipsum_auth.serializers import to_json, from_json

app = Flask('lorem-ipsum-auth')
LOGGER = logging.getLogger('lorem-ipsum-auth')
LOGGER.setLevel(logging.DEBUG)


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


@app.route('/auth/health', methods=['GET'])
def health():
    LOGGER.info('Checking system health...')
    return response({'body': 'all_good', 'status_code': '200'})


@app.route('/auth/metrics', methods=['GET'])
def metrics():
    fields = request.args.get('fields')
    if fields is None:
        fields = ''

    LOGGER.info('Metrics...')
    metrics = {}
    try:
        metrics = to_json(app_context().metrics_service.metrics(fields.split(',')))
    except:
        e = sys.exc_info()[0]
        LOGGER.exception('Could not get metrics...')
        print(e)
    return response({'body': metrics, 'status_code': '200'})


@app.route('/auth/.well-known/jwks.json', methods=['GET'])
def jwk():
    LOGGER.debug('JWK...')
    key = get_jwk()
    print(key)
    LOGGER.debug(key)
    return response({"status_code": '200', 'body': json.dumps(key)})


@app.route('/auth/token', methods=['POST'])
def token():
    payload = json.loads(request.data.decode('utf-8'))
    LOGGER.debug(f'New access token with payload {payload}')
    _token = new_token(payload)
    LOGGER.debug(_token)
    return response({"status_code": '200', 'body': json.dumps({'access_token': _token})})


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
        g.app_context = lorem_ipsum_auth.AppContext()
    return g.app_context


print(f'Name is {__name__}')


def get_jwk():
    LOGGER.debug('Loading jwk from public key...')
    key_data = None
    with open('/jwk/certs/public.pem', 'r') as _key_file:
        key_data = _key_file.read()
    _jwk = JsonWebKey(JWK_ALGORITHMS)
    _key_dict = _jwk.dumps(key_data, kty='RSA', use='sig', alg='RS256',
                           kid="demo_key")
    return {'keys': [_key_dict]}


def new_token(payload: dict):
    with open('/jwk/certs/private.pem', 'rb') as f:
        key = f.read()
    header = {'alg': 'RS256', 'kid': 'demo_key'}
    token = jwt.encode(header, payload, key)
    return token.decode('utf-8')


def prepare_orm_for_gevent():
    """
    In order to make psycopg2 work with gevent, we need to apply this patch, otherwise all worker connections will use
    only one connection which might cause serious issues in production.
    Also, the patch needs to be applied before creating the db engine.
    """
    gevent_psycopg2.monkey_patch()


if __name__ == "__main__" or __name__ == 'app' and os.getenv('env') != 'test':
    prepare_orm_for_gevent()
    lorem_ipsum_auth.create_app()
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.debug(app.config)
