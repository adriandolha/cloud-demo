# Sypmtoms sevice.
Symptoms service can be dployed both as serverless AWS lambda or MSA kubernetes.

## Monitoring
Done using Grafana (http://localhost:31910) and Prometheus(http://localhost:30320/. To monitor gunicorn look at this tutorial:
https://signoz.io/blog/monitor-gunicorn-django-in-prometheus/ 
Statsd was deployed to monitor gunicorn stats.