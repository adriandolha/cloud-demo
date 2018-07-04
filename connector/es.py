from elasticsearch import Elasticsearch

from connector import Connector


class MetadataRepo:
    def __init__(self):
        self.es = Elasticsearch()

    def save(self, metadata: Connector):
        print('save')
        self.es.index(index="metadata", doc_type='metadata', id=metadata.connector_id, body=metadata.__dict__)

    def get(self, connector_id):
        print('get')
        return Connector(**self.es.get(index="metadata", doc_type='metadata', id=connector_id)['_source'])
