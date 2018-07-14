import pytest

from connection import make_connection


class TestDcmConnection:

    def test_resource_created_when_valid_request(self, model_valid):
        connection = make_connection(model_valid)
        assert connection

    def test_report_id_required(self, model_valid):
        del model_valid['parameters']['report_id']
        with pytest.raises(KeyError) as err:
            make_connection(model_valid)

    def test_profile_id_required(self, model_valid):
        del model_valid['parameters']['profile_id']
        with pytest.raises(KeyError) as err:
            make_connection(model_valid)
