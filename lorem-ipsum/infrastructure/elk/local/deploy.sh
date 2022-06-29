#!/usr/bin/env bash
helm repo add elastic https://Helm.elastic.co
helm delete --purge elasticsearch
helm delete --purge kibana
helm delete --purge fluentd
# persistence
kubectl delete pvc -l app=elasticsearch-master -n efk --ignore-not-found
kubectl delete pv -l type=local --ignore-not-found
rm -rf /Users/adriandolha/data/vol0 /Users/adriandolha/data/vol1 /Users/adriandolha/data/vol2
mkdir /Users/adriandolha/data/vol0 /Users/adriandolha/data/vol1 /Users/adriandolha/data/vol2
kubectl apply -f local-storage.yaml


helm install --namespace efk --name elasticsearch elastic/elasticsearch -f elasticsearch-values.yaml
helm install --namespace efk --name kibana elastic/kibana -f kibana-values.yaml
kubectl delete -f fluentd.yaml --ignore-not-found
kubectl apply -f fluentd.yaml
#helm install --namespace efk stable/fluentd -n fluentd \
#--set=image.tag=v2.5.2,resources.limits.cpu=200m,output.host=elasticsearch-master.efk.svc.cluster.local,\
#elasticsearch.hosts=[elasticsearch-master.efk.svc.cluster.local:9200],\
#image.repository=quay.io/fluentd_elasticsearch/fluentd