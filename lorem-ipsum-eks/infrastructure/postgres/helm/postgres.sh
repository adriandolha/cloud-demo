#!/usr/bin/env bash
echo Postgres password:
read password
helm del postgres
helm install postgres bitnami/postgresql \
    --set postgresqlPassword=$password,postgresqlDatabase=lorem-ipsum
kubectl get secret postgres-postgresql  --namespace=default -o json |\
    jq 'del(.metadata.namespace,.metadata.resourceVersion,.metadata.uid)| .metadata.creationTimestamp=null'|\
    kubectl apply --namespace=demo -f -
