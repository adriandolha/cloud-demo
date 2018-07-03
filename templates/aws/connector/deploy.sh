#!/usr/bin/env bash

rm -rf lambda_package
mkdir lambda_package
cp -r ../../../connector lambda_package
cd lambda_package
zip -r ../lambda_package.zip *