import json
import os

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json, to_json
import requests


class TestBookApi:
    def test_book_list_one(self, config_valid, book_valid, requests_standard_settings):
        _response= self.add_book(book_valid, config_valid, requests_standard_settings)
        _book_json = from_json(_response.content.decode('utf-8'))
        print(_book_json)
        _uuid = _book_json['items'][0]['id']
        response = requests.get(url=f'{config_valid["root_url"]}/books/{_uuid}', **requests_standard_settings)
        book = json.loads(response.content.decode('utf-8'))
        print(book)
        assert book['title'] == book_valid['title']
        assert 200 == response.status_code

    def test_book_delete(self, config_valid, book_valid, requests_standard_settings):
        _response = self.add_book(book_valid, config_valid, requests_standard_settings)
        _book_json = from_json(_response.content.decode('utf-8'))
        print(_book_json)
        _uuid = _book_json['items'][0]['id']
        response = requests.get(url=f'{config_valid["root_url"]}/books/{_uuid}', **requests_standard_settings)
        assert 200 == response.status_code
        assert _uuid == from_json(_response.content.decode('utf-8'))['items'][0]['id']
        response = requests.delete(url=f'{config_valid["root_url"]}/books/{_uuid}', **requests_standard_settings)
        assert response.status_code == 204

    def test_book_list_count(self, config_valid, book_valid, requests_standard_settings):
        self.add_book(book_valid, config_valid, requests_standard_settings)

        response = requests.get(url=f'{config_valid["root_url"]}/books', **requests_standard_settings)
        books = json.loads(response.content.decode('utf-8'))
        print(books)
        assert books['total']
        assert books['page_count'] is None
        assert len(books['items']) >= 1
        assert 200 == response.status_code

    def test_book_list_page_count(self, config_valid, book_valid, requests_standard_settings):
        self.add_book(book_valid, config_valid, requests_standard_settings)

        response = requests.get(url=f'{config_valid["root_url"]}/books?includes=page_count', **requests_standard_settings)
        books = json.loads(response.content.decode('utf-8'))
        print(books)
        assert books['total']
        assert books['page_count'] > 0
        assert len(books['items']) >= 1
        assert 200 == response.status_code

    def add_book(self, book_valid, config_valid, requests_standard_settings):
        _response = requests.post(url=f'{config_valid["root_url"]}/books',
                                  data=to_json([book_valid]).encode('utf-8'), **requests_standard_settings)
        assert _response.status_code == 200
        return _response

    def test_book_list_offset_and_limit(self, config_valid, book_valid, requests_standard_settings):
        self.add_book(book_valid, config_valid, requests_standard_settings)
        self.add_book(book_valid, config_valid, requests_standard_settings)

        response = requests.get(url=f'{config_valid["root_url"]}/books?offset=1&limit=2', **requests_standard_settings)
        books_for_offset1 = json.loads(response.content.decode('utf-8'))
        assert 200 == response.status_code
        response = requests.get(url=f'{config_valid["root_url"]}/books?offset=2&limit=2', **requests_standard_settings)
        books_for_offset2 = json.loads(response.content.decode('utf-8'))
        assert 200 == response.status_code
        assert len(books_for_offset1['items']) == 2
        assert len(books_for_offset2['items']) == 2
        assert books_for_offset1['items'][0]['id'] != books_for_offset2['items'][0]['id']

    def test_book_list_default_limit(self, config_valid, book_valid, requests_standard_settings):
        self.add_book(book_valid, config_valid, requests_standard_settings)
        self.add_book(book_valid, config_valid, requests_standard_settings)
        response = requests.get(url=f'{config_valid["root_url"]}/books', **requests_standard_settings)
        books = json.loads(response.content.decode('utf-8'))
        print(books)
        assert books['total'] >= 2
        # assert len(books['items']) == 1
        assert 200 == response.status_code

    def test_book_add(self, book_valid, config_valid, requests_standard_settings):
        response = requests.post(url=f'{config_valid["root_url"]}/books',
                                 data=to_json([book_valid]).encode('utf-8'), **requests_standard_settings)
        assert from_json(response.content.decode('utf-8'))['items'][0]['title']
        assert 200 == response.status_code

    def test_book_add_insufficient_permissions(self, config_valid, book_valid, requests_user_token_settings):
        response = requests.post(url=f'{config_valid["root_url"]}/books',
                                 data=to_json([book_valid]).encode('utf-8'), **requests_user_token_settings)
        assert 403 == response.status_code
        assert from_json(response.content.decode('utf-8')) == 'Forbidden.'
