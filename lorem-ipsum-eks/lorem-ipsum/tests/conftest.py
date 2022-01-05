import logging
import os

import faker
import flask
import mock
import pytest

import lorem_ipsum
from lorem_ipsum.serializers import to_json


# from mock import mock


@pytest.fixture()
def db_session():
    with mock.patch('lorem_ipsum.repo.Transaction._db'):
        with mock.patch('lorem_ipsum.repo.Transaction._session_maker'):
            with mock.patch('lorem_ipsum.repo.Transaction.session'):
                with mock.patch('lorem_ipsum.repo.Transaction.pool'):
                    with mock.patch('lorem_ipsum.repo.TransactionManager.create_db_engine'):
                        yield


@pytest.fixture()
def config_valid(db_session):
    import json
    config_file = f"{os.path.expanduser('~')}/.cloud-projects/lorem-ipsum-local-unit.json"
    print(f'Config file is {config_file}')
    if os.path.exists(config_file):
        with open(config_file, "r") as _file:
            _config = dict(json.load(_file))
            for k, v in _config.items():
                os.environ[k] = str(v)
    else:
        _config = os.environ
    print('Config...')
    print(_config)
    return _config


@pytest.fixture()
def app_valid(config_valid, db_session):
    lorem_ipsum.create_app()
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.setLevel(logging.DEBUG)


@pytest.fixture()
def admin_token_valid(app_valid):
    yield os.getenv('admin_token')


@pytest.fixture()
def user_token_valid(app_valid):
    yield os.getenv('user_token')


@pytest.fixture()
def book_valid():
    _faker = faker.Faker()
    _book = {f'page_{page}': [_faker.text(max_nb_chars=100) for i in range(30)] for page in range(10)}
    yield {"author": _faker.name(),
           "title": _faker.text(max_nb_chars=5),
           "book": to_json(_book),
           "no_of_pages": 10,
           }


@pytest.fixture()
def user_valid1():
    yield {"username": 'test_user1',
           "password": 'pwd'
           }


@pytest.fixture()
def user_valid2():
    yield {"username": 'test_user2',
           "password": 'pwd'
           }


@pytest.fixture()
def config_valid_request(config_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        yield True


@pytest.fixture()
def metrics_request_with_fields(app_valid):
    import app
    with app.app.test_request_context():
        flask.request.args = {'fields': 'connections,threads'}
        _pool = lorem_ipsum.repo.Transaction.pool
        _pool.return_value._max_overflow = 50
        _pool.return_value._pool.maxsize = 50
        _pool.return_value._pool.queue = ['conn1']
        _pool.return_value.size.return_value = 30
        _pool.return_value.checkedin.return_value = 10
        _pool.return_value.checkedout.return_value = 10
        yield flask.request.args


@pytest.fixture()
def metrics_request_no_fields(app_valid):
    import app
    with app.app.test_request_context():
        _pool = lorem_ipsum.repo.Transaction.pool
        _pool.return_value._max_overflow = 50
        _pool.return_value._pool.maxsize = 50
        _pool.return_value.size.return_value = 30
        _pool.return_value.checkedin.return_value = 10
        _pool.return_value.checkedout.return_value = 10
        yield flask.request.args


@pytest.fixture()
def user_valid_list_one_request(user_valid1, app_valid):
    import app
    import lorem_ipsum.views as api
    with app.app.test_request_context():
        flask.request.data = to_json([user_valid1]).encode('utf-8')
        lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.first.return_value = lorem_ipsum.repo.User(
            **user_valid1)
        yield user_valid1
        # print(lorem_ipsum.repo.Transaction.session.mock_calls)
        api.app_context().user_service.delete(user_valid1['username'])


@pytest.fixture()
def user_valid_list_request(user_valid2, app_valid):
    import app
    import lorem_ipsum.views as api
    with app.app.test_request_context():
        api.app_context().user_service.save([user_valid2])
        flask.request.data = to_json([user_valid2]).encode('utf-8')
        lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 1
        lorem_ipsum.repo.Transaction.session.query.return_value.limit.return_value = [
            lorem_ipsum.repo.User(**user_valid2)]
        yield user_valid2
        api.app_context().user_service.delete(user_valid2['username'])


@pytest.fixture()
def user_valid_list_default_limit(user_valid2, user_valid1, app_valid):
    import lorem_ipsum.views as api
    import app

    with app.app.test_request_context():
        api.app_context().user_service.save([user_valid1])
        api.app_context().user_service.save([user_valid2])

        flask.request.args = {}
        lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
        lorem_ipsum.repo.Transaction.session.query.return_value.limit.return_value = [
            lorem_ipsum.repo.User(**user_valid1)]
        yield user_valid2
        api.app_context().user_service.delete(user_valid1['username'])
        api.app_context().user_service.delete(user_valid2['username'])


@pytest.fixture()
def book_valid_add_request(book_valid, admin_token_valid):
    # from flask import request
    import app
    with app.app.test_request_context(headers={'X-Token-String': admin_token_valid}):
        # book_valid = book_valid
        lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.first.return_value = lorem_ipsum.repo.Book(
            **book_valid)
        flask.request.data = to_json([book_valid]).encode('utf-8')
        yield book_valid


@pytest.fixture()
def book_add_request_insufficient_permissions(book_valid, user_token_valid):
    # from flask import request
    import app
    with app.app.test_request_context(headers={'X-Token-String': user_token_valid}):
        book_valid = book_valid
        flask.request.data = to_json([book_valid]).encode('utf-8')
        yield book_valid


@pytest.fixture()
def book_valid_get_request(app_valid, book_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        flask.request.args = {'limit': '2'}
        lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
        lorem_ipsum.repo.Transaction.session.query.return_value.limit.return_value = [
            lorem_ipsum.repo.Book(**book_valid), lorem_ipsum.repo.Book(**book_valid)]
        yield book_valid


@pytest.fixture()
def book_valid_get_default_limit(app_valid, book_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        flask.request.args = {}
        lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
        lorem_ipsum.repo.Transaction.session.query.return_value.limit.return_value = [
            lorem_ipsum.repo.Book(**book_valid)]
        yield book_valid
