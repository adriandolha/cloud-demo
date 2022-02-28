from typing import List

import logging
import uuid
from sqlalchemy.sql import functions
from urllib.parse import quote

import bcrypt
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy import create_engine, JSON, Integer
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

import lorem_ipsum.model as model
from lorem_ipsum.model import AppContext
from lorem_ipsum.model import BookRepo
from lorem_ipsum.model import UserRepo
from lorem_ipsum.model import WordRepo
from lorem_ipsum.model import EventRepo
import sys
import inspect

from lorem_ipsum.serializers import from_json

LOGGER = logging.getLogger('lorem-ipsum')


def domain_model(function):
    def wrapper(self, *args, **kwargs):
        _model = function(self, *args, **kwargs)

        _model.__setattr__('_entity', self)

        def set_attr(_self, key, value):
            # print(f'set {object} {key}:{value}')
            _self.__dict__[key] = value
            if _self.__dict__.get('_entity') is not None:
                _self.__dict__['_entity'].__setattr__(key, value)

        _model.__class__.__setattr__ = set_attr

        return _model

    wrapper.__name__ = function.__name__
    return wrapper


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
        LOGGER.debug(f'New session {self.session}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            LOGGER.debug(f'Commit connection for session transaction {self.session}')
            self.session.commit()
        except:
            LOGGER.debug('Database error...')
            self.session.rollback()
            raise
        finally:
            LOGGER.debug(f'Closing connection for session {self.session}')
            self.session.close()


class TransactionManager:
    def __init__(self, app_context: AppContext):
        self.config = app_context.config

        if Transaction._db is None:
            user = self.config['aurora_user']
            password = self.config['aurora_password']
            host = self.config['aurora_host']
            port = self.config['aurora_port']
            database = self.config.get("database_name")
            minconn = self.config.get('connection_pool_minconn')
            maxconn = self.config.get('connection_pool_maxconn')
            _db = TransactionManager.create_db_engine(user=user, password=password, host=host, port=port,
                                                      database=database,
                                                      minconn=minconn, maxconn=maxconn)
            Transaction._db = _db
            Transaction._session_maker = sessionmaker(_db)
            LOGGER.debug(f'Created db {Transaction._db}')
        self._transaction = Transaction(app_context)

    @staticmethod
    def create_db_engine(user: str, password: str, host: str, port: str, database: str, minconn: str, maxconn: str):
        # we need to encode passowrd in case it contains special chars
        encoded_password = quote(password)
        _db = create_engine(f"postgres://{user}:{encoded_password}@{host}:{port}/{database}",
                            pool_size=minconn, max_overflow=maxconn - minconn, poolclass=QueuePool, echo=False)
        return _db

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


class Word(declarative_base()):
    __tablename__ = 'words'

    id = Column(String, primary_key=True)
    name = Column(String)
    index = Column(JSON)
    count = Column(Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @domain_model
    def as_model(self) -> model.Word:
        word = model.Word(self.id, self.name, self.index, self.count)
        return word

    def __eq__(self, other):
        return other and self.id == other.id

    @staticmethod
    def from_dict(data: dict):
        return Word(**data)

    @staticmethod
    def from_model(word: model.Word):
        word = Word(**word.as_dict())
        return word


class Event(declarative_base()):
    __tablename__ = 'events'

    id = Column(String, primary_key=True)
    name = Column(String)
    data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.id) for c in self.__table__.columns}

    @staticmethod
    def from_dict(data: dict):
        return Event(**data)

    def as_model(self) -> model.Event:
        return model.Event(self.id, self.name, self.data, self.created_at)

    @staticmethod
    def from_model(event: model.Event):
        return Event(**event.as_dict())


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

    @domain_model
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


class PostgresWordRepo(WordRepo):
    def __init__(self, app_context: AppContext):
        self._transaction_manager = app_context.transaction_manager

    def get(self, id=None) -> model.Word:
        _session = self._transaction_manager.transaction.session
        word = _session.query(Word).filter(Word.id == id).first()
        result = None
        if word:
            result = word.as_model()
        return result

    def delete(self, word: model.Word):
        _session = self._transaction_manager.transaction.session
        _user = _session.query(Word).filter(Word.id == word.id).first()
        _session.delete(_user)

    def get_all(self, limit=10, offset=1):
        _session = self._transaction_manager.transaction.session
        count = _session.query(Word).count()
        words = _session.query(Word).order_by(Word.count.desc()).limit(limit).offset(offset)
        return {"total": count, "items": [word.as_model() for word in words]}

    def save(self, word: model.Word) -> model.Word:
        _word = Word.from_model(word)
        LOGGER.info(f'data = {_word.as_dict()}')
        _session = self._transaction_manager.transaction.session
        _session.add(_word)
        return _word.as_model()

    def update_all(self, words: List[model.Word]):
        _session = self._transaction_manager.transaction.session
        word_entities = [word.__dict__.get('_entity') or Word.from_model(word) for word in words]
        _session.bulk_save_objects(word_entities)

    def find_by_ids(self, ids: List[str]):
        _session = self._transaction_manager.transaction.session
        count = _session.query(Word).filter(Word.id.in_(ids)).count()
        words = _session.query(Word).filter(Word.id.in_(ids)).order_by(Word.count.desc())
        return {"total": count, "items": [word.as_model() for word in words]}


class PostgresBookRepo(BookRepo):
    def next_id(self):
        return str(uuid.uuid4())

    def __init__(self, app_context: AppContext):
        self._transaction_manager = app_context.transaction_manager

    def get(self, id=None) -> model.Book:
        _session = self._transaction_manager.transaction.session
        book = _session.query(Book).filter(Book.id == id).first()
        return book.as_model() if book else None

    def get_all(self, limit=10, offset=1, includes=None):
        _session = self._transaction_manager.transaction.session
        count = _session.query(Book).count()
        page_count = None
        if includes == 'page_count':
            page_count = _session.query(
                functions.sum(Book.no_of_pages)
            ).scalar()
        books = _session.query(Book).limit(limit).offset(offset)
        return {"total": count, "page_count": page_count, "items": [book.as_model() for book in books]}

    def save(self, book: model.Book) -> model.Book:
        _book = Book.from_model(book)
        LOGGER.info(f'data = {_book}')
        _session = self._transaction_manager.transaction.session
        _session.add(_book)
        return _book.as_model()

    def delete(self, book: model.Book):
        _session = self._transaction_manager.transaction.session

        _book = book.__dict__.get('_entity') or _session.query(Book).filter(Book.id == book.id).first()

        _session.delete(_book)

    def search(self, query: str):
        _session = self._transaction_manager.transaction.session
        words = _session.query(Word).filter(Word.name.like(query)).all()
        LOGGER.info(words)
        book_ids = [item for sublist in [from_json(word.index) for word in words] for item in sublist]
        LOGGER.info(book_ids)
        count = len(book_ids)
        books = _session.query(Book).filter(Book.id.in_(book_ids)).limit(15).offset(0).all()
        return {"total": count, "items": [book.as_model() for book in books]}


class PostgresEventRepo(EventRepo):
    def next_id(self):
        return str(uuid.uuid4())

    def __init__(self, app_context: AppContext):
        self._transaction_manager = app_context.transaction_manager

    def get(self, id=None) -> model.Event:
        _session = self._transaction_manager.transaction.session
        event = _session.query(Event).filter(Event.id == id).first()
        return event.as_model() if event else None

    def get_all(self, limit=10, offset=1, event_type: model.Events = None):
        _session = self._transaction_manager.transaction.session
        count = _session.query(Event).count()
        events = _session.query(Event).filter(Event.name == str(model.Events.BOOK_UPDATED)).limit(limit).offset(offset)
        result = {"total": count, "items": [event.as_model() for event in events]}
        return result

    def save(self, event: model.Event) -> model.Event:
        _event = Event.from_model(event)
        LOGGER.info(f'data = {_event}')
        _session = self._transaction_manager.transaction.session
        _session.add(_event)
        return _event.as_model()

    def delete(self, event: model.Event):
        _session = self._transaction_manager.transaction.session
        _event = _session.query(Event).filter(Event.id == event.id).first()
        LOGGER.info(f'Deleting event {_event.id}')
        _session.delete(_event)


def create_database_if_not_exists(config: dict):
    user = config['postgres_user']
    password = config['postgres_password']
    host = config['aurora_host']
    port = config['aurora_port']
    database = config.get("postgres_database_name")
    minconn = config.get('connection_pool_minconn')
    maxconn = config.get('connection_pool_maxconn')
    _db = TransactionManager.create_db_engine(user=user, password=password, host=host, port=port,
                                              database=database,
                                              minconn=minconn, maxconn=maxconn)

    _db_name = config.get('database_name')
    conn = None
    try:
        conn = _db.connect()
        with conn:
            _result = conn.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{_db_name}'")
            exists = _result.cursor.fetchone()
            print(f'Database {_db_name} exists status is {exists}')
        conn = _db.connect()
        with conn:
            if not exists:
                conn.connection.set_isolation_level(
                    ISOLATION_LEVEL_AUTOCOMMIT
                )
                conn.execute(f"CREATE DATABASE {_db_name}")
    except:
        LOGGER.debug('Database setup error.')
        raise
    finally:
        if conn and not conn.closed:
            conn.close()


def db_setup(app_context: AppContext):
    LOGGER.info('Running database setup...')
    _db_name = app_context.config.get('database_name', 'postgres')
    _session = app_context.transaction_manager.transaction.session
    _session.execute('CREATE TABLE IF NOT EXISTS public.books\
            (\
                id character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                author character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                title character varying(100) COLLATE pg_catalog."default" NOT NULL,\
                no_of_pages integer NOT NULL,\
                book jsonb NOT NULL,\
                CONSTRAINT book_pk PRIMARY KEY (id)\
            )')

    _session.execute('CREATE TABLE IF NOT EXISTS public.users\
            (\
                username character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                password character varying(200) COLLATE pg_catalog."default" NOT NULL,\
                CONSTRAINT user_pk PRIMARY KEY (username)\
            )')
    _session.execute('CREATE TABLE IF NOT EXISTS public.words\
            (\
                id character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                name character varying(200) COLLATE pg_catalog."default" NOT NULL,\
                index jsonb NOT NULL,\
                count integer NOT NULL,\
                CONSTRAINT word_pk PRIMARY KEY (id)\
            )')
    _session.execute('CREATE TABLE IF NOT EXISTS public.events\
            (\
                id character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                name character varying(200) COLLATE pg_catalog."default" NOT NULL,\
                data jsonb NOT NULL,\
                created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,\
                CONSTRAINT event_pk PRIMARY KEY (id)\
            )')
    create_admin_user(app_context)


def create_admin_user(app_context):
    if app_context.user_repo.get(app_context.config['admin_user']) is None:
        password_plain = app_context.config['admin_password']
        password_encrypted = app_context.user_repo.encrypt_password(password_plain)
        app_context.user_repo.save(model.User.from_dict(
            {'username': app_context.config['admin_user'], 'password': password_encrypted}))
