import json

import boto3
from locust import HttpLocust, TaskSet, task

model_new = {
    "title": "false",
    "author": "false",
    "text": "false",
}
ids = []

ENV = 'kube'


class LoremIpsumApi(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.verify = False
        self._client = self.get_api_client()
        if ENV == 'kube':

            # self.api_url = "http://localhost:30101/symptoms"
            self.api_url = "https://afd5f0664acd240b58332fc071456250-1ff6d404d0ca84d4.elb.eu-central-1.amazonaws.com/pandemic-support/symptoms"
            self.api_key = "no-key"
        else:
            self.api_url = self.get_api_url(self.get_api_id(self._client))
            self.api_key = self.get_api_key(self._client)

    @task(3)
    def add(self):
        response = self.client.post(self.api_url, data=json.dumps([model_new]),
                                    headers=self.basic_headers(self.api_key))
        print(response)
        print(response.content)
        ids.append(json.loads(response.content)['items'][0]['id'])
        symptom_id = ids.pop(-1)
        # self.client.get(f'{self.api_url}?id={symptom_id}', name='/symptoms',
        #                 headers=self.basic_headers(self.api_key))

    @task(5)
    def list_count(self):
        self.client.get(f'{self.api_url}', headers=self.basic_headers(self.api_key))
        self.wait()

    def basic_headers(self, api_key):
        return {
            'Content-Type': 'application/json',
            'x-api-key': api_key
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
    min_wait = 100
    max_wait = 1000
