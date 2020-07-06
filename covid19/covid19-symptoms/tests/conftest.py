import logging
import os

import boto3
import flask
import pytest
import mock
# from mock import mock

import covid19_symptoms
from covid19_symptoms.serializers import to_json


@pytest.fixture()
def config_valid():
    import json
    with open(f"{os.path.expanduser('~')}/.cloud-projects/covid19-local.json", "r") as _file:
        json = dict(json.load(_file))
        print(json)
        for k, v in json.items():
            os.environ[k] = str(v)
    covid19_symptoms.create_app()
    LOGGER = logging.getLogger('symptoms')
    LOGGER.setLevel(logging.DEBUG)

@pytest.fixture()
def symptom_valid():
    yield {"contact": False,
           "red_zone_travel": False,
           "fever": False,
           "cough": True,
           "tiredness": True,
           "difficulty_breathing": False
           }


@pytest.fixture()
def symptom_valid_request(symptom_valid):
    # from flask import request
    with mock.patch('flask.request'):
        flask.request.data.return_value = to_json(symptom_valid)
        yield ''


@pytest.fixture(scope='session')
def mock_ddb_table():
    with mock.patch('boto3.resource'):
        yield boto3.resource('dynamodb').Table('orders')
