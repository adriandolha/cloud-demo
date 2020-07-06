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


@pytest.fixture()
def config_valid():
    import json
    with open(f"{os.path.expanduser('~')}/.cloud-projects/lorem-ipsum-local.json", "r") as _file:
        json = dict(json.load(_file))
        print(json)
        for k, v in json.items():
            os.environ[k] = str(v)
    lorem_ipsum.create_app()
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.setLevel(logging.DEBUG)


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
def book_valid_add_request(book_valid):
    # from flask import request
    import app
    with app.app.test_request_context():
        book_valid = book_valid
        flask.request.data = to_json([book_valid]).encode('utf-8')
        yield book_valid
