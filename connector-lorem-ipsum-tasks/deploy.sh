#!/usr/bin/env bash
#docker run --env-file ~/aws/environment/connector-lorem-ipsum-tasks.txt -t connector-lorem-ipsum-tasks:dev
kubectl -n airflow delete --ignore-not-found deployment connector-lorem-ipsum-tasks
kubectl apply -f pod.yaml