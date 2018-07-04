import importlib


def make_repo(dbtype):
    module = importlib.import_module(f'connector.{dbtype}')
    return getattr(module, 'ConnectorRepo')()
