#!/usr/bin/env bash
cp dags/airflow.py ~/airflow/dags
#airflow clear connector_task -s 2018-07-18
airflow backfill -s 2018-07-18 connector_task