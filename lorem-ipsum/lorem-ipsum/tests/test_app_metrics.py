import json
import os

os.environ['env'] = 'test'
import lorem_ipsum.views as app


class TestMetricsApi:
    def test_metrics_no_fields(self, metrics_request_no_fields):
        from lorem_ipsum.config import DEFAULT_CONFIGS
        _result = app.metrics()
        metrics = json.loads(_result.response[0].decode('utf-8'))
        assert metrics.get('connection_pool.maxconn')
        assert metrics.get('connection_pool.minconn')
        assert metrics.get('connection_pool.usedconn') is not None
        assert metrics.get('connection_pool.size') == DEFAULT_CONFIGS['connection_pool_minconn']
        assert 200 == _result.status_code

    def test_metrics_when_threads(self, metrics_request_with_fields):
        _result = app.metrics()
        metrics = json.loads(_result.response[0].decode('utf-8'))
        assert metrics.get('threads')
        assert 200 == _result.status_code

    def test_metrics_when_connections(self, metrics_request_with_fields):
        _result = app.metrics()
        metrics = json.loads(_result.response[0].decode('utf-8'))
        assert metrics.get('connection_pool.connections')
        assert 200 == _result.status_code
