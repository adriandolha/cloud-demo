import logging
import uuid
from functools import lru_cache

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

import lorem_ipsum
from lorem_ipsum import AppContext

LOGGER = logging.getLogger('symptoms')


class Transaction:
    _connection_pool = None
    _connection_pool_stats = {'usedconn': 0}

    def __init__(self, app_context: lorem_ipsum.AppContext):
        self.connection = None
        self._cursor = None
        self.config = app_context.config

    @staticmethod
    def connection_pool() -> psycopg2.pool.ThreadedConnectionPool:
        return Transaction._connection_pool

    def __new_connection(self):
        connection = psycopg2.connect(user=self.config['aurora_user'],
                                      password=self.config['aurora_password'],
                                      host=self.config['aurora_host'],
                                      port=self.config['aurora_port'],
                                      database="covid19",
                                      cursor_factory=RealDictCursor)
        return connection

    def __new_connection_from_pool(self):
        connection = Transaction.connection_pool().getconn()
        Transaction._connection_pool_stats['usedconn'] = Transaction._connection_pool_stats['usedconn'] + 1
        return connection

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.connection.cursor()
        return self._cursor

    def __enter__(self):
        self.connection = self.__new_connection_from_pool()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.commit()
        except:
            self.connection.rollback()
        finally:
            # self.connection.close()
            Transaction.connection_pool().putconn(self.connection)
            Transaction._connection_pool_stats['usedconn'] = Transaction._connection_pool_stats['usedconn'] - 1

            if self._cursor is not None:
                LOGGER.debug(f'Closing cursor {self._cursor}')
                self._cursor.close()


class TransactionManager:
    def __init__(self, app_context: AppContext):
        self.config = app_context.config
        if Transaction._connection_pool is None:
            Transaction._connection_pool = psycopg2.pool.ThreadedConnectionPool(user=self.config['aurora_user'],
                                                                                password=self.config['aurora_password'],
                                                                                host=self.config['aurora_host'],
                                                                                port=self.config['aurora_port'],
                                                                                database="lorem-ipsum",
                                                                                cursor_factory=RealDictCursor,
                                                                                minconn=self.config.get(
                                                                                    'connection_pool_minconn', 1),
                                                                                maxconn=self.config.get(
                                                                                    'connection_pool_maxconn', 50))
            LOGGER.debug(f'Created connection pool {Transaction._connection_pool}')
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


class BookRepo:
    def __init__(self, app_context: lorem_ipsum.AppContext):
        self._transaction_manager = app_context.transaction_manager

    def db_setup(self):
        LOGGER.debug('Creating table...')
        _db_name = self._transaction_manager.config.get('db_name', 'lorem-ipsum')
        _cursor = self._transaction_manager.transaction.cursor
        # _cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{_db_name}'")
        # exists = _cursor.fetchone()
        # if not exists:
        #     _cursor.execute(f'CREATE DATABASE {_db_name}')
        _cursor.execute('CREATE TABLE IF NOT EXISTS public.books\
            (\
                id character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                author character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                title character varying(100) COLLATE pg_catalog."default" NOT NULL,\
                book jsonb NOT NULL,\
                CONSTRAINT book_pk PRIMARY KEY (id)\
            )')

        _cursor.execute('CREATE TABLE IF NOT EXISTS public.books\
            (\
                id character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                author character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                title character varying(100) COLLATE pg_catalog."default" NOT NULL,\
                book jsonb NOT NULL,\
                CONSTRAINT book_pk PRIMARY KEY (id)\
            )')

    def get(self, id=None, limit=10):
        items = []
        count = 0
        _cursor = self._transaction_manager.transaction.cursor
        if id is not None:
            _cursor.execute(
                'select *'
                'from books where id = %s',
                (id,))

            result = _cursor.fetchone()
            if result is not None:
                items.append(result)
                count = 1
        else:
            _cursor.execute('select count(*) from books')
            count = _cursor.fetchone()['count']
            _cursor.execute(f'select * from books limit {limit}')
            records = _cursor.fetchall()
            for record in records:
                items.append(record)
        return {"total": count, "items": items}

    def save(self, data=None):
        LOGGER.info(f'data = {data}')
        _data = dict(data)
        _cursor = self._transaction_manager.transaction.cursor
        _data['id'] = str(uuid.uuid4())
        _cursor.execute(
            "INSERT INTO books(id, author, title, book) "
            "VALUES (%s, %s, %s, %s)",
            (_data['id'],
             _data['author'],
             _data['title'],
             _data['book']))
        return _data
