"""
REST API. Responsible for serialization, deserialization, responses and exception handlers.
Other than this, it should be light and let the services handle the business logic.
It should be the common entry point for all cloud platforms.
"""
import json

from functools import wraps

from connection.exceptions import ResourceNotFoundException
from connection.serializers import from_json
from connection.service import ConnectionService


def response(message, status_code):
    return {
        'status_code': str(status_code),
        'body': json.dumps(message)
    }


def handle_request():
    """
    Handle common exceptions.
    :return: Decorated function.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return response(f(*args, *kwargs), 200)
            except ResourceNotFoundException as e:
                return response(str(e), 404)
            except ValueError as e:
                return response(str(e), 412)
            except KeyError as e:
                return response(str(e), 412)

        return wrapper

    return decorator


class ConnectionRestApi:
    def __init__(self, context=None):
        self.context = context
        self.service = ConnectionService(context)

    @handle_request()
    def add(self):
        """
        Add connection.
        :param body: Add connection request.
        :return: Added connection id.
        """
        return self.service.add(from_json(self.context['body']))

    @handle_request()
    def get(self):
        """
        Get connection.
        :return: Connection
        """
        return self.service.get(self.context['path_parameters']['id']).model

    @handle_request()
    def list(self):
        items = [connection.model for connection in self.service.list()]
        return {'items': items, 'count': len(items)}

    @handle_request()
    def delete(self):
        connection_id = self.context['path_parameters']['id']
        self.service.delete(connection_id)
        return f'Successfully removed connection {connection_id}'
