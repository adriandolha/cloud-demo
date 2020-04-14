#!/usr/bin/env bash
set -e

#VARS


ENV="dev"




# call the build script
function build {
  # ./build.sh branch
  ./build.sh "${BRANCH}"
}


function terraform_init {
  # init terraform
  echo "%b⚓Terraform init...%b\n" 
  terraform init

  # make sure that the workspace exists, if not create a new one and use that one
  echo "%b⚓Creating and selecting the $ENV environment(workspace)...%b\n" 
  terraform workspace select "$ENV" || terraform workspace new "$ENV"
}

case "$1" in
  apply)
    build
    terraform_init
    echo "%b⚓Deploying to \"$ENV\" environment%b\n" 
    terraform apply -auto-approve -var env="$ENV"
    echo "%b⚓Deployment finished from branch \"$BRANCH\" to \"$ENV\" environment%b\n" "$green" "$default"
    ;;
  destroy)
    # if destroy is called then the environment should be the next argument
    
    echo "%b⚓Destroying \"$ENV\" environment for this component\n%b" 
    terraform_init
    terraform destroy -auto-approve -var env="$ENV"
    # switch to the default workspace so that we can delete the workspace
    terraform workspace select default
    # delete the workspace/environment
    terraform workspace delete "$ENV"
    ;;
  *)
    
esac