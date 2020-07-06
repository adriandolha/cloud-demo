import logging
import uuid
from functools import lru_cache

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

import covid19_symptoms
from covid19_symptoms import AppContext

LOGGER = logging.getLogger('symptoms')


class Transaction:
    _connection_pool = None
    _connection_pool_stats = {'usedconn': 0}

    def __init__(self, app_context: covid19_symptoms.AppContext):
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
                                                                                database="covid19",
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


class SymptomRepo:
    def __init__(self, app_context: covid19_symptoms.AppContext):
        self._transaction_manager = app_context.transaction_manager

    def create_table(self):
        LOGGER.debug('Creating table...')
        _cursor = self._transaction_manager.transaction.cursor
        _cursor.execute('CREATE TABLE IF NOT EXISTS public.symptoms\
            (\
                contact boolean NOT NULL,\
                cough boolean NOT NULL,\
                fever boolean NOT NULL,\
                id character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                red_zone_travel boolean NOT NULL,\
                tiredness boolean NOT NULL,\
                difficulty_breathing boolean NOT NULL,\
                CONSTRAINT symptoms_pk PRIMARY KEY (id)\
            )')

    def get(self, id=None, limit=10):
        items = []
        count = 0
        _cursor = self._transaction_manager.transaction.cursor
        if id is not None:
            _cursor.execute(
                'select *'
                'from symptoms where id = %s',
                (id,))

            result = _cursor.fetchone()
            if result is not None:
                items.append(result)
                count = 1
        else:
            _cursor.execute('select count(*) from symptoms')
            count = _cursor.fetchone()['count']
            _cursor.execute(f'select * from symptoms limit {limit}')
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
            "INSERT INTO symptoms(id, contact, red_zone_travel, fever, cough, tiredness,difficulty_breathing) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (_data['id'],
             _data['contact'],
             _data['red_zone_travel'],
             _data['fever'],
             _data['cough'],
             _data['tiredness'],
             _data['difficulty_breathing']))
        return _data
