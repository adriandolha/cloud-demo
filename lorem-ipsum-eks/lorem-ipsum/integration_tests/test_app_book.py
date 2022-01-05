import json
import os

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json, to_json
import requests


class TestBookApi:
    def test_book_list_one(self, config_valid, book_valid, test_client, basic_headers):
        _response = requests.post(url=f'{config_valid["root_url"]}/books', headers=basic_headers,
                                  data=to_json([book_valid]).encode('utf-8'))
        self.debug_response(_response)
        assert _response.status_code == 200
        _book_json = from_json(_response.content.decode('utf-8'))
        print(_book_json)
        _uuid = _book_json['items'][0]['id']
        response = requests.get(url=f'{config_valid["root_url"]}/books/{_uuid}', headers=basic_headers)
        book = json.loads(response.content.decode('utf-8'))
        print(book)
        assert book['title'] == book_valid['title']
        assert 200 == response.status_code

    def debug_response(self, _response):
        print(_response.headers)
        print(_response.url)
        print(_response.status_code)
        print(_response.content)
        print(_response.request.headers)
        print(_response.request.url)
        print(_response.request.method)
        print(_response.request.body)

    def test_book_list_count(self, config_valid, test_client, basic_headers):
        response = requests.get(url=f'{config_valid["root_url"]}/books', headers=basic_headers)
        books = json.loads(response.content.decode('utf-8'))
        print(books)
        assert books['total']
        assert len(books['items']) >= 1
        assert 200 == response.status_code

    def test_book_list_default_limit(self, config_valid, test_client, basic_headers):
        response = requests.get(url=f'{config_valid["root_url"]}/books', headers=basic_headers)
        books = json.loads(response.content.decode('utf-8'))
        print(books)
        assert books['total'] > 2
        assert len(books['items']) == 1
        assert 200 == response.status_code

    def test_book_add(self, book_valid, config_valid, test_client, basic_headers):
        response = requests.post(url=f'{config_valid["root_url"]}/books', headers=basic_headers,
                                 data=to_json([book_valid]).encode('utf-8'))
        assert from_json(response.content.decode('utf-8'))['items'][0]['title']
        assert 200 == response.status_code

    def test_book_add_insufficient_permissions(self, config_valid, test_client, book_valid, basic_headers_user):
        response = requests.post(url=f'{config_valid["root_url"]}/books', headers=basic_headers_user,
                                 data=to_json([book_valid]).encode('utf-8'))
        assert 403 == response.status_code
        assert from_json(response.content.decode('utf-8')) == 'Forbidden.'
