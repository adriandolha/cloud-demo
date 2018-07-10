import importlib
import os

import logme

from connection import serializers

date_format = '%Y%m%d'
datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'
repos = {}


def make_repo():
    dbtype = os.environ.get('dbtype') or 'dynamo'
    if 'connection' not in repos:
        module = importlib.import_module(f'connection.{dbtype}')
        repo = getattr(module, 'ConnectorRepo')()
        repos['connection'] = repo
        return repo
    else:
        return repos['connection']


@logme.log
def make_resource(model, logger):
    """
    Instantiates associated resource from model.
    It determines associated class from data_source. E.g. data_source=dcm -> connection.dcm.DcmConnector
    :param model: Resource model
    :param logger: Logger
    :return: Resource instance
    """
    if 'connector_type' not in model:
        raise ValueError(f'Field connector_type is required.')
    connector_type = model['connector_type']
    packages = connector_type.split('.')
    module_name = ''.join(packages)
    connector_name = ''.join([word.capitalize() for word in packages])
    class_name = f'{connector_name}Connection'
    logger.debug(f'Initializing connection {connector_name} from class {class_name}.')
    module = importlib.import_module(f'connection.{module_name}')
    print(dir(module))
    return getattr(module, class_name)(model)
