from flask import current_app as app, jsonify
from flask import Blueprint

from lorem_ipsum.model import Permissions, BookViews
from lorem_ipsum.serializers import to_json, from_json
from flask import request
import lorem_ipsum
from lorem_ipsum.auth import requires_permission
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
stats = Blueprint('stats', __name__)
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
@requires_permission([Permissions.BOOKS_READ])
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


@stats.route('/', methods=['GET'])
@requires_permission([Permissions.USERS_ADMIN])
def get_stats():
    """
        Get stats, e.g. total no of books, pages and words
        ---
        definitions:
          - schema:
              id: Stats
              properties:
                no_of_books:
                 type: integer
                 description: no of books
                no_of_pages:
                 type: integer
                 description: no of pages
                no_of_words:
                 type: integer
                 description: no of pages
        parameters:
            - in: header
              name: X-Token-String
              required: true
              type: string
              description: Access token JWT.
        responses:
                200:
                    description: Stats ok
                    schema:
                        $ref: '#/definitions/Stats'
                401:
                    description: Authentication error
                403:
                    description: Authorization error
    """
    LOGGER.info('Get stats...')
    result = app_context().stats_service.get()
    return response({"status_code": '200', 'body': to_json(result)})


@books.route('/', methods=['GET', 'OPTIONS'])
@requires_permission([Permissions.BOOKS_READ])
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
            - in: query
              name: view
              description: Books view: my_books, shared_books
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
    _view = BookViews.from_value(request.args.get('view', BookViews.MY_BOOKS.value))

    _includes = request.args.get('includes')
    LOGGER.info(f'Get all data [limit={_limit}, offset=[{_offset}], view={_view}]...')
    result = app_context().book_service.get_all(limit=_limit, offset=_offset, includes=_includes,
                                                owner_id=g.user.username, view=_view)
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
@requires_permission([Permissions.BOOKS_READ])
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
@requires_permission([Permissions.BOOKS_ADD])
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


@books.route('/<id>/share', methods=['POST'])
@requires_permission([Permissions.BOOKS_READ])
def share_book(id):
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
              name: user
              required: true
              description: User to share book with
            - in: path
              name: id
              description: Unique id of the book to share
              required: true
              type: string
              schema:
                type: object
                properties:
                  username:
                    type: string
                    description: The user name.
        responses:
                204:
                    description: Book shared successfully
                    schema:
                        $ref: '#/definitions/BookPaginationResult'
                401:
                    description: Authentication error
                403:
                    description: Authorization error
    """

    LOGGER.info('Sharing book...')
    _request = from_json(request.data.decode('utf-8'))

    app_context().book_service.share_book_with_user(id, _request['username'])
    return '', 204


@words.route('/', methods=['POST'])
@requires_permission([Permissions.USERS_ADMIN])
def save_word():
    LOGGER.info('Adding data...')
    _request = from_json(request.data.decode('utf-8'))
    result = app_context().word_service.save(_request)
    return response({"status_code": '200', 'body': to_json({"items": result['items'], "total": result['total']})})


@words.route('/<id>', methods=['GET'])
@requires_permission([Permissions.USERS_ADMIN])
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
@requires_permission([Permissions.USERS_ADMIN])
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
@requires_permission([Permissions.BOOKS_WRITE])
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
