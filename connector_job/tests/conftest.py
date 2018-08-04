import importlib
import os

import pytest
from mock import mock


@pytest.fixture()
def mock_connection_valid():
    return {
        'connection_id': '012ad701-57ca-453f-9733-1de1d77d2840',
        'connector': {'connector_id': 'dcmapireport'},
        'parameters':
            {
                'profile_id': '22340723',
                'report_id': '138567177'
            }
    }


@pytest.fixture(scope='module')
def generate_dcmapireport_job_file(mock_connection_valid):
    templates_dir = os.path.dirname(os.path.abspath(__file__).replace('tests', 'templates'))
    print(templates_dir)
    job_dir = os.path.dirname(os.path.abspath(__file__).replace('tests', 'jobs'))
    for file_path in os.listdir(templates_dir):
        if file_path.endswith('.template'):
            job_name = file_path.replace('.py.template', '')
            with open(os.path.join(templates_dir, file_path), 'r') as file:
                template = file.read()
            job_content = template.replace('$connection', str(mock_connection_valid))
            with open(os.path.join(job_dir, f'{job_name}.py'), 'w') as job_file:
                job_file.write(job_content)


@pytest.fixture()
def mock_job_valid(mock_connection_valid):
    templates_dir = os.path.dirname(os.path.abspath(__file__).replace('tests', 'templates'))
    print(templates_dir)
    job_dir = os.path.dirname(os.path.abspath(__file__).replace('tests', 'jobs'))
    for file_path in os.listdir(templates_dir):
        if file_path.endswith('.template'):
            job_name = file_path.replace('.py.template', '')
            with open(os.path.join(templates_dir, file_path), 'r') as file:
                template = file.read()
            job_content = template.replace('$connection', str(mock_connection_valid))
            with open(os.path.join(job_dir, f'{job_name}.py'), 'w') as job_file:
                job_file.write(job_content)


def reload_module():
    """
    Reload the module after a new file was generated.
    """
    importlib.reload(importlib.import_module('jobs.dcmapireport'))


@pytest.fixture()
def mock_airflow():
    with mock.patch('airflow.DAG'):
        with mock.patch('airflow.operators.python_operator.PythonOperator'):
            with mock.patch('airflow.operators.bash_operator.BashOperator'):
                reload_module()
                yield ''
