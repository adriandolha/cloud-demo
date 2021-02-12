import datetime
import logging
import platform
from functools import lru_cache

import boto3


def get_ssm_secret(parameter_name, decrypt=True):
    ssm = boto3.client("ssm")
    return ssm.get_parameter(
        Name=parameter_name,
        WithDecryption=decrypt
    )


def configure_logging():
    logging.basicConfig(format='%(asctime)s.%(msecs)03dZ %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.setLevel(logging.WARNING)
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    # LOGGER.addHandler(logging.StreamHandler())
    LOGGER.info('logging configured...')


class AppContext:
    def __init__(self):
        from lorem_ipsum_auth.repo import transaction, UserRepo, TransactionManager
        from lorem_ipsum_auth.service import MetricsService, UserService
        from lorem_ipsum_auth.config import get_config
        self.config = get_config()
        self.transaction_manager = TransactionManager(self)
        self.user_repo = UserRepo(self)
        self.user_service = UserService(self)
        self.metrics_service = MetricsService(self)

    def init(self):
        from lorem_ipsum_auth.repo import db_setup
        with self.transaction_manager.transaction:
            db_setup(self)


def setup(app_context: AppContext):
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.debug('Running database setup...')
    app_context.init()


@lru_cache()
def create_app() -> AppContext:
    configure_logging()
    LOGGER = logging.getLogger('lorem-ipsum-auth')
    LOGGER.info('Application init...')
    LOGGER.info(f'Platform: {platform.python_implementation()}')
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    LOGGER.info(f'Start time: {now}')
    app_context = AppContext()
    setup(app_context)
    return app_context
