import json
import logging
import uuid

import boto3
import pytest
import requests

from connection.service import ConnectionService


class TestConnectionAWS:
    """
    It requires terraform scripts to be applied and the infrastructure online.
    Deployment scripts can be found in templates/aws/connection
    """

    @pytest.fixture
    def setup(self):
        logging.basicConfig(level=logging.DEBUG)

    # @pytest.mark.skip(reason='Run it only on demand')
    def test_add_connection(self, model_new, api_url, basic_headers):
        add_response = requests.post(api_url, data=json.dumps(model_new), headers=basic_headers)
        assert add_response.status_code == 200
        body = json.loads(add_response.content)
        connection_id = body.get('connection_id')
        assert connection_id
        url = f'{api_url}/{connection_id}'
        response = requests.get(str(url), headers=basic_headers)
        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'name', 'instance_type' in content
        assert model_new['name'] == content['name']

    @pytest.mark.skip(reason='Run it only on demand')
    def test_get_connection_not_found(self, api_url, basic_headers):
        connection_id = '99999999-547b-4f0d-8034-00000000000'
        url = f'{api_url}/{connection_id}'
        response = requests.get(url, headers=basic_headers)
        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'name', 'instance_type' in content

    @pytest.mark.skip(reason='Run it only on demand')
    def test_playground(self):
        # ConnectionService().get(str(uuid.uuid4()))
        print(ConnectionService().list())

    @pytest.fixture(scope='module')
    def basic_headers(self, api_key):
        return {
            'Content-Type': 'application/json',
            'x-api-key': api_key
        }

    @pytest.fixture(scope='module')
    def api_url(self, api_id):
        region = 'us-east-1'
        stage = 'test'
        resource = 'connection'
        api_url = f'https://{api_id}.execute-api.{region}.amazonaws.com/{stage}/{resource}'
        print(f'API url is {api_url}')
        return api_url

    @pytest.fixture(scope='module')
    def api_client(self):
        return boto3.client('apigateway')

    @pytest.fixture(scope='module')
    def api_id(self, api_client):
        apis = api_client.get_rest_apis()
        rest_api_id = [item['id'] for item in apis['items'] if item['name'] == 'connection'][0]
        return rest_api_id

    @pytest.fixture(scope='module')
    def api_key(self, api_client):
        key_id = None
        key_name = 'mykey'
        keys = api_client.get_api_keys()
        for item in keys['items']:
            if item['name'] == key_name:
                key_id = item['id']
        if not key_id:
            raise ValueError(f'Could not find api key {key_name}')
        return api_client.get_api_key(apiKey=key_id, includeValue=True)['value']
