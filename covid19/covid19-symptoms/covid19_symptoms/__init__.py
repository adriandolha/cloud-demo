import base64
import logging
import os
from functools import lru_cache

import binascii
import boto3


@lru_cache()
def get_config():
    aurora_password = os.getenv('aurora_password')
    if os.getenv('app_env') == 'aws':
        session = boto3.session.Session()
        kms = session.client('kms')
        aurora_password = kms.decrypt(CiphertextBlob=base64.b64decode(aurora_password))['Plaintext'].decode('utf-8')
    _config = {
        'aurora_host': os.getenv('aurora_host'),
        'aurora_user': os.getenv('aurora_user'),
        'aurora_port': int(os.getenv('aurora_port', default=5432)),
        'aurora_password': aurora_password
    }
    LOGGER = logging.getLogger('symptoms')
    LOGGER.debug('Configuration:')
    for config_name in _config.keys():
        if 'password' not in config_name:
            LOGGER.debug(f'{config_name}={_config[config_name]}')
    return _config


def get_ssm_secret(parameter_name, decrypt=True):
    ssm = boto3.client("ssm")
    return ssm.get_parameter(
        Name=parameter_name,
        WithDecryption=decrypt
    )


def configure_logging():
    logging.basicConfig(format='%(levelname)s:%(message)s')
    LOGGER = logging.getLogger('symptoms')
    LOGGER.setLevel(logging.DEBUG)
    # LOGGER.addHandler(logging.StreamHandler())
    LOGGER.info('logging configured...')


class AppContext:
    def __init__(self):
        from covid19_symptoms.repo import transaction, SymptomRepo, TransactionManager
        from covid19_symptoms.service import SymptomService
        self.config = get_config()
        self.transaction_manager = TransactionManager(self)
        self.symptom_repo = SymptomRepo(self)
        self.symptom_service = SymptomService(self)


def setup(app_context: AppContext):
    LOGGER = logging.getLogger('symptoms')
    LOGGER.debug('Running database setup...')
    with app_context.transaction_manager.transaction as transaction:
        app_context.symptom_repo.create_table()


@lru_cache()
def create_app() -> AppContext:
    print('Application init...')
    configure_logging()
    app_context = AppContext()
    setup(app_context)
    return app_context
