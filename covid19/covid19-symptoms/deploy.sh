#!/bin/bash
docker build -t covid19:dev .

kubectl -n demo delete deployment covid19 --ignore-not-found
kubectl -n demo delete service covid19 --ignore-not-found

kubectl apply -f pod.yaml
kubectl apply -f service.yaml
