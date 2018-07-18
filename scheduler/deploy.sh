#!/usr/bin/env bash
docker build . -t hello
mkdir ~/airflow/dags
cp dags/airflow.py ~/airflow/dags