import importlib
import os

import logme

from connector import serializers

date_format = '%Y%m%d'
datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'
repos = {}

def make_repo():
    dbtype = os.environ.get('dbtype') or 'dynamo'
    if 'connector' not in repos:
        module = importlib.import_module(f'connector.{dbtype}')
        repo = getattr(module, 'ConnectorRepo')()
        repos['connector'] = repo
        return repo
    else:
        return repos['connector']


@logme.log
def make_resource(model, logger):
    """
    Instantiates associated resource from model.
    It determines associated class from data_source. E.g. data_source=dcm -> connector.dcm.DcmConnector
    :param model: Resource model
    :param logger: Logger
    :return: Resource instance
    """
    if 'data_source' not in model:
        raise ValueError(f'Field data_source is required.')
    data_source = model['data_source']
    packages = data_source.split('.')
    connector_name = packages[-1].capitalize()
    class_name = f'{connector_name}Connector'
    logger.debug(f'Initializing connector {connector_name} from class {class_name}.')
    return getattr(importlib.import_module(f'connector.{data_source}'), class_name)(model)
