# Lorem Ipsum
This is a simple text generator, useful to generate books and get some random content to be used elsewhere.

It uses faker library in the backend to generate books with a given number of pages, a random title and random author.

The application is actually used as a technical playground to prove architectural concepts: 
* architecture styles: serverless, microservices
* cloud: aws, azure
* api gateway
* caching
* nosql
* monitoring: prometheus, grafana
* log aggregator: fluentd, elasticsearch, kibana
* frontend: React, Bootstrap
* etc.

Tech stack for the architecture described below:
- python
- terraform (s3 backup)
- tekton, argocd
- ambassador, aws api gw, istio
- eks, kuberneteds
- parameter store, kube secrets
- prometheus, grafana
- elasticsearch, fluentd, kibana
- flask, gunicorn, pytest, sqlalchemy, authlib, flask-swagger, pydantic
- faker
- docker
- react, bootstrap, cdbreact

## Achitecture diagrams
<details>
  <summary>Architecure diagrams for local and cloud native deployments </summary>
  
### Local
![img|500x500](design/lorem_ipsum_simple.png)
### Cloud Native
![](design/lorem_ipsum_cloud_native.png)
### Books service
![](design/lorem_ipsum_cloud_native_books_service.png)
### CI/CD
![](design/lorem_ipsum_cloud_native_cidcd.png)
</details>
     

## Configuration and pre-requisites
Pre-requisites:
* docker
* kubernetes
* helm
* npm
* ~/.cloud-projects/oauth/public.key and ~/.cloud-projects/oauth/private.key (you can create these with openssl)
* ~/.cloud-projects/lorem-ipsum-secrets.yaml

### Lorem Ipsum secrets example
<details>
  <summary>Secrets example for lorem ipsum and authentication service </summary>

````
apiVersion: v1
kind: Secret
metadata:
  name: lorem-ipsum
  namespace: dev
type: Opaque
stringData:
  aurora-host: "postgres-postgresql.platform.svc.cluster.local"
  aurora-database: "lorem_ipsum_dev"
  root-url: "http://lorem-ipsum.dev.svc.cluster.local"
  aurora-user: "postgres"
  aurora-port: "5432"
  admin-user: admin
  admin-password: <admin_password>
  jwk-public-key-path: "/jwk/certs/public.key"
---
apiVersion: v1
kind: Secret
metadata:
  name: lorem-ipsum-auth
  namespace: dev
type: Opaque
stringData:
  aurora-host: "postgres-postgresql.platform.svc.cluster.local"
  aurora-database: "lorem_ipsum_dev"
  root-url: "http://lorem-ipsum.dev.svc.cluster.local"
  aurora-user: "postgres"
  aurora-port: "5432"
  admin-user: admin
  admin-password: <admin_password>
  guest-user: guest
  guest-password: <guest_password>
  jwk-public-key-path: "/jwk/certs/public.key"
  jwk_private_key_path: "/jwk/certs/private.key"
  google-client-id: "<google_client_id>"
  google-client-secret: "<google_client_secret>"

````
</details>

## Authentication and authorization
Authentication and authorization is done using OAuth and OIDC.

### Microservices
* decodes and validates token, checks for expiration, etc. 
* use authlib jose (https://pypi.org/project/Authlib/) for oauth
* enforces permissions using decorators

## Install
Run the following command inside terraform folder:
````
./boostrap.sh apply
````
To cleanup resources, run the following command inside terraform folder:
````
./destrpy.sh 
````
## Usage
 
Once deployed you can start using the app and make requests.
 
 