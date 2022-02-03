import requests
from requests.auth import HTTPBasicAuth

from lorem_ipsum_auth.serializers import to_json, from_json


class TestJWT:
    def test_register(self, config_valid, user_valid1):
        _response = requests.post(url=f'{config_valid["root_url"]}/auth/register',
                                  headers={'Content-Type': 'application/json'}, timeout=3,
                                  data=to_json(user_valid1).encode('utf-8'))
        print(_response.content)
        assert _response.status_code == 200
        _response_data = from_json(_response.content.decode('utf-8'))
        print(_response_data)
        assert _response_data['access_token']

    def test_login(self, config_valid):
        _response = requests.get(url=f'{config_valid["root_url"]}/auth/login',
                                 headers={'Content-Type': 'application/json'}, timeout=3,
                                 auth=HTTPBasicAuth(config_valid['guest_user'], config_valid['guest_password']))
        print(_response.content)
        assert _response.status_code == 200
        _response_data = from_json(_response.content.decode('utf-8'))
        print(_response_data)
        assert _response_data['access_token']

    def test_profile(self, config_valid, user_access_token):
        _response = requests.get(url=f'{config_valid["root_url"]}/auth/profile',
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': f'Bearer {user_access_token}'}, timeout=3)
        assert _response.status_code == 200
        _response_data = from_json(_response.content.decode('utf-8'))
        assert _response_data['username'] == 'guest'

    def test_get_user(self, config_valid, admin_access_token):
        _response = requests.get(url=f'{config_valid["root_url"]}/users/guest',
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': f'Bearer {admin_access_token}'}, timeout=3)
        assert _response.status_code == 200
        _response_data = from_json(_response.content.decode('utf-8'))
        assert _response_data['username'] == 'guest'

    def test_logout(self, config_valid, admin_access_token_logout):
        _response = requests.get(url=f'{config_valid["root_url"]}/auth/logout',
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': f'Bearer {admin_access_token_logout}'}, timeout=3)
        assert _response.status_code == 200
        assert from_json(_response.content.decode('utf-8')) == 'Logged out.'
