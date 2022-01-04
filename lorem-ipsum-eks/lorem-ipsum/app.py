import logging
import os

import lorem_ipsum
from flask import Flask
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
    REGISTRY.register(JsonCollector())


if __name__ == "__main__" or __name__ == 'app' and os.getenv('env') != 'test':
    prepare_orm_for_gevent()
    from lorem_ipsum.views import books, users, JsonCollector

    app.register_blueprint(books, url_prefix="/books")
    app.register_blueprint(users, url_prefix="/users")
    lorem_ipsum.create_app()
    LOGGER = logging.getLogger('lorem-ipsum')
    LOGGER.debug(app.config)
    start_prometheus_metrics(app)
