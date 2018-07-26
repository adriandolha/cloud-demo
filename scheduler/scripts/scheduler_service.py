import datetime
import json

import boto3 as boto3
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

    def get_last_log(self, dag_id, task_id):
        s3 = boto3.client('s3')
        task_prefix = '{}/{}'.format(dag_id, task_id)
        items = s3.list_objects(Bucket='cloud-demo-airflow-logs', Prefix=task_prefix)
        last_log_s3_path = items['Contents'][0]['Key']
        print(last_log_s3_path)
        content = boto3.resource('s3').Object('cloud-demo-airflow-logs', last_log_s3_path).get()['Body'].read().decode('utf-8')
        return content
