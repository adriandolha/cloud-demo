import os
import lorem_ipsum.views as app

os.environ['env'] = 'test'


class TestConfig:
    def test_app_context_is_unique_per_request(self, config_valid_request):
        _result = app.get_config()
        from flask import g
        assert app.app_context() == g.app_context

