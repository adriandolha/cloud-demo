import importlib
import os

import logme

from connection import serializers
from connection.domain import Metadata

repos = {}


def make_repo():
    dbtype = os.environ.get('dbtype') or 'dynamo'
    env = os.environ.get('env') or 'dev'
    client = os.environ.get('client') or 'dan'
    if 'connection' not in repos:
        module = importlib.import_module(f'connection.{dbtype}')
        repo = getattr(module, 'ConnectionRepo')(env, client)
        repos['connection'] = repo
        return repo
    else:
        return repos['connection']


@logme.log
def make_connection(model, logger):
    """
    Instantiates associated connection from model.
    It determines associated class from data_source. E.g. data_source=dcm -> connection.dcm.DcmConnector
    :param model: Resource model
    :param logger: Logger
    :return: Resource instance
    """
    connector_type = model['connector_type']
    packages = connector_type.split('.')
    module_name = ''.join(packages)
    connector_name = ''.join([word.capitalize() for word in packages])
    class_name = f'{connector_name}Connection'
    logger.debug(f'Initializing connection {connector_name} from class {class_name}.')
    module = importlib.import_module(f'connection.{module_name}')
    connection = getattr(module, class_name)(name=model['name'], client=model['client'],
                                             account=model['account'], connector_id=model.get('connector_id'),
                                             connector_type=model['connector_type'], parameters=model.get('parameters'))
    if 'metadata' not in model:
        connection.metadata = Metadata(name=model['name'], connector_type=model['connector_type'],
                                       created=model.get('created'), updated=model.get('updated'),
                                       created_by=model.get('created_by'), modified_by=model.get('modified_by'))
    else:
        connection.metadata = Metadata(**model.get('metadata'))
    return connection
