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


def requires_permission(permissions: list):
    def requires_permission_decorator(function):
        def wrapper(*args, **kwargs):
            LOGGER.info(f'Authorization...\n{request.headers}')
            user_service = app_context().user_service
            authorization_header = request.headers['Authorization']
            if not authorization_header:
                LOGGER.debug('Authorization header not found.')
                return make_response('Invalid token.', 401)
            if 'Bearer ' not in authorization_header:
                LOGGER.debug('Bearer token not found.')
                return make_response('Invalid token.', 401)
            access_token = authorization_header.split(' ')[1]
            g.access_token = access_token
            payload = user_service.decode_auth_token(access_token)
            is_blacklisted_token = BlacklistToken.check_blacklist(access_token)
            if is_blacklisted_token:
                LOGGER.debug('Token blacklisted.')
                return make_response('Invalid token.', 401)
            LOGGER.debug(payload)
            if not payload.get('sub'):
                LOGGER.debug('Token missing sub.')
                return make_response('Forbidden.', 403)
            user = User.query.filter_by(username=payload['sub']).first()
            g.user = user
            if not user:
                LOGGER.debug('Token user not found.')
                return make_response('Forbidden.', 403)
            has_permissions = True
            for permission in permissions:
                if not user.role.has_permission(permission):
                    LOGGER.debug(f'Missing permission {permission}.')
                    has_permissions = False
            LOGGER.debug(f'Required permissions: {permissions}')
            if not has_permissions:
                return make_response('Forbidden.', 403)
            _result = function(*args, **kwargs)
            return _result

        wrapper.__name__ = function.__name__
        return wrapper

    return requires_permission_decorator


@token_auth.route('/login', methods=['GET'])
def login():
    user = User.query.filter_by(username=request.authorization.username).filter_by(
        login_type=LoginType.BASIC).first()
    if user is None or not user.verify_password(request.authorization.password):
        return make_response('Invalid username or password', 401)
    access_token = issue_token_for_user(user)
    LOGGER.debug(f'Access token {access_token}')
    return jsonify({'access_token': access_token}), 200


@token_auth.route('/logout', methods=['GET'])
@requires_permission([])
def logout():
    if not BlacklistToken.query.filter_by(token=g.access_token).first():
        blacklist_token = BlacklistToken(token=g.access_token)
        db.session.add(blacklist_token)
        db.session.commit()
    return jsonify('Logged out.'), 200


@token_auth.route('/register', methods=['POST'])
def register():
    _request = from_json(request.data.decode('utf-8'))
    if User.query.filter_by(username=_request['username']).first():
        return make_response('User already registered', 400)
    user = User(email=_request['email'],
                username=_request['username'],
                password=_request['password'])

    db.session.add(user)
    db.session.commit()
    access_token = issue_token_for_user(user)
    return jsonify({'access_token': access_token}), 200


@token_auth.route('/profile', methods=['GET'])
@requires_permission([Permission.PROFILE])
def profile():
    user = g.user
    return jsonify(user.to_json()), 200


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
