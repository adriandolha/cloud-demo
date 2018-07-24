import datetime
import json

import requests
from airflow.api.common.experimental import trigger_dag as trigger

dag_request = {
    'owner': 'airflow',
    # 'start_date': datetime.datetime.utcnow().isoformat(),
    # 'execution_date': datetime.datetime.utcnow().isoformat(),
    'schedule_interval': '@once'
}
print('hello')
response = requests.post('http://34.207.74.29:8080/api/experimental/dags/connector_task/dag_runs',
                         json=json.dumps(dag_request))
# r = trigger.trigger_dag(dag_id='connector_task', conf=dag_request)
print(response.status_code)
print(response.content)
# print(r)
