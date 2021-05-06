from abc import ABC, abstractmethod


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def as_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data: dict):
        return User(**data)


class Book:
    def __init__(self, id: str, author: str, title: str, no_of_pages: int, book: str):
        self.id = id
        self.author = author
        self.title = title
        self.no_of_pages = no_of_pages
        self.book = book

    def as_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data: dict):
        return Book(**data)


def start_mappers():
    pass


class UserRepo(ABC):
    @abstractmethod
    def is_password_valid(self, user: User):
        pass

    @abstractmethod
    def get(self, username=None) -> User:
        pass

    @abstractmethod
    def delete(self, user: User):
        pass

    @abstractmethod
    def get_all(self, limit=10):
        pass

    @abstractmethod
    def save(self, user: User):
        pass

    @abstractmethod
    def encrypt_password(self, pwd):
        pass


class BookRepo(ABC):
    @abstractmethod
    def get(self, id=None) -> Book:
        pass

    @abstractmethod
    def get_all(self, limit=10):
        pass

    @abstractmethod
    def save(self, book: Book):
        pass

    @abstractmethod
    def next_id(self):
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


class AppContext(ABC):
    @property
    @abstractmethod
    def user_service(self) -> UserService:
        pass

    @property
    @abstractmethod
    def transaction_manager(self):
        pass

    @property
    @abstractmethod
    def metrics_service(self) -> MetricsService:
        pass

    @property
    @abstractmethod
    def book_repo(self) -> BookRepo:
        pass

    @property
    @abstractmethod
    def user_repo(self) -> UserRepo:
        pass

    @property
    @abstractmethod
    def config(self):
        pass

    @property
    @abstractmethod
    def book_service(self) -> BookService:
        pass
