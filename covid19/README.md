# COVID-19 app to collect and monitor pacients data.
An application to monitor pacients data and view heat map.
Tech stack:
python
terraform
aws aurora, lambda, api gateway

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