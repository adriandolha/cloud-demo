import copy
import json
import uuid

import pytest

from connection import make_connection


class TestConnection:

    def test_resource_created_when_valid_request(self, model_valid):
        connection = make_connection(model_valid)
        assert connection.name == model_valid['name']
        assert connection.connection_type == model_valid['connection_type']

    def test_connection_type_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['connection_type']
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

    def test_connection_id_is_uuid(self, model_valid):
        model_valid['connection_id'] = '5ee7dcd0-54'
        with pytest.raises(ValueError) as err:
            make_connection(model_valid)

    def test_name_required(self, model_valid):
        model = copy.deepcopy(model_valid)
        del model['name']
        with pytest.raises(KeyError) as err:
            make_connection(model)

    def test_connection_serialization(self, model_valid):
        dumps = json.dumps(make_connection(model_valid).model).encode()
        print(dumps)
        assert dumps

    def test_connection_id_setter(self, model_new):
        model = copy.deepcopy(model_new)
        connection = make_connection(model)
        cid = str(uuid.uuid4())
        connection.connection_id = cid
        assert connection.connection_id == cid
        assert connection.model['connection_id'] == cid
