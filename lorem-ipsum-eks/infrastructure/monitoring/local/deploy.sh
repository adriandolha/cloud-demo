#!/usr/bin/env bash
#helm repo add stable https://kubernetes-charts.storage.googleapis.com
helm repo add stable https://charts.helm.sh/stable
kubectl delete ns monitoring
kubectl apply -f monitoring-namespace.yaml
kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f prometheus-service.yaml
helm del --purge grafana
helm install grafana stable/grafana -f grafana-values.yaml -n grafana
