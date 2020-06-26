import base64
import os
import sys
from functools import lru_cache

import boto3
import uuid
from covid19_symptoms.serializers import to_json, from_json
import psycopg2
import logging
from psycopg2.extras import RealDictCursor

logging.basicConfig(format='%(levelname)s:%(message)s')

ssm = boto3.client("ssm")
session = boto3.session.Session()

LOGGER = logging.getLogger('symptoms')
LOGGER.setLevel(logging.DEBUG)
LOGGER.info('hello5')


@lru_cache()
def get_config():
    kms = session.client('kms')
    secret = os.getenv('aurora_password')
    aurora_password = kms.decrypt(CiphertextBlob=base64.b64decode(secret))['Plaintext'].decode('utf-8')
    return {
        'aurora_host': os.getenv('aurora_host'),
        'aurora_user': os.getenv('aurora_user'),
        'aurora_password': aurora_password
    }


def get_ssm_secret(parameter_name, decrypt=True):
    return ssm.get_parameter(
        Name=parameter_name,
        WithDecryption=decrypt
    )


def response(api_response):
    return {
        'statusCode': api_response['status_code'],
        'body': api_response['body']
    }


def api_context(event, context):
    if not event:
        event = {}
    if not context:
        context = {}
    return {
        'user_id': str(uuid.uuid4()),
        'body': event.get('body') or {},
        'path_parameters': event.get('pathParameters') or {}
    }


@lru_cache()
def setup():
    LOGGER.debug('Running database setup...')
    print(f'here{LOGGER.level}')

    connection = get_connection(get_config())
    cursor = connection.cursor()
    try:
        LOGGER.debug('Creating table...')

        cursor.execute('CREATE TABLE IF NOT EXISTS public.symptoms\
            (\
                contact boolean NOT NULL,\
                cough boolean NOT NULL,\
                fever boolean NOT NULL,\
                id character varying(50) COLLATE pg_catalog."default" NOT NULL,\
                red_zone_travel boolean NOT NULL,\
                tiredness boolean NOT NULL,\
                difficulty_breathing boolean NOT NULL,\
                CONSTRAINT symptoms_pk PRIMARY KEY (id)\
            )')
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def get_connection(config):
    connection = psycopg2.connect(user=config['aurora_user'],
                                  password=config['aurora_password'],
                                  host=config['aurora_host'],
                                  port=5432,
                                  database="covid19",
                                  cursor_factory=RealDictCursor)
    return connection


def add(event, context=None):
    LOGGER.info(f'event = {event}')
    LOGGER.info(f'context={context}')
    config = get_config()

    setup()
    data = from_json(event['body'])
    LOGGER.info(f'data = {data}')
    data['id'] = str(uuid.uuid4())
    connection = get_connection(config)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO symptoms(id, contact, red_zone_travel, fever, cough, tiredness,difficulty_breathing) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (data['id'],
             data['contact'],
             data['red_zone_travel'],
             data['fever'],
             data['cough'],
             data['tiredness'],
             data['difficulty_breathing']))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return response({"status_code": '200', 'body': to_json(data)})


def list(event, context=None):
    print(event)
    print(context)
    connection = get_connection(get_config())
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query_params = event.get('queryStringParameters')
    items = []
    try:
        LOGGER.debug('Reading items...')
        if query_params and query_params.get('id'):
            cursor.execute(
                'select *'
                'from symptoms where id = %s',
                (query_params['id'],))
            items.append(cursor.fetchone())
            count = 1
        else:
            cursor.execute('select count(*) from symptoms')
            result = cursor.fetchone()
            count = result['count']


    finally:
        cursor.close()
        connection.close()
    return response({"status_code": '200', 'body': to_json({"items": items, "total": count})})
