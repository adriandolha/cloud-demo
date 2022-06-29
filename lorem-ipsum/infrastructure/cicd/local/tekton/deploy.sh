#!/usr/bin/env bash
kubectl delete secret jwk-certs-auth0 -n tekton-pipelines
kubectl create secret generic jwk-certs-auth0 -n tekton-pipelines --from-file=/Users/adriandolha/auth0
kubectl apply -f /Users/adriandolha/.cloud-projects/lorem-ipsum-local-unit.yaml