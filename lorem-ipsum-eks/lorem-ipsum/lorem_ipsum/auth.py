import datetime
import logging
import os
from functools import lru_cache
from authlib.jose import JsonWebKey, jwt

from flask import g, request, jsonify
from lorem_ipsum.model import User, AppContext
import lorem_ipsum
from lorem_ipsum.model import Permission, BlacklistToken

LOGGER = logging.getLogger('lorem-ipsum')


def app_context():
    if 'app_context' not in g:
        g.app_context = lorem_ipsum.create_app_context()
    return g.app_context


@lru_cache()
def get_jwk():
    LOGGER.debug('Loading jwk from public key...')
    key_data = None
    with open(app_context().config['jwk_public_key_path'], 'rb') as _key_file:
        key_data = _key_file.read()
    LOGGER.debug(key_data)
    key = JsonWebKey.import_key(key_data, {'kty': 'RSA'})
    _jwks = {'keys': [{**key.as_dict(), 'kid': 'demo_key'}]}
    LOGGER.debug(_jwks)
    return _jwks


class AuthenticationError(ValueError):
    pass


class AuthorizationError(ValueError):
    pass


class BearerTokenValidator:
    def __init__(self, access_token, app_context: AppContext):
        self.access_token = access_token
        user_service = app_context.user_service
        self.blacklist_token_repo = app_context.blacklist_token_repo
        self.payload = user_service.decode_auth_token(access_token, get_jwk())

    def check_is_blacklisted(self):
        is_blacklisted_token = BlacklistToken.check_blacklist(self.access_token, self.blacklist_token_repo)
        if is_blacklisted_token:
            LOGGER.debug('Token blacklisted.')
            raise AuthenticationError('Invalid token.')
        return self

    def check_username_claim(self):
        if not self.payload.get('sub'):
            LOGGER.debug('Token missing sub.')
            raise AuthorizationError('Forbidden.')
        return self

    def check_user_exists(self, user):
        if not user:
            LOGGER.debug('Token user not found.')
            raise AuthorizationError('Forbidden.')
        return self

    def check_has_permissions(self, user: User, permissions: list):
        has_permissions = True
        for permission in permissions:
            if not user.role.has_permission(Permission.from_enum(permission)):
                LOGGER.debug(f'Missing permission {permission}.')
                has_permissions = False
        LOGGER.debug(f'Required permissions: {permissions}')
        if not has_permissions:
            raise AuthorizationError('Forbidden.')
        return self

    @staticmethod
    def from_authorization_header(authorization_header: str, app_context: AppContext):
        if not authorization_header:
            LOGGER.debug('Authorization header not found.')
            raise AuthenticationError('Invalid token.')
        if 'Bearer ' not in authorization_header:
            LOGGER.debug('Bearer token not found.')
            raise AuthenticationError('Invalid token.')
        access_token = authorization_header.split('Bearer')[1].strip()
        LOGGER.debug(f'Bearer token is:\n"{access_token}"')
        return BearerTokenValidator(access_token, app_context)


def should_skip_auth(flask_request):
    """
    Return true if should skip auth, e.g. when method is OPTIONS like when performing a React request.
    :param flask_request: Flask request.
    :return:
    """
    return flask_request.method in ['HEAD', 'OPTIONS']


def requires_permission(permissions: list):
    def requires_permission_decorator(function):
        def wrapper(*args, **kwargs):
            LOGGER.info(f'Authorization...\n{request.headers}')
            if should_skip_auth(request):
                return jsonify('ok')
            authorization_header = request.headers.get('Authorization')
            context = app_context()
            with context.transaction_manager.transaction:
                bearer_token_validator = BearerTokenValidator.from_authorization_header(authorization_header, context) \
                    .check_is_blacklisted() \
                    .check_username_claim()
                user = context.user_repo.get(username=bearer_token_validator.payload['sub'])

                bearer_token_validator.check_user_exists(user) \
                    .check_has_permissions(user, permissions)
                g.access_token = bearer_token_validator.access_token
                g.user = user

            _result = function(*args, **kwargs)
            return _result

        wrapper.__name__ = function.__name__
        return wrapper

    return requires_permission_decorator


class ExceptionHandlers:
    def __init__(self, app):
        @app.errorhandler(AuthorizationError)
        def handle_authorization_exception(e):
            """Return403 forbidden."""
            return jsonify(str(e)), 403

        @app.errorhandler(AuthenticationError)
        def handle_authentication_exception(e):
            """Return401 authentication error."""
            return jsonify(str(e)), 401


@lru_cache()
def jwk_key():
    jwk_path = os.environ.get('jwk_private_key_path') or app_context().config['jwk_private_key_path']
    with open(jwk_path, 'rb') as f:
        key = JsonWebKey.import_key(f.read())
    return key


def new_token(payload: dict):
    key = jwk_key()
    header = {'alg': 'RS256', 'kid': 'demo_key'}
    token = jwt.encode(header, payload, key)
    LOGGER.debug(token)
    return token.decode('utf-8')


def issue_token_for_user(user: User):
    access_token = new_token({
        "iss": "lorem.ipsum.dev",
        "aud": "lorem.ipsum.auth",
        "sub": user.username,
        "email": user.email,
        "roles": [
            user.role.name
        ],
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=4),
        "iat": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    return access_token
