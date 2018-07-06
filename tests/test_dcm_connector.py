import pytest

from connector import make_resource


class TestDcmConnector:

    def test_resource_created_when_valid_request(self, model_valid):
        connector = make_resource(model_valid)
        assert connector

    def test_report_id_required(self, model_valid):
        del model_valid['parameters']['report_id']
        with pytest.raises(ValueError) as err:
            make_resource(model_valid)

    def test_profile_id_required(self, model_valid):
        del model_valid['parameters']['profile_id']
        with pytest.raises(ValueError) as err:
            make_resource(model_valid)
