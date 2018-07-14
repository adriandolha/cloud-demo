cd c:\apps\cloud_demo\templates\aws\connection
rm -Force -Recurse lambda_package
rm -Force lambda_package.zip
New-Item -Type Directory lambda_package
Copy-Item -Destination lambda_package -Path ..\..\..\logme.ini -v
Copy-Item -Destination lambda_package -Path ..\..\..\connection -Recurse -v
Copy-Item -Destination lambda_package -Path ..\..\..\venv\Lib\site-packages\logme -Recurse -v
Copy-Item -Destination lambda_package -Path ..\..\..\venv\Lib\site-packages\click -Recurse -v
Copy-Item -Destination lambda_package -Path ..\..\..\venv\Lib\site-packages\bnmutils -Recurse -v
cd lambda_package
dos2unix .
cd ..
7z a -tzip lambda_package.zip .\lambda_package\*
#Compress-Archive lambda_package\* -DestinationPath lambda_package.zip -v -Force
terraform apply