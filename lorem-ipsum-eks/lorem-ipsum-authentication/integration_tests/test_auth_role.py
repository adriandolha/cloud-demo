import requests

from lorem_ipsum_auth.serializers import to_json, from_json


class TestRole:
    def test_role_add(self, config_valid, admin_access_token, role_editor_valid):
        _response = requests.delete(url=f'{config_valid["root_url"]}/api/auth/roles/{role_editor_valid["name"]}',
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': f'Bearer {admin_access_token}'}, timeout=5,
                                    data=to_json(role_editor_valid).encode('utf-8'))
        assert _response.status_code == 204
        _response = requests.post(url=f'{config_valid["root_url"]}/api/auth/roles',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': f'Bearer {admin_access_token}'}, timeout=5,
                                  data=to_json(role_editor_valid).encode('utf-8'))
        print(_response.content)
        assert _response.status_code == 200
        data = from_json(_response.content.decode('utf-8'))
        assert data['name'] == role_editor_valid['name']
        assert len(data['permissions']) == 4
        assert data['permissions'] == role_editor_valid['permissions']

    def test_role_get(self, config_valid, admin_access_token, role_admin_valid):
        _response = requests.get(url=f'{config_valid["root_url"]}/api/auth/roles/{role_admin_valid["name"]}',
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': f'Bearer {admin_access_token}'}, timeout=5)
        assert _response.status_code == 200
        data = from_json(_response.content.decode('utf-8'))
        assert data['name'] == role_admin_valid['name']
        assert len(data['permissions']) == 5
        assert data['permissions'] == role_admin_valid['permissions']

    def test_get_roles(self, config_valid, admin_access_token, role_admin_valid):
        _response = requests.get(url=f'{config_valid["root_url"]}/api/auth/roles',
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': f'Bearer {admin_access_token}'}, timeout=5)
        assert _response.status_code == 200
        data = from_json(_response.content.decode('utf-8'))
        assert data['total'] > 1
        assert data['total'] == len(data['items'])
        _role = data['items'][0]
        assert _role.get('name')
        assert _role.get('permissions')
