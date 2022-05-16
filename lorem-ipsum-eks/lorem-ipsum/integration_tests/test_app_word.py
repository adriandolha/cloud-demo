import json
import os

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json, to_json
import requests


class TestWordApi:
    def test_word_list_one(self, config_valid, word_valid, requests_standard_settings):
        _response= self.add_word(word_valid, config_valid, requests_standard_settings)
        _word_json = from_json(_response.content.decode('utf-8'))
        print(_word_json)
        _id = _word_json['items'][0]['id']
        response = requests.get(url=f'{config_valid["root_url"]}/words/{_id}', **requests_standard_settings)
        word = json.loads(response.content.decode('utf-8'))
        print(word)
        assert word['name'] == word_valid['name']
        assert 200 == response.status_code

    def test_word_delete(self, config_valid, word_valid, requests_standard_settings):
        _response = self.add_word(word_valid, config_valid, requests_standard_settings)
        _word_json = from_json(_response.content.decode('utf-8'))
        print(_word_json)
        _id = _word_json['items'][0]['id']
        response = requests.get(url=f'{config_valid["root_url"]}/words/{_id}', **requests_standard_settings)
        assert 200 == response.status_code
        assert _id == from_json(_response.content.decode('utf-8'))['items'][0]['id']
        response = requests.delete(url=f'{config_valid["root_url"]}/words/{_id}', **requests_standard_settings)
        assert response.status_code == 204

    def test_word_list_count(self, config_valid, word_valid, requests_standard_settings):
        self.add_word(word_valid, config_valid, requests_standard_settings)

        response = requests.get(url=f'{config_valid["root_url"]}/words', **requests_standard_settings)
        words = json.loads(response.content.decode('utf-8'))
        print(words)
        assert words['total']
        assert len(words['items']) >= 1
        assert 200 == response.status_code

    def add_word(self, word_valid, config_valid, requests_standard_settings):
        _response = requests.post(url=f'{config_valid["root_url"]}/words',
                                  data=to_json([word_valid]).encode('utf-8'), **requests_standard_settings)
        assert _response.status_code == 200
        return _response

    def test_word_list_offset_and_limit(self, config_valid, word_valid, requests_standard_settings):
        self.add_word(word_valid, config_valid, requests_standard_settings)
        self.add_word(word_valid, config_valid, requests_standard_settings)

        response = requests.get(url=f'{config_valid["root_url"]}/words?offset=1&limit=2', **requests_standard_settings)
        words_for_offset1 = json.loads(response.content.decode('utf-8'))
        assert 200 == response.status_code
        response = requests.get(url=f'{config_valid["root_url"]}/words?offset=2&limit=2', **requests_standard_settings)
        words_for_offset2 = json.loads(response.content.decode('utf-8'))
        assert 200 == response.status_code
        assert len(words_for_offset1['items']) == 2
        assert len(words_for_offset2['items']) == 2
        assert words_for_offset1['items'][0]['id'] != words_for_offset2['items'][0]['id']

    def test_word_list_default_limit_and_order_desc(self, config_valid, word_valid, word_valid_max, requests_standard_settings):
        self.add_word(word_valid, config_valid, requests_standard_settings)
        self.add_word(word_valid_max, config_valid, requests_standard_settings)
        response = requests.get(url=f'{config_valid["root_url"]}/words?limit=1&offset=0', **requests_standard_settings)
        words = json.loads(response.content.decode('utf-8'))
        print(words)
        assert words['total'] >= 2
        assert words['items'][0]['count'] == word_valid_max['count']
        # assert len(books['items']) == 1
        assert 200 == response.status_code

    def test_word_add(self, word_valid, config_valid, requests_standard_settings):
        response = requests.post(url=f'{config_valid["root_url"]}/words',
                                 data=to_json([word_valid]).encode('utf-8'), **requests_standard_settings)
        assert from_json(response.content.decode('utf-8'))['items'][0]['name']
        assert 200 == response.status_code

    def test_word_add_insufficient_permissions(self, config_valid, word_valid, requests_user_token_settings):
        response = requests.post(url=f'{config_valid["root_url"]}/words',
                                 data=to_json([word_valid]).encode('utf-8'), **requests_user_token_settings)
        assert 403 == response.status_code
        assert from_json(response.content.decode('utf-8')) == 'Forbidden.'
