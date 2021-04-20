import logging
from abc import ABC, abstractmethod

LOGGER = logging.getLogger('lorem-ipsum')


class AppContext(ABC):
    @property
    @abstractmethod
    def user_service(self):
        pass

    @property
    @abstractmethod
    def transaction_manager(self):
        pass

    @property
    @abstractmethod
    def metrics_service(self):
        pass

    @property
    @abstractmethod
    def book_repo(self):
        pass

    @property
    @abstractmethod
    def user_repo(self):
        pass

    @property
    @abstractmethod
    def config(self):
        pass

    @property
    @abstractmethod
    def book_service(self):
        pass


class MetricsService(ABC):
    @abstractmethod
    def metrics(self, fields: list = []):
        pass


class BookService(ABC):
    @abstractmethod
    def get(self, id=None):
        pass

    @abstractmethod
    def get_all(self, id=None, limit=1):
        pass

    @abstractmethod
    def save(self, data_records):
        pass


class UserService(ABC):
    @abstractmethod
    def get(self, username=None):
        pass

    @abstractmethod
    def delete(self, username=None):
        pass

    @abstractmethod
    def get_all(self, id=None, limit=1):
        pass

    @abstractmethod
    def save(self, data_records):
        pass

    @abstractmethod
    def validate(self, user):
        pass

    @abstractmethod
    def secret_key(self):
        pass

    @abstractmethod
    def decode_auth_token(self, auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        pass
