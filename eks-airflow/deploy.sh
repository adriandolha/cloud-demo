#!/usr/bin/env bash
helm del --purge airflow
helm install --values values.yaml --namespace "airflow" --name "airflow" stable/airflow