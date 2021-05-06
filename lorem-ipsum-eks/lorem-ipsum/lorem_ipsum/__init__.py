import datetime
import logging
import platform
from functools import lru_cache

import boto3

from lorem_ipsum.config import get_config
from lorem_ipsum.repo import transaction, PostgresBookRepo, TransactionManager, PostgresUserRepo
from lorem_ipsum.model import UserRepo, MetricsService, BookService, UserService, AppContext
from lorem_ipsum.service import DefaultBookService
from lorem_ipsum.service import DefaultMetricsService
from lorem_ipsum.service import DefaultUserService
import lorem_ipsum.model as model


def get_ssm_secret(parameter_name, decrypt=True):
    ssm = boto3.client("ssm")
    return ssm.get_parameter(
        Name=parameter_name,
        WithDecryption=decrypt
    )


def configure_logging():
    logging.basicConfig(format='%(asctime)s.%(msecs)03dZ %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.setLevel(logging.DEBUG)
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    # LOGGER.addHandler(logging.StreamHandler())
    LOGGER.info('logging configured...')


class DefaultAppContext(AppContext):
    def __init__(self):
        self._config = get_config()
        self._transaction_manager = TransactionManager(self)
        self._book_repo = PostgresBookRepo(self)
        self._book_service = DefaultBookService(self)
        self._user_repo = PostgresUserRepo(self)
        self._user_service = DefaultUserService(self)
        self._metrics_service = DefaultMetricsService(self)

    def init(self):
        from lorem_ipsum.repo import db_setup
        with self._transaction_manager.transaction:
            db_setup(self)

    @property
    def transaction_manager(self):
        return self._transaction_manager

    @property
    def book_service(self):
        return self._book_service

    @property
    def metrics_service(self):
        return self._metrics_service

    @property
    def user_repo(self):
        return self._user_repo

    @property
    def book_repo(self):
        return self._book_repo

    @property
    def user_service(self):
        return self._user_service

    @property
    def config(self):
        return self._config


@lru_cache()
def create_app() -> AppContext:
    configure_logging()
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.info('Application init...')
    LOGGER.info(f'Platform: {platform.python_implementation()}')
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    LOGGER.info(f'Start time: {now}')
    model.start_mappers()
    app_context = create_app_context()
    return app_context


def create_app_context() -> AppContext:
    _app_context = DefaultAppContext()
    _app_context.init()
    return _app_context
