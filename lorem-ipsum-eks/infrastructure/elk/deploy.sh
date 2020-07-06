#!/usr/bin/env bash
#helm repo add elastic https://Helm.elastic.co
#Helm install --name elasticsearch elastic/elasticsearch -f values.yaml
#Helm install --name kibana elastic/kibana -f kibana-values.yaml
#helm install stable/fluentd \
#--set=image.tag=v2.5.2,resources.limits.cpu=200m,output.host=elasticsearch-master.default.svc.cluster.local,\
#elasticsearch.hosts=[elasticsearch-master.default.svc.cluster.local:9200],\
#image.repository=quay.io/fluentd_elasticsearch/fluentd