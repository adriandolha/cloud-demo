import json
import os

os.environ['env'] = 'test'
from lorem_ipsum.serializers import from_json
import lorem_ipsum.views as app


class TestStatsApi:
    def test_stats_top_words(self, word_valid_add_request):
        _response = app.get_top_words_stats()
        assert _response.status_code == 200
        _word_json = from_json(_response.response[0].decode('utf-8'))
        print(_word_json)
        _id = _word_json['items'][0]['id']
        response = app.get_word(_id)
        words = json.loads(response.response[0].decode('utf-8'))
        print(words)
        assert words['name'] == word_valid_add_request['name']
        assert words['id'] == word_valid_add_request['id']
        assert words['count'] == word_valid_add_request['count']
        assert 200 == response.status_code


