KEY_FILE=/Users/adriandolha/.cloud-projects/nginx/tls.key
CERT_FILE=/Users/adriandolha/.cloud-projects/nginx/tls.crt
kubectl create secret tls nginx-tls -n dev --key ${KEY_FILE} --cert ${CERT_FILE}
helm upgrade --install ingress-nginx ingress-nginx   --repo https://kubernetes.github.io/ingress-nginx   --namespace ingress-nginx --create-namespace