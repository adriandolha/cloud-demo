cd c:\apps\cloud_demo\templates\aws\connector
rm -Force -Recurse lambda_package
New-Item -Type Directory lambda_package
Copy-Item -Destination lambda_package -Path ..\..\..\connector -Recurse -v
Compress-Archive lambda_package\* -DestinationPath lambda_package.zip -v -Force
terraform apply