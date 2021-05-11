import logging
import uuid

import bcrypt
from sqlalchemy import Column, String
from sqlalchemy import create_engine, JSON, Integer
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from lorem_ipsum.model import UserRepo
from lorem_ipsum.model import BookRepo
from lorem_ipsum.model import AppContext
import lorem_ipsum.model as model


LOGGER = logging.getLogger('lorem-ipsum')


class Transaction:
    _db = None
    _session_maker = None
    _connection_pool_stats = {'usedconn': 0}

    def __init__(self, app_context: AppContext):
        self._session = None
        self.config = app_context.config

    @staticmethod
    def db() -> Engine:
        return Transaction._db

    @staticmethod
    def pool() -> QueuePool:
        return Transaction._db.pool

    def __new_session(self):
        return Transaction._session_maker()

    @property
    def session(self) -> Session:
        return self._session

    def __enter__(self):
        self._session = self.__new_session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            LOGGER.debug(f'Commit connection for session transaction {self.session.transaction}')
            self.session.commit()
        except:
            print('Database error...')
            self.session.rollback()
            raise
        finally:
            LOGGER.debug(f'Closing connection for session {self.session.transaction}')
            self.session.close()


class TransactionManager:
    def __init__(self, app_context: AppContext):
        self.config = app_context.config

        if Transaction._db is None:
            user = self.config['aurora_user']
            password = self.config['aurora_password']
            host = self.config['aurora_host']
            port = self.config['aurora_port']
            database = "lorem-ipsum"
            minconn = self.config.get('connection_pool_minconn')
            maxconn = self.config.get('connection_pool_maxconn')
            _db = create_engine(f"postgres://{user}:{password}@{host}:{port}/{database}",
                                pool_size=minconn, max_overflow=maxconn - minconn, poolclass=QueuePool, echo=False)
            Transaction._db = _db
            Transaction._session_maker = sessionmaker(_db)
            LOGGER.debug(f'Created db {Transaction._db}')
        self._transaction = Transaction(app_context)

    @property
    def transaction(self) -> Transaction:
        return self._transaction


def transaction(function):
    def wrapper(self, *args, **kwargs):
        _result = None
        with self._app_context.transaction_manager.transaction as _tm:
            _result = function(self, *args, **kwargs)
        return _result

    return wrapper


class User(declarative_base()):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c != User.password}

    @staticmethod
    def from_dict(data: dict):
        return User(**data)

    def as_model(self) -> model.User:
        return model.User(self.username, self.password)

    @staticmethod
    def from_model(user: model.User):
        return User(**user.as_dict())


class Book(declarative_base()):
    __tablename__ = 'books'

    id = Column(String, primary_key=True)
    author = Column(String)
    title = Column(String)
    no_of_pages = Column(Integer)
    book = Column(JSON)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def from_dict(data: dict):
        return Book(**data)

    def as_model(self) -> model.Book:
        return model.Book(self.id, self.author, self.title, self.no_of_pages, self.book)

    @staticmethod
    def from_model(book: model.Book):
        return Book(**book.as_dict())


class PostgresUserRepo(UserRepo):
    def __init__(self, app_context: AppContext):
        self._transaction_manager = app_context.transaction_manager

    def is_password_valid(self, user: model.User):
        _user = User.from_model(user)
        _session = self._transaction_manager.transaction.session
        result = _session.query(User).filter(
            User.username == _user.username and User.password == _user.password).first()
        if result is None:
            return False
        return True

    def get(self, username=None) -> model.User:
        _session = self._transaction_manager.transaction.session
        user = _session.query(User).filter(User.username == username).first()
        result = None
        if user:
            result = user.as_model()
        return result

    def delete(self, user: model.User):
        _session = self._transaction_manager.transaction.session
        _user = _session.query(User).filter(User.username == user.username).first()
        _session.delete(_user)

    def get_all(self, limit=10):
        _session = self._transaction_manager.transaction.session
        count = _session.query(User).count()
        users = _session.query(User).limit(limit)
        return {"total": count, "items": [user.as_model() for user in users]}

    def save(self, user: model.User) -> model.User:
        _user = User.from_model(user)
        LOGGER.info(f'data = {_user.as_dict()}')
        _session = self._transaction_manager.transaction.session
        _session.add(_user)
        return _user.as_model()

    def encrypt_password(self, pwd):
        encrypted_password = bcrypt.hashpw(password=pwd.encode('utf-8'),
                                           salt=self._transaction_manager.config['password_encryption_key'].encode(
                                               'utf-8'))
        return encrypted_password


class PostgresBookRepo(BookRepo):
    def next_id(self):
        return str(uuid.uuid4())

    def __init__(self, app_context: AppContext):
        self._transaction_manager = app_context.transaction_manager

    def get(self, id=None) -> model.Book:
        _session = self._transaction_manager.transaction.session
        book = _session.query(Book).filter(Book.id == id).first()
        return book.as_model() if book else None

    def get_all(self, limit=10):
        items = []
        _session = self._transaction_manager.transaction.session
        count = _session.query(Book).count()
        books = _session.query(Book).limit(limit)
        return {"total": count, "items": [book.as_model() for book in books]}

    def save(self, book: model.Book) -> model.Book:
        _book = Book.from_model(book)
        LOGGER.info(f'data = {_book}')
        _session = self._transaction_manager.transaction.session
        _session.add(_book)
        return _book.as_model()


def db_setup(app_context: AppContext):
    LOGGER.debug('Creating table...')
    _db_name = app_context.config.get('db_name', 'lorem-ipsum')
    _cursor = app_context.transaction_manager.transaction.session
    # _cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{_db_name}'")
    # exists = _cursor.fetchone()
    # if not exists:
    #     _cursor.execute(f'CREATE DATABASE {_db_name}')
    _cursor.execute('CREATE TABLE IF NOT EXISTS public.books\
        (\
            id character varying(50) COLLATE pg_catalog."default" NOT NULL,\
            author character varying(50) COLLATE pg_catalog."default" NOT NULL,\
            title character varying(100) COLLATE pg_catalog."default" NOT NULL,\
            no_of_pages integer NOT NULL,\
            book jsonb NOT NULL,\
            CONSTRAINT book_pk PRIMARY KEY (id)\
        )')

    _cursor.execute('CREATE TABLE IF NOT EXISTS public.users\
        (\
            username character varying(50) COLLATE pg_catalog."default" NOT NULL,\
            password character varying(200) COLLATE pg_catalog."default" NOT NULL,\
            CONSTRAINT user_pk PRIMARY KEY (username)\
        )')
    if app_context.user_repo.get(app_context.config['admin_user']) is None:
        password_plain = app_context.config['admin_password']
        password_encrypted = app_context.user_repo.encrypt_password(password_plain)
        app_context.user_repo.save(model.User.from_dict(
            {'username': app_context.config['admin_user'], 'password': password_encrypted}))
