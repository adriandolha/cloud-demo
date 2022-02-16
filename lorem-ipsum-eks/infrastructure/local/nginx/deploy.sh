KEY_FILE=/Users/adriandolha/.cloud-projects/nginx/tls.key
CERT_FILE=/Users/adriandolha/.cloud-projects/nginx/tls.crt
kubectl create secret tls nginx-tls -n dev --key ${KEY_FILE} --cert ${CERT_FILE}