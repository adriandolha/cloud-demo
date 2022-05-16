import json
import os

os.environ['env'] = 'test'
import lorem_ipsum.views as app


class TestUserApi:
    def test_user_list_one(self, config_valid, get_user_valid_request):
        app.app_context().user_service.save([get_user_valid_request])
        response = app.get_user(get_user_valid_request['username'])
        user = json.loads(response.response[0].decode('utf-8'))
        print(user)
        assert user['username'] == get_user_valid_request['username']
        assert 200 == response.status_code

    def test_user_list_count(self, user_valid_list_request):
        response = app.get_all_users()
        users = json.loads(response.response[0].decode('utf-8'))
        print(users)
        assert users['total']
        assert len(users['items']) == 1
        assert 200 == response.status_code

    def test_user_list_default_limit(self, user_valid_list_default_limit):
        response = app.get_all_users()
        users = json.loads(response.response[0].decode('utf-8'))
        print(users)
        assert users['total'] > 2
        assert len(users['items']) == 1
        assert 200 == response.status_code
