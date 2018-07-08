import datetime
import json

import boto3

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

    def test_get_connector(self, model_valid, mock_ddb_table):
        model_valid.update({'created': datetime.datetime.utcnow().isoformat(),
                            'updated': datetime.datetime.utcnow().isoformat()})
        boto3.resource('dynamodb').Table('connectors').get_item.return_value = {'Item': model_valid}
        response = aws.get({'pathParameters': {'id': model_valid['connector_id']}})
        assert response['statusCode'] == '200'
        assert response['body']
        body = json.loads(response['body'])
        assert domain.validate_uuid(body['connector_id'])
        assert domain.validate_date_format(body['created'])
        assert domain.validate_date_format(body['updated'])
