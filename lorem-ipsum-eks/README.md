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

You also need to define the secrets:
E.g.
````
{
 "aurora_user":"",
 "aurora_password":""
}
````
### AWS Lambda connect to Postgres
In order to connect to postgres we need psycopg2, which is C compiled and won't work in AWS Lambda if installed locally, 
on MAC at least. To solve this, I've used a predefined layer:
arn:aws:lambda:eu-central-1:898466741470:layer:psycopg2-py37:6
More details here:
https://github.com/jetbridge/psycopg2-lambda-layer
### Database connection from local
Make sure the following are set on AWS database instance:
* public accesibility: yes
* Inbound rules: allow from local

## Authentication and authorization
Authentication and authorization is done using OAuth and OIDC.

### Microservices
* decodes and validates token, checks for expiration, etc. 
* use authlib jose (https://pypi.org/project/Authlib/) for oauth
* enforces permissions using decorators

## Install
Run the following command inside terraform folder:
````
./deploy.sh apply
````
To cleanup aws resources, run the following command inside terraform folder:
````
./deploy.sh destroy
````
## Usage
 
Once deployed you can start using the app and make requests.
 
 