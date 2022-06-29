import base64
import os
from functools import lru_cache
import logging

import boto3

DEFAULT_CONFIGS = {
    'connection_pool_minconn': 30,
    'connection_pool_maxconn': 40
}


@lru_cache()
def get_config():
    aurora_password = os.getenv('aurora_password')
    postgres_password = os.getenv('postgres_password', aurora_password)
    if os.getenv('app_env') == 'aws':
        session = boto3.session.Session()
        kms = session.client('kms')
        aurora_password = kms.decrypt(CiphertextBlob=base64.b64decode(aurora_password))['Plaintext'].decode('utf-8')
    _config = dict(DEFAULT_CONFIGS)
    _config.update({
        'aurora_host': os.getenv('aurora_host').split(":")[0],
        'postgres_user': os.getenv('postgres_user', default='postgres'),
        'postgres_password': postgres_password,
        'postgres_database_name': os.getenv('postgres_database_name', default='postgres'),
        'aurora_user': os.getenv('aurora_user'),
        'aurora_password': aurora_password,
        'database_name': os.getenv('database_name', default='postgres'),
        'aurora_port': int(os.getenv('aurora_port', default=5432)),
        'password_encryption_key': os.getenv('password_encryption_key'),
        'admin_password': os.getenv('admin_password'),
        'admin_user': os.getenv('admin_user'),
        'prometheus_metrics': True if os.getenv('prometheus_metrics', default='True') == 'True' else False,
        'pod_name': os.getenv('pod_name', default='pod_name'),
        'jwk_public_key_path': os.getenv('jwk_public_key_path', '/jwk/certs/public.key'),
        'jwk_private_key_path': os.getenv('jwk_private_key_path', '/jwk/certs/private.key'),
        'auth0_public_key': os.getenv('auth0_public_key')
    })
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.debug('Configuration is:')
    for config_name in _config.keys():
        if 'password' not in config_name:
            LOGGER.debug(f'{config_name}={_config[config_name]}')
    return _config
