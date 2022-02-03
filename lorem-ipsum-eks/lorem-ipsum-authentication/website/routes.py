import json
import logging
from collections import namedtuple

import time
import uuid
from functools import lru_cache
from authlib.integrations.flask_client import OAuth
from authlib.integrations.flask_oauth2 import current_token
from authlib.jose import JsonWebKey, jwt
from authlib.oauth2 import OAuth2Error
from flask import Blueprint, request, session, url_for, g
from flask import current_app as app
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from flask import _app_ctx_stack

import lorem_ipsum_auth
from .models import db, User, OAuth2Client, OAuth2Token
from .oauth2 import authorization, require_oauth

bp = Blueprint('home', __name__)
LOGGER = logging.getLogger('lorem-ipsum')


def app_context():
    if 'app_context' not in g:
        g.app_context = lorem_ipsum_auth.AppContext.local_context()

    return g.app_context


oauth_ = OAuth(app)


def oauth():
    if 'oauth' not in g:
        g.oauth = oauth_
    return g.oauth


@lru_cache()
def get_jwk():
    LOGGER.debug('Loading jwk from public key...')
    key_data = None
    with open(app_context().config['jwk_public_key_path'], 'rb') as _key_file:
        key_data = _key_file.read()
    _jwk = JsonWebKey.import_key(key_data, {'kty': 'RSA', 'use': 'sig', 'alg': 'RS256',
                                            'kid': 'demo_key', 'iss': 'lorem.ipsum.dev'})
    _key_dict = _jwk.as_dict()
    LOGGER.debug(_key_dict)
    return {'keys': [_key_dict]}


def response(api_response):
    return app.response_class(response=api_response['body'], status=api_response['status_code'])


def api_context(event, context):
    if not event:
        event = {}
    if not context:
        context = {}
    return {
        'user_id': str(uuid.uuid4()),
        'body': event.get('body') or {},
        'path_parameters': event.get('pathParameters') or {}
    }


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]


@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        update_current_user(username)
        # if user is not just to log in, but need to head back to the auth page, then go for it
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect('/')
    user = current_user()
    if user:
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []

    return render_template('home.html', user=user, clients=clients)


def update_current_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    session['id'] = user.id
    return current_user()


@bp.route('/logout')
def logout():
    del session['id']
    return redirect('/')


@bp.route('/create_client', methods=('GET', 'POST'))
def create_client():
    user = current_user()
    if not user:
        return redirect('/')
    if request.method == 'GET':
        return render_template('create_client.html')

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user.id,
    )

    form = request.form
    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form["client_uri"],
        "grant_types": split_by_crlf(form["grant_type"]),
        "redirect_uris": split_by_crlf(form["redirect_uri"]),
        "response_types": split_by_crlf(form["response_type"]),
        "scope": form["scope"],
        "token_endpoint_auth_method": form["token_endpoint_auth_method"]
    }
    client.set_client_metadata(client_metadata)

    if form['token_endpoint_auth_method'] == 'none':
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)

    db.session.add(client)
    db.session.commit()
    return redirect('/')


@bp.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    user = current_user()
    # if user log status is not true (Auth server), then to log it in
    if not user:
        return redirect(url_for('website.routes.home', next=request.url))
    if request.method == 'GET':
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error
        return render_template('authorize.html', user=user, grant=grant)
    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return authorization.create_authorization_response(grant_user=grant_user)


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    _response = authorization.create_token_response()
    return _response


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


@bp.route('/api/me')
@require_oauth('profile')
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.username)


@bp.route('/health')
def health():
    return jsonify(result="all good")


@bp.route('/.well-known/jwks.json', methods=['GET'])
def jwk():
    LOGGER.debug('JWK...')
    key = get_jwk()

    LOGGER.debug(key)
    LOGGER.debug(key)
    return response({"status_code": '200', 'body': json.dumps(key)})


def new_token(payload: dict):
    with open(app_context().config['jwk_private_key_path'], 'rb') as f:
        key = JsonWebKey.import_key(f.read())
    header = {'alg': 'RS256', 'kid': 'demo_key'}
    token = jwt.encode(header, payload, key)
    LOGGER.debug(token)
    return token.decode('utf-8')


@bp.route('/token', methods=['POST'])
def token():
    payload = json.loads(request.data.decode('utf-8'))
    LOGGER.debug(f'New access token with payload {payload}')
    _token = new_token(payload)
    LOGGER.debug(_token)
    return response({"status_code": '200', 'body': json.dumps({'access_token': _token})})


@bp.route('/google/')
def google():
    # Google Oauth Config
    # Get client_id and client_secret from environment variables
    # For developement purpose you can directly put it
    # here inside double quotes
    _app_context = app_context()
    GOOGLE_CLIENT_ID = _app_context.config.get('google_client_id')
    GOOGLE_CLIENT_SECRET = _app_context.config.get('google_client_secret')

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth().register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('home.google_auth', _external=True)
    return oauth().google.authorize_redirect(f'{redirect_uri}')


@bp.route('/google/auth/')
def google_auth():
    _config = app_context().config
    client_id = _config['google_client_id']
    client_secret = _config['google_client_secret']
    _token = oauth().google.authorize_access_token()
    user = oauth().google.parse_id_token(_token)
    google_token = OAuth2Token()
    LOGGER.debug(f" Google User {user}")
    username = user['name'].replace(' ', '').lower()
    _request = namedtuple('Request', 'user client')
    user = update_current_user(username)
    _request.user = user
    clients = OAuth2Client.query.filter_by(user_id=user.id).all()
    if len(clients) == 0:
        create_google_client(user)
    _request.client = OAuth2Client.query.filter_by(user_id=user.id).all()[0]
    authorization.save_token(_token, request=_request)
    return redirect('/')


def create_google_client(user):
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=gen_salt(24),
        client_id_issued_at=client_id_issued_at,
        user_id=user.id,
        client_secret=gen_salt(48)
    )

    client_metadata = {
        "client_name": 'lorem.ipsum.google',
        "client_uri": 'http://localhost:5000',
        "grant_types": 'authorization_code',
        "redirect_uris": ['http://localhost:5000'],
        "response_types": ['code'],
        "scope": 'profile',
        "token_endpoint_auth_method": 'client_secret_basic'
    }
    client.set_client_metadata(client_metadata)
    db.session.add(client)
    db.session.commit()


def gen_access_token(client, grant_type, user, scope):
    return new_token({
        "iss": "lorem.ipsum.dev",
        "sub": "admin",
        "name": "admin",
        "roles": [
            "user"
        ]
    })
