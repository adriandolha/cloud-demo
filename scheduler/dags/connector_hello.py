"""
Code that goes along with the Airflow tutorial located at:
https://github.com/airbnb/airflow/blob/master/airflow/example_dags/tutorial.py
"""
# import BashOperator
import json
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from connector_notification import sqs

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=60),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


def connector_started(ds, **kwargs):
    print(ds)
    print(kwargs)
    sqs.queue_url = 'https://sqs.us-east-1.amazonaws.com/856816586042/connection_dev_myapp'
    print('Publishing connector started event on queue {}'.format(sqs.queue_url))
    event = json.dumps(
        {'next_execution_date': kwargs['next_execution_date'].isoformat(),
         'prev_execution_date': kwargs['prev_execution_date'].isoformat(),
         'execution_date': kwargs['execution_date'].isoformat(),
         'connection': '',
         'connector': ''})
    sqs.publish(event)
    return 'Event:{}'.format(event)


dag = DAG('connector_hello', default_args=default_args)

connector_started_task = PythonOperator(
    task_id='connector_started',
    provide_context=True,
    python_callable=connector_started,
    dag=dag
)

run_some_docker_job = BashOperator(
    task_id='run_report',
    env={'RUN_AS': 'root', 'AIRFLOW_ENV': ''},
    bash_command='docker run hello',
    dag=dag)


run_some_docker_job.set_upstream(connector_started_task)
