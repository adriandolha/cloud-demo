import datetime
import uuid


class Connector:
    def __init__(self, kwargs):
        self.__dict__.update(kwargs)
        if not hasattr(self, 'creation_date'):
            self.creation_date = str(datetime.datetime.utcnow())
        if not hasattr(self, 'connector_id'):
            self.connector_id = str(uuid.uuid4())

