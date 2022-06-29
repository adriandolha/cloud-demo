#!/bin/bash
KEY_FILE=$HOME/.cloud-projects/nginx/tls.key
CERT_FILE=$HOME/.cloud-projects/nginx/tls.crt
kubectl delete secret nginx-tls -n dev
kubectl create secret tls nginx-tls -n dev --key ${KEY_FILE} --cert ${CERT_FILE}

helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
 kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
kubectl delete -f nginx.yaml
kubectl apply -f nginx.yaml