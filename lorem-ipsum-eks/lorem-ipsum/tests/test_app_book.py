import json
import os

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json
import app


class TestBookApi:
    def test_book_list_one(self, config_valid, book_valid_add_request):
        _uuid = from_json(app.save_book().response[0].decode('utf-8'))['items'][0]['id']
        response = app.get_book(_uuid)
        book = json.loads(response.response[0].decode('utf-8'))
        print(book)
        assert book['title'] == book_valid_add_request['title']
        assert '200' == response.status

    def test_book_list_count(self, book_valid_get_request):
        response = app.get_all_books()
        books = json.loads(response.response[0].decode('utf-8'))
        print(books)
        assert books['total']
        assert len(books['items']) == 2
        assert '200' == response.status

    def test_book_list_default_limit(self, book_valid_get_default_limit):
        response = app.get_all_books()
        books = json.loads(response.response[0].decode('utf-8'))
        print(books)
        assert books['total'] > 2
        assert len(books['items']) == 1
        assert '200' == response.status

    def test_book_add(self, book_valid_add_request, config_valid):
        print(json.dumps(book_valid_add_request))
        response = app.save_book()
        assert from_json(response.response[0].decode('utf-8'))['items'][0]['title']
        assert '200' == response.status

    def test_book_add_insufficient_permissions(self, book_add_request_insufficient_permissions):
        print(json.dumps(book_add_request_insufficient_permissions))
        response = app.save_book()
        assert '403' == response.status
        assert from_json(response.response[0].decode('utf-8')) == 'Forbidden.'
