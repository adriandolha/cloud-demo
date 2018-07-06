import json
import pytest
import mock
from connector import aws
from connector.domain import Connector
from connector.service import ConnectorService

add_connector_request = {
    "client_id": "1",
    "user_id": "2",
    "account_id": "3",
    "report_id": "4",
    "profile_id": "5",
    "data_source": "gcs",
    "metadata": {"pid": 1}
}


class TestConnectorAWS:
    """
    It requires terraform scripts to be applied and the infrastructure online.
    Deployment scripts can be found in templates/aws/connector
    """

    @pytest.mark.skip(reason='Run it only on demand')
    def test_add_connector(self):
        response = json.loads(aws.add({'body': json.dumps(add_connector_request)})['body'])
        assert response['connector_id']
        metadata = ConnectorService().get(response['connector_id'])
        assert metadata.creation_date
        assert metadata.connector_id
