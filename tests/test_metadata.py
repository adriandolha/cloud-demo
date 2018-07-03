import json

from connector.metadata import aws
from connector.metadata.app import ConnectorService

metadata_request = {
    "connector_id": "0",
    "client_id": "1",
    "user_id": "2",
    "account_id": "3",
    "report_id": "4",
    "profile_id": "5",
    "data_source": "gcs"
}


class TestMetadataService:

    def test_add_metadata(self):
        response = json.loads(aws.create_metadata({'body': json.dumps(metadata_request)})['body'])
        print(response)
        assert response['connector_id']
        metadata = ConnectorService().get(response['connector_id'])
        print(metadata)
        assert metadata.creation_date
        assert metadata.connector_id
