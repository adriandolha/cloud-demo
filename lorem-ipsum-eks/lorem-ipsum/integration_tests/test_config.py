import json
import os

from lorem_ipsum.repo import Transaction

os.environ['env'] = 'test'
import app


class TestConfig:
    def test_config_valid(self, config_valid_request):
        _result = app.get_config()
        config = json.loads(_result.response[0].decode('utf-8'))
        print(config)
        assert config.get('aurora_host') == os.getenv('aurora_host')
        assert '200' == _result.status

    def test_config_no_sensitive_data(self, config_valid_request):
        _result = app.get_config()
        config = json.loads(_result.response[0].decode('utf-8'))
        assert '200' == _result.status
        for (k, v) in config.items():
            assert 'password' not in k
            assert 'encryption' not in k

    def test_config_connection_pool_defaults(self, config_valid_request):
        from lorem_ipsum.config import DEFAULT_CONFIGS
        _result = app.get_config()
        config = json.loads(_result.response[0].decode('utf-8'))
        assert '200' == _result.status
        assert config.get('connection_pool_minconn') == 30
        assert config.get('connection_pool_maxconn') == 40
        assert config.get('pod_name') == 'pod_name'
