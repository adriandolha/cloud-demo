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
    It determines associated class from data_source. E.g. data_source=dcm -> connection.dcm.DcmConnection
    :param model: Resource model
    :param logger: Logger
    :return: Resource instance
    """
    connection_type = model['connection_type']
    packages = connection_type.split('.')
    module_name = ''.join(packages)
    connection_name = ''.join([word.capitalize() for word in packages])
    class_name = f'{connection_name}Connection'
    logger.debug(f'Initializing connection {connection_name} from class {class_name}.')
    module = importlib.import_module(f'connection.{module_name}')
    connection = getattr(module, class_name)(name=model['name'], client=model['client'],
                                             account=model['account'], connection_id=model.get('connection_id'),
                                             connection_type=model['connection_type'], parameters=model.get('parameters'))
    if 'metadata' not in model:
        connection.metadata = Metadata(name=model['name'], connection_type=model['connection_type'],
                                       created=model.get('created'), updated=model.get('updated'),
                                       created_by=model.get('created_by'), modified_by=model.get('modified_by'))
    else:
        connection.metadata = Metadata(**model.get('metadata'))
    return connection
