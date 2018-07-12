import json
import uuid

import boto3

from connection.api import ConnectorRestApi
from connection.domain import validate_uuid
from connection.serializers import to_json, from_json


class TestConnectorApi:
    def test_get_connector_not_found(self, mock_ddb_table):
        boto3.resource('dynamodb').Table('connectors').get_item.return_value = {'status_code': '200'}
        connector_id = str(uuid.uuid4())
        response = ConnectorRestApi({'path_parameters': {'id': connector_id}}).get()
        assert response['status_code'] == '404'
        assert response['body'] == json.dumps(f'Resource {connector_id} not found.')

    def test_add_connector_valid(self, mock_ddb_table, model_new):
        response = ConnectorRestApi({'body': to_json(model_new)}).add()
        assert response['status_code'] == '200'
        assert validate_uuid(from_json(response['body'])['connector_id'])

    def test_add_connector_when_connector_id_provided(self, mock_ddb_table, model_valid):
        response = ConnectorRestApi({'body': to_json(model_valid)}).add()
        assert response['status_code'] == '412'
        assert 'Expected empty' in from_json(response['body'])
