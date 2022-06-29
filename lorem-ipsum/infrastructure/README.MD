# Infrstracture provisioning

The infrastructure can be provisioned on different environments, i.e. local, aws, etc.
## Pre-requisites
* kubernetes installed, e.g. docker for desktop
* helm installed, e.g. brew
* helm repos
```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

## Local
Local environment is on kubernetes and contains the following:
* postgres database
* monitoring with grafana and prometheus
* centralized logging with elastic, statsd and kibana
* ambassador api gateway

## Monitoring
Monitoring is implemented using Prometheus and Grafana.
Prometheus metrics:
* server monitoring: cAdvisor
* app metrics: prometheus-flask-exporter
* server health status: blackbox-exporter

Grafana dashboards:
* Kubernetes cluster monitoring
* Prometheus Blackbox Exporter
* Lorem ipsum metrics: gunicorn requests, connection pool stats
 
## Troubleshooting
There might be some errors that you encounter when running for the first time.

### Error: could not find tiller
Probably the kubernetes cluster was rebuild and it doesn't have tiller installed.
To fix it run the following:
```
helm init --service-account tiller --override spec.selector.matchLabels.'name'='tiller',spec.selector.matchLabels.'app'='helm' --output yaml | sed 's@apiVersion: extensions/v1beta1@apiVersion: apps/v1@' | kubectl apply -f -
```
