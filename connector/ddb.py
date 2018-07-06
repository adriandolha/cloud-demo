"""
Dynamodb repo implementation. Dynamodb seems the best NoSQL choice for AWS. It integrates very well with API Gateway and
Lambda as well.
It doesn't seem to be a standard solution (managed service) that would work for all clouds, therefore
Similar modules should be added for the chosen solution on Azure and Google.
"""
import boto3

from connector.domain import Connector


class ConnectorRepo:
    """
    Persistent store for connectors. Currently, we only need one store as it's only one table.
    Future plans might require further isolation and one table per connector might be required. Even then, one repo
    should do it.
    Keep the repo simple, just to abstract persistence details and put all the logic in the domain.
    """
    def __init__(self):
        self.ddb = boto3.resource('dynamodb')

    def save(self, connector):
        self.ddb.Table('connectors').put_item(Item=connector.__repr__())

    def get(self, connector_id):
        return Connector(self.ddb.Table('connectors').get_item(Key={'connector_id': connector_id})['Item'])
