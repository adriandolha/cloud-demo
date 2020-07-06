import json
import os

from flask import request

os.environ['env'] = 'test'
from covid19_symptoms.serializers import to_json, from_json
import app


class TestSymptomApi:
    def test_symptom_list_one(self, config_valid):
        response = app.get("247cb4db-cf5b-402b-baf9-2f90ceea8622")
        symptoms = json.loads(response.response[0].decode('utf-8'))
        print(symptoms)
        assert symptoms['total']
        assert '200' == response.status

    def test_symptom_list_count(self, config_valid):
        response = app.get_all()
        symptoms = json.loads(response.response[0].decode('utf-8'))
        print(symptoms)
        assert symptoms['total']
        assert '200' == response.status

    def test_symptom_metrics(self, config_valid):
        _result = app.metrics()
        metrics = json.loads(_result.response[0].decode('utf-8'))
        assert metrics.get('connection_pool.maxconn')
        assert metrics.get('connection_pool.minconn')
        assert metrics.get('connection_pool.usedconn') is not None
        assert metrics.get('connection_pool.size') == 1
        assert '200' == _result.status

    def test_symptom_add(self, symptom_valid_request, config_valid):
        response = app.save()
        assert not from_json(response.response[0].decode('utf-8'))['contact']
        assert '200' == response.status