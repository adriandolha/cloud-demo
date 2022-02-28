import os

import faker
import pytest

from lorem_ipsum.serializers import to_json


@pytest.fixture()
def config_valid():
    import json
    config_file = f"{os.path.expanduser('~')}/.cloud-projects/lorem-ipsum-local-integration.json"
    print(f'Config file is {config_file}')
    if os.path.exists(config_file):
        with open(config_file, "r") as _file:
            _config = dict(json.load(_file))
            print(_config)
            for k, v in _config.items():
                os.environ[k] = str(v)
    else:
        _config = os.environ
    return _config


@pytest.fixture()
def admin_token_valid(config_valid):
    yield os.getenv('admin_token')


@pytest.fixture()
def user_token_valid(config_valid):
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


@pytest.fixture
def requests_standard_settings(config_valid):
    return {"headers": {'Content-Type': 'application/json',
                        'Authorization': f"Bearer {config_valid['admin_token']}"}, "timeout": 10}


@pytest.fixture
def requests_user_token_settings(config_valid):
    return {"headers": {'Content-Type': 'application/json',
                        'X-Token-String': config_valid['user_token']}, "timeout": 10}


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
    yield {"id": 'wirdwrddfskjlfjsdlk',
           "name": 'wirdwrddfskjlfjsdlk',
           "count": 100000,
           }
