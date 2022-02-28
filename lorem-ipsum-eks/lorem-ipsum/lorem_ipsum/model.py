from collections import Counter
from enum import Enum

from typing import List

import re

import faker
from abc import ABC, abstractmethod

from lorem_ipsum.serializers import to_json, from_json
import datetime


class Events(Enum):
    BOOK_UPDATED = "book.updated"
    BOOK_DELETED = "book.deleted"
    BOOK_INDEXED = "book.indexed"


def model_as_dict_(object):
    if object is None:
        return None
    return {k: v for k, v in object.__dict__.items() if not k.startswith('_')}


class BaseModel:
    def model_as_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


class Event:
    def __init__(self, id: str, name: str, data: str, created_at: datetime.datetime = None):
        self.id = id
        self.name = name
        self.data = data
        self.created_at = created_at

    def as_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data: dict):
        return Event(**data)


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def as_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data: dict):
        return User(**data)


class Word(BaseModel):
    def __init__(self, id: str, name: str, index:str, count: int):
        self.id = id
        self.name = name
        self.index = index
        self.count = count

    def as_dict(self):
        return BaseModel.model_as_dict(self)

    def __eq__(self, other):
        return other and self.id == other.id

    @staticmethod
    def from_dict(data: dict):
        return Word(**data)


class Book(BaseModel):
    def __init__(self, id: str, author: str, title: str, no_of_pages: int, book: str):
        self.id = id
        self.author = author
        self.title = title
        self.no_of_pages = no_of_pages
        self.book = book

    def as_dict(self):
        return BaseModel.model_as_dict(self)

    @property
    def text(self):
        book_text = ' '.join([' '.join(text) for (page, text) in from_json(self.book).items()])
        return book_text

    @staticmethod
    def from_dict(data: dict):
        return Book(**data)

    @staticmethod
    def random(no_of_pages: int):
        _faker = faker.Faker()
        _book = {f'page_{page}': [_faker.text(max_nb_chars=100) for i in range(30)] for page in range(no_of_pages)}
        return {"author": _faker.name(),
                "title": _faker.text(max_nb_chars=100),
                "book": to_json(_book),
                "no_of_pages": no_of_pages,
                }


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


class WordRepo(ABC):
    @abstractmethod
    def get(self, id=None) -> Word:
        pass

    @abstractmethod
    def delete(self, word: Word):
        pass

    @abstractmethod
    def get_all(self, limit=10, offset=1):
        pass

    @abstractmethod
    def save(self, word: Word):
        pass

    @abstractmethod
    def update_all(self, words: List[Word]):
        pass

    @abstractmethod
    def find_by_ids(self, ids: List[str]):
        pass


class BookRepo(ABC):
    @abstractmethod
    def get(self, id=None) -> Book:
        pass

    @abstractmethod
    def get_all(self, limit=10, offset=1, includes=None):
        pass

    @abstractmethod
    def save(self, book: Book):
        pass

    @abstractmethod
    def next_id(self):
        pass

    def delete(self, book: Book):
        pass

    def search(self, query: str):
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
    def get_all(self, id=None, limit=1, offset=1, includes=None):
        pass

    @abstractmethod
    def save(self, data_records):
        pass

    def delete(self, id: str):
        pass

    def random(self, no_of_pages: int):
        pass

    def search(self, query: str):
        pass

class WordService(ABC):
    @abstractmethod
    def get(self, id=None):
        pass

    @abstractmethod
    def get_all(self, id=None, limit=1, offset=1):
        pass

    @abstractmethod
    def save(self, data_records):
        pass

    def delete(self, id: str):
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
    def public_key(self):
        pass

    @abstractmethod
    def decode_auth_token(self, auth_token, jwks: dict):
        """
        Decodes the auth token
        :param jwks: JWK keys created from public key
        :param auth_token:
        :return: integer|string
        """
        pass


class EventService(ABC):
    @abstractmethod
    def get(self, id=None):
        pass

    @abstractmethod
    def delete(self, id=None):
        pass

    @abstractmethod
    def get_all(self, id=None, limit=1):
        pass

    @abstractmethod
    def save(self, event: Event):
        pass


class EventRepo(ABC):
    @abstractmethod
    def get(self, id=None) -> Event:
        pass

    @abstractmethod
    def get_all(self, limit=10, offset=1) -> dict:
        pass

    @abstractmethod
    def save(self, event: Event):
        pass

    @abstractmethod
    def next_id(self):
        pass

    def delete(self, event: Event):
        pass


class AppContext(ABC):
    def __init__(self):
        pass

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
    def event_repo(self) -> EventRepo:
        pass

    @property
    @abstractmethod
    def word_repo(self) -> WordRepo:
        pass

    @property
    @abstractmethod
    def config(self):
        pass

    @property
    @abstractmethod
    def book_service(self) -> BookService:
        pass

    @property
    @abstractmethod
    def word_service(self) -> WordService:
        pass

    @abstractmethod
    def run_database_setup(self):
        pass
