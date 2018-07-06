import json

from connector import aws
from connector import domain


class TestConnectorAWS:
    def test_add_connector(self, model_valid, mock_ddb_table):
        request = {'body': json.dumps(model_valid)}
        response = aws.add(request)
        assert response['statusCode'] == '200'
        assert response['body']
        body = json.loads(response['body'])
        assert domain.validate_uuid(body['connector_id'])
