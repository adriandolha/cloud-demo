import logging

from authlib.integrations.flask_client import OAuth
from flask import Blueprint, url_for, g, redirect, request, flash
from flask import current_app as app
from flask_login import login_user

from lorem_ipsum_auth import AppContext, db
from lorem_ipsum_auth.models import User, LoginType

google_oauth = Blueprint('google_oauth', __name__)
LOGGER = logging.getLogger('lorem-ipsum')


def app_context():
    if 'app_context' not in g:
        g.app_context = AppContext.local_context()

    return g.app_context


oauth = OAuth(app)


@google_oauth.route('/')
def google():
    # Google Oauth Config
    # Get client_id and client_secret from environment variables
    # For developement purpose you can directly put it
    # here inside double quotes
    _app_context = app_context()
    GOOGLE_CLIENT_ID = _app_context.config.get('google_client_id')
    GOOGLE_CLIENT_SECRET = _app_context.config.get('google_client_secret')

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_oauth.google_auth', _external=True)
    return oauth.google.authorize_redirect(f'{redirect_uri}')


@google_oauth.route('/auth/')
def google_auth():
    _token = oauth.google.authorize_access_token()
    google_user = oauth.google.parse_id_token(_token)
    LOGGER.debug(f" Google User {google_user}")
    username = google_user['name'].replace(' ', '').lower()
    LOGGER.debug(f" Google User Name {username}")
    user = User.query.filter_by(email=google_user['email']).first()
    _password = "google"
    if not user:
        user = User(email=google_user['email'],
                    username=username,
                    password=_password,
                    login_type=LoginType.GOOGLE)
        db.session.add(user)
        db.session.commit()
    if user is not None and user.verify_password(_password):
        login_user(user, remember=False)
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('main.index')
        return redirect(next)
    flash('Invalid username or password.')

    return redirect(url_for('main.index'))
