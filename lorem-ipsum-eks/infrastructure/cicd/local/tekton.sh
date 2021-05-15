#!/usr/bin/env bash
# https://docs.ventuscloud.eu/docs/tutorials/tekton-pipelines

kubectl apply --filename https://storage.googleapis.com/tekton-releases/latest/release.yaml
kubectl apply --filename https://storage.googleapis.com/tekton-releases/dashboard/latest/tekton-dashboard-release.yaml
brew install istioctl
cat << EOF > ./istio-minimal-operator.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      proxy:
        autoInject: disabled
      useMCP: false
      # The third-party-jwt is not enabled on all k8s.
      # See: https://istio.io/docs/ops/best-practices/security/#configure-third-party-service-account-tokens
      jwtPolicy: first-party-jwt

  addonComponents:
    pilot:
      enabled: true

  components:
    ingressGateways:
      - name: istio-ingressgateway
        enabled: true
EOF
istioctl install -f istio-minimal-operator.yaml

kubectl apply -f https://github.com/knative/serving/releases/download/v0.22.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/v0.22.0/serving-core.yaml
kubectl apply -f https://github.com/knative/net-kourier/releases/download/v0.22.0/kourier.yaml
kubectl apply -f https://github.com/knative/eventing/releases/download/v0.22.0/eventing-crds.yaml
kubectl apply -f https://github.com/knative/eventing/releases/download/v0.22.0/eventing-core.yaml
kubectl apply --filename https://github.com/tektoncd/dashboard/releases/download/v0.10.1/tekton-webhooks-extension-release.yaml -n tekton-pipelines