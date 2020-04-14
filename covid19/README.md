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