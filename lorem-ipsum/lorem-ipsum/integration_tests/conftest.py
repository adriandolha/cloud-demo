import os

import faker
import pytest
import requests
from lorem_ipsum.serializers import to_json


@pytest.fixture(scope="session")
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

    def get_access_token(credentials: dict):
        _response = requests.post(url='https://localhost/api/auth/signin',
                                  data=to_json(credentials), verify=False)
        return json.loads(_response.content.decode('utf-8'))['access_token']

    _config['admin_token'] = get_access_token(
        {'username': _config['admin_user'], 'password': _config['admin_password']})
    _config['user_token'] = get_access_token({'username': _config['guest_user'], 'password': _config['guest_password']})

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
def requests_standard_settings(config_valid, admin_token_valid):
    return {"headers": {'Content-Type': 'application/json',
                        'Authorization': f"Bearer {admin_token_valid}"}, "timeout": 10}


@pytest.fixture()
def user_moderator_valid():
    yield {"username": 'moderator',
           "password_hash": 'fake_moderator',
           "email": "moderator@yahoo.com",
           "login_type": "basic",
           "role": {"id": 2, "name": "user", "default": False, "users": [],
                    "permissions": [{"id": "users:profile", "name": "users:profile", "roles": []},
                                    {"id": "books:read", "name": "books:read", "roles": []}]},
           "id": 1
           }


@pytest.fixture()
def user_valid():
    yield {"username": 'guest',
           "password_hash": 'fake_user',
           "email": "guest@yahoo.com",
           "login_type": "basic",
           "role": {"id": 2, "name": "user", "default": False, "users": [],
                    "permissions": [{"id": "users:profile", "name": "users:profile", "roles": []},
                                    {"id": "books:read", "name": "books:read", "roles": []},
                                    {"id": "books:add", "name": "books:add", "roles": []}]
                    },
           "id": 1
           }


@pytest.fixture()
def user_token_valid(config_valid, user_valid):
    from lorem_ipsum.auth import issue_token_for_user
    from lorem_ipsum.model import User
    yield issue_token_for_user(User.from_dict(user_valid))


@pytest.fixture()
def moderator_token_valid(config_valid, user_moderator_valid):
    from lorem_ipsum.auth import issue_token_for_user
    from lorem_ipsum.model import User
    yield issue_token_for_user(User.from_dict(user_moderator_valid))


@pytest.fixture
def requests_user_token_settings(config_valid, user_token_valid):
    return {"headers": {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {user_token_valid}'}, "timeout": 10}


@pytest.fixture
def requests_moderator_token_settings(config_valid, moderator_token_valid):
    return {"headers": {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {moderator_token_valid}'}, "timeout": 10}


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
