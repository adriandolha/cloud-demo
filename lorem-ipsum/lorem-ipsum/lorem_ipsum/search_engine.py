from functools import reduce

import re
from collections import Counter

import datetime

import time

import threading

import logging
from lorem_ipsum.serializers import from_json, to_json
from lorem_ipsum import model, AppContext, transaction

LOGGER = logging.getLogger('lorem-ipsum')


class Indexer:
    def __init__(self, app_context: AppContext):
        self._app_context = app_context
        self.word_repo = app_context.word_repo

    def index_book(self, book: model.Book):
        word_frequency = Indexer.word_frequency(book.text)
        _id_list = list(word_frequency.keys())
        existing_words = self.word_repo.find_by_ids(_id_list)['items']
        LOGGER.info(existing_words)
        existing_words_by_ids = {word.id: word for word in existing_words}
        new_words = []
        for word_id in _id_list:
            existing_word = existing_words_by_ids.get(word_id)
            if existing_word is not None:
                LOGGER.debug(existing_word.index)
                frequency = word_frequency.get(existing_word.name)
                LOGGER.debug(type(existing_word.index))
                index = dict(from_json(existing_word.index))
                # if index.get(book.id) is not None:
                index[book.id] = frequency
                existing_word.count = reduce(lambda a, b: a + b, index.values())
                existing_word.index = to_json(index)
            else:
                word_count = word_frequency[word_id]
                new_words.append(
                    model.Word(id=word_id, name=word_id, index=to_json({book.id: word_count}), count=word_count))

        self.word_repo.update_all([*existing_words, *new_words])

    @staticmethod
    def word_frequency(text: str) -> Counter:
        words = re.findall(r'\w+', text.lower())
        words_frequency = Counter(words)
        return words_frequency


class SearchEngine:
    def __init__(self, app_context: AppContext):
        self._app_context = app_context
        self.word_repo = app_context.word_repo
        self.event_repo = app_context.event_repo

    def handle_book_updated(self, event: model.Event):
        LOGGER.info(f'Handling book updated event {event.id}...')
        started_at = datetime.datetime.utcnow()
        book = model.Book.from_dict(from_json(from_json(event.data)['new']))
        Indexer(self._app_context).index_book(book)
        event_repo = self._app_context.event_repo
        event_repo.save(model.Event(id=event_repo.next_id(), name=str(model.Events.BOOK_INDEXED), data=to_json({
            'started_at': started_at,
            'completed_at': datetime.datetime.utcnow(),
            'book_id': book.id
        })))
        LOGGER.info(f'Handled book updated event {event.id}...')

    @transaction
    def process_events(self):
        events = self.event_repo.get_all(limit=1, offset=0)['items']
        no_of_events = len(events)
        # LOGGER.info(f'Processing events {no_of_events}...')
        if no_of_events == 1:
            event = events[0]
            if event.name == str(model.Events.BOOK_UPDATED):
                LOGGER.info(f'Processing event {event.id}:{event.name}')
                self.handle_book_updated(event)
                self.event_repo.delete(event)

    @staticmethod
    def start_search_engine():
        from lorem_ipsum import create_app_context

        def run():
            LOGGER.info('Started search engine...')
            while True:
                app_context = create_app_context()
                search_engine = SearchEngine(app_context)
                search_engine.process_events()
                time.sleep(3)

        threading.Thread(target=run, args=()).start()
