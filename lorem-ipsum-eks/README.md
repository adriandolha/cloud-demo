# Lorem Ipsum app to collect and monitor pacients data.
An application to prove architectural concepts: 
* architecture styles: serverless, microservices
* cloud: aws, azure
* api gateway
* caching
* nosql
* monitoring: prometheus, grafana
* log aggregator: fluentd, elasticsearch, kibana
* etc.
This example is focused on microservices in eks.
Tech stack:
python
terraform (s3 backup)
ambassador
eks, ambassador
parameter store
prometheus, grafana
elasticsearch, fluentd, kibana
flask, gunicorn, pytest, sqlalchemy
docker


## Configuration and pre-requisites

Terraform secrets are stored in user's home folder under .terraform/<app_name>.json.
E.g.
````
{
 "aurora_user":"",
 "aurora_password":""
}
````
In order to be able tu use external data, you need to install terraform module in your python env:
```
pip install terraform_external_data
``` 
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

### Auth0
* auth0 (https://auth0.com/docs/architecture-scenarios/spa-api)
* use auth0 rules to add scope and custom role claim
* JWT token contains roles and permissions
````
{
  "http://schemas.microsoft.com/ws/2008/06/identity/claims/role": [
    "Admin"
  ],
  "iss": "https://dev-5z89rql0.eu.auth0.com/",
  "sub": "google-oauth2|100541778233022946437",
  "aud": [
    "https://dev-5z89rql0.eu.auth0.com/api/v2/",
    "https://dev-5z89rql0.eu.auth0.com/userinfo"
  ],
  "iat": 1616735582,
  "exp": 1616821982,
  "azp": "yZUy3dduMozo9pjFC6WLSwPySBgrBMFo",
  "scope": "openid profile email read:books create:books update:books delete:books"
}
````
### API Gateway
* API Gateway validates token and enforces Bearer Token (JWT)

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
 
 ## Testing
 Unit tests should mock the boundaries (sqlalchemy) and focus on APIs.
 
 ### Mocking tips
Mocking is quite powerful, but not always straight forward, therefore you can find some tips below.
Of course there are other ways/flavors to achieve the same goal, but this is one that works.

#### Mocking chained function calls
The key here is to use the return_value for the chained functions.
```
lorem_ipsum.repo.Transaction.session.query.return_value.filter.return_value.first.return_value = lorem_ipsum.repo.Book(
            **book_valid)
```
#### Mocking attributes
The key here is to use the return_value for the mocked object.
```
_pool = lorem_ipsum.repo.Transaction.pool
_pool.return_value._max_overflow = 50
```