#!/bin/bash

docker build -t lorem-ipsum-auth:dev .
kubectl delete -f app.yaml --ignore-not-found
kubectl delete secret jwk-certs -n demo --ignore-not-found
kubectl -n kube-system create secret generic jwk-certs -n demo --from-file=/Users/adriandolha/ambassador/certificates

# aws
#docker tag lorem-ipsum:dev 103050589342.dkr.ecr.eu-central-1.amazonaws.com/lorem-ipsum:dev
#docker push 103050589342.dkr.ecr.eu-central-1.amazonaws.com/lorem-ipsum:dev

kubectl apply -f app.yaml