"""
This module should contain business logic and validation.
"""
import abc
import datetime
import uuid

import dateutil
import logme as logme

from connector import date_format


class Metadata:
    def __init__(self, name, instance_type, transaction_type, transaction_date):
        self.name = name
        self.instance_type = instance_type
        self.transaction_type = transaction_type
        self.transaction_date = transaction_date


class Connector(metaclass=abc.ABCMeta):
    """
    Models connector. It includes validation for common fields like client, account,
    data_source, etc.
    It may be considered the aggregate resource.
    """

    def __init__(self, model: dict):
        """
        Initializes connector based on model or payload.
        It validates data input. Data input can come from API payload or database. We may want to separate
        this in the future.
        It also adds audit fields: created, updated.
        :param model: Data input dictionary with all fields and associated values.
        """
        validate_required_fields(model, 'client', 'account', 'data_source', 'name', 'instance_type')
        self.__dict__.update(model)
        self.name = model['name']
        self.instance_type = model['instance_type']
        self.data_source = model['data_source']
        self._connector_id = model.get('connector_id')
        if 'connector_id' in model:
            validate_uuid(self.connector_id)

    @property
    def connector_id(self):
        return self._connector_id

    @connector_id.setter
    def connector_id(self, value):
        validate_uuid(value)
        self._connector_id = value

    @property
    def model(self) -> dict:
        """
        It returns connector public model. We should carefully validate the model from which
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
            if not key.startswith('_'):
                target[key] = model[key]
        target.update({'connector_id': self.connector_id})
        return target

    @property
    def audit(self):
        audit = {}
        if 'connector_id' not in audit:
            audit['created'] = datetime.datetime.utcnow()
        audit['updated'] = datetime.datetime.utcnow()
        return audit


def format_date(val: datetime.date):
    return val.strftime(date_format)


@logme.log
def validate_uuid(val, logger=None):
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
