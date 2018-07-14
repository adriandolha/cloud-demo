import datetime

from connection import make_repo, make_connection
from connection.domain import Connection, validate_uuid
from connection.exceptions import ResourceNotFoundException


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
