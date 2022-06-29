#!/bin/bash
docker build -t lorem-ipsum:dev .
kubectl delete -f app.yaml --ignore-not-found
kubectl apply -f app.yaml


