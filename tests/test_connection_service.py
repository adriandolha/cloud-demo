import uuid

import boto3
import pytest

from connection import make_repo
from connection.domain import validate_date_format
from connection.exceptions import ResourceNotFoundException
from connection.service import ConnectorService


class TestConnectorService:
    def test_repo_is_cached(self, model_valid, mock_ddb_table):
        assert make_repo() == make_repo()

    def test_add_connector_metadata(self, model_new, mock_ddb_table):
        ConnectorService().add(model_new)
        args, kwargs = boto3.resource('dynamodb').Table('connections').put_item.call_args_list[-1]
        metadata = kwargs['Item'].get('metadata')
        assert metadata
        validate_date_format(metadata['created'])
        validate_date_format(metadata['updated'])

    def test_repo_table_name(self, model_valid, mock_ddb_table):
        ConnectorService().delete(model_valid['connector_id'])
        args, kwargs = boto3.resource('dynamodb').delete_item.call_args_list[-1]
        assert kwargs['TableName'] == 'connections'

    def test_get_not_found(self, mock_ddb_table):
        boto3.resource('dynamodb').Table('connections').get_item.return_value = {'status_code': '200'}
        with pytest.raises(ResourceNotFoundException):
            ConnectorService().get(str(uuid.uuid4()))

    def test_repo_called_with_entity(self, model_new, mock_ddb_table):
        ConnectorService().add(model_new)
        mock_table = boto3.resource('dynamodb').Table('connections')
        args_list = mock_table.put_item.call_args_list
        assert args_list[-1]
        args, kwargs = args_list[-1]
        assert kwargs['Item']['client'] == 'my client'
