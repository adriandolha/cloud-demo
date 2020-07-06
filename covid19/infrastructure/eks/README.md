#Deploys eks cluster.
https://www.padok.fr/en/blog/aws-eks-cluster-terraform

To set local kube config:
aws eks --region eu-central-1 update-kubeconfig --name eks_cluster_pandemic_support
To build docker images in ECR (latest awscli):
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 103050589342.dkr.ecr.eu-central-1.amazonaws.com
