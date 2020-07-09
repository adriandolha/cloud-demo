#!/usr/bin/env bash
kubectl apply -f local-storage.yaml
helm repo add elastic https://Helm.elastic.co
helm delete --purge elasticsearch
helm delete --purge kibana
helm delete --purge fluentd

Helm install --name elasticsearch elastic/elasticsearch -f values-local.yaml
Helm install --name kibana elastic/kibana -f kibana-values.yaml
helm install stable/fluentd -n fluentd \
--set=image.tag=v2.5.2,resources.limits.cpu=200m,output.host=elasticsearch-master.default.svc.cluster.local,\
elasticsearch.hosts=[elasticsearch-master.default.svc.cluster.local:9200],\
image.repository=quay.io/fluentd_elasticsearch/fluentd