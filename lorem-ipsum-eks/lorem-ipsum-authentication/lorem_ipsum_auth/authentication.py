import json
import logging
from functools import lru_cache
from urllib.request import urlopen

from authlib.jose import jwt

import lorem_ipsum_auth
from lorem_ipsum_auth.service import Authenticator

LOGGER = logging.getLogger('lorem-ipsum')


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class Auth0Authenticator(Authenticator):
    def __init__(self, app_context: lorem_ipsum_auth.AppContext):
        self._app_context = app_context

    @lru_cache()
    def secret_key(self):
        with open(self._app_context.config['jwk_public_key_path'], 'rb') as f:
            key = f.read()
        # return key
        return "GZqgnQYylZ8Kuf2HxB11rd50ajGlLhDa2iSZkm4ZihHLH8vd73oNbIqXdGVT7GNY"

    @lru_cache()
    def _jwks(self):
        jsonurl = urlopen("https://dev-5z89rql0.eu.auth0.com/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        return jwks

    @lru_cache()
    def _pulic_key(self):
        with open(self._app_context.config['jwk_public_key_path'], "r") as pk_file:
            pk = pk_file.read()
        LOGGER.debug(pk)
        return pk

    def decode_auth_token(self, auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            LOGGER.debug(auth_token)
            payload = jwt.decode(auth_token, self._pulic_key())
            return payload
        except:
            LOGGER.exception('token is invalid', exc_info=True)
            raise Exception('token is invalid')
