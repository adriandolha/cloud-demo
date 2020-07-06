#!/bin/bash
docker build -t covid19-prometheus:dev .
docker tag covid19-prometheus:dev 103050589342.dkr.ecr.eu-central-1.amazonaws.com/covid19-prometheus:dev
docker push 103050589342.dkr.ecr.eu-central-1.amazonaws.com/covid19-prometheus:dev
