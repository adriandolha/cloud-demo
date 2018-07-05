import datetime
import sys
import uuid

import logme as logme

current_module = sys.modules[__name__]


class Resource:
    def __init__(self, model):
        print(self.__class__.__name__)
        for k, v in model.items():
            embedded_resource = self.get_embedded_resource(model, k, v)
            if embedded_resource:
                self.__dict__[k] = embedded_resource
            else:
                self.__dict__[k] = v

    def __repr__(self):
        model = {}
        for k, v in self.__dict__.items():
            if self.embedded_resource_exists(k):
                model[k] = v.__repr__()
            else:
                model[k] = v
        return model

    @logme.log
    def get_embedded_resource(self, model, name, embedded_model, logger):
        capitalized_name = name.capitalize()
        if self.embedded_resource_exists(name):
            return getattr(current_module, capitalized_name)(embedded_model)
        if isinstance(embedded_model, dict) and '#resource_name' in model:
            resource_name = model['#resource_name']
            embedded_resource_class = f'{resource_name}{capitalized_name}'
            if self.embedded_resource_exists(embedded_resource_class):
                return getattr(current_module, embedded_resource_class)(embedded_model)
            else:
                logger.debug(f'Could not find embedded resource class {embedded_resource_class}')

        return None

    def embedded_resource_exists(self, name):
        return hasattr(current_module, name)

    def validate_required_fields(self, *fields):
        for field in fields:
            if not hasattr(self, field):
                raise ValueError(f'Field {field} is required.')

    @logme.log
    def validate_uuid(self, val, logger):
        try:
            uuid.UUID(val)
        except ValueError as e:
            logger.error(e)
            raise ValueError(f'{val} is not valid id.')


class Metadata(Resource):
    def __init__(self, model):
        super().__init__(model)


class Connector(Resource):
    def __init__(self, model: dict):
        super().__init__(model)
        self.validate_required_fields('data_source', 'name', 'instance_type')
        self.data_source = model['data_source']
        if not hasattr(self, 'created'):
            self.created = str(datetime.datetime.utcnow())
        if not hasattr(self, 'updated'):
            self.updated = str(datetime.datetime.utcnow())
        if not hasattr(self, 'connector_id'):
            self.connector_id = str(uuid.uuid4())
        self.validate_uuid(self.connector_id)


class DcmConnector(Connector):
    def __init__(self, model):
        super().__init__(model)


class DcmParameters(Resource):
    def __init__(self, model):
        super().__init__(model)
        self.validate_required_fields('report_id', 'profile_id')


def capitalize_resource_name(name):
    capitalized_name_from_dot_separator = ''.join([word.capitalize() for word in name.split('.')])
    return capitalized_name_from_dot_separator


@logme.log
def make_resource(model, logger):
    if 'data_source' not in model:
        raise ValueError(f'Field data_source is required.')
    resource_name = capitalize_resource_name(model['data_source'])
    model['#resource_name'] = resource_name
    class_name = f'{resource_name}Connector'
    logger.debug(f'Initializing resource {resource_name} from class {class_name}.')
    return getattr(current_module, class_name)(model)
