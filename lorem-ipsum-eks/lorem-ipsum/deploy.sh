#!/bin/bash
docker build -t lorem-ipsum:dev .
docker tag lorem-ipsum:dev 103050589342.dkr.ecr.eu-central-1.amazonaws.com/lorem-ipsum:dev
docker push 103050589342.dkr.ecr.eu-central-1.amazonaws.com/lorem-ipsum:dev
kubectl apply -f app.yaml --ignore-not-found
kubectl apply -f app.yaml


