#!/bin/bash
docker build -t lorem-ipsum:dev .
#docker tag lorem-ipsum:dev 103050589342.dkr.ecr.eu-central-1.amazonaws.com/lorem-ipsum:dev
#docker push 103050589342.dkr.ecr.eu-central-1.amazonaws.com/lorem-ipsum:dev
# kubectl -n dev create secret generic jwk-certs-oauth -n tekton-pipelines --from-file=/Users/adriandolha/.cloud-projects/oauth

kubectl delete -f app.yaml --ignore-not-found
kubectl apply -f app.yaml


