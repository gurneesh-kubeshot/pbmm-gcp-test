#!/bin/bash
set -xe

# Set base directory
base_dir=$(pwd)
# Defin variables

export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=labels-app-sa@vratant-test-prj.iam.gserviceaccount.com

cd $base_dir/1-org
ls ./envs/shared/
#copy the wrapper script
cp ../build/tf-wrapper.sh .

#set read,write,execute permissions
chmod 755 ./tf-wrapper.sh

ls -ltr

#get organization_id
export ORGANIZATION_ID=$(terraform -chdir="../0-bootstrap/" output -json common_config | jq '.org_id' --raw-output)
$(gcloud scc notifications describe "scc-notify" --organization=${ORGANIZATION_ID} ) || true

# Retrieve AACCESS_CONTEXT_MANAGER_ID Policy ID
export ACCESS_CONTEXT_MANAGER_ID=$(gcloud access-context-manager policies list --organization ${ORGANIZATION_ID} --format="value(name)")
echo "access_context_manager_policy_id = ${ACCESS_CONTEXT_MANAGER_ID}"

set +e
#Update .tfvars File
if [ ! -z "${ACCESS_CONTEXT_MANAGER_ID}" ]; then
  sed -i'' -e "s=//create_access_context_manager_access_policy=create_access_context_manager_access_policy=" ./envs/shared/terraform.tfvars;
fi
set -xe
#Retrieve Backend Bucket Name
export backend_bucket=$(terraform -chdir="../0-bootstrap/" output -raw gcs_bucket_tfstate)
echo "remote_state_bucket = ${backend_bucket}"

# Update .tfvars File
sed -i'' -e "s/REMOTE_STATE_BUCKET/${backend_bucket}/" ./envs/shared/terraform.tfvars

#Retrieve Service Account Email
export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=$(terraform -chdir="../0-bootstrap/" output -raw organization_step_terraform_service_account_email)
echo ${GOOGLE_IMPERSONATE_SERVICE_ACCOUNT}

export seed_project_id=$(terraform -chdir="../0-bootstrap/" output -raw seed_project_id)
echo "seed_project_id = ${seed_project_id}"

sed -i'' -e "s/\"projects\/fortigcp-project-001\"/\"projects\/fortigcp-project-001\",\"projects\/${seed_project_id}\"/" ./envs/shared/terraform.tfvars

sed -i'' -e "s/DOMAIN/${DOMAIN}/" ./envs/shared/terraform.tfvars
cat ./envs/shared/terraform.tfvars

./tf-wrapper.sh init production
./tf-wrapper.sh plan production
set +e
./tf-wrapper.sh validate production $(pwd)/../policy-library ${CLOUD_BUILD_PROJECT_ID}
#./tf-wrapper.sh apply production
set +e

unset GOOGLE_IMPERSONATE_SERVICE_ACCOUNT

rm -rf ./envs/shared/.terraform
cd ..
tar -zcf env.tar.gz --exclude env.tar.gz . 
tar -zcf env.tar.gz --exclude env.tar.gz --exclude .git --exclude docs . 
ls -la
pwd
