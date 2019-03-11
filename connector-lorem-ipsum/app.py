import datetime
import sys
import uuid

from celery import Celery
import os
import redis
import boto3

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']

app = Celery('connector-lorem-ipsum-tasks', backend=CELERY_BROKER_URL, broker=CELERY_BROKER_URL)


def create_job(arguments):
    app.send_task(name='app.create_job', kwargs={
        'no_of_pages': int(arguments['no_of_pages']),
        'job_id': arguments['job_id']
    })


def download_book(arguments):
    _redis=redis.Redis(host=os.environ['REDIS_HOST'], password=os.environ['REDIS_PASSWORD'])
    job_id = f'job_{arguments["job_id"]}'
    book = str(_redis.get(job_id))
    print(book)

    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    file_name= str(datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S%z'))
    print(file_name)
    with open(file_name, "w") as text_file:
        text_file.write(book)
    s3_resource.Object('connector-demo-data', file_name).upload_file(Filename=file_name)
    # _redis.delete(job_id)


if __name__ == "__main__":
    print('Running connector...')
    arguments = {item.split('=')[0]: item.split('=')[1] for item in sys.argv[1:]}
    if arguments['action'] == 'create-job':
        create_job(arguments)

    if arguments['action'] == 'download-book':
        download_book(arguments)
    print('Run completed...')
