from connector.metadata import make_repo
from connector.metadata.model import Connector


class ConnectorService:
    def __init__(self):
        self.repo = make_repo('ddb')

    def add(self, request):
        connector = Connector(request)
        self.repo.save(connector)
        return {'connector_id': connector.connector_id}

    def get(self, id: int) -> Connector:
        return self.repo.get(id)
