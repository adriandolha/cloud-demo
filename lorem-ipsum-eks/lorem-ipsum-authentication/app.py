import logging
import sys
import threading
import uuid
from authlib.jose import JsonWebKey
from authlib.jose import JWK_ALGORITHMS
from flask import Flask
import json
from authlib.jose import jwt

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
    LOGGER.info('Metrics...')
    metrics = {}
    try:
        thread_count = 0
        for thread in threading.enumerate():
            thread_count += 1
        metrics = {'thread_count': thread_count}
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
    LOGGER.debug('JWK...')
    _token = new_token()
    print(_token)
    LOGGER.debug(_token)
    return response({"status_code": '200', 'body': json.dumps({'token': _token})})


def get_jwk():
    LOGGER.debug('Loading jwk from public key...')
    key_data = None
    with open('/jwk/certs/public.pem', 'r') as _key_file:
        key_data = _key_file.read()
    _jwk = JsonWebKey(JWK_ALGORITHMS)
    _key_dict = _jwk.dumps(key_data, kty='RSA', use='sig', alg='RS256',
                           kid="demo_key")
    return {'keys': [_key_dict]}


def new_token():
    with open('/jwk/certs/private.pem', 'rb') as f:
        key = f.read()

    payload = {'iss': 'Authlib', 'sub': '123', 'role': 'admin'}
    header = {'alg': 'RS256', 'kid': 'demo_key'}
    token = jwt.encode(header, payload, key)
    return token.decode('utf-8')
