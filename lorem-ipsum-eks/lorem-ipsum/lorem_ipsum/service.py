import sys
import threading

import lorem_ipsum
from lorem_ipsum.repo import transaction
from lorem_ipsum.repo import Transaction
import logging

LOGGER = logging.getLogger('lorem-ipsum')


class MetricsService:
    def __init__(self, app_context: lorem_ipsum.AppContext):
        self._app_context = app_context

    def metrics(self):
        _metrics = {
            'connection_pool._id': "",
            'connection_pool.maxconn': 0,
            'connection_pool.minconn': 0,
            'connection_pool.usedconn': 0,
            'connection_pool.rusedconn': 0,
            'connection_pool.size': 0,
            'thread_count': 0,
        }
        try:
            pool = Transaction.connection_pool()
            thread_count = 0
            for thread in threading.enumerate():
                # LOGGER.debug(thread)
                thread_count += 1
            _metrics = {
                'connection_pool._id': str(pool),
                'connection_pool.maxconn': pool.maxconn,
                'connection_pool.minconn': pool.minconn,
                'connection_pool.usedconn': Transaction._connection_pool_stats['usedconn'],
                'connection_pool.rusedconn': len(pool._rused),
                'connection_pool.size': len(pool._pool),
                'thread_count': thread_count,
            }
            LOGGER.debug(_metrics)
        except:
            e = sys.exc_info()[0]
            LOGGER.exception('Could not get metrics...')
            print(e)
        return _metrics


class BookService:
    def __init__(self, app_context: lorem_ipsum.AppContext):
        self._app_context = app_context

    @transaction
    def get(self, id=None):
        LOGGER.debug(f'using connection pool {Transaction.connection_pool()}')
        return self._app_context.book_repo.get(id)

    @transaction
    def get_all(self, id=None, limit=1):
        LOGGER.debug(f'using connection pool {Transaction.connection_pool()}')
        return self._app_context.book_repo.get_all(limit=limit)

    @transaction
    def save(self, data_records):
        saved_records = []
        for record in data_records:
            saved_records.append(self._app_context.book_repo.save(record))
        return {'items': saved_records, 'total': len(saved_records)}
