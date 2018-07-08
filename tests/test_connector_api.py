import json
import uuid

import boto3

from connector.api import ConnectorRestApi
from connector.domain import validate_uuid
from connector.serializers import to_json, from_json


class TestConnectorApi:
    def test_get_connector_not_found(self, mock_ddb_table):
        boto3.resource('dynamodb').Table('connectors').get_item.return_value = {'status_code': '200'}
        connector_id = str(uuid.uuid4())
        response = ConnectorRestApi().get(connector_id)
        assert response['status_code'] == '404'
        assert response['body'] == json.dumps(f'Resource {connector_id} not found.')

    def test_add_connector_valid(self, mock_ddb_table, model_new):
        response = ConnectorRestApi().add(to_json(model_new))
        assert response['status_code'] == '200'
        assert validate_uuid(from_json(response['body'])['connector_id'])
