import json
import os
# secrets must be stored user's home directory under .terraform/<app_name>_secrets.json
from terraform_external_data import terraform_external_data


@terraform_external_data
def get_secrets(query):
    # Terraform requires the values you return be strings,
    # so terraform_external_data will error if they aren't.
    with open('{}/.terraform/lorem_ipsum_secrets.json'.format(os.path.expanduser('~')), "r") as _file:
        secrets = _file.read()

    return json.loads(str(secrets))


if __name__ == '__main__':
    # Always protect Python scripts from import side effects with
    # a condition to check the __name__. Not specifically necessary
    # for terraform_external_data, but it's a best practice in general.
    get_secrets()
