import importlib
import airflow


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
           'report_id=138567177 ' \
           'aws_access_key_id= ' \
           'aws_secret_access_key=' == kwargs['bash_command']


def test_connector_started_call_valid(mock_job_valid, mock_airflow):
    args, kwargs = airflow.operators.python_operator.PythonOperator.call_args_list[0]
    print(kwargs)
    assert kwargs['task_id'] == 'connector_started'
    assert kwargs['provide_context']
    # args_list = job.service.job_running.call_args_list
    # print(args_list)
