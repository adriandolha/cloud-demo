#!/bin/bash
helm uninstall ingress-nginx -n ingress-nginx
helm uninstall postgres -n platform
kubectl delete ns platform
kubectl delete ns dev
kubectl delete ns ingress-nginx
