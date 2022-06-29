from __future__ import annotations
import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List
import faker

from lorem_ipsum.serializers import to_json, from_json


class Events(Enum):
    BOOK_UPDATED = "book.updated"
    BOOK_DELETED = "book.deleted"
    BOOK_INDEXED = "book.indexed"


class BookViews(Enum):
    MY_BOOKS = "my_books"
    SHARED_BOOKS = "shared_books"

    @staticmethod
    def from_value(val: str):
        by_value = {member.value: member for name, member in BookViews.__members__.items()}
        return by_value[val]


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


@dataclass
class ObjectPermission(BaseModel):
    user_id: str
    object_id: str
    object_type: str
    permission_id: str


class User(BaseModel):
    def __init__(self, id: int, username: str, password_hash: str, email: str, login_type: str, role: Role):
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.id = id
        self.login_type = login_type
        self.role = role

    def as_dict(self):
        user = self.__dict__
        user['role'] = self.role.as_dict()
        return user

    @staticmethod
    def from_dict(data: dict):
        user = User(**data)
        user.role = Role.from_dict(data['role'])
        return user


class Permissions(Enum):
    BOOKS_ADD = 'books:add'
    BOOKS_READ = 'books:read'
    BOOKS_WRITE = 'books:write'
    USERS_ADMIN = 'users:admin'
    USERS_PROFILE = 'users:profile'


class ObjectType(Enum):
    BOOK = 'book'


class Permission(BaseModel):
    def __init__(self, id: str, name: str, roles: list[Role]):
        self.id = id
        self.name = name
        self.roles = roles

    def as_dict(self):
        perm = self.__dict__
        perm['roles'] = [role.as_dict() for role in self.roles]
        return perm

    def to_enum(self) -> Permissions:
        return Permissions(self.name)

    def __eq__(self, other):
        return other and other.id == self.id

    @staticmethod
    def from_dict(data: dict):
        permission = Permission(**data)
        permission.roles = [Role.from_dict(role) for role in data["roles"]]
        return permission

    @staticmethod
    def from_enum(perm: Permissions):
        return Permission(id=perm.value, name=perm.value, roles=[])


class Role(BaseModel):
    def __init__(self, id: str, name: str, default: bool, users: list[User], permissions: list[Permission]):
        self.id = id
        self.name = name
        self.default = default
        self.permissions = permissions
        self.users = users

    def as_dict(self):
        _role = self.__dict__
        _role['users'] = [user.as_dict() for user in self.users]
        _role['permissions'] = [perm.as_dict() for perm in self.permissions]
        return _role

    @staticmethod
    def from_dict(data: dict):
        role = Role(**data)
        role.users = [User.from_dict(user) for user in data['users']]
        role.permissions = [Permission.from_dict(perm) for perm in data['permissions']]
        return role

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions.append(perm)

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions.remove(perm)

    def reset_permissions(self):
        self.permissions = []

    def has_permission(self, perm):
        return perm in self.permissions


class BlacklistToken(BaseModel):
    def __init__(self, id: int, token: str, blacklisted_on: datetime):
        self.id = id
        self.token = token
        self.blacklisted_on = blacklisted_on

    @staticmethod
    def check_blacklist(auth_token: str, repo: BlacklistTokenRepo):
        # check whether auth token has been blacklisted
        result = repo.get(auth_token)
        if result is None:
            return False
        return True

    def as_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data: dict):
        return BlacklistToken(**data)


class Word(BaseModel):
    def __init__(self, id: str, name: str, index: str, count: int):
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
    def __init__(self, id: str, owner_id: str, author: str, title: str, no_of_pages: int, book: str):
        self.id = id
        self.owner_id = owner_id
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
    def random(no_of_pages: int, owner_id: str):
        _faker = faker.Faker()
        _book = {f'page_{page}': [_faker.text(max_nb_chars=100) for i in range(30)] for page in range(no_of_pages)}
        return {"author": _faker.name(),
                "title": _faker.text(max_nb_chars=100),
                "book": to_json(_book),
                "no_of_pages": no_of_pages,
                "owner_id": owner_id
                }


def start_mappers():
    pass


class BlacklistTokenRepo(ABC):
    @abstractmethod
    def get(self, auth_token: str):
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


class StatsRepo(ABC):
    @abstractmethod
    def get(self) -> Stats:
        pass


class BookRepo(ABC):
    @abstractmethod
    def get(self, id=None) -> Book:
        pass

    @abstractmethod
    def get_all(self, limit=10, offset=1, includes=None, owner_id=None, view=BookViews.MY_BOOKS):
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

    def share_book_with_user(self, book: Book, user: User):
        pass

    def get_permissions(self, book: Book) -> list[ObjectPermission]:
        pass


class MetricsService(ABC):
    @abstractmethod
    def metrics(self, fields: list = []):
        pass


@dataclass
class Stats:
    """Class for keeping track of an item in inventory."""
    no_of_books: int
    no_of_pages: int
    no_of_words: int

    def as_dict(self) -> dict:
        return self.__dict__


class StatsService:
    @abstractmethod
    def get(self) -> dict:
        pass


class BookService(ABC):
    @abstractmethod
    def get(self, id=None):
        pass

    @abstractmethod
    def get_all(self, id=None, limit=1, offset=1, includes=None, owner_id=None, view: BookViews = BookViews.MY_BOOKS):
        pass

    @abstractmethod
    def save(self, data_records):
        pass

    def delete(self, id: str):
        pass

    def random(self, no_of_pages: int, owner_id: str):
        pass

    def search(self, query: str):
        pass

    def share_book_with_user(self, id: str, username: str):
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
    def stats_service(self) -> StatsService:
        pass

    @property
    @abstractmethod
    def stats_repo(self) -> StatsRepo:
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
    def blacklist_token_repo(self) -> BlacklistTokenRepo:
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
