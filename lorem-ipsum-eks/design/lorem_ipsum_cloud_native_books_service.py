from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.oci.compute import Container
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Gunicorn
from diagrams.programming.framework import Flask

with Diagram("Lorem Ipsum Cloud Native Books Service", show=True, filename='lorem_ipsum_cloud_native_books_service'):
    with Cluster("Kube"):
        svc = Service('svc')
        pod = Pod('pod')

        with Cluster('Runtime'):
            stats = Custom('stats', './resources/statsd.png')
            container = Container('container')
            docker = Docker('')
            web = Flask('web')
            wsgi = Gunicorn('wsgi')
            container >> Edge(label='runs_on') >> docker
            container >> Edge(label='runs') >> [wsgi]
            container >> Edge(label='uses') >> [web]
            wsgi >> stats
        svc >> pod >> container
