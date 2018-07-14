"""
Dynamodb repo implementation. Dynamodb seems the best NoSQL choice for AWS. It integrates very well with API Gateway and
Lambda as well.
It doesn't seem to be a standard solution (managed service) that would work for all clouds, therefore
Similar modules should be added for the chosen solution on Azure and Google.
"""
import uuid

import boto3

from connection import make_connection
from connection.domain import Connection
from connection.serializers import to_dynamo


class ConnectionRepo:
    """
    Persistent store for connections. Currently, we only need one store as it's only one table.
    Future plans might require further isolation and one table per connection might be required. Even then, one repo
    should do it.
    Keep the repo simple, just to abstract persistence details and put all the logic in the domain.
    """

    def __init__(self, env, client):
        self.ddb = boto3.resource('dynamodb')
        self.table_name = f'connections_{env}_{client}'
        self.table = self.ddb.Table(self.table_name)

    def save(self, connection: Connection):
        if not connection.connection_id:
            connection.connection_id = str(uuid.uuid4())
        model = connection.model
        self.table.put_item(Item=to_dynamo(model))

    def get(self, connection_id):
        response = self.table.get_item(Key={'connection_id': connection_id})
        if 'Item' not in response:
            return None
        return make_connection(response['Item'])

    def list(self):
        return [make_connection(item) for item in self.table.scan()['Items']]

    def delete(self, connection_id):
        self.ddb.delete_item(TableName=self.table_name, Key={'connection_id': connection_id})
