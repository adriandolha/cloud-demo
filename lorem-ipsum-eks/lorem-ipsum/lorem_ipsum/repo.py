from __future__ import annotations
import datetime
import logging
import uuid
from typing import List
from urllib.parse import quote

import bcrypt
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import Column, String, DateTime, func, Boolean, Table, ForeignKey
from sqlalchemy import create_engine, JSON, Integer
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.pool import QueuePool
from sqlalchemy.sql import functions

import lorem_ipsum.model as model
from lorem_ipsum.model import AppContext
from lorem_ipsum.model import BlacklistTokenRepo
from lorem_ipsum.model import BookRepo
from lorem_ipsum.model import EventRepo
from lorem_ipsum.model import UserRepo
from lorem_ipsum.model import WordRepo
from lorem_ipsum.serializers import from_json

LOGGER = logging.getLogger('lorem-ipsum')

Base = declarative_base()


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
        _db = create_engine(f"postgresql://{user}:{encoded_password}@{host}:{port}/{database}",
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


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    login_type = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")
    email = Column(String)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c != User.password_hash}

    @staticmethod
    def from_dict(data: dict):
        user = User(**data)
        user.role = Role(**data['role'])
        return user

    def as_model(self) -> model.User:
        _user = model.User(self.id, self.username, self.password_hash, self.email, self.login_type, None)
        if self.role:
            _user.role = self.role.as_model(includes=['permissions'])
        return _user

    @staticmethod
    def from_model(user: model.User):
        user = User(**user.as_dict())
        user.role = Role.from_model(**user.role)
        return user


role_permissions = Table(
    'roles_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', String(64), ForeignKey('permissions.id'), primary_key=True))


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    default = Column(Boolean, default=False, index=True)
    permissions = relationship('Permission', secondary=role_permissions, back_populates="roles")
    users = relationship('User', back_populates="role")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = []

    def as_model(self, includes: list = ('users', 'permissions')) -> model.Role:
        _role = model.Role(self.id, self.name, self.default, [], [])
        _users = [user.as_model() for user in self.users] if 'users' in includes else []
        _permissions = [permission.as_model(includes=[]) for permission in
                        self.permissions] if 'permissions' in includes else []
        _role.permissions = _permissions
        _role.users = _users
        return _role

    @staticmethod
    def from_model(role: model.Role):
        _role = Role(**role.as_dict())
        _role.users = [User.from_model(user) for user in role.users]
        _role.permissions = [Permission.from_model(perm) for perm in role.permissions]
        return role


class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(String(100), primary_key=True)
    name = Column(String(100), unique=True)
    roles = relationship('Role', secondary=role_permissions, back_populates="permissions")

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)

    def __eq__(self, other):
        return other and other.id == self.id

    def as_model(self, includes: list = ('roles')) -> model.Permission:
        permission = model.Permission(self.id, self.name, [])

        _roles = [role.as_model() for role in self.roles] if 'roles' in includes else []
        permission.roles = _roles
        return permission

    @staticmethod
    def from_model(perm: model.Permission) -> Permission:
        permission = Permission(**perm.as_dict())
        _roles = [Role.from_model(role) for role in perm.roles]
        permission.roles = _roles
        return permission

    @staticmethod
    def from_str(perm: str):
        return Permission(id=perm, name=perm)


class BlacklistToken(Base):
    """
    Token Model for storing blacklisted JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(2000), unique=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    def as_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def from_dict(data: dict):
        return BlacklistToken(**data)

    def as_model(self) -> model.BlacklistToken:
        return model.BlacklistToken(self.id, self.token, self.blacklisted_on)

    @staticmethod
    def from_model(blacklist_token: model.BlacklistToken):
        return BlacklistToken(**blacklist_token.as_dict())


class Word(Base):
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


class Event(Base):
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


class Book(Base):
    __tablename__ = 'books'

    id = Column(String, primary_key=True)
    owner_id = Column(String)
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
        return model.Book(self.id, self.owner_id, self.author, self.title, self.no_of_pages, self.book)

    @staticmethod
    def from_model(book: model.Book):
        return Book(**book.as_dict())


class PostgresBlacklistTokenRepo(BlacklistTokenRepo):
    def __init__(self, app_context: AppContext):
        self._transaction_manager = app_context.transaction_manager

    def get(self, auth_token: str) -> model.BlacklistToken:
        _session = self._transaction_manager.transaction.session
        _token = _session.query(BlacklistToken).filter(BlacklistToken.token == auth_token).first()
        return _token.as_model() if _token else None


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

    def get_all(self, limit=10, offset=1, includes=None, owner_id=None):
        _session = self._transaction_manager.transaction.session
        count = _session.query(Book).count()
        page_count = None
        if includes == 'page_count':
            page_count = _session.query(
                functions.sum(Book.no_of_pages)
            ).scalar()
        if owner_id:
            books = _session.query(Book).filter(Book.owner_id == owner_id).limit(limit).offset(offset)
        else:
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
                owner_id character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                author character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                title character varying(100) COLLATE pg_catalog."default" NOT NULL,\
                no_of_pages integer NOT NULL,\
                book jsonb NOT NULL,\
                CONSTRAINT book_pk PRIMARY KEY (id)\
            )')

    # _session.execute('CREATE TABLE IF NOT EXISTS public.users\
    #         (\
    #             username character varying(50) COLLATE pg_catalog."default" NOT NULL,\
    #             password character varying(200) COLLATE pg_catalog."default" NOT NULL,\
    #             CONSTRAINT user_pk PRIMARY KEY (username)\
    #         )')
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
    # create_admin_user(app_context)


def create_admin_user(app_context):
    if app_context.user_repo.get(app_context.config['admin_user']) is None:
        password_plain = app_context.config['admin_password']
        password_encrypted = app_context.user_repo.encrypt_password(password_plain)
        app_context.user_repo.save(model.User.from_dict(
            {'username': app_context.config['admin_user'], 'password': password_encrypted}))
