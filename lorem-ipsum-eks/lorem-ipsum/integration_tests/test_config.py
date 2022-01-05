import json
import os

import requests

os.environ['env'] = 'test'


class TestConfig:
    def test_config_valid(self, config_valid, requests_standard_settings):
        response = requests.get(url=f'{config_valid["root_url"]}/books/config', **requests_standard_settings)
        config = json.loads(response.content.decode('utf-8'))
        print(f'Configuration:\n{config}')
        assert 200 == response.status_code
        assert config.get('aurora_host') is not None

    def test_config_no_sensitive_data(self, config_valid, requests_standard_settings):
        response = requests.get(url=f'{config_valid["root_url"]}/books/config', **requests_standard_settings)
        config = json.loads(response.content.decode('utf-8'))
        assert 200 == response.status_code
        for (k, v) in config.items():
            assert 'password' not in k
            assert 'encryption' not in k

    def test_config_connection_pool_defaults(self, config_valid, requests_standard_settings):
        response = requests.get(url=f'{config_valid["root_url"]}/books/config', **requests_standard_settings)
        config = json.loads(response.content.decode('utf-8'))
        assert 200 == response.status_code
        assert config.get('connection_pool_minconn') == 30
        assert config.get('connection_pool_maxconn') == 40
