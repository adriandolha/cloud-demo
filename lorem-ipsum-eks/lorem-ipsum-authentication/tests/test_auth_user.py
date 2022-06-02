import json
import os

os.environ['env'] = 'test'


class TestAuthUser:
    def test_user_signin(self, client, config_valid, login_valid_request, user_admin_valid, role_admin_valid,
                         query_mock):
        _response = client.post('/api/auth/signin', json={'username': config_valid['admin_user'],
                                                          'password': config_valid['admin_password']})
        assert _response.status_code == 200
        data = json.loads(_response.data.decode('utf-8'))
        assert data['access_token']
        assert data['username'] == user_admin_valid['username']
        assert len(data['roles']) == 1
        assert role_admin_valid['name'] in data['roles']
        assert len(data['permissions']) == 5
        assert data['permissions'] == ['books:add', 'books:read', 'books:write', 'users:profile', 'users:admin']

    def test_user_signin_invalid_password(self, client, config_valid, login_valid_request, user_admin_valid,
                                          role_admin_valid, query_mock):
        _response = client.post('/api/auth/signin', json={'username': config_valid['admin_user'],
                                                          'password': 'wrong_password'})
        assert _response.status_code == 401
        data = json.loads(_response.data.decode('utf-8'))
        assert data == 'Invalid username or password'

    def test_user_signup(self, client, config_valid, signup_valid_request, user_admin_valid, role_admin_valid,
                         query_mock):
        _response = client.post('/api/auth/signup', json={'username': config_valid['admin_user'],
                                                          'email': user_admin_valid['email'],
                                                          'password': config_valid['admin_password']})
        assert _response.status_code == 200
        data = json.loads(_response.data.decode('utf-8'))
        assert data['access_token']
        assert data['username'] == user_admin_valid['username']
        assert len(data['roles']) == 1
        assert role_admin_valid['name'] in data['roles']

    def test_user_signup_user_already_registered(self, client, config_valid, login_valid_request, user_admin_valid,
                                                 role_admin_valid,
                                                 query_mock):
        _response = client.post('/api/auth/signup', json={'username': config_valid['admin_user'],
                                                          'password': config_valid['admin_password']})
        assert _response.status_code == 400
        data = json.loads(_response.data.decode('utf-8'))
        assert data == 'User already registered'
