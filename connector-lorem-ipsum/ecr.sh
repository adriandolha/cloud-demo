#!/usr/bin/env bash
echo "Version is $1"
docker build -t connector-lorem-ipsum:dev .
docker tag connector-lorem-ipsum:dev 103050589342.dkr.ecr.eu-central-1.amazonaws.com/connector-lorem-ipsum:$1
docker push 103050589342.dkr.ecr.eu-central-1.amazonaws.com/connector-lorem-ipsum:$1