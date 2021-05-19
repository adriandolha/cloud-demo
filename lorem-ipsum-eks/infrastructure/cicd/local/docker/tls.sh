#!/usr/bin/env bash
openssl req \
  -newkey rsa:4096 -nodes -sha256 -keyout ~/.cloud-projects/tls.key \
  -subj "/C=RO/CN=lorem-ipsum" \
  -x509 -days 365 -out ~/.cloud-projects/tls.crt -config /etc/ssl/openssl.cnf -extensions req_ext
kubectl delete secret tls-cert -n demo
kubectl create secret tls tls-cert --cert=/Users/adriandolha/.cloud-projects/tls.crt \
--key=/Users/adriandolha/.cloud-projects/tls.key -n demo
#Add this in /etc/ssl/openssl.conf
#[ alternate_names ]
#DNS.1        = docker-registry.demo
#DNS.2        = kubernetes.docker.internal