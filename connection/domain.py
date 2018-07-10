"""
This module should contain business logic and validation.
"""
import abc
import datetime
import uuid

import dateutil
import logme as logme

from connection import date_format


class Metadata:
    def __init__(self, name, connector_type, transaction_type=None, transaction_date=None):
        self.name = name
        self.instance_type = connector_type
        self.transaction_type = transaction_type
        self.transaction_date = transaction_date

    @property
    def model(self):
        return vars(self)


class Connection(metaclass=abc.ABCMeta):
    """
    Models connection. It includes validation for common fields like client, account,
    data_source, etc.
    It may be considered the aggregate resource.
    """

    def __init__(self, model: dict):
        """
        Initializes connection based on model or payload.
        It validates data input. Data input can come from API payload or database. We may want to separate
        this in the future.
        It also adds audit fields: created, updated.
        :param model: Data input dictionary with all fields and associated values.
        """
        validate_required_fields(model, 'client', 'account', 'connector_type', 'name')
        self.__dict__.update(model)
        self.name = model['name']
        self.connector_type = model['connector_type']
        self._connector_id = None
        self.resource_id = model.get('connector_id')
        self.metadata = Metadata(self.name, self.connector_type)

    @property
    def resource_id(self):
        return self._connector_id

    @resource_id.setter
    def resource_id(self, value):
        validate_uuid(value)
        self._connector_id = value

    @property
    def model(self) -> dict:
        """
        It returns connection public model. We should carefully validate the model from which
        it's built or be more specific in the representation in order to make sure that no
        additional fields are included by mistake. This could result in persistence or API contract
        failure.
        Be careful not to leak internal state.
        This could be achieved by specifying the public fields instead of copying the dictionary.
        :return: Connector model.
        """
        target = {}
        model = vars(self)
        for key in model:
            value = model.get(key)
            if not self.is_private_field(key):
                target[key] = value
                if value and hasattr(value, 'model'):
                    target[key] = value.model

        target.update({'connector_id': self.resource_id})
        return target

    def is_private_field(self, name: str):
        return name.startswith('_')


def audit(model):
    """
    Creates audit information. (i.e. created and updated info)
    :return: Audit information.
    """
    target = {}
    if 'resource_id' not in model:
        target['created'] = datetime.datetime.utcnow()
    target['updated'] = datetime.datetime.utcnow()
    return target


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