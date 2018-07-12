import copy
import json
import uuid

import pytest

from connection import make_connection


class TestConnector:

    def test_resource_created_when_valid_request(self, model_valid):
        connector = make_connection(model_valid)
        assert connector.name == model_valid['name']
        assert connector.connector_type == model_valid['connector_type']

    def test_connector_type_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['connector_type']
        with pytest.raises(KeyError) as err:
            make_connection(model)

    def test_client_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['client']
        with pytest.raises(KeyError) as err:
            make_connection(model)

    def test_account_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['account']
        with pytest.raises(KeyError) as err:
            make_connection(model)

    def test_connector_id_is_uuid(self, model_valid):
        model_valid['connector_id'] = '5ee7dcd0-54'
        with pytest.raises(ValueError) as err:
            make_connection(model_valid)

    def test_name_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['name']
        with pytest.raises(KeyError) as err:
            make_connection(model)

    def test_connector_serialization(self, model_valid):
        dumps = json.dumps(make_connection(model_valid).model).encode()
        print(dumps)
        assert dumps

    def test_connector_id_setter(self, model_new):
        model = copy.deepcopy(model_new)
        connector = make_connection(model)
        cid = str(uuid.uuid4())
        connector.connector_id = cid
        assert connector.connector_id == cid
        assert connector.model['connector_id'] == cid
