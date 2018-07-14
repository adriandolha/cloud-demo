import json
import uuid

import boto3

from connection.api import ConnectionRestApi
from connection.domain import validate_uuid
from connection.serializers import to_json, from_json


class TestConnectionApi:
    def test_get_connection_not_found(self, mock_ddb_table):
        boto3.resource('dynamodb').Table('connections').get_item.return_value = {'status_code': '200'}
        connection_id = str(uuid.uuid4())
        response = ConnectionRestApi({'path_parameters': {'id': connection_id}}).get()
        assert response['status_code'] == '404'
        assert response['body'] == json.dumps(f'Resource {connection_id} not found.')

    def test_add_connection_valid(self, mock_ddb_table, model_new):
        response = ConnectionRestApi({'body': to_json(model_new)}).add()
        assert response['status_code'] == '200'
        assert validate_uuid(from_json(response['body'])['connection_id'])

    def test_add_connection_when_connection_id_provided(self, mock_ddb_table, model_valid):
        response = ConnectionRestApi({'body': to_json(model_valid)}).add()
        assert response['status_code'] == '412'
        assert 'Expected empty' in from_json(response['body'])
