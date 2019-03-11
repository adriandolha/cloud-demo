from celery import Celery
import os

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']

app = Celery('connector-lorem-ipsum-tasks',roker=CELERY_BROKER_URL)
app.conf.result_backend=CELERY_BROKER_URL


@app.task
def create_job(job_id, no_of_pages):
    return {'a': 'b'}
