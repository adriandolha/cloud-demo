import json
import os

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json
import lorem_ipsum.views as app


class TestWordApi:
    def test_word_list_one(self, word_valid_add_request):
        _response = app.save_word()
        assert _response.status_code == 200
        _word_json = from_json(_response.response[0].decode('utf-8'))
        print(_word_json)
        _id = _word_json['items'][0]['id']
        response = app.get_word(_id)
        book = json.loads(response.response[0].decode('utf-8'))
        print(book)
        assert book['name'] == word_valid_add_request['name']
        assert book['id'] == word_valid_add_request['id']
        assert book['count'] == word_valid_add_request['count']
        assert 200 == response.status_code

    def test_word_list_count(self, word_valid_add_request):
        response = app.get_all_words()
        words = json.loads(response.response[0].decode('utf-8'))
        print(words)
        assert words['total']
        assert len(words['items']) == 2
        assert 200 == response.status_code

    def test_word_list_limit_and_offset(self, word_valid_get_request_limit_offset):
        response = app.get_all_words()
        words = json.loads(response.response[0].decode('utf-8'))
        import lorem_ipsum
        assert words['total']
        assert len(words['items']) == 2
        assert 200 == response.status_code
        assert lorem_ipsum.repo.Transaction.session.query.return_value.limit.call_args.args[0] == 3
        assert lorem_ipsum.repo.Transaction.session.query.return_value.limit.return_value.offset.call_args.args[0] == 4

    def test_word_list_default_limit(self, word_valid_get_default_limit):
        response = app.get_all_words()
        words = json.loads(response.response[0].decode('utf-8'))
        assert words['total'] > 2
        assert len(words['items']) == 1
        assert 200 == response.status_code

    def test_word_add(self, word_valid_add_request, config_valid):
        response = app.save_word()
        assert from_json(response.response[0].decode('utf-8'))['items'][0]['name']
        assert 200 == response.status_code

    def test_word_add_insufficient_permissions(self, book_add_request_insufficient_permissions):
        response = app.save_word()
        assert 403 == response.status_code
        assert from_json(response.response[0].decode('utf-8')) == 'Forbidden.'
