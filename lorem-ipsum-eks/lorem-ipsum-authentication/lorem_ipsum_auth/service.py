from abc import ABC, abstractmethod
from functools import lru_cache

import sys
import threading

import lorem_ipsum_auth
from lorem_ipsum_auth.repo import transaction, User
from lorem_ipsum_auth.repo import Transaction
import logging
from authlib.jose import JsonWebKey
from authlib.jose import JWK_ALGORITHMS
from authlib.jose import jwt

LOGGER = logging.getLogger('lorem-ipsum')


class MetricsService:
    def __init__(self, app_context: lorem_ipsum_auth.AppContext):
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


class UserService:
    def __init__(self, app_context: lorem_ipsum_auth.AppContext):
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
    def secret_key(self):
        with open(self._app_context.config['jwk_public_key_path'], 'rb') as f:
            key = f.read()
        # return key
        return "GZqgnQYylZ8Kuf2HxB11rd50ajGlLhDa2iSZkm4ZihHLH8vd73oNbIqXdGVT7GNY"

    def decode_auth_token(self, auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        return self._app_context.authenticator.decode_auth_token(auth_token)


class Authenticator(ABC):
    @abstractmethod
    def decode_auth_token(self, auth_token):
        pass
