import boto3

from connector.metadata.model import Connector


class ConnectorRepo:
    def __init__(self):
        self.ddb = boto3.resource('dynamodb')

    def save(self, metadata):
        self.ddb.Table('connectors').put_item(Item=metadata.__dict__)

    def get(self, connector_id):
        return Connector(self.ddb.Table('connectors').get_item(Key={'connector_id': connector_id})['Item'])
