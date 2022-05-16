from datetime import datetime

import uuid

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
def request_valid_admin(admin_token_valid, user_admin_valid):
    import app
    with mock.patch("lorem_ipsum.repo.PostgresUserRepo.get"):
        lorem_ipsum.repo.PostgresUserRepo.get.return_value = lorem_ipsum.model.User.from_dict(user_admin_valid)
        with app.app.test_request_context(headers={'X-Token-String': admin_token_valid}):
            yield


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
           "owner_id": "admin"
           }


@pytest.fixture()
def book_valid_request():
    _faker = faker.Faker()
    _book = {f'page_{page}': [_faker.text(max_nb_chars=100) for i in range(30)] for page in range(10)}
    yield {"author": _faker.name(),
           "title": _faker.text(max_nb_chars=5),
           "book": to_json(_book),
           "no_of_pages": 10,
           }


@pytest.fixture()
def book_valid_user():
    _faker = faker.Faker()
    _book = {f'page_{page}': [_faker.text(max_nb_chars=100) for i in range(30)] for page in range(10)}
    yield {"author": _faker.name(),
           "title": _faker.text(max_nb_chars=5),
           "book": to_json(_book),
           "no_of_pages": 10,
           "owner_id": "user"
           }


@pytest.fixture()
def book_small_valid():
    _book = {f'page_{page}': ["Just a sample page." for i in range(1)] for page in range(1)}
    yield {'id': str(uuid.uuid4()),
           "author": "My Author",
           "title": "My Book",
           "owner_id": "system",
           "book": to_json(_book),
           "no_of_pages": 10,
           }


@pytest.fixture()
def book_words_valid():
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
           "password_hash": 'fake_admin_password',
           "email": "test_user1@yahoo.com",
           "login_type": "basic",
           "role_id": 1,
           "id": 1
           }


@pytest.fixture()
def user_admin_valid():
    yield {"username": 'admin',
           "password_hash": 'fake_admin_password',
           "email": "admin@yahoo.com",
           "login_type": "basic",
           "role_id": 1,
           "id": 1
           }


@pytest.fixture()
def user_valid2():
    yield {"username": 'test_user2',
           "password_hash": 'fake_admin_password',
           "email": "test_user2@yahoo.com",
           "login_type": "basic",
           "role_id": 1,
           "id": 1
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
def user_valid_list_one_request(user_valid1, request_valid_admin):
    import app
    import lorem_ipsum.views as api
    flask.request.data = to_json([user_valid1]).encode('utf-8')
    lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.first.return_value = lorem_ipsum.repo.User(
        **user_valid1)
    yield user_valid1
    # print(lorem_ipsum.repo.Transaction.session.mock_calls)
    api.app_context().user_service.delete(user_valid1['username'])


@pytest.fixture()
def get_user_valid_request(user_valid1):
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
def book_valid_add_request(book_valid, book_valid_request, admin_token_valid, request_valid_admin):
    # from flask import request
    import app

    # book_valid = book_valid
    lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.first.return_value = lorem_ipsum.repo.Book(
        **book_valid)
    flask.request.data = to_json([book_valid_request]).encode('utf-8')
    yield book_valid


@pytest.fixture()
def book_valid_add_request_user(book_valid, book_valid_user, admin_token_valid):
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
def book_add_request_options_method_no_auth(book_valid, user_token_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        book_valid = book_valid
        flask.request.method = 'OPTIONS'
        yield book_valid

@pytest.fixture()
def book_valid_get_request(app_valid, book_valid, request_valid_admin):
    # from flask import request
    import app
    flask.request.args = {'limit': '2'}
    lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
    lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.limit.return_value.offset.return_value = [
        lorem_ipsum.repo.Book(**book_valid), lorem_ipsum.repo.Book(**book_valid)]
    yield book_valid


@pytest.fixture()
def book_valid_get_request_user(app_valid, book_valid, book_valid_user, admin_token_valid, user_admin_valid):
    # from flask import request
    import app
    from lorem_ipsum import model
    from lorem_ipsum.repo import Book, User
    with app.app.test_request_context(headers={'X-Token-String': admin_token_valid}):
        flask.request.args = {'limit': '2'}
        orig_query = lorem_ipsum.repo.Transaction.session.query.return_value

        def query_side_effect(args):
            # print(f'Mock {args}')
            if args == Book:
                lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
                lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.limit.return_value.offset.return_value = [
                    lorem_ipsum.repo.Book(**book_valid)
                ]

            if args == User:
                lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.first.return_value = \
                    lorem_ipsum.repo.User(**user_admin_valid)
            return orig_query

        lorem_ipsum.repo.Transaction.session.query.side_effect = query_side_effect

        yield book_valid


@pytest.fixture()
def book_random_valid_get_request(app_valid, admin_token_valid, user_admin_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        with app.app.test_request_context(headers={'X-Token-String': admin_token_valid}):
            lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.first.return_value = lorem_ipsum.repo.User(
                **user_admin_valid)
            flask.request.args = {'no_of_pages': '3'}
            yield ''


@pytest.fixture()
def page_count_valid_get_request(app_valid, book_valid, request_valid_admin):
    # from flask import request
    import app
    flask.request.args = {'limit': '2', 'includes': 'page_count'}
    lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
    lorem_ipsum.repo.Transaction.session.query.return_value.scalar.return_value = 10
    lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.limit.return_value.offset.return_value = [
        lorem_ipsum.repo.Book(**book_valid), lorem_ipsum.repo.Book(**book_valid)]
    yield book_valid


@pytest.fixture()
def book_valid_get_request_limit_offset(app_valid, book_valid, request_valid_admin):
    # from flask import request
    import app
    flask.request.args = {'limit': '3', 'offset': '4'}
    lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
    lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.limit.return_value.offset.return_value = [
        lorem_ipsum.repo.Book(**book_valid), lorem_ipsum.repo.Book(**book_valid)]
    yield book_valid


@pytest.fixture()
def book_valid_get_default_limit(app_valid, book_valid, request_valid_admin):
    # from flask import request
    import app
    flask.request.args = {}
    lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
    lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.limit.return_value.offset.return_value = [
        lorem_ipsum.repo.Book(**book_valid)]
    yield book_valid


@pytest.fixture()
def word_valid():
    _faker = faker.Faker()
    name = _faker.word()
    yield {"id": name,
           "name": name,
           "count": _faker.random_int(1, 50),
           }


@pytest.fixture()
def word_valid_max():
    _faker = faker.Faker()
    name = _faker.word()
    yield {"id": name,
           "name": 'wirdwrddfskjlfjsdlk',
           "count": 100000,
           }


@pytest.fixture()
def word_valid_add_request(word_valid, admin_token_valid, request_valid_admin):
    # from flask import request
    import app
    lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.first.return_value = lorem_ipsum.repo.Word(
        **word_valid)
    lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
    lorem_ipsum.repo.Transaction.session.query.return_value.order_by.return_value.limit.return_value.offset.return_value = [
        lorem_ipsum.repo.Word(**word_valid), lorem_ipsum.repo.Word(**word_valid)]
    flask.request.data = to_json([word_valid]).encode('utf-8')
    yield word_valid


@pytest.fixture()
def stats_top_words_valid_request(word_valid, admin_token_valid):
    # from flask import request
    import app
    with app.app.test_request_context(headers={'X-Token-String': admin_token_valid}):
        # book_valid = book_valid
        lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.first.return_value = lorem_ipsum.repo.Word(
            **word_valid)
        lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
        lorem_ipsum.repo.Transaction.session.query.return_value.limit.return_value.offset.return_value = [
            lorem_ipsum.repo.Word(**word_valid), lorem_ipsum.repo.Word(**word_valid)]
        flask.request.data = to_json([word_valid]).encode('utf-8')
        yield word_valid


@pytest.fixture()
def word_valid_get_request_limit_offset(app_valid, word_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        flask.request.args = {'limit': '3', 'offset': '4'}
        lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
        lorem_ipsum.repo.Transaction.session.query.return_value \
            .order_by.return_value \
            .limit.return_value \
            .offset.return_value = [
            lorem_ipsum.repo.Word(**word_valid), lorem_ipsum.repo.Word(**word_valid)]
        yield word_valid


@pytest.fixture()
def word_valid_get_default_limit(app_valid, word_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        flask.request.args = {}
        lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 3
        lorem_ipsum.repo.Transaction.session.query.return_value.order_by.return_value.limit.return_value.offset.return_value = [
            lorem_ipsum.repo.Word(**word_valid)]
        yield book_valid


@pytest.fixture()
def app_context(config_valid):
    yield lorem_ipsum.create_app_context()


@pytest.fixture()
def book_updated_event_valid(app_context, book_small_valid):
    from lorem_ipsum import model
    from lorem_ipsum.repo import Word, Event
    event_repo = app_context.event_repo

    event = model.Event(id=event_repo.next_id(), name=str(model.Events.BOOK_UPDATED),
                        data=to_json({'new': to_json(book_small_valid)}), created_at=datetime.utcnow())
    _event_entity = lorem_ipsum.repo.Event(**event.as_dict())
    orig_query = lorem_ipsum.repo.Transaction.session.query.return_value

    def query_side_effect(args):
        # print(f'Mock {args}')
        if args == Event:
            orig_query.count.return_value = 1
            orig_query.filter.return_value.first.return_value = _event_entity
            orig_query.filter.return_value.limit.return_value.offset.return_value = [_event_entity]
        if args == Word:
            index = {
                book_small_valid['id']: 1
            }
            orig_query.filter.return_value.order_by.return_value = [lorem_ipsum.repo.Word(id=word,
                                                                                          name=word,
                                                                                          index=to_json(index),
                                                                                          count=1)
                                                                    for word in ['just', 'a', 'sample', 'page']]
        return orig_query

    lorem_ipsum.repo.Transaction.session.query.side_effect = query_side_effect
    # lorem_ipsum.repo.Transaction.session.query.return_value.count.return_value = 1
    # lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.first.return_value = _event_entity
    # lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.limit.return_value.offset.return_value = [
    #     _event_entity]
    # with mock.patch('lorem_ipsum.repo.Transaction._session_maker'):

    yield event
