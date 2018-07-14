import pytest
import os

from connection.service import ConnectionService, ConnectionConsumer


class TestHarnessService:
    @pytest.fixture
    def setup(self):
        os.environ['env'] = 'dev'
        os.environ['client'] = 'myapp'
        ConnectionConsumer().start()

    def test_connection_created_event(self, setup, model_new):
        ConnectionService().add(model_new)
