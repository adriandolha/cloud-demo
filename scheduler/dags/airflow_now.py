"""
Code that goes along with the Airflow tutorial located at:
https://github.com/airbnb/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
# import BashOperator
from datetime import datetime, timedelta

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from connector_notification import sqs

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'schedule_interval': '@once',
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


def connector_started(ds, **kwargs):
    print(ds)
    print(kwargs)
    sqs.publish('connector started')
    return 'Whatever you return gets printed in the logs'


dag = DAG('connector_task_now', default_args=default_args)

connector_started_task = PythonOperator(
    task_id='connector_started',
    provide_context=True,
    python_callable=connector_started,
    dag=dag
)
run_some_docker_job = BashOperator(
    task_id='connection_job',
    env={'RUN_AS': 'adrian', 'AIRFLOW_ENV': ''},
    bash_command='docker run --rm  856816586042.dkr.ecr.us-east-1.amazonaws.com/hello',
    dag=dag)

connector_started_task.set_upstream(run_some_docker_job)
