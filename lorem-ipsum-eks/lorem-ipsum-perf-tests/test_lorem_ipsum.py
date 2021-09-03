import json

import boto3
import faker
import json
import os
from locust import HttpLocust, TaskSet, task


def model_new():
    _faker = faker.Faker()
    _book = {f'page_{page}': [_faker.text(max_nb_chars=10) for i in range(30)] for page in range(1)}
    return {"author": _faker.name(),
            "title": _faker.text(max_nb_chars=5),
            "book": json.dumps(_book),
            "no_of_pages": 1,
            }


ids = []

ENV = 'kube'


class LoremIpsumApi(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.verify = False
        self._client = self.get_api_client()
        print('Starting performance tests...')
        if ENV == 'kube':
            with open(f"{os.path.expanduser('~')}/.cloud-projects/lorem-ipsum-local.json", "r") as _file:
                _json = dict(json.load(_file))
                print(json)
                for k, v in _json.items():
                    os.environ[k] = str(v)
            # self.api_url = "http://localhost:30101/symptoms"
            self.api_url = "https://localhost:31862/lorem-ipsum/books"
            # self.api_url = "http://localhost:5000/books"
            self.api_key = "no-key"
            self.token = os.environ.get('admin_token')
        else:
            self.api_url = self.get_api_url(self.get_api_id(self._client))
            self.api_key = self.get_api_key(self._client)

    @task(3)
    def add(self):
        response = self.client.post(self.api_url, data=json.dumps([model_new()]),
                                    headers=self.basic_headers(self.api_key))
        # print(response)
        # print(response.content)
        ids.append(json.loads(response.content)['items'][0]['id'])
        # self.client.get(f'{self.api_url}?id={symptom_id}', name='/symptoms',
        #                 headers=self.basic_headers(self.api_key))

    @task(5)
    def list_count(self):
        try:
            book_id = ids.pop()
            # client.get("/blog?id=%i" % i, name="/blog?id=[id]")
            self.client.get(f'{self.api_url}/{book_id}', headers=self.basic_headers(self.api_key),
                            name="/books?id=[id]")
            self.wait()
        except IndexError:
            print('index error')

    def basic_headers(self, api_key):
        return {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            "authorization": "Bearer " + self.token
        }

    def get_api_url(self, api_id):
        region = 'eu-central-1'
        stage = 'test'
        resource = 'symptoms'
        api_url = f'https://{api_id}.execute-api.{region}.amazonaws.com/{stage}/{resource}'
        print(f'API url is {api_url}')
        return api_url

    def get_api_client(self):
        return boto3.client('apigateway')

    def get_api_id(self, api_client):
        apis = api_client.get_rest_apis()
        rest_api_id = [item['id'] for item in apis['items'] if item['name'] == 'symptom_api'][0]
        return rest_api_id

    def get_api_key(self, api_client):
        key_id = None
        key_name = 'mykey'
        keys = api_client.get_api_keys()
        for item in keys['items']:
            if item['name'] == key_name:
                key_id = item['id']
        if not key_id:
            raise ValueError(f'Could not find api key {key_name}')
        return api_client.get_api_key(apiKey=key_id, includeValue=True)['value']


class WebsiteUser(HttpLocust):
    task_set = LoremIpsumApi
    min_wait = 20
    max_wait = 50
