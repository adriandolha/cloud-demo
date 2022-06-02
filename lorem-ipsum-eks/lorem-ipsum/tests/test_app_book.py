import json
import os

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json
import lorem_ipsum.views as app


class TestBookApi:
    def test_book_list_one(self, book_valid_add_request):
        _response = app.save_book()
        assert _response.status_code == 200
        _book_json = from_json(_response.response[0].decode('utf-8'))
        print(_book_json)
        _uuid = _book_json['items'][0]['id']
        response = app.get_book(_uuid)
        assert 200 == response.status_code
        book = json.loads(response.response[0].decode('utf-8'))
        print(book)
        assert book['title'] == book_valid_add_request['title']

    def test_book_random(self, book_random_valid_get_request):
        _response = app.random_book()
        book = json.loads(_response.response[0].decode('utf-8'))
        assert book['title']
        assert book['no_of_pages'] == 3
        assert 200 == _response.status_code

    def test_book_list_count(self, book_valid_get_request, request_valid_admin):
        response = app.get_all_books()
        books = json.loads(response.response[0].decode('utf-8'))
        print(books)
        assert books['total']
        assert len(books['items']) == 2
        assert 200 == response.status_code

    def test_book_list_user_books(self, book_valid_get_request_user, user_admin_valid):
        import lorem_ipsum
        response = app.get_all_books()
        books = json.loads(response.response[0].decode('utf-8'))
        print(books)
        book_filter_args = lorem_ipsum.repo.Transaction.session.query.return_value.filter.call_args.args
        assert book_filter_args[0].right.value == user_admin_valid['username']
        assert books['total']
        assert len(books['items']) == 1
        assert books['items'][0]['owner_id'] == user_admin_valid['username']
        assert 200 == response.status_code

    def test_book_list_page_count(self, page_count_valid_get_request):
        response = app.get_all_books()
        books = json.loads(response.response[0].decode('utf-8'))
        print(books)
        assert books['total']
        assert books['page_count'] == 10
        assert len(books['items']) == 2
        assert 200 == response.status_code

    def test_book_list_limit_and_offset(self, book_valid_get_request_limit_offset):
        response = app.get_all_books()
        books = json.loads(response.response[0].decode('utf-8'))
        import lorem_ipsum
        assert books['total']
        assert len(books['items']) == 2
        assert 200 == response.status_code
        assert lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.limit.call_args.args[0] == 3
        assert lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.limit.return_value.offset.call_args.args[0] == 4

    def test_book_list_default_limit(self, book_valid_get_default_limit):
        response = app.get_all_books()
        books = json.loads(response.response[0].decode('utf-8'))
        assert books['total'] > 2
        assert len(books['items']) == 1
        assert 200 == response.status_code

    def test_book_add(self, book_valid_add_request, config_valid):
        response = app.save_book()
        assert from_json(response.response[0].decode('utf-8'))['items'][0]['title']
        assert 200 == response.status_code

    def test_book_add_insufficient_permissions(self, client, book_valid, user_token_valid, book_add_request_insufficient_permissions):
        response = client.post('/books', json=json.dumps([book_valid]), headers={'Authorization': f'Bearer {user_token_valid}'})
        assert 403 == response.status_code
        assert from_json(response.data.decode('utf-8')) == 'Forbidden.'

    def test__options_method_no_auth(self, book_add_request_options_method_no_auth):
        response = app.get_all_books()
        assert 200 == response.status_code
        assert from_json(response.response[0].decode('utf-8')) == 'ok'
        response = app.save_book()
        assert 200 == response.status_code
        assert from_json(response.response[0].decode('utf-8')) == 'ok'
