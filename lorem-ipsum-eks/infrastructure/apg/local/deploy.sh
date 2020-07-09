#!/usr/bin/env bash
# pre-requisites: create certificate using the following command:
# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -subj '/CN=ambassador-cert' -nodes
kubectl create secret tls tls-cert --cert=/Users/adriandolha/ambassador/cert.pem \
--key=/Users/adriandolha/ambassador/key.pem
kubectl delete -f https://www.getambassador.io/yaml/aes-crds.yaml --ignore-not-found
kubectl delete -f https://www.getambassador.io/yaml/aes.yaml --ignore-not-found
kubectl delete -f ambassador.yaml --ignore-not-found

kubectl apply -f https://www.getambassador.io/yaml/aes-crds.yaml && \
kubectl wait --for condition=established --timeout=90s crd -lproduct=aes && \
kubectl apply -f https://www.getambassador.io/yaml/aes.yaml && \
kubectl -n ambassador wait --for condition=available --timeout=90s deploy -lproduct=aes
kubectl apply -f ambassador.yaml
kubectl apply -f mappings.yaml