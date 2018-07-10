import datetime
import json

import boto3
import pytest as pytest

from connection import aws
from connection import domain


class TestConnectorAWS:
    def test_add_connector(self, model_new, mock_ddb_table):
        request = {'body': json.dumps(model_new)}
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

    def test_list_connectors(self, model_valid, mock_ddb_table):
        model_valid.update({'created': datetime.datetime.utcnow().isoformat(),
                            'updated': datetime.datetime.utcnow().isoformat()})
        boto3.resource('dynamodb').Table('connectors').scan.return_value = {'Items': [model_valid, model_valid]}
        response = aws.list({})
        assert response['statusCode'] == '200'
        assert response['body']
        body = json.loads(response['body'])
        assert body.get('items')
        assert len(body['items']) == 2
        assert body['count'] == 2
        item = body['items'][0]
        assert domain.validate_uuid(item['connector_id'])
        assert domain.validate_date_format(item['created'])
        assert domain.validate_date_format(item['updated'])

    def test_delete_connector(self, model_valid, mock_ddb_table):
        model_valid.update({'created': datetime.datetime.utcnow().isoformat(),
                            'updated': datetime.datetime.utcnow().isoformat()})
        response = aws.delete({'pathParameters': {'id': model_valid['connector_id']}})
        assert response['statusCode'] == '200'
        assert response['body']
        body = json.loads(response['body'])
        assert 'Successfully removed' in body
        args_list = boto3.resource('dynamodb').delete_item.call_args_list
        assert args_list
        args, kwargs = args_list[-1]
        assert kwargs['Key']['connector_id'] == model_valid['connector_id']
        assert kwargs['TableName'] == 'connectors'

    @pytest.mark.skip(reason='In progress')
    def test_delete_connector_not_found(self, model_valid, mock_ddb_table):
        model_valid.update({'created': datetime.datetime.utcnow().isoformat(),
                            'updated': datetime.datetime.utcnow().isoformat()})
        response = aws.delete({'pathParameters': {'id': model_valid['connector_id']}})
        assert response['statusCode'] == '404'
        assert response['body']
        body = json.loads(response['body'])
        assert 'Resource not found' in body
