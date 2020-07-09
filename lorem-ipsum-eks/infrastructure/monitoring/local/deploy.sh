#!/usr/bin/env bash
kubectl delete ns monitoring
kubectl apply -f monitoring-namespace.yaml
kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f prometheus-service.yaml
helm del --purge grafana
helm install stable/grafana -f grafana-values.yaml -n grafana
