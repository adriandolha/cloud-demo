import json

from covid19_symptoms.serializers import to_json, from_json
import app
import logging


class TestSymptomApi:
    def test_symptom_list(self):
        response = app.list({})
        orders = json.loads(response['body'])
        assert 1 == len(orders)
        assert '200' == response['statusCode']

    def test_symptom_add(self, symptom_valid, config_valid):
        response = app.add({'body': to_json(symptom_valid)})
        assert not from_json(response['body'])['contact']
        assert '200' == response['statusCode']
