import json

from celery import Celery
import os
import faker
import redis

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']

app = Celery('connector-lorem-ipsum-tasks', roker=CELERY_BROKER_URL)
app.conf.result_backend = CELERY_BROKER_URL


@app.task
def create_job(job_id, no_of_pages):
    print(f'Running job {job_id}.')
    _redis = redis.Redis(host=os.environ['REDIS_HOST'], password=os.environ['REDIS_PASSWORD'])
    _faker = faker.Faker()
    book = json.dumps(
        {f'page_{page}': [_faker.text(max_nb_chars=100) for i in range(30)] for page in range(no_of_pages)})
    redis_key_name = f'job_{job_id}'
    _redis.set(name=redis_key_name, value=book)

    redis_stored_value = _redis.get(name=redis_key_name)
    print(f'Completed job {job_id}.')
    return redis_stored_value
