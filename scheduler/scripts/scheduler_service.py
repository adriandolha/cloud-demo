import datetime
import json

import requests


class SchedulerService:
    def __init__(self, url):
        self.url = url

    def run(self, dag_id):
        dag_request = {
            'owner': 'airflow',
            'start_date': datetime.datetime.utcnow().isoformat(),
            # 'execution_date': datetime.datetime.utcnow().isoformat(),
            'schedule_interval': '@once'
        }
        request_url = f'{self.url}/api/experimental/dags/{dag_id}/dag_runs'
        print(request_url)
        return requests.post(
            request_url,
            json=json.dumps(dag_request))

    def get_task(self, dag_id, task_id):
        request_url = f'{self.url}/api/experimental/dags/{dag_id}/tasks/{task_id}'
        print(request_url)
        return requests.get(request_url)
