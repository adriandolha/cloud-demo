import copy
import json

import pytest

from connector import make_resource
from connector.domain import validate_date_format


class TestConnector:

    def test_resource_created_when_valid_request(self, model_valid):
        connector = make_resource(model_valid)
        assert connector.name == model_valid['name']
        assert connector.data_source == model_valid['data_source']
        assert connector.instance_type == model_valid['instance_type']

    def test_data_source_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['data_source']
        with pytest.raises(ValueError) as err:
            make_resource(model)

    def test_client_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['client']
        with pytest.raises(ValueError) as err:
            make_resource(model)

    def test_account_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['account']
        with pytest.raises(ValueError) as err:
            make_resource(model)

    def test_connector_id_is_uuid(self, model_valid):
        model_valid['connector_id'] = '5ee7dcd0-54'
        with pytest.raises(ValueError) as err:
            make_resource(model_valid)

    def test_name_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['name']
        with pytest.raises(ValueError) as err:
            make_resource(model)

    def test_instance_type_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['instance_type']
        with pytest.raises(ValueError) as err:
            make_resource(model)

    def test_created_date_format(self, model_new):
        connector = make_resource(model_new)
        entity = connector.entity
        assert entity['created']
        assert validate_date_format(entity['created'])
        assert entity['updated']
        assert validate_date_format(entity['updated'])

    def test_updated_date_format(self, model_valid):
        connector = make_resource(model_valid)
        entity = connector.entity
        assert entity['updated']
        assert validate_date_format(entity['updated'])

    def test_connector_serialization(self, model_valid):
        assert json.dumps(make_resource(model_valid).entity)
