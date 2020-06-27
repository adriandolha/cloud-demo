import json
import os

from flask import request

os.environ['env'] = 'test'
from covid19_symptoms.serializers import to_json, from_json
import app


class TestSymptomApi:
    def test_symptom_list_one(self, config_valid):
        response = app.get("247cb4db-cf5b-402b-baf9-2f90ceea8622")
        symptoms = json.loads(response['body'])
        print(symptoms)
        assert symptoms['total']
        assert '200' == response['statusCode']

    def test_symptom_list_count(self, config_valid):
        response = app.get()
        symptoms = json.loads(response['body'])
        print(symptoms)
        assert symptoms['total']
        assert '200' == response['statusCode']

    def test_symptom_add(self, symptom_valid_request, config_valid):
        response = app.save()
        assert not from_json(response['body'])['contact']
        assert '200' == response['statusCode']
