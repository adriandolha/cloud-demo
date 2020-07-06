import json
import os

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json
import app


class TestBookApi:
    def test_book_list_one(self, config_valid, book_valid_add_request):
        _uuid = from_json(app.save().response[0].decode('utf-8'))['items'][0]['id']
        response = app.get(_uuid)
        books = json.loads(response.response[0].decode('utf-8'))
        print(books)
        assert books['items'][0]['title'] == book_valid_add_request['title']
        assert '200' == response.status

    def test_book_list_count(self, config_valid):
        response = app.get_all()
        books = json.loads(response.response[0].decode('utf-8'))
        print(books)
        assert books['total']
        assert '200' == response.status

    def test_book_metrics(self, config_valid):
        _result = app.metrics()
        metrics = json.loads(_result.response[0].decode('utf-8'))
        assert metrics.get('connection_pool.maxconn')
        assert metrics.get('connection_pool.minconn')
        assert metrics.get('connection_pool.usedconn') is not None
        assert metrics.get('connection_pool.size') == 1
        assert '200' == _result.status

    def test_book_add(self, book_valid_add_request, config_valid):
        response = app.save()
        assert from_json(response.response[0].decode('utf-8'))['items'][0]['title']
        assert '200' == response.status
