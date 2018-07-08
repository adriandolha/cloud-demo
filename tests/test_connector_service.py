import uuid

import boto3
import pytest

from connector import make_repo
from connector.exceptions import ResourceNotFoundException
from connector.service import ConnectorService


class TestConnectorService:
    def test_repo_is_cached(self, model_valid, mock_ddb_table):
        assert make_repo() == make_repo()

    def test_get_not_found(self, mock_ddb_table):
        boto3.resource('dynamodb').Table('connectors').get_item.return_value = {'status_code': '200'}
        with pytest.raises(ResourceNotFoundException):
            ConnectorService().get(str(uuid.uuid4()))

    def test_repo_called_with_entity(self, model_new, mock_ddb_table):
        ConnectorService().add(model_new)
        mock_table = boto3.resource('dynamodb').Table('connectors')
        args_list = mock_table.put_item.call_args_list
        assert args_list[-1]
        args, kwargs = args_list[-1]
        assert kwargs['Item']['client'] == 'my client'
