import json
import os

from lorem_ipsum_auth.repo import Transaction

os.environ['env'] = 'test'
import app


class TestConnectionPool:
    def test_pool_size_increases_when_connect(self, metrics_request_no_fields):
        c1 = Transaction.pool().connect()
        c2 = Transaction.pool().connect()
        _result = app.metrics()
        metrics = json.loads(_result.response[0].decode('utf-8'))
        print(metrics)
        assert metrics.get('connection_pool.rusedconn') == 2
        c1.close()
        c2.close()
        _result = app.metrics()
        metrics = json.loads(_result.response[0].decode('utf-8'))
        print(metrics)
        assert metrics.get('connection_pool.rusedconn') == 0
        assert '200' == _result.status

    def test_pool_size_increases_when_new_session_transaction(self, metrics_request_no_fields):
        app_context = app.app_context()
        _result = app.metrics()
        metrics = json.loads(_result.response[0].decode('utf-8'))
        print(f'Metrics v1 = {metrics}')
        assert metrics.get('connection_pool.rusedconn') == 0
        s1 = app_context.transaction_manager.transaction._session_maker()
        s2 = app_context.transaction_manager.transaction._session_maker()
        s1.execute('select 1')
        s2.execute('select 1')
        _result = app.metrics()
        metrics = json.loads(_result.response[0].decode('utf-8'))
        print(f'Metrics v2 = {metrics}')
        assert metrics.get('connection_pool.rusedconn') == 2
        s1.commit()
        s2.commit()
        s1.close()
        s2.close()
        _result = app.metrics()
        metrics = json.loads(_result.response[0].decode('utf-8'))
        print(f'Metrics v3 = {metrics}')
        assert metrics.get('connection_pool.rusedconn') == 0
        assert '200' == _result.status
