import copy
import json

import pytest

from connector.model import capitalize_resource_name, make_resource


class TestConnector:
    @pytest.fixture()
    def model_valid(self):
        yield {'connector_id': '5ee7dcd0-547b-4f0d-8034-31e5fd430a83',
               'name': 'DCM API Report Aggregator',
               'data_source': 'dcm',
               'instance_type': 'dcmapireport',

               }

    def test_resource_name_valid(self, model_valid):
        make_resource(model_valid)
        assert model_valid['#resource_name'] == 'Dcm'

    def test_capitalize_resource_name_valid(self):
        assert capitalize_resource_name('google.dcm') == 'GoogleDcm'

    def test_resource_created_when_valid_request(self, model_valid):
        connector = make_resource(model_valid)
        print(json.dumps(connector.__repr__()))
        assert connector.name == model_valid['name']
        assert connector.data_source == model_valid['data_source']
        assert connector.instance_type == model_valid['instance_type']

    def test_data_source_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['data_source']
        with pytest.raises(ValueError) as err:
            make_resource(model)
        print(err.value)

    def test_connector_id_is_uuid(self, model_valid):
        model_valid['connector_id'] = '5ee7dcd0-54'
        with pytest.raises(ValueError) as err:
            make_resource(model_valid)
        print(err.value)

    def test_name_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['name']
        with pytest.raises(ValueError) as err:
            make_resource(model)
        print(err.value)

    def test_instance_type_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['instance_type']
        with pytest.raises(ValueError) as err:
            make_resource(model)
        print(err.value)
