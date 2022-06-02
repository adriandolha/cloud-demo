import datetime
import logging
import platform
from functools import lru_cache

import boto3

from lorem_ipsum.config import get_config
from lorem_ipsum.repo import transaction, PostgresBookRepo, TransactionManager, PostgresUserRepo, PostgresEventRepo, \
    PostgresWordRepo, PostgresBlacklistTokenRepo, \
    create_database_if_not_exists
from lorem_ipsum.model import UserRepo, MetricsService, BookService, UserService, WordRepo, EventRepo, WordService, \
    AppContext
from lorem_ipsum.service import DefaultBookService
from lorem_ipsum.service import DefaultMetricsService
from lorem_ipsum.service import DefaultUserService
from lorem_ipsum.service import DefaultWordService
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
    LOGGER.setLevel(logging.INFO)
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    # LOGGER.addHandler(logging.StreamHandler())
    LOGGER.info('logging configured...')


class DefaultAppContext(AppContext):
    def __init__(self):
        AppContext.__init__(self)
        self._config = get_config()
        self._transaction_manager = TransactionManager(self)
        self._book_repo = PostgresBookRepo(self)
        self._book_service = DefaultBookService(self)
        self._user_repo = PostgresUserRepo(self)
        self._blacklist_token_repo = PostgresBlacklistTokenRepo(self)
        self._event_repo = PostgresEventRepo(self)
        self._user_service = DefaultUserService(self)
        self._word_repo = PostgresWordRepo(self)
        self._word_service = DefaultWordService(self)
        self._metrics_service = DefaultMetricsService(self)

    def init(self):
        pass

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
    def blacklist_token_repo(self):
        return self._blacklist_token_repo

    @property
    def word_repo(self):
        return self._word_repo

    @property
    def event_repo(self):
        return self._event_repo

    @property
    def book_repo(self):
        return self._book_repo

    @property
    def user_service(self):
        return self._user_service

    @property
    def word_service(self):
        return self._word_service

    @property
    def config(self):
        return self._config

    def run_database_setup(self):
        create_database_if_not_exists(get_config())
        with self._transaction_manager.transaction:
            from lorem_ipsum.repo import db_setup
            db_setup(self)


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
    return _app_context
