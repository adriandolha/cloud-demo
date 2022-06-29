#!/usr/bin/env bash
echo Postgres password:
read password
helm del postgres
helm install postgres bitnami/postgresql -n platform\
    --set postgresqlPassword=$password,postgresqlDatabase=lorem_ipsum_dev

