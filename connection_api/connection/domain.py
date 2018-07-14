"""
This module should contain business logic and validation.
"""
import abc
import datetime
import uuid

import dateutil
import logme as logme

date_format = '%Y%m%d'
datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'


class Metadata:
    def __init__(self, name, connection_type, created=None, updated=None, created_by=None, modified_by=None):
        self.name = name
        self.connection_type = connection_type
        self.created = created
        self.updated = updated
        self.created_by = created_by
        self.modified_by = modified_by

    @property
    def model(self):
        return vars(self)


class Connection(metaclass=abc.ABCMeta):
    """
    Models connection. It includes validation for common fields like client, account,
    data_source, etc.
    It may be considered the aggregate resource.
    """

    def __init__(self, **kwargs):
        """
        Initializes connection based on model or payload.
        It validates data input. Data input can come from API payload or database. We may want to separate
        this in the future.
        It also adds audit fields: created, updated.
        :param model: Data input dictionary with all fields and associated values.
        """
        self.name = kwargs['name']
        self._connection_id = None
        self.connection_id = kwargs.get('connection_id')
        self._metadata = None
        self._metadata = kwargs.get('metadata')
        self.parameters = kwargs.get('parameters')
        self.client = kwargs['client']
        self.account = kwargs['account']
        self.connection_type = kwargs['connection_type']

    @property
    def metadata(self) -> Metadata:
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = value

    @property
    def connection_id(self):
        return self._connection_id

    @connection_id.setter
    def connection_id(self, value):
        validate_uuid(value)
        self._connection_id = value

    @property
    def model(self) -> dict:
        """
        It returns connection public model. We should carefully validate the model from which
        it's built or be more specific in the representation in order to make sure that no
        additional fields are included by mistake. This could result in persistence or API contract
        failure.
        Be careful not to leak internal state.
        This could be achieved by specifying the public fields instead of copying the dictionary.
        :return: Connection model.
        """
        return {
            'connection_id': self.connection_id,
            'name': self.name,
            'client': self.client,
            'account': self.account,
            'metadata': self.metadata.model,
            'parameters': self.parameters,
            'connection_type': self.connection_type
        }

    def is_private_field(self, name: str):
        return name.startswith('_')


def format_date(val: datetime.date):
    return val.strftime(date_format)


@logme.log
def validate_uuid(val, logger=None):
    if not val:
        return val
    try:
        uuid.UUID(val)
        return val
    except ValueError as e:
        logger.error(e)
        raise ValueError(f'{val} is not valid id.')


def validate_required_fields(model, *fields):
    for field in fields:
        if field not in model:
            raise ValueError(f'Field {field} is required.')


@logme.log
def validate_date_format(val, logger=None):
    try:
        dateutil.parser.parse(val)
    except ValueError as e:
        logger.error(e)
        raise ValueError(f'Invalid date format for value {val}. Expected date format is {date_format}.')
    return val
