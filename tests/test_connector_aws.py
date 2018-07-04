import json
import pytest
import mock
from connector import aws
from connector.model import Connector
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

    def test_add_connector(self):
        response = json.loads(aws.add({'body': json.dumps(add_connector_request)})['body'])
        print(response)
        assert response['connector_id']
        metadata = ConnectorService().get(response['connector_id'])
        assert metadata.creation_date
        assert metadata.connector_id

    def test_resource(self):
        connector = Connector(json.loads(aws.add({'body': json.dumps(add_connector_request)})['body']))
        print(connector.__repr__())
