#!/bin/bash

set -e

# Help function
usage() {
    echo "Usage: $0 -k <service-account-key-file> -p <project-id> -c <config-file>"
    echo "  -k: Path to service account key JSON file"
    echo "  -p: GCP Project ID"
    echo "  -c: Path to configuration YAML file"
    exit 1
}

# Parse command line arguments
while getopts "k:p:c:h" opt; do
    case $opt in
        k) SA_KEY_FILE="$OPTARG";;
        p) PROJECT_ID="$OPTARG";;
        c) CONFIG_FILE="$OPTARG";;
        h) usage;;
        \?) usage;;
    esac
done

# Validate required parameters
if [ -z "$SA_KEY_FILE" ] || [ -z "$PROJECT_ID" ] || [ -z "$CONFIG_FILE" ]; then
    echo "Error: All parameters are required"
    usage
fi

# Set base directory
BASE_DIR=$(pwd)

# Export credentials
export GOOGLE_APPLICATION_CREDENTIALS="$SA_KEY_FILE"

# Function to deploy a stage
deploy_stage() {
    local stage=$1
    local stage_dir=$2
    
    echo "Deploying stage: $stage"
    cd "$stage_dir"
    
    # Use main.py to handle the configuration and deployment
    python3 ../../src/main.py deploy "$CONFIG_FILE" --project-id="$PROJECT_ID"
    
    cd "$BASE_DIR"
}

# Deploy stages in sequence
echo "Starting GCP Landing Zone deployment..."

# 0-bootstrap
deploy_stage "bootstrap" "0-bootstrap"

# 1-org
deploy_stage "org" "1-org"

# 2-env
deploy_stage "environments" "2-env"

# 3-networks
deploy_stage "networking" "3-networks"

# 4-projects
deploy_stage "projects" "4-projects"

# 5-app-infra
deploy_stage "app_infra" "5-app-infra"

echo "GCP Landing Zone deployment completed successfully!" 