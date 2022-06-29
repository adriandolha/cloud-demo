#!/bin/bash
docker build -t lorem-ipsum-auth:dev .
kubectl delete -f app.yaml --ignore-not-found
kubectl apply -f app.yaml