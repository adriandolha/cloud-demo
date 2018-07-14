import datetime
import uuid
from threading import Thread
from time import sleep

import boto3

from connection import make_repo, make_connection, sqs
from connection.domain import Connection, validate_uuid, ConnectionCreated
from connection.exceptions import ResourceNotFoundException
from connection.serializers import to_json, from_json, to_dynamo
import logme


class Context:
    """
    Holds context information. E.g. current user
    Context information is further needed for authorization, resource audit, etc.
    """

    def __init__(self, context):
        self._user = {
            'user_id': context['user_id']
        }

    @property
    def user(self):
        return self._user


class ConnectionService:
    """
    Connection service. Domain specific logic should be handled in domain specific classes. The service orchestrates.
    """

    def __init__(self, context=None):
        self.repo = make_repo()
        self.context = context

    def add(self, request, connection_id=None):
        if 'connection_id' in request:
            raise ValueError(f'Invalid argument: connection_id. Expected empty but actual {request["connection_id"]}')
        connection = make_connection(self.enhanced_request(request))
        now = datetime.datetime.utcnow()
        connection.metadata.created = now
        connection.metadata.updated = now

        self.repo.save(connection)
        sqs.publish(str(to_json(vars(ConnectionCreated(connection.model)))))
        return {'connection_id': connection.connection_id}

    def enhanced_request(self, request: dict):
        """
        Add context information.
        :param request: Request
        :return: Request with context.
        """
        request.update({'_context': self.context})
        return request

    def get(self, connection_id) -> Connection:
        validate_uuid(connection_id)
        connection = self.repo.get(connection_id)
        if not connection:
            raise ResourceNotFoundException(connection_id)
        return connection

    def list(self):
        return self.repo.list()

    def delete(self, connection_id):
        validate_uuid(connection_id)
        self.repo.delete(connection_id)

    def connection_created(self, connection):
        boto3.resource('dynamodb').Table('tasks_dev_myapp').put_item(Item={'task_id':str(uuid.uuid4()),'connection_id':connection.connection_id})


class ConnectionConsumer(Thread):
    @logme.log
    def run(self, logger=None):
        while True:
            try:
                for message in sqs.receive():
                    if 'Body' in message:
                        print(message['Body'])
                        connection = make_connection(from_json(message['Body'])['body'])
                        print(connection)
                        ConnectionService().connection_created(connection)
                    sqs.delete(message)

            except Exception as e:
                logger.exception(e)
                sleep(1)
