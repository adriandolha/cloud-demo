"""
REST API. Responsible for serialization, deserialization, responses and exception handlers.
It should be the common entry point for all cloud platforms.
"""
import json

from functools import wraps

from connector.exceptions import ResourceNotFoundException
from connector.serializers import from_json
from connector.service import ConnectorService


def response(message, status_code):
    return {
        'status_code': str(status_code),
        'body': json.dumps(message)
    }


def handle_exceptions():
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

        return wrapper

    return decorator


class ConnectorRestApi:
    def __init__(self):
        self.service = ConnectorService()

    @handle_exceptions()
    def add(self, body):
        """
        Add connector.
        :param body: Add connector request.
        :return: Added connector id.
        """
        return self.service.add(from_json(body))

    @handle_exceptions()
    def get(self, connector_id):
        """
        Get connector.
        :param connector_id: Connector id (path parameter)
        :return: Connector
        """
        return self.service.get(connector_id).model
