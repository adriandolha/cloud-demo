#!/usr/bin/env bash
docker build -t connector-lorem-ipsum:dev .
docker run --env-file ~/aws/environment/connector-lorem-ipsum.txt -t connector-lorem-ipsum:dev hello=hollo