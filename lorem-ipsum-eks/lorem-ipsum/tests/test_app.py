import json
import os

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json
import app


class TestBookApi:
    def test_book_list_one(self, config_valid, book_valid_add_request):
        _uuid = from_json(app.save().response[0].decode('utf-8'))['items'][0]['id']
        response = app.get(_uuid)
        book = json.loads(response.response[0].decode('utf-8'))
        print(book)
        assert book['title'] == book_valid_add_request['title']
        assert '200' == response.status

    def test_book_list_count(self, book_valid_get_request):
        response = app.get_all()
        books = json.loads(response.response[0].decode('utf-8'))
        print(books)
        assert books['total']
        assert len(books['items']) == 2
        assert '200' == response.status

    def test_book_list_default_limit(self, book_valid_get_default_limit):
        response = app.get_all()
        books = json.loads(response.response[0].decode('utf-8'))
        print(books)
        assert books['total'] > 2
        assert len(books['items']) == 1
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
        print(json.dumps(book_valid_add_request))
        response = app.save()
        assert from_json(response.response[0].decode('utf-8'))['items'][0]['title']
        assert '200' == response.status
