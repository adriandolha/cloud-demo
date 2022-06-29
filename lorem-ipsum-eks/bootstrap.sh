#!/bin/bash
echo $HOME
rc=$(kubectl get ns platform --ignore-not-found)
if [[ "$rc" == *"platform"* ]]; then
    echo "Platform ready."
else
    echo "Creating platform ns."
    kubectl create ns platform
    ./infrastructure/postgres/deploy.sh
    echo "Platform ready."
fi
rc=$(kubectl get ns dev --ignore-not-found)
if [[ "$rc" == *"dev"* ]]; then
    echo "Dev ns ready."
else
    echo "Creating dev ns."
    kubectl create ns dev
fi

# secrets
kubectl delete secret -n dev jwk-certs --ignore-not-found
kubectl -n dev create secret generic jwk-certs --from-file=$HOME/.cloud-projects/oauth
kubectl delete secret -n dev  postgres-postgresql --ignore-not-found
kubectl get secret postgres-postgresql -n platform -o yaml | grep -v '^\s*namespace:\s' | kubectl apply -n dev -f -
kubectl delete secret -n dev  lorem-ipsum --ignore-not-found
kubectl delete secret -n dev  lorem-ipsum-auth --ignore-not-found
kubectl apply -f $HOME/.cloud-projects/lorem-ipsum-secrets.yaml
MY_PATH=$(pwd)
echo $MY_PATH

# Authentication service
cd $MY_PATH/lorem-ipsum-authentication
./deploy.sh

# Lorem Ipsum service
cd $MY_PATH/lorem-ipsum
./deploy.sh

# Nginx
rc=$(kubectl get ns ingress-nginx --ignore-not-found)
if [[ "$rc" == *"ingress-nginx"* ]]; then
    echo "Nginx ready."
else
    echo "Deploying nginx."
    cd $MY_PATH/infrastructure/local/nginx
    ./deploy.sh
    echo "Nginx ready."
fi

# UI
cd $MY_PATH/lorem-ipsum-react/lorem-ipsum-web
npm install
npm start
