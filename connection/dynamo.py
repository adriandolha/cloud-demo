"""
Dynamodb repo implementation. Dynamodb seems the best NoSQL choice for AWS. It integrates very well with API Gateway and
Lambda as well.
It doesn't seem to be a standard solution (managed service) that would work for all clouds, therefore
Similar modules should be added for the chosen solution on Azure and Google.
"""
import uuid

import boto3

from connection.domain import Connection, audit
from connection.serializers import to_dynamo


class ConnectorRepo:
    """
    Persistent store for connectors. Currently, we only need one store as it's only one table.
    Future plans might require further isolation and one table per connection might be required. Even then, one repo
    should do it.
    Keep the repo simple, just to abstract persistence details and put all the logic in the domain.
    """

    def __init__(self):
        self.ddb = boto3.resource('dynamodb')

    def save(self, connector: Connection):
        if not connector.resource_id:
            connector.resource_id = str(uuid.uuid4())
        model = connector.model
        model.update(audit(model))
        self.ddb.Table('connectors').put_item(Item=to_dynamo(model))

    def get(self, connector_id):
        response = self.ddb.Table('connectors').get_item(Key={'connector_id': connector_id})
        if 'Item' not in response:
            return None
        return Connection(response['Item'])

    def list(self):
        return [Connection(item) for item in self.ddb.Table('connectors').scan()['Items']]

    def delete(self, connector_id):
        self.ddb.delete_item(TableName='connectors', Key={'connector_id': connector_id})