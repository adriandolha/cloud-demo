import json
import os

from lorem_ipsum_auth.repo import Transaction

os.environ['env'] = 'test'


class TestConfig:
    def test_app_context_is_unique_per_request(self, config_valid_request):
        import app
        _result = app.get_config()
        from flask import g
        assert app.app_context() == g.app_context

