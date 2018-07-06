import boto3
import pytest
from mock import mock


@pytest.fixture()
def model_valid():
    yield {'connector_id': '5ee7dcd0-547b-4f0d-8034-31e5fd430a83',
           'client': 'my client',
           'account': 'my account',
           'name': 'DCM API Report Aggregator',
           'data_source': 'dcm',
           'instance_type': 'dcmapireport',
           'parameters': {
               'profile_id': '1',
               'report_id': '2'
           }
           }
@pytest.fixture()
def model_new():
    yield {
           'client': 'my client',
           'account': 'my account',
           'name': 'DCM API Report Aggregator',
           'data_source': 'dcm',
           'instance_type': 'dcmapireport',
           'parameters': {
               'profile_id': '1',
               'report_id': '2'
           }
           }


@pytest.fixture
def mock_ddb_table():
    with mock.patch('boto3.resource'):
        yield boto3.resource('dynamodb').Table('connector')
