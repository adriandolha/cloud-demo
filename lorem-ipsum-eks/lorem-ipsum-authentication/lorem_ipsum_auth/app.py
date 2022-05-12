import logging
from flask_bootstrap import Bootstrap

from flask import Flask, g
from flask_swagger_ui import get_swaggerui_blueprint

import gevent_psycopg2
import lorem_ipsum_auth
from lorem_ipsum_auth.auth import token_auth, users, swagger_bp
from lorem_ipsum_auth.models import AnonymousUser, Role, User
from lorem_ipsum_auth.routes import auth, main

from lorem_ipsum_auth import login_manager, db
from lorem_ipsum_auth.google_oauth import google_oauth


def prepare_orm_for_gevent():
    """
    In order to make psycopg2 work with gevent, we need to apply this patch, otherwise all worker connections will use
    only one connection which might cause serious issues in production.
    Also, the patch needs to be applied before creating the db engine.
    """
    gevent_psycopg2.monkey_patch()


def create_flask_app():
    prepare_orm_for_gevent()
    app = Flask(__name__)
    _app_context = lorem_ipsum_auth.create_app()
    _config = _app_context.config
    LOGGER = logging.getLogger('lorem-ipsum')
    app.config.update({
        'SECRET_KEY': _app_context.user_service.secret_key(),
        'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_DATABASE_URI': _app_context.transaction_manager.database_connection_string,
    })

    # app = create_app({
    #     'SECRET_KEY': app_context.user_service.secret_key(),
    #     'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
    #     'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    #     'SQLALCHEMY_DATABASE_URI': app_context.transaction_manager.database_connection_string,
    # })
    @app.before_first_request
    def create_tables():
        db.create_all()
        LOGGER.debug('Setting roles...')
        Role.insert_roles()
        LOGGER.debug('Setting users...')
        User.insert_users(_config)

    db.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(google_oauth, url_prefix='/api/auth/google')
    app.register_blueprint(token_auth, url_prefix='/api/auth')
    app.register_blueprint(users, url_prefix='/api/users')
    app.register_blueprint(swagger_bp, url_prefix='/')
    swaggerui_blueprint = get_swaggerui_blueprint('/api/docs', '/spec')
    app.register_blueprint(swaggerui_blueprint)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.anonymous_user = AnonymousUser
    app.url_map.strict_slashes = False
    Bootstrap(app)

    LOGGER.debug(app.config)
    return app
