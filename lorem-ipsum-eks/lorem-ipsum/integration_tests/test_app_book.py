import json
import os

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json, to_json
import requests


class TestBookApi:
    def test_book_list_one(self, config_valid, book_valid, requests_standard_settings):
        _response = self.add_book(book_valid, config_valid, requests_standard_settings)
        _book_json = from_json(_response.content.decode('utf-8'))
        print(_book_json)
        _uuid = _book_json['items'][0]['id']
        response = requests.get(url=f'{config_valid["root_url"]}/books/{_uuid}', **requests_standard_settings)
        book = json.loads(response.content.decode('utf-8'))
        print(book)
        assert book['title'] == book_valid['title']
        assert 200 == response.status_code

    def test_book_search(self, config_valid, book_valid, requests_standard_settings):
        _response = self.add_book(book_valid, config_valid, requests_standard_settings)
        _book_json = from_json(_response.content.decode('utf-8'))
        print(_book_json)
        from lorem_ipsum.model import Book
        book = Book.from_dict(_book_json['items'][0])
        print(book.text)
        query = book.text.split(' ')[0]
        print(query)
        _uuid = _book_json['items'][0]['id']
        response = requests.get(url=f'{config_valid["root_url"]}/books/search?query={query}',
                                **requests_standard_settings)
        books = [Book.from_dict(b) for b in json.loads(response.content.decode('utf-8'))['items']]
        for b in books:
            assert query in b.text
        assert book.id in [book.id for book in books]
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

    def test_book_list_users_books(self, config_valid, book_valid, requests_standard_settings):
        self.add_book(book_valid, config_valid, requests_standard_settings)

        response = requests.get(url=f'{config_valid["root_url"]}/books?limit=10', **requests_standard_settings)
        books = json.loads(response.content.decode('utf-8'))
        print(books)
        assert 200 == response.status_code
        assert books['total']
        assert len(books['items']) >= 1
        for book in books['items']:
            assert book['owner_id'] == 'admin'

    def test_book_list_page_count(self, config_valid, book_valid, requests_standard_settings):
        self.add_book(book_valid, config_valid, requests_standard_settings)

        response = requests.get(url=f'{config_valid["root_url"]}/books?includes=page_count',
                                **requests_standard_settings)
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
        assert response.status_code == 403
        assert from_json(response.content.decode('utf-8')) == 'Forbidden.'
