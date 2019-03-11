#!/usr/bin/env bash
kubectl -n airflow port-forward pod/airflow-web-79b846b94c-pg9ff  8080:8080 & \
kubectl -n airflow port-forward pod/airflow-flower-6c898fbb6-8gxwh 8001:5555 & \
kubectl -n airflow port-forward pod/connector-lorem-ipsum-tasks-flower-bc4d85cf8-p8m6c 8002:5555