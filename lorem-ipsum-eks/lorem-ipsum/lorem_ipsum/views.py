from authlib.jose import JsonWebKey
from functools import lru_cache

from flask import current_app as app, jsonify
from flask import Blueprint
from lorem_ipsum.serializers import to_json, from_json
from flask import request
import lorem_ipsum
import logging
import uuid
import sys
import json
from prometheus_client import Metric
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

books = Blueprint('books', __name__)
words = Blueprint('words', __name__)
users = Blueprint('users', __name__)
from flask import g

LOGGER = logging.getLogger('lorem-ipsum')

swaggerui_blueprint = get_swaggerui_blueprint('/books/docs', '/books/spec')


@books.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['base'] = "http://localhost:5000"
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Lorem Ipsum"
    return jsonify(swag)


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


def should_skip_auth(flask_request):
    """
    Return true if should skip auth, e.g. when method is OPTIONS like when performing a React request.
    :param flask_request: Flask request.
    :return:
    """
    return flask_request.method in ['HEAD', 'OPTIONS']


def requires_permission(permissions: list):
    def requires_permission_decorator(function):
        def wrapper(*args, **kwargs):
            if should_skip_auth(request):
                return jsonify('ok')
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
            username = payload.get('sub')
            if not username:
                LOGGER.debug(f'Payload sub not found.')

                return response({'body': to_json('Forbidden.'), 'status_code': '403'})

            user = user_service.get(username)
            if not user:
                LOGGER.debug(f'User {username} not found.')
                return response({'body': to_json('Forbidden.'), 'status_code': '403'})
            g.user = lorem_ipsum.model.User.from_dict(user)
            _result = function(*args, **kwargs)
            return _result

        wrapper.__name__ = function.__name__
        wrapper.__doc__ = function.__doc__
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
    """
        Get book
        ---
        definitions:
          - schema:
              id: Book
              properties:
                id:
                 type: string
                 description: book id (uuid)
                no_of_pages:
                 type: integer
                 description: Number of pages
                author:
                  type: string
                  description: book author full name
                title:
                  type: string
                  description: book title
                book:
                  type: string
                  description: book content as JSON containing a list of pages
        parameters:
            - in: header
              name: X-Token-String
              required: true
              type: string
              description: Access token JWT.
            - in: path
              name: id
              description: Unique id of the book
              required: true
              type: string
        responses:
                200:
                    description: Book found
                    schema:
                        $ref: '#/definitions/Book'
                401:
                    description: Authentication error
                403:
                    description: Authorization error
    """
    LOGGER.info('Get all data...')
    result = app_context().book_service.get(id)
    return response({"status_code": '200', 'body': to_json(result)})


@books.route('/', methods=['GET', 'OPTIONS'])
@requires_permission(['ROLE_ADMIN'])
def get_all_books():
    """
        Get books
        ---
        definitions:
          - schema:
              id: BookPaginationResult
              type: object
              properties:
                total:
                  type: integer
                  description: Total number of items.
                items:
                  type: array
                  description: List of books
                  items:
                    oneOf:
                      - $ref: "#/definitions/Book"
        parameters:
            - in: header
              name: X-Token-String
              required: true
              type: string
              description: Access token JWT.
            - in: query
              name: limit
              description: Limit the number of items returned
              type: integer
            - in: query
              name: offset
              description: Offset of items result
              type: integer
            - in: query
              name: includes
              description: List of fields to include, separated by comma
              type: string
        responses:
                200:
                    description: List of books
                    schema:
                        $ref: '#/definitions/BookPaginationResult'
                401:
                    description: Authentication error
                403:
                    description: Authorization error
    """
    _limit = int(request.args.get('limit', 20))
    _offset = int(request.args.get('offset', 1))
    _includes = request.args.get('includes')
    LOGGER.info(f'Get all data [limit={_limit}, offset=[{_offset}]]...')
    result = app_context().book_service.get_all(limit=_limit, offset=_offset, includes=_includes,
                                                owner_id=g.user.username)
    return response({"status_code": '200', 'body': to_json(result)})


@books.route('/search', methods=['GET', 'OPTIONS'])
def search_books_by_query():
    """
        Search books
        ---
        parameters:
            - in: header
              name: X-Token-String
              required: true
              type: string
              description: Access token JWT.
            - in: query
              name: limit
              description: Limit the number of items returned
              type: integer
            - in: query
              name: offset
              description: Offset of items result
              type: integer
            - in: query
              name: query
              description: Search query, e.g. word to search for
              type: string
        responses:
                200:
                    description: List of books
                    schema:
                        $ref: '#/definitions/BookPaginationResult'
                401:
                    description: Authentication error
                403:
                    description: Authorization error
    """

    _limit = int(request.args.get('limit', 20))
    _offset = int(request.args.get('offset', 1))
    _query = request.args.get('query', '')
    LOGGER.info(f'Get all data [limit={_limit}, offset=[{_offset}], _query=[{_query}]]...')
    result = app_context().book_service.search(query=_query)
    return response({"status_code": '200', 'body': to_json(result)})


@books.route('/random', methods=['GET', 'OPTIONS'])
@requires_permission(['ROLE_ADMIN'])
def random_book():
    """
        Generate random book
        ---
        parameters:
            - in: header
              name: X-Token-String
              required: true
              type: string
              description: Access token JWT.
            - in: query
              name: no_of_paged
              description: Limit the number of items returned
              type: integer
        responses:
                200:
                    description: Random book
                    schema:
                        $ref: '#/definitions/Book'
                401:
                    description: Authentication error
                403:
                    description: Authorization error
    """

    no_of_pages = int(request.args.get('no_of_pages', 1))
    LOGGER.info(f'Generate book, no_of_pages=[{no_of_pages}]]...')
    result = app_context().book_service.random(no_of_pages=no_of_pages, owner_id=g.user.username)
    return response({"status_code": '200', 'body': to_json(result)})


@books.route('/', methods=['POST'])
@requires_permission(['ROLE_ADMIN'])
def save_book():
    """
        Save books
        ---
        parameters:
            - in: header
              name: X-Token-String
              required: true
              type: string
              description: Access token JWT.
            - in: body
              name: books
              required: true
              description: List of Books to be created
              schema:
                type: array
                items:
                  oneOf:
                    - $ref: "#/definitions/Book"
        responses:
                200:
                    description: List of books created
                    schema:
                        $ref: '#/definitions/BookPaginationResult'
                401:
                    description: Authentication error
                403:
                    description: Authorization error
    """

    LOGGER.info('Adding data...')
    _request = from_json(request.data.decode('utf-8'))
    for _book in _request:
        _book['owner_id'] = g.user.username
    result = app_context().book_service.save(_request)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@words.route('/', methods=['POST'])
@requires_permission(['ROLE_ADMIN'])
def save_word():
    LOGGER.info('Adding data...')
    _request = from_json(request.data.decode('utf-8'))
    result = app_context().word_service.save(_request)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@words.route('/<id>', methods=['GET'])
@requires_permission(['ROLE_ADMIN'])
def get_word(id):
    """
        Get word
        ---
        definitions:
          - schema:
              id: Word
              properties:
                id:
                 type: string
                 description: word id (same as word name at this point)
                count:
                 type: integer
                 description: Word frequency
                index:
                  type: string
                  description: Word index
                name:
                  type: string
                  description: Word name, could be different than id
        parameters:
            - in: header
              name: X-Token-String
              required: true
              type: string
              description: Access token JWT.
            - in: path
              name: id
              description: Unique id of the word
              required: true
              type: string
        responses:
                200:
                    description: Word found
                    schema:
                        $ref: '#/definitions/Word'
                401:
                    description: Authentication error
                403:
                    description: Authorization error
    """

    LOGGER.info('Get all data...')
    result = app_context().word_service.get(id)
    return response({"status_code": '200', 'body': to_json(result)})


@words.route('/', methods=['GET', 'OPTIONS'])
def get_all_words():
    _limit = int(request.args.get('limit', 20))
    _offset = int(request.args.get('offset', 1))
    LOGGER.info(f'Get all data [limit={_limit}, offset=[{_offset}]]...')
    result = app_context().word_service.get_all(limit=_limit, offset=_offset)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@words.route('/<id>', methods=['DELETE'])
@requires_permission(['ROLE_ADMIN'])
def delete_word(id: str):
    """
        Delete word
        ---
        parameters:
            - in: header
              name: X-Token-String
              required: true
              type: string
              description: Access token JWT.
            - in: path
              name: id
              description: Unique id of the word
              required: true
              type: string
        responses:
                204:
                    description: Word deleted
                401:
                    description: Authentication error
                403:
                    description: Authorization error
    """

    LOGGER.info(f'Delete word {id}...')
    app_context().word_service.delete(id)
    return '', 204


@books.route('/config', methods=['GET'])
def get_config():
    LOGGER.info(app.config)
    LOGGER.info(request.headers)
    public_config = {k: v for (k, v) in app_context().config.items() if 'password' not in k}
    return response({"status_code": '200', 'body': to_json(public_config)})


@books.route('/<id>', methods=['DELETE'])
@requires_permission(['ROLE_ADMIN'])
def delete_book(id: str):
    """
        Delete book
        ---
        parameters:
            - in: header
              name: X-Token-String
              required: true
              type: string
              description: Access token JWT.
            - in: path
              name: id
              description: Unique id of the book
              required: true
              type: string
        responses:
                204:
                    description: Book deleted
                401:
                    description: Authentication error
                403:
                    description: Authorization error
    """

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
@words.after_request
def apply_cors(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
