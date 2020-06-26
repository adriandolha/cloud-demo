#!/usr/bin/env bash
echo $1
helm install bitnami/postgresql \
  --set postgresqlPassword=$1,postgresqlDatabase=covid19
