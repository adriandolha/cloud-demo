from diagrams import Cluster, Diagram
from diagrams.alibabacloud.compute import ElasticSearch
from diagrams.elastic.elasticsearch import Kibana
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.network import Istio
from diagrams.onprem.tracing import Jaeger
from diagrams.programming.framework import React


def kube_svc(name, replica_count, db):
    svc = Service(name)
    apps = []
    for _ in range(replica_count):
        pod = Pod("pod")
        apps.append(svc >> pod >> db)
    return svc


with Diagram("Lorem Ipsum Cloud Native", show=True, filename='lorem_ipsum_cloud_native'):
    ui = React("UI")

    with Cluster("Kube"):
        net = Istio("loremipsum.com")
        with Cluster('Logging'):
            logging = Fluentd('logging')
            es = ElasticSearch('index')
            kibana = Kibana('Log View')
            logging >> es >> kibana
        with Cluster('Monitoring'):
            metrics = Prometheus('metrics')
            monitoring = Grafana('monitoring')
            tracing = Jaeger('tracing')

        with Cluster("DB") as cluster:
            db_books = PostgreSQL("books")
            db_auth = PostgreSQL("auth")
            # pvc = PVC("pvc")
            # pvc << [db_books, db_auth]
        with Cluster('Lorem Ipsum Apps'):
            books_svc = Service('books')
            apps = []
            for _ in range(2):
                pod = Pod("pod")
                apps.append(books_svc >> pod >> [db_books, metrics, logging])
            auth_svc = Service('auth')
            apps = []
            for _ in range(2):
                pod = Pod("pod")
                apps.append(auth_svc >> pod >> [db_auth, metrics, logging])
            search_engine = Service("Search Engine")

        net >> [books_svc, auth_svc, tracing]
        metrics >> [monitoring, tracing]
        db_books - search_engine
    ui >> net
