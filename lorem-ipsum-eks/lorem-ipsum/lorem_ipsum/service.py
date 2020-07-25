import sys
import threading

import lorem_ipsum
from lorem_ipsum.repo import transaction, User, Book
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
            pool = Transaction.pool()
            thread_count = 0
            for thread in threading.enumerate():
                # LOGGER.debug(thread)
                thread_count += 1
            _metrics = {
                'connection_pool._id': str(pool),
                'connection_pool.maxconn': pool._max_overflow,
                'connection_pool.minconn': pool._pool.maxsize,
                'connection_pool.usedconn': pool.checkedin(),
                'connection_pool.rusedconn': pool.checkedout(),
                'connection_pool.size': pool.size(),
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
        LOGGER.debug(f'using connection pool {Transaction.db()}')
        return self._app_context.book_repo.get(id).as_dict()

    @transaction
    def get_all(self, id=None, limit=1):
        LOGGER.debug(f'using connection pool {Transaction.db()}')
        results = self._app_context.book_repo.get_all(limit=limit)
        results['items'] = [book.as_dict() for book in results['items']]
        return results

    @transaction
    def save(self, data_records):
        saved_records = []
        for record in data_records:
            book_repo = self._app_context.book_repo
            book = None
            if record.get('id') is not None:
                book = book_repo.get(record['id'])
            if book is None:
                book = Book.from_dict(record)
            saved_records.append(book_repo.save(book).as_dict())
        return {'items': saved_records, 'total': len(saved_records)}


class UserService:
    def __init__(self, app_context: lorem_ipsum.AppContext):
        self._app_context = app_context

    @transaction
    def get(self, username=None):
        return self._app_context.user_repo.get(username).as_dict()

    @transaction
    def delete(self, username=None):
        user = self._app_context.user_repo.get(username)
        if user is not None:
            self._app_context.user_repo.delete(user)
        else:
            LOGGER.debug(f'User {username} does not exist. No delete performed.')
        return True

    @transaction
    def get_all(self, id=None, limit=1):
        results = self._app_context.user_repo.get_all(limit=limit)
        results['items'] = [user.as_dict() for user in results['items']]
        return results

    @transaction
    def save(self, data_records):
        saved_records = []
        for record in data_records:
            user_repo = self._app_context.user_repo
            user = user_repo.get(record['username'])
            if user is None:
                user = User.from_dict(record)
                user_repo.save(user)
            saved_records.append(user.as_dict())
        return {'items': saved_records, 'total': len(saved_records)}

    @transaction
    def validate(self, user):
        errors = {}
        if not self._app_context.user_repo.is_password_valid(User.from_dict(user)):
            errors['invalid_password'] = 'Invalid username or password.'
        return {'errors': errors}
