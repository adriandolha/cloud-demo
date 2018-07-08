from connector import make_repo
from connector.domain import Connector, validate_uuid
from connector.exceptions import ResourceNotFoundException


class ConnectorService:
    """
    Connector service. It will handle requests from all clouds: AWS, Azure and Google. This is the place where they meet.
    Domain specific logic should be handled in domain specific classes.
    """

    def __init__(self):
        self.repo = make_repo()

    def add(self, request):
        connector = Connector(request)
        self.repo.save(connector)
        return {'connector_id': connector.connector_id}

    def get(self, connector_id) -> Connector:
        validate_uuid(connector_id)
        connector = self.repo.get(connector_id)
        if not connector:
            raise ResourceNotFoundException(connector_id)
        return connector
