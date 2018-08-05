import importlib
import airflow
from mock import mock

from job import service


def test_schedule_interval_six_bst_am(mock_job_valid, mock_airflow):
    args, kwargs = airflow.DAG.call_args_list[0]
    print(kwargs)
    assert kwargs['default_args']['schedule_interval'] == '0 5 * *'


def test_docker_command_valid(mock_job_valid, mock_airflow):
    args, kwargs = airflow.operators.bash_operator.BashOperator.call_args_list[0]
    assert 'docker run 933886674506.dkr.ecr.us-east-1.amazonaws.com/dcmapireport_connector:dev_dan ' \
           'program=/app/dcmapireport_connector/dcmapireport_' \
           'connector.py credential_store=aws account=dcmapireport ' \
           'data_source=gcs ' \
           'client=dan ' \
           'env=dev ' \
           'destination_storage=aws.s3 ' \
           'envname=nonprod ' \
           'region=eu-west-1 ' \
           'download_delay=300 ' \
           'profile_id=22340723 ' \
           'report_id=138567177 ' in kwargs['bash_command']


def test_connector_run_task_id_valid(mock_job_valid, mock_airflow):
    args, kwargs = airflow.operators.bash_operator.BashOperator.call_args_list[0]
    assert 'dcmapireport_connector' == kwargs['task_id']


def test_connector_running_task_id_valid(mock_job_valid, mock_airflow):
    args, kwargs = airflow.operators.python_operator.PythonOperator.call_args_list[0]
    assert 'connector_running' == kwargs['task_id']
    assert kwargs['provide_context']


def test_connector_success_task_id_valid(mock_job_valid, mock_airflow):
    args, kwargs = airflow.operators.python_operator.PythonOperator.call_args_list[1]
    assert 'connector_success' == kwargs['task_id']
    assert kwargs['provide_context']


def test_connector_run_on_failure_callback_arguments_valid(mock_job_valid, mock_airflow, mock_connection_valid):
    args, kwargs = service.job_failed.call_args_list[0]
    assert mock_connection_valid['connection_id'] == args[0]
    assert 'dcmapireport' == args[1]


def test_connector_running_arguments_valid(mock_job_valid, mock_airflow, mock_connection_valid):
    args, kwargs = service.job_running.call_args_list[0]
    assert mock_connection_valid['connection_id'] == args[0]
    assert 'dcmapireport' == args[1]


def test_connector_success_arguments_valid(mock_job_valid, mock_airflow, mock_connection_valid):
    args, kwargs = service.job_success.call_args_list[0]
    assert mock_connection_valid['connection_id'] == args[0]
    assert 'dcmapireport' == args[1]
