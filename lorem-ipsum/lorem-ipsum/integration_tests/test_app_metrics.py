import json
import os

import requests

os.environ['env'] = 'test'


class TestMetricsApi:
    def test_metrics_no_fields(self, config_valid, requests_standard_settings):
        from lorem_ipsum.config import DEFAULT_CONFIGS
        response = requests.get(url=f'{config_valid["root_url"]}/books/metrics', **requests_standard_settings)
        metrics = json.loads(response.content.decode('utf-8'))
        assert metrics.get('connection_pool.maxconn')
        assert metrics.get('connection_pool.minconn')
        assert metrics.get('connection_pool.usedconn') is not None
        assert metrics.get('connection_pool.size') == DEFAULT_CONFIGS['connection_pool_minconn']
        assert 200 == response.status_code

    def test_metrics_when_threads(self, config_valid, requests_standard_settings):
        response = requests.get(url=f'{config_valid["root_url"]}/books/metrics?fields=threads',
                                **requests_standard_settings)
        metrics = json.loads(response.content.decode('utf-8'))
        assert metrics.get('threads')
        assert metrics.get('connection_pool.connections') is None
        assert 200 == response.status_code

    def test_metrics_when_connections(self, config_valid, requests_standard_settings):
        response = requests.get(url=f'{config_valid["root_url"]}/books/metrics?fields=connections',
                                **requests_standard_settings)
        metrics = json.loads(response.content.decode('utf-8'))
        assert metrics.get('connection_pool.connections')
        assert metrics.get('threads') is None
        assert 200 == response.status_code
