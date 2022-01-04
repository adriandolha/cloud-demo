import json
import os

os.environ['env'] = 'test'
import lorem_ipsum.views as app


class TestConfig:
    def test_config_valid(self, config_valid_request):
        _result = app.get_config()
        config = json.loads(_result.response[0].decode('utf-8'))
        print(f'Configuration:\n{config}')
        assert config.get('aurora_host') == os.getenv('aurora_host')
        assert 200 == _result.status_code

    def test_config_no_sensitive_data(self, config_valid_request):
        _result = app.get_config()
        config = json.loads(_result.response[0].decode('utf-8'))
        assert 200 == _result.status_code
        for (k, v) in config.items():
            assert 'password' not in k
            assert 'encryption' not in k

    def test_config_connection_pool_defaults(self, config_valid_request):
        _result = app.get_config()
        config = json.loads(_result.response[0].decode('utf-8'))
        assert 200 == _result.status_code
        assert config.get('connection_pool_minconn') == 30
        assert config.get('connection_pool_maxconn') == 40
        assert config.get('pod_name') == 'pod_name'
