from connector_notification import sqs
import json
import uuid


def test_sqs_add():
    sqs.publish(json.dumps({'id': str(uuid.uuid4()), 'name': 'sample_event'}))


def test_sqs_consume():
    messages = sqs.receive()
    for msg in messages:
        print(msg['Body'])
        sqs.delete(msg)
