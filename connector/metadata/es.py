from elasticsearch import Elasticsearch

from connector.metadata.model import Metadata


class MetadataRepo:
    def __init__(self):
        self.es = Elasticsearch()

    def save(self, metadata: Metadata):
        print('save')
        self.es.index(index="metadata", doc_type='metadata', id=metadata.connector_id, body=metadata.__dict__)

    def get(self, connector_id):
        print('get')
        return Metadata(**self.es.get(index="metadata", doc_type='metadata', id=connector_id)['_source'])
