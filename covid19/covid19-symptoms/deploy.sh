#!/bin/bash
docker build -t covid19:dev .
docker tag covid19:dev 103050589342.dkr.ecr.eu-central-1.amazonaws.com/covid19:dev
docker push 103050589342.dkr.ecr.eu-central-1.amazonaws.com/covid19:dev

kubectl -n demo delete deployment covid19 --ignore-not-found
kubectl -n demo delete service covid19 --ignore-not-found
kubectl -n demo delete service covid19-prometheus-np --ignore-not-found
kubectl -n demo delete service covid19-prometheus-cip --ignore-not-found
kubectl -n demo delete service covid19-statsd-np --ignore-not-found

kubectl apply -f pod.yaml
kubectl apply -f service.yaml

