import logging
import os
import faker
import boto3
import flask
import pytest
import mock
# from mock import mock

import lorem_ipsum
from lorem_ipsum.serializers import to_json
import bcrypt


@pytest.fixture()
def config_valid():
    import json
    with open(f"{os.path.expanduser('~')}/.cloud-projects/lorem-ipsum-local.json", "r") as _file:
        _config = dict(json.load(_file))
        print(_config)
        for k, v in _config.items():
            os.environ[k] = str(v)
    lorem_ipsum.create_app()
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.setLevel(logging.DEBUG)
    return _config


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
def book_valid_add_request(book_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        book_valid = book_valid
        flask.request.data = to_json([book_valid]).encode('utf-8')
        yield book_valid


@pytest.fixture()
def metrics_request_with_fields(config_valid):
    import app
    with app.app.test_request_context():
        flask.request.args = {'fields': 'connections,threads'}
        yield flask.request.args


@pytest.fixture()
def metrics_request_no_fields(config_valid):
    import app
    with app.app.test_request_context():
        flask.request.args = {'fields': 'connections,threads'}
        yield flask.request.args


@pytest.fixture()
def user_valid_list_one_request(user_valid1):
    # from flask import request
    import app
    with app.app.test_request_context():
        flask.request.data = to_json([user_valid1]).encode('utf-8')
        yield user_valid1
        app.app_context().user_service.delete(user_valid1['username'])


@pytest.fixture()
def user_valid_list_request(user_valid2, config_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        app.app_context().user_service.save([user_valid2])
        flask.request.data = to_json([user_valid2]).encode('utf-8')
        yield user_valid2
        app.app_context().user_service.delete(user_valid2['username'])


@pytest.fixture()
def user_valid_list_default_limit(user_valid2, user_valid1, config_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        app.app_context().user_service.save([user_valid1])
        app.app_context().user_service.save([user_valid2])

        flask.request.args = {}
        yield user_valid2
        app.app_context().user_service.delete(user_valid1['username'])
        app.app_context().user_service.delete(user_valid2['username'])


@pytest.fixture()
def book_valid_get_request(config_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        flask.request.args = {'limit': '2'}
        yield book_valid


@pytest.fixture()
def book_valid_get_default_limit(config_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        flask.request.args = {}
        yield book_valid
