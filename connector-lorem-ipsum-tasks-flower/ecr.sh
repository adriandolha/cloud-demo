#!/usr/bin/env bash
docker build -t connector-lorem-ipsum-tasks-flower:dev .
docker tag connector-lorem-ipsum-tasks-flower:dev 103050589342.dkr.ecr.eu-central-1.amazonaws.com/connector-lorem-ipsum-tasks-flower:1.6
docker push 103050589342.dkr.ecr.eu-central-1.amazonaws.com/connector-lorem-ipsum-tasks-flower:1.6