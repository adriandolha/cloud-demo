import logging
import os
import pytest
import mock


@pytest.fixture(scope='session')
def config_valid():
    import json
    with open(f"{os.path.expanduser('~')}/.cloud-projects/lorem-ipsum-local-integration.json", "r") as _file:
        json = dict(json.load(_file))
        print(json)
        for k, v in json.items():
            os.environ[k] = str(v)
        os.environ['db_setup'] = 'False'
        yield os.environ


@pytest.fixture()
def db_session(config_valid):
    with mock.patch('flask_sqlalchemy.SQLAlchemy.get_app'):
        with mock.patch('flask_sqlalchemy.SQLAlchemy.get_engine'):
            with mock.patch('flask_sqlalchemy.SQLAlchemy.create_session'):
                with mock.patch('flask_sqlalchemy.SignallingSession'):
                    with mock.patch('flask_sqlalchemy.SQLAlchemy.create_scoped_session'):
                        yield


@pytest.fixture()
def query_mock(db_session):
    with mock.patch('flask_sqlalchemy._QueryProperty.__get__') as q_mock:
        with mock.patch('lorem_ipsum_auth.repo.Transaction._db'):
            from lorem_ipsum_auth.repo import Transaction
            Transaction._db = None
            with mock.patch('lorem_ipsum_auth.repo.Transaction._session_maker'):
                with mock.patch('lorem_ipsum_auth.repo.Transaction.session'):
                    with mock.patch('lorem_ipsum_auth.repo.Transaction.pool'):
                        from lorem_ipsum_auth.models import User, Role, Permission, BlacklistToken
                        User.query = mock.MagicMock()
                        Role.query = mock.MagicMock()
                        Permission.query = mock.MagicMock()
                        BlacklistToken.query = mock.MagicMock()

                        def _filter_by(*args, **kwargs):
                            _mock = mock.MagicMock()
                            _mock.first.return_value = Permission.from_str(kwargs['name'])
                            return _mock

                        Permission.query.filter_by.side_effect = _filter_by
                        BlacklistToken.query.filter_by.return_value.first.return_value = None
                        yield q_mock


@pytest.fixture()
def login_valid_request(query_mock, user_admin_valid, role_admin_valid):
    from lorem_ipsum_auth.models import User, Role, Permission

    Role.query.filter_by.return_value.first.return_value = Role(id=role_admin_valid['id'],
                                                                name=role_admin_valid['name'],
                                                                permissions=[Permission.from_str(perm) for perm in
                                                                             role_admin_valid['permissions']])
    User.query.filter_by.return_value.filter_by.return_value.first.return_value = User.from_dict(
        user_admin_valid)
    User.query.filter_by.return_value.first.return_value = User.from_dict(
        user_admin_valid)
    yield user_admin_valid


@pytest.fixture()
def signup_valid_request(query_mock, user_admin_valid, role_admin_valid):
    from lorem_ipsum_auth.models import User, Role, Permission
    Role.query.filter_by.return_value.first.return_value = Role(id=role_admin_valid['id'],
                                                                name=role_admin_valid['name'],
                                                                permissions=[Permission.from_str(perm) for perm in
                                                                             role_admin_valid['permissions']])
    User.query.filter_by.return_value.first.return_value = None
    yield user_admin_valid


@pytest.fixture()
def app(db_session):
    import lorem_ipsum_auth.app
    app = lorem_ipsum_auth.app.create_flask_app()
    LOGGER = logging.getLogger('lorem-ipsum-auth')
    LOGGER.setLevel(logging.DEBUG)
    app.config.update({
        "TESTING": True,
    })
    # yield app
    with app.test_request_context():
        yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def user_admin_valid():
    import werkzeug.security
    yield {"username": 'admin',
           "password_hash": werkzeug.security.generate_password_hash('fake_admin_password'),
           "email": "admin@yahoo.com",
           "login_type": "basic",
           "role_id": 1,
           "id": 1
           }


@pytest.fixture(scope='session')
def user_valid():
    import werkzeug.security
    yield {"username": 'admin',
           "password_hash": werkzeug.security.generate_password_hash('fake_admin_password'),
           "email": "admin@yahoo.com",
           "login_type": "basic",
           "role_id": 2,
           "id": 2
           }


@pytest.fixture()
def role_user_valid():
    yield {
        "name": "ROLE_USER",
        "id": 2,
        "permissions": ['books:add', 'books:read', 'books:write', 'users:profile']
    }


@pytest.fixture()
def role_admin_valid():
    yield {
        "name": "ROLE_USER",
        "id": 2,
        "permissions": ['books:add', 'books:read', 'books:write', 'users:profile', 'users:admin']
    }
