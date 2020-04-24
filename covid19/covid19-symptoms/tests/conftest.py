import os

import boto3
import pytest
from mock import mock


@pytest.fixture()
def config_valid():
    import json
    with open(f"{os.path.expanduser('~')}/.cloud-projects/covid19.json", "r") as _file:
        json = dict(json.load(_file))
        print(json)
        for k, v in json.items():
            os.environ[k] = v


@pytest.fixture()
def symptom_valid():
    yield {"contact": False,
           "red_zone_travel": False,
           "fever": False,
           "cough": True,
           "tiredness": True,
           "difficulty_breathing": False
           }


@pytest.fixture(scope='session')
def mock_ddb_table():
    with mock.patch('boto3.resource'):
        yield boto3.resource('dynamodb').Table('orders')
