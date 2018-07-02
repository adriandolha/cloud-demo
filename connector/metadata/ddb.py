import boto3

from connector.metadata.model import Metadata


class MetadataRepo:
    def __init__(self):
        self.ddb = boto3.resource('dynamodb')
        pass

    def save(self, metadata):
        metadata.creation_date = str(metadata.creation_date)
        self.ddb.Table('metadata').put_item(Item=metadata.__dict__)

    def get(self, connector_id):
        return Metadata(**self.ddb.Table('metadata').get_item(Key={'connector_id': connector_id})['Item'])
