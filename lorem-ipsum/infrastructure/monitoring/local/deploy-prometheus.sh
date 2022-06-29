#!/usr/bin/env bash
kubectl delete -f prometheus-config.yaml --ignore-not-found
kubectl delete -f prometheus-deployment.yaml --ignore-not-found
kubectl delete -f prometheus-service.yaml --ignore-not-found

kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f prometheus-service.yaml

