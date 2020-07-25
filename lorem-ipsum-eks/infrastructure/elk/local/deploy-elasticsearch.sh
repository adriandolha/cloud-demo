#!/usr/bin/env bash
helm repo add elastic https://Helm.elastic.co
helm delete --purge elasticsearch
# persistence
kubectl delete pvc -l app=elasticsearch-master -n efk --ignore-not-found
kubectl delete pv -l type=local --ignore-not-found
rm -rf /Users/adriandolha/data/vol0 /Users/adriandolha/data/vol1 /Users/adriandolha/data/vol2
mkdir /Users/adriandolha/data/vol0 /Users/adriandolha/data/vol1 /Users/adriandolha/data/vol2
kubectl apply -f local-storage.yaml

helm install --namespace efk --name elasticsearch elastic/elasticsearch -f elasticsearch-values.yaml \
--set=replicas=1,--set=minimumMasterNodes=1