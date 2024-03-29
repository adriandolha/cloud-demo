import logging
import os

import lorem_ipsum
from lorem_ipsum.auth import ExceptionHandlers

from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

import gevent_psycopg2

app = Flask('lorem-ipsum')
LOGGER = logging.getLogger('lorem-ipsum')
from prometheus_client import REGISTRY

print(f'Name is {__name__}')


def prepare_orm_for_gevent():
    """
    In order to make psycopg2 work with gevent, we need to apply this patch, otherwise all worker connections will use
    only one connection which might cause serious issues in production.
    Also, the patch needs to be applied before creating the db engine.
    """
    gevent_psycopg2.monkey_patch()


def start_prometheus_metrics(app):
    _prometheus_metrics = PrometheusMetrics(app=None)
    _prometheus_metrics.init_app(app)
    from lorem_ipsum.views import JsonCollector
    REGISTRY.register(JsonCollector())


def create_flask_app(flask_app=app):
    # global app
    from lorem_ipsum.views import books, users, words, stats, swaggerui_blueprint

    flask_app.url_map.strict_slashes = False
    flask_app.register_blueprint(books, url_prefix="/books")
    flask_app.register_blueprint(users, url_prefix="/users")
    flask_app.register_blueprint(words, url_prefix="/words")
    flask_app.register_blueprint(stats, url_prefix="/stats")
    flask_app.register_blueprint(swaggerui_blueprint)
    ExceptionHandlers(flask_app)
    _app_context = lorem_ipsum.create_app()
    _app_context.run_database_setup()
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.info(app.config)
    if _app_context.config['prometheus_metrics']:
        start_prometheus_metrics(flask_app)
    return flask_app


if __name__ == "__main__" or __name__ == 'app' and os.getenv('env') != 'test':
    prepare_orm_for_gevent()
    create_flask_app()
    from lorem_ipsum.search_engine import SearchEngine

    SearchEngine.start_search_engine()
