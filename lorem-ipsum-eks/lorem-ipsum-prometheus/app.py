import os

from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time
import logging

logging.basicConfig(format='%(levelname)s:%(message)s')
LOGGER = logging.getLogger('lorem-ipsum')


# LOGGER.setLevel(logging.DEBUG)


class JsonCollector(object):
    def __init__(self, endpoint):
        self._endpoint = endpoint
        self.pod_name = os.getenv('pod_name', default='pod_name')

    def collect(self):
        # Fetch the JSON
        metrics = requests.get(self._endpoint)
        # LOGGER.debug(metrics)
        response = json.loads(metrics.content.decode('UTF-8'))
        LOGGER.debug(response)
        # Convert requests and duration to a summary in seconds
        _labels = {'pod_name': self.pod_name}
        metric = Metric('lorem_ipsum_metric',
                        'Requests time taken in seconds', 'summary')
        metric.add_sample('lorem_ipsum_metric_connection_pool_maxconn',
                          value=response['connection_pool.maxconn'], labels=_labels)
        metric.add_sample('lorem_ipsum_metric_connection_pool_usedconn',
                          value=response['connection_pool.usedconn'], labels=_labels)
        metric.add_sample('lorem_ipsum_metric_connection_pool_rusedconn',
                          value=response['connection_pool.rusedconn'], labels=_labels)
        metric.add_sample('lorem_ipsum_metric_connection_pool_size',
                          value=response['connection_pool.size'], labels=_labels)
        metric.add_sample('lorem_ipsum_metric_thread_count',
                          value=response['thread_count'], labels=_labels)
        yield metric


if __name__ == '__main__':
    start_http_server(int(sys.argv[1]))
    REGISTRY.register(JsonCollector(sys.argv[2]))
    while True: time.sleep(1)
