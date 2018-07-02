import copy
import importlib
import uuid

from connector.metadata.model import Metadata


def make_repo(dbtype):
    module = importlib.import_module(f'connector.metadata.{dbtype}')
    return getattr(module, 'MetadataRepo')()


class MetadataService:
    def __init__(self):
        self.repo = make_repo('ddb')

    def add(self, metadata):
        connector_id = str(uuid.uuid4())
        entity = copy.deepcopy(metadata)
        entity.connector_id = connector_id
        self.repo.save(entity)
        return {'connector_id': connector_id}

    def get(self, id: int) -> Metadata:
        return self.repo.get(id)
