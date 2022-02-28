import os

from lorem_ipsum.serializers import to_json, from_json

os.environ['env'] = 'test'


class TestBookUpdated:
    def test_book_updated(self, app_context, book_small_valid, book_updated_event_valid):
        from lorem_ipsum import model, repo
        from lorem_ipsum.search_engine import SearchEngine
        SearchEngine(app_context).process_events()
        new_words = repo.Transaction.session.bulk_save_objects.call_args.args[0]
        expected = ['just', 'a', 'sample', 'page']
        actual = [w.name for w in new_words]
        print(actual)
        assert len(actual) == len(expected)
        assert actual == expected

        self.assert_book_indexed_event_is_created(book_small_valid)

        self.assert_processed_event_is_deleted(book_updated_event_valid)

    def assert_book_indexed_event_is_created(self, book_expected):
        from lorem_ipsum import model, repo
        book_indexed_event = repo.Transaction.session.add.call_args.args[0]
        print(book_indexed_event)
        assert book_indexed_event.name == str(model.Events.BOOK_INDEXED)
        assert from_json(book_indexed_event.data)['book_id'] == book_expected['id']

    def assert_processed_event_is_deleted(self, event_expected):
        from lorem_ipsum import repo
        book_indexed_event = repo.Transaction.session.delete.call_args.args[0]
        print(book_indexed_event)
        assert book_indexed_event.id == event_expected.id
