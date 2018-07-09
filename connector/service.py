from connector import make_repo, make_resource
from connector.domain import Connector, validate_uuid
from connector.exceptions import ResourceNotFoundException


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


class ConnectorService:
    """
    Connector service. Domain specific logic should be handled in domain specific classes. The service orchestrates.
    """

    def __init__(self, context=None):
        self.repo = make_repo()
        self.context = context

    def add(self, request):
        if 'connector_id' in request:
            raise ValueError(f'Invalid argument: connector_id. Expected empty but actual {request["connector_id"]}')
        connector = make_resource(self.enhanced_request(request))
        self.repo.save(connector)
        return {'connector_id': connector.resource_id}

    def enhanced_request(self, request: dict):
        """
        Add context information.
        :param request: Request
        :return: Request with context.
        """
        request.update({'_context': self.context})
        return request

    def get(self, connector_id) -> Connector:
        validate_uuid(connector_id)
        connector = self.repo.get(connector_id)
        if not connector:
            raise ResourceNotFoundException(connector_id)
        return connector
