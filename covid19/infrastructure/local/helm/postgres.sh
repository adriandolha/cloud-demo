#!/usr/bin/env bash
echo $1
helm install bitnami/postgresql \
  --set postgresqlPassword=$1,postgresqlDatabase=covid19
kubectl get secret existing-peahen-postgresql  --namespace=default --export -o yaml |\
   kubectl apply --namespace=demo -f -
