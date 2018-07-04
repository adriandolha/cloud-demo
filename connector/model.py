import datetime
import uuid
import sys

current_module = sys.modules[__name__]


class Resource:
    def __init__(self, model):
        for k, v in model.items():
            if hasattr(current_module, k.capitalize()):
                self.__dict__[k] = getattr(current_module, k.capitalize())(v)
            else:
                self.__dict__[k] = v

    def __repr__(self):
        model = {}
        for k, v in self.__dict__.items():
            if hasattr(current_module, k.capitalize()):
                model[k] = v.__repr__()
            else:
                model[k] = v
        return model


class Metadata(Resource):
    def __init__(self, model):
        super().__init__(model)


class Connector(Resource):
    def __init__(self, model: dict):
        super().__init__(model)
        if not hasattr(self, 'creation_date'):
            self.creation_date = str(datetime.datetime.utcnow())
        if not hasattr(self, 'connector_id'):
            self.connector_id = str(uuid.uuid4())
