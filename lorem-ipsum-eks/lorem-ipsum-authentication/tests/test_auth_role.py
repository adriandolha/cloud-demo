import json
import os

os.environ['env'] = 'test'


class TestAuthRole:
    def test_role_delete(self, client, config_valid, role_add_valid_request, user_admin_valid, role_editor_valid,
                         query_mock, admin_access_token):
        _response = client.delete(f'/api/auth/roles/{role_editor_valid["name"]}',
                                  headers={'Authorization': f'Bearer {admin_access_token}'})
        assert _response.status_code == 204

    def test_role_add(self, client, config_valid, role_add_valid_request, admin_access_token, role_editor_valid):
        _response = client.post('/api/auth/roles', json=role_editor_valid,
                                headers={'Authorization': f'Bearer {admin_access_token}'})
        assert _response.status_code == 200
        data = json.loads(_response.data.decode('utf-8'))
        print(data)
        assert data['name'] == role_editor_valid['name']
        assert len(data['permissions']) == 4
        assert data['permissions'] == role_editor_valid['permissions']

    def test_role_add_existing(self, client, config_valid, role_add_existing_request, user_admin_valid,
                               role_editor_valid,
                               query_mock, admin_access_token):
        _response = client.post('/api/auth/roles', json=role_editor_valid,
                                headers={'Authorization': f'Bearer {admin_access_token}'})
        assert _response.status_code == 400
        data = json.loads(_response.data.decode('utf-8'))
        assert data == 'Role already exists.'

    def test_role_add_permission_required(self, client, config_valid, role_add_existing_request, user_admin_valid,
                                          role_editor_valid, user_access_token,
                                          query_mock):
        _response = client.post('/api/auth/roles', json=role_editor_valid,
                                headers={'Authorization': f'Bearer {user_access_token}'})
        assert _response.status_code == 403

    def test_role_delete_permission_required(self, client, config_valid, role_add_existing_request, user_admin_valid,
                                             role_editor_valid, user_access_token,
                                             query_mock):
        _response = client.delete(f'/api/auth/roles/fake', json=role_editor_valid,
                                  headers={'Authorization': f'Bearer {user_access_token}'})
        assert _response.status_code == 403
