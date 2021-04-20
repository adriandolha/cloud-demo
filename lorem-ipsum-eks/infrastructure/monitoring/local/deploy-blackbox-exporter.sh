#!/usr/bin/env bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install blackbox prometheus-community/prometheus-blackbox-exporter -n monitoring
