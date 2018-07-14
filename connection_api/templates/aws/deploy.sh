#!/usr/bin/env bash
source ~/PycharmProjects/cloud-demo/venv/bin/activate
S3_BUCKET='cloud-demo-terraform-state-connection-api'

aws --version
if aws s3 ls "s3://$S3_BUCKET" 2>&1 | grep -q 'An error occurred'
then
    echo "bucket does not exit or permission is not there to view it."
    aws s3api create-bucket --bucket $S3_BUCKET --region us-east-1
else
    echo "bucket exists"
fi
aws s3 cp s3://$S3_BUCKET/terraform.tfstate ./
aws s3 cp s3://$S3_BUCKET/terraform.tfstate.backup ./
echo "Backup restored"

aws s3 cp terraform.tfstate s3://$S3_BUCKET
aws s3 cp terraform.tfstate.backup s3://$S3_BUCKET
#rm -rf lambda_package
#mkdir lambda_package
#cp -r ../../../connection lambda_package
#cd lambda_package
#zip -r ../lambda_package.zip *
#cd ..
#terraform apply