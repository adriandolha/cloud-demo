from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret
from datetime import datetime, timedelta
from airflow import DAG
import uuid



default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': datetime.utcnow()
}
dag = DAG('connector-lorem-ipsum', schedule_interval='*/10 * * * *', default_args=default_args)

KubernetesPodOperator(namespace='airflow',
                      image="103050589342.dkr.ecr.eu-central-1.amazonaws.com/connector-lorem-ipsum:1.9",
                      env_vars={'CELERY_BROKER_URL': 'redis://:airflow@airflow-redis-master:6379/0'},
                      arguments=["action=create-job", f'no_of_pages=100', 'job_id=book_1'],
                      name="create-job",
                      task_id="create-job",
                      is_delete_operator_pod=True,
                      hostnetwork=False,
                      in_cluster=True,
                      dag=dag
                      )
KubernetesPodOperator(namespace='airflow',
                      image="103050589342.dkr.ecr.eu-central-1.amazonaws.com/connector-lorem-ipsum:1.15",
                      env_vars={'CELERY_BROKER_URL': 'redis://:airflow@airflow-redis-master:6379/0',
                                'REDIS_HOST': 'airflow-redis-master',
                                'REDIS_PASSWORD': 'airflow'},
                      arguments=["action=download-book", 'job_id=book_1'],
                      name="download-book",
                      task_id="download-book",
                      is_delete_operator_pod=True,
                      hostnetwork=False,
                      in_cluster=True,
                      dag=dag
                      )
