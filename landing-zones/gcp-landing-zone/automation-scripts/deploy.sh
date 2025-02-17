#!/bin/bash

set -e

# Help function
usage() {
    echo "Usage: $0 -k <service-account-key-file> -p <project-id> -m <mode>"
    echo "  -k: Path to service account key JSON file"
    echo "  -p: GCP Project ID"
    echo "  -m: Mode (plan or apply)"
    exit 1
}

# Parse command line arguments
while getopts "k:p:m:h" opt; do
    case $opt in
        k) SA_KEY_FILE="$OPTARG";;
        p) PROJECT_ID="$OPTARG";;
        m) MODE="$OPTARG";;
        h) usage;;
        \?) usage;;
    esac
done

# Validate required parameters
if [ -z "$SA_KEY_FILE" ] || [ -z "$PROJECT_ID" ] || [ -z "$MODE" ]; then
    echo "Error: All parameters are required"
    usage
fi

# Validate mode
if [ "$MODE" != "plan" ] && [ "$MODE" != "apply" ]; then
    echo "Error: Mode must be either 'plan' or 'apply'"
    usage
fi

# Export credentials
export GOOGLE_APPLICATION_CREDENTIALS="$SA_KEY_FILE"

# Set base directory
base_dir=$(pwd)

# Bootstrap stage
cd "$base_dir/0-bootstrap"
./prep.sh tf_local

# Replace configuration values
sed -i'' -e "s|ORG_ID_REPLACE_ME|${ORG_ID}|" ./terraform.tfvars
sed -i'' -e "s|BILLING_ID_REPLACE_ME|${BILLING_ID}|" ./terraform.tfvars
sed -i'' -e "s|PARENT_FOLDER_REPLACE_ME|${ROOT_FOLDER_ID}|" ./terraform.tfvars
sed -i'' -e "s|DEFAULT_REGION_REPLACE_ME|${REGION}|" ./terraform.tfvars

# Initialize and validate configuration
terraform init
terraform validate

# Create a timestamp for the plan file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PLAN_FILE="terraform_plan_${TIMESTAMP}.txt"

# Show plan and save to file
echo "Saving plan to ${PLAN_FILE}"
terraform plan -out=tfplan | tee "${PLAN_FILE}"

# Upload plan to GCS
echo "Uploading plan to GCS bucket"
BUCKET_NAME="${PROJECT_ID}-terraform-plans"
if ! gsutil ls -b "gs://${BUCKET_NAME}" >/dev/null 2>&1; then
    echo "Creating bucket ${BUCKET_NAME}"
    gsutil mb -p "${PROJECT_ID}" "gs://${BUCKET_NAME}"
fi
gsutil cp "${PLAN_FILE}" "gs://${BUCKET_NAME}/bootstrap/${PLAN_FILE}"

# Apply if in apply mode
if [ "$MODE" == "apply" ]; then
    terraform apply tfplan
fi

# Get the service account for impersonation
export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=$(terraform output -raw projects_step_terraform_service_account_email)

# Deploy stages in sequence
stages=("1-org" "2-env" "3-networks" "4-projects" "5-app-infra")
for stage in "${stages[@]}"; do
    echo "Deploying stage: $stage"
    cd "$base_dir/$stage"
    
    # Initialize Terraform
    terraform init
    
    # Plan and save
    terraform plan -out=tfplan | tee "${stage}_${PLAN_FILE}"
    gsutil cp "${stage}_${PLAN_FILE}" "gs://${BUCKET_NAME}/${stage}/${PLAN_FILE}"
    
    # Validate
    set +e
    terraform validate
    set -e
    
    # Apply if in apply mode
    if [ "$MODE" == "apply" ]; then
        terraform apply tfplan
    fi
done

# Cleanup
unset GOOGLE_IMPERSONATE_SERVICE_ACCOUNT 