from functools import lru_cache

import datetime
import logging

from authlib.jose import JsonWebKey, jwt
from flask import g, jsonify, Blueprint, request, make_response
from lorem_ipsum_auth import db, create_app_context
from lorem_ipsum_auth.models import LoginType, User, Permission, BlacklistToken
from lorem_ipsum_auth.serializers import from_json, to_json

LOGGER = logging.getLogger('lorem-ipsum')
token_auth = Blueprint('token_auth', __name__)
users = Blueprint('users', __name__)


def app_context():
    if 'app_context' not in g:
        g.app_context = create_app_context()
    return g.app_context


def new_token(payload: dict):
    with open(app_context().config['jwk_private_key_path'], 'rb') as f:
        key = JsonWebKey.import_key(f.read())
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


class AuthenticationError(ValueError):
    pass


class AuthorizationError(ValueError):
    pass


class BearerTokenValidator:
    def __init__(self, access_token):
        self.access_token = access_token
        user_service = app_context().user_service
        self.payload = user_service.decode_auth_token(access_token, get_jwk())

    def check_is_blacklisted(self):
        is_blacklisted_token = BlacklistToken.check_blacklist(self.access_token)
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
            if not user.role.has_permission(permission):
                LOGGER.debug(f'Missing permission {permission}.')
                has_permissions = False
        LOGGER.debug(f'Required permissions: {permissions}')
        if not has_permissions:
            raise AuthorizationError('Forbidden.')
        return self

    @staticmethod
    def from_authorization_header(authorization_header: str):
        if not authorization_header:
            LOGGER.debug('Authorization header not found.')
            raise AuthenticationError('Invalid token.')
        if 'Bearer ' not in authorization_header:
            LOGGER.debug('Bearer token not found.')
            raise AuthenticationError('Invalid token.')
        access_token = authorization_header.split('Bearer')[1].strip()
        LOGGER.debug(f'Bearer token is:\n"{access_token}"')
        return BearerTokenValidator(access_token)


def requires_permission(permissions: list):
    def requires_permission_decorator(function):
        def wrapper(*args, **kwargs):
            LOGGER.info(f'Authorization...\n{request.headers}')
            authorization_header = request.headers['Authorization']
            bearer_token_validator = BearerTokenValidator.from_authorization_header(authorization_header) \
                .check_is_blacklisted() \
                .check_username_claim()
            user = User.query.filter_by(username=bearer_token_validator.payload['sub']).first()

            bearer_token_validator.check_user_exists(user) \
                .check_has_permissions(user, permissions)
            g.access_token = bearer_token_validator.access_token
            g.user = user

            _result = function(*args, **kwargs)
            return _result

        wrapper.__name__ = function.__name__
        return wrapper

    return requires_permission_decorator


@token_auth.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _request = from_json(request.data.decode('utf-8'))
        username = _request['username']
        password = _request['password']
    else:
        username = request.authorization.username
        password = request.authorization.password

    user = User.query.filter_by(username=username).filter_by(
        login_type=LoginType.BASIC).first()
    if user is None or not user.verify_password(password):
        return jsonify('User already registered')('Invalid username or password'), 401
    access_token = issue_token_for_user(user)
    LOGGER.debug(f'Access token {access_token}')
    return jsonify({**user.to_json(), 'access_token': access_token}), 200


@token_auth.route('/signout', methods=['GET'])
@requires_permission([])
def logout():
    if not BlacklistToken.query.filter_by(token=g.access_token).first():
        blacklist_token = BlacklistToken(token=g.access_token)
        db.session.add(blacklist_token)
        db.session.commit()
    return jsonify('Logged out.'), 200


@token_auth.route('/signup', methods=['POST'])
def register():
    _request = from_json(request.data.decode('utf-8'))
    if User.query.filter_by(username=_request['username']).first():
        return jsonify('User already registered'), 400
    user = User(email=_request['email'],
                username=_request['username'],
                password=_request['password'])

    db.session.add(user)
    db.session.commit()
    access_token = issue_token_for_user(user)
    return jsonify({**user.to_json(), 'access_token': access_token}), 200


@token_auth.route('/profile', methods=['GET'])
@requires_permission([Permission.PROFILE])
def profile():
    user = g.user
    return jsonify(user.to_json()), 200


@lru_cache()
def get_jwk():
    LOGGER.debug('Loading jwk from public key...')
    key_data = None
    with open(app_context().config['jwk_public_key_path'], 'rb') as _key_file:
        key_data = _key_file.read()
    LOGGER.debug(key_data)
    key = JsonWebKey.import_key(key_data, {'kty': 'RSA'})
    return {'keys': [{**key.as_dict(), 'kid': 'demo_key'}]}


@token_auth.route('/.well-known/jwks.json', methods=['GET'])
def jwk():
    LOGGER.debug('JWK...')
    key = get_jwk()
    LOGGER.debug(key)
    LOGGER.debug(key)
    return jsonify(key)


@users.route('/<username>', methods=['DELETE'])
@requires_permission([Permission.ADMIN])
def delete_user(username):
    LOGGER.info('Delete user...')
    user = User.query.filter_by(username=username).first()
    if user:
        User.query.filter_by(username=username).delete()
    db.session.commit()
    return '', 204


@users.route('/<username>', methods=['GET'])
@requires_permission([Permission.ADMIN])
def get_user(username):
    LOGGER.info('Get user...')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify('Not found.'), 404
    return jsonify(user.to_json()), 200


@token_auth.after_request
def apply_cors(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response
