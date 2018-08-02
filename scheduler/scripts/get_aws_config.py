import os
from configparser import ConfigParser

with open(os.path.expanduser('~/.aws/credentials'), 'r') as file:
    content = file.readlines()
configuration_properties = [line.split('=') for line in content if '=' in line]
aws_credentials = {}

for config in configuration_properties:
    aws_credentials[config[0].strip()] = config[1].strip()
print(len(aws_credentials))
for k, v in aws_credentials.items():
    print('{}={}'.format(k, v))
