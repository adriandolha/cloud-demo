import logging
import os

import lorem_ipsum
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

import gevent_psycopg2
from lorem_ipsum.views import words, swaggerui_blueprint

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


def create_flask_app():
    global app
    from lorem_ipsum.views import books, users
    app.url_map.strict_slashes = False
    app.register_blueprint(books, url_prefix="/books")
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(words, url_prefix="/words")
    app.register_blueprint(swaggerui_blueprint)

    _app_context = lorem_ipsum.create_app()
    _app_context.run_database_setup()
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.info(app.config)
    start_prometheus_metrics(app)
    return app


if __name__ == "__main__" or __name__ == 'app' and os.getenv('env') != 'test':
    prepare_orm_for_gevent()
    create_flask_app()
    from lorem_ipsum.search_engine import SearchEngine

    SearchEngine.start_search_engine()
