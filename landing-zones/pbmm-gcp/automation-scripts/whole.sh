#!/bin/bash

set -xe

# Help function
usage() {
    echo "Usage: $0 -k <service-account-key-file> -p <project-id> [-d <landing-zone-dir>] [-m <mode>]"
    echo "  -k: Path to service account key JSON file"
    echo "  -p: GCP Project ID for secrets"
    echo "  -d: Landing zone directory (default: landing-zones/pbmm-gcp)"
    echo "  -m: Mode (plan or apply, default: plan)"
    exit 1
}

# Default values
LANDING_ZONE_DIR="."
MODE="plan"

# Parse command line arguments
while getopts "k:p:d:m:h" opt; do
    case $opt in
        k) SA_KEY_FILE="$OPTARG";;
        p) PROJECT_ID="$OPTARG";;
        d) LANDING_ZONE_DIR="$OPTARG";;
        m) MODE="$OPTARG";;
        h) usage;;
        \?) usage;;
    esac
done

# Validate required parameters
if [ -z "$SA_KEY_FILE" ] || [ -z "$PROJECT_ID" ]; then
    echo "Error: Service account key file and project ID are required"
    usage
fi

# Validate mode
if [ "$MODE" != "plan" ] && [ "$MODE" != "apply" ]; then
    echo "Error: Mode must be either 'plan' or 'apply'"
    usage
fi

# Set base directory
base_dir=$(pwd)
landing_zone_path="$base_dir/$LANDING_ZONE_DIR"

# Validate landing zone directory exists
if [ ! -d "$landing_zone_path" ]; then
    echo "Error: Landing zone directory $landing_zone_path does not exist"
    exit 1
fi

# Export credentials
export GOOGLE_APPLICATION_CREDENTIALS="$SA_KEY_FILE"

# Bootstrap stage
cd "$landing_zone_path/0-bootstrap"
./prep.sh tf_local

# Replace configuration values using a different delimiter for sed
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
echo "Plan file uploaded to: gs://${BUCKET_NAME}/bootstrap/${PLAN_FILE}"

# Apply if in apply mode
if [ "$MODE" == "apply" ]; then
    terraform apply tfplan
fi

# Display configuration files for verification
echo "Configuration files:"
cat ./provider.tf
cat ./variables.tf
cat ./terraform.tfvars
cat ./terraform.tf
