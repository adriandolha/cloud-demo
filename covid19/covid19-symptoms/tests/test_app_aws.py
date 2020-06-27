import json
import os

os.environ['env'] = 'test'
from covid19_symptoms.serializers import to_json, from_json
import app_aws


class TestSymptomApi:
    def test_symptom_list_one(self, config_valid):
        response = app_aws.get({"queryStringParameters": {"id": "247cb4db-cf5b-402b-baf9-2f90ceea8622"}})
        symptoms = json.loads(response['body'])
        print(symptoms)
        assert symptoms['total']
        assert '200' == response['statusCode']

    def test_symptom_list_count(self, config_valid):
        response = app_aws.get({'body': to_json({})})
        symptoms = json.loads(response['body'])
        print(symptoms)
        assert symptoms['total']
        assert '200' == response['statusCode']

    def test_symptom_add(self, symptom_valid, config_valid):
        response = app_aws.add({'body': to_json(symptom_valid)})
        assert not from_json(response['body'])['contact']
        assert '200' == response['statusCode']
