import logging
import os
import boto3
import flask
import pytest
import mock
# from mock import mock

import lorem_ipsum_auth
from lorem_ipsum_auth.serializers import to_json


@pytest.fixture()
def config_valid():
    import json
    with open(f"{os.path.expanduser('~')}/.cloud-projects/lorem-ipsum-local.json", "r") as _file:
        json = dict(json.load(_file))
        print(json)
        for k, v in json.items():
            os.environ[k] = str(v)
    lorem_ipsum_auth.create_app()
    LOGGER = logging.getLogger('lorem-ipsum-auth')
    LOGGER.setLevel(logging.DEBUG)


@pytest.fixture()
def app():
    app = lorem_ipsum_auth.create_app()
    LOGGER = logging.getLogger('lorem-ipsum-auth')
    LOGGER.setLevel(logging.DEBUG)
    return app


@pytest.fixture()
def admin_token_valid(config_valid):
    yield os.getenv('admin_token')


@pytest.fixture()
def user_token_valid(config_valid):
    yield os.getenv('user_token')


@pytest.fixture()
def user_valid1():

    yield {"username": 'test_user1',
           "password": 'pwd',
           "email": "test_user1@gmail.com"
           }


@pytest.fixture()
def user_valid2():
    yield {"username": 'test_user2',
           "password": 'pwd'
           }


@pytest.fixture()
def valid_user_token():
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
def metrics_request_with_fields(config_valid):
    import app
    with app.app.test_request_context():
        flask.request.args = {'fields': 'connections,threads'}
        yield flask.request.args


@pytest.fixture()
def metrics_request_no_fields(config_valid):
    import app
    with app.app.test_request_context():
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
