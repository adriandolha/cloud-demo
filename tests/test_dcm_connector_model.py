import pytest

from connector.model import make_resource
import pytest

from connector.model import make_resource


class TestDcmConnector:
    @pytest.fixture()
    def model_valid(self):
        yield {'connector_id': '5ee7dcd0-547b-4f0d-8034-31e5fd430a83',
               'name': 'DCM API Report Aggregator',
               'data_source': 'dcm',
               'instance_type': 'dcmapireport',
               'parameters': {
                   'profile_id': '2234072',
                   'report_id': '138567177'
               }
               }

    def test_resource_created_when_valid_request(self, model_valid):
        connector = make_resource(model_valid)
        assert connector.parameters.profile_id == model_valid['parameters']['profile_id']
        assert connector.parameters.report_id == model_valid['parameters']['report_id']

    def test_report_id_required(self, model_valid):
        del model_valid['parameters']['report_id']
        with pytest.raises(ValueError) as err:
            make_resource(model_valid)

    def test_profile_id_required(self, model_valid):
        del model_valid['parameters']['profile_id']
        with pytest.raises(ValueError) as err:
            make_resource(model_valid)
