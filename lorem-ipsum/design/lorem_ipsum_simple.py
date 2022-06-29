from diagrams import Cluster, Diagram
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import React


def kube_svc(name, replica_count, db):
    svc = Service(name)
    apps = []
    for _ in range(replica_count):
        pod = Pod("pod")
        apps.append(svc >> pod >> db)
    return svc


with Diagram("Lorem Ipsum Simple", show=True, filename='lorem_ipsum_simple'):
    ui = React("UI")

    with Cluster("Lorem Ipsum - Kube"):
        with Cluster("db") as cluster:
            db_books = PostgreSQL("books")
            db_auth = PostgreSQL("auth")
        net = Nginx("loremipsum.com")
        net >> kube_svc('books', 2, db_books)
        net >> kube_svc('auth', 2, db_auth)
        search_engine = Service("Search Engine")
        db_books - search_engine
    ui >> net
