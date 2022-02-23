import faker
import logging
import threading
from functools import lru_cache

import sys
from authlib.jose import jwt

import lorem_ipsum.model
from lorem_ipsum.model import MetricsService, BookService, UserService, WordService
from lorem_ipsum.model import User, Book
from lorem_ipsum.repo import Transaction, transaction, Word
from lorem_ipsum.serializers import to_json

LOGGER = logging.getLogger('lorem-ipsum')


class DefaultMetricsService(MetricsService):
    def __init__(self, app_context: lorem_ipsum.model.AppContext):
        self._app_context = app_context

    def metrics(self, fields: list = []):
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
            threads = []
            for thread in threading.enumerate():
                threads.append(str(thread))
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
            if 'connections' in fields:
                _metrics.update({
                    'connection_pool.connections': [str(conn) for conn in pool._pool.queue]
                })
            if 'threads' in fields:
                _metrics.update({
                    'threads': threads
                })
            LOGGER.debug(_metrics)
        except:
            e = sys.exc_info()[0]
            LOGGER.exception('Could not get metrics...')
            print(e)
        return _metrics


class DefaultBookService(BookService):
    def __init__(self, app_context: lorem_ipsum.model.AppContext):
        self._app_context = app_context

    @transaction
    def get(self, id=None):
        LOGGER.debug(f'using connection pool {Transaction.db()}')
        return self._app_context.book_repo.get(id).as_dict()

    @transaction
    def get_all(self, id=None, limit=1, offset=1):
        LOGGER.debug(f'using connection pool {Transaction.db()}')
        results = self._app_context.book_repo.get_all(limit=limit, offset=offset)
        results['items'] = [book.as_dict() for book in results['items']]
        return results

    @transaction
    def delete(self, id: str = None):
        _book = self._app_context.book_repo.get(id)
        self._app_context.book_repo.delete(_book)
        return True

    def random(self, no_of_pages: int):
        _faker = faker.Faker()
        _book = {f'page_{page}': [_faker.text(max_nb_chars=100) for i in range(30)] for page in range(no_of_pages)}
        return {"author": _faker.name(),
                "title": _faker.text(max_nb_chars=100),
                "book": to_json(_book),
                "no_of_pages": no_of_pages,
                }

    @transaction
    def save(self, data_records):
        saved_records = []
        for record in data_records:
            book_repo = self._app_context.book_repo
            book = None
            if record.get('id') is not None:
                book = book_repo.get(record['id'])
            if book is None:
                record['id'] = self._app_context.book_repo.next_id()
                book = Book.from_dict(record)
            saved_records.append(book_repo.save(book).as_dict())
        return {'items': saved_records, 'total': len(saved_records)}


class DefaultUserService(UserService):
    def __init__(self, app_context: lorem_ipsum.model.AppContext):
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

    @lru_cache()
    def public_key(self):
        key = None

        with open(self._app_context.config['jwk_public_key_path'], 'rb') as f:
            key = f.read()
        return key

    def decode_auth_token(self, auth_token, jwks=None):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            if jwks:
                payload = jwt.decode(auth_token, jwks)
            else:
                payload = jwt.decode(auth_token, self.public_key())
            return payload
        except:
            LOGGER.exception('token is invalid', exc_info=True)
            raise Exception('token is invalid')


class DefaultWordService(WordService):
    def __init__(self, app_context: lorem_ipsum.model.AppContext):
        self._app_context = app_context

    @transaction
    def get(self, id=None):
        return self._app_context.word_repo.get(id).as_dict()

    @transaction
    def delete(self, username=None):
        user = self._app_context.user_repo.get(username)
        if user is not None:
            self._app_context.user_repo.delete(user)
        else:
            LOGGER.debug(f'User {username} does not exist. No delete performed.')
        return True

    @transaction
    def get_all(self, id=None, limit=10, offset=1):
        results = self._app_context.word_repo.get_all(limit=limit, offset=offset)
        results['items'] = [word.as_dict() for word in results['items']]
        return results

    @transaction
    def save(self, data_records):
        saved_records = []
        for record in data_records:
            word_repo = self._app_context.word_repo
            word = word_repo.get(record['id'])
            if word is None:
                word = Word.from_dict(record)
                word_repo.save(word)
            saved_records.append(word.as_dict())
        return {'items': saved_records, 'total': len(saved_records)}
