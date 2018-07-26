import datetime
import json

import requests
from airflow.api.common.experimental import trigger_dag as trigger

response = requests.get('http://34.207.74.29:8080/api/experimental/dags/just_run/tasks')
# r = trigger.trigger_dag(dag_id='connector_task', conf=dag_request)
print(response.status_code)
print(response.content)
# print(r)
