import json
import os

import requests

os.environ['env'] = 'test'


class TestUserApi:
    def test_user_list_count(self, config_valid, requests_standard_settings):
        response = requests.get(url=f'{config_valid["root_url"]}/users', **requests_standard_settings)
        users = json.loads(response.content.decode('utf-8'))
        print(users)
        assert users['total']
        assert len(users['items']) == 1
        assert 200 == response.status_code