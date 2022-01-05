import json
import os

import requests

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json, to_json
import app


class TestUserApi:
    def test_user_list_count(self, config_valid, basic_headers):
        response = requests.get(url=f'{config_valid["root_url"]}/users', headers=basic_headers)
        users = json.loads(response.content.decode('utf-8'))
        print(users)
        assert users['total']
        assert len(users['items']) == 1
        assert 200 == response.status_code