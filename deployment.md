# Deploying GCP Landing Zone

## Repository Structure

Create different private repositories for each stage (names need not be the same):

- **Repo 1**: `gcp-0-bootstrap-repo`
- **Repo 2**: `gcp-1-org-repo`
- **Repo 3**: `gcp-2-environments-repo`
- **Repo 4**: `gcp-3-networks-dual-repo`
- **Repo 5**: `gcp-3-networks-hubandspoke-repo`

---

## **Deploying Bootstrap**

### **1. Repository Structure**
```
/gcp-0-bootstrap-repo
│── gcp-bootstrap/
│   │── envs/
│   │   ├── shared/                     # Terraform bootstrap configurations
│   │   │   ├── main.tf & other files    # All files from 0-bootstrap of the landing zone
│   │
│   │── policy-library/                  # Policy guardrails (copied from LZ)
│   │   ├── policies/
│   │   ├── constraints/
│   │   ├── README.md
│   │
│   │── .github/workflows/               # GitHub Actions CI/CD workflows
│   │   ├── github-tf-plan.yaml
│   │   ├── github-tf-apply.yaml
│   │
│   │── tf-wrapper.sh                     # Terraform wrapper script
│   │── README.md
```

### **2. Update Terraform Configurations**
- Un-comment the required sections for your CI/CD platform in `versions.tf`, `variables.tf`, `outputs.tf`.
- Rename the following files:
```sh
mv ./cb.tf ./cb.tf.example
mv ./github.tf.example ./github.tf
mv ./terraform.example.tfvars ./terraform.tfvars
```
- Update `terraform.tfvars` with required values.
- Set access token as an environment variable: `TF_VAR_gh_token`.

### **3. Validation Steps**
```sh
../../../terraform-example-foundation/scripts/validate-requirements.sh -o <ORG_ID> -b <BILLING_ACCOUNT_ID> -u <EMAIL> -e
gcloud beta terraform vet
terraform init
terraform plan -input=false -out bootstrap.tfplan
```
```sh
export VET_PROJECT_ID=<VALID_PROJECT_ID>
terraform show -json bootstrap.tfplan > bootstrap.json
gcloud beta terraform vet bootstrap.json --policy-library="../../policy-library" --project ${VET_PROJECT_ID}
```

### **4. Apply Terraform Plan**
```sh
terraform apply bootstrap.tfplan
```

### **5. Extract Outputs**
```sh
export network_step_sa=$(terraform output -raw networks_step_terraform_service_account_email)
export projects_step_sa=$(terraform output -raw projects_step_terraform_service_account_email)
export cicd_project_id=$(terraform output -raw cicd_project_id)
```

### **6. Migrate to Remote Backend**
```sh
export backend_bucket=$(terraform output -raw gcs_bucket_tfstate)
echo "backend_bucket = ${backend_bucket}"
cp backend.tf.example backend.tf
```
```sh
for i in `find . -name 'backend.tf'`; do sed -i'' -e "s/UPDATE_ME/${backend_bucket}/" $i; done
```

### **7. Push to GitHub and Trigger Pipeline**
Push to the required branch and check the GitHub Actions output.

---

## **Deploying Further Stages**

### **1. Initialize Repositories**
```sh
git commit --allow-empty -m 'repository seed'
git push --set-upstream origin main
git checkout -b production
git push --set-upstream origin production
git checkout -b nonproduction
git push --set-upstream origin nonproduction
git checkout -b development
git push --set-upstream origin development
git checkout -b plan
```

### **2. Repository Structure**
```
/gcp-0-{stage}-repo
│── gcp-{stage}/
│   │── envs/
│   │   ├── shared/                     # Terraform configurations
│   │   │   ├── main.tf & other files   # All files from 0-bootstrap from landing zone
│   │
│   │── policy-library/                  # Policy guardrails (copied from LZ)
│   │   ├── policies/
│   │   ├── constraints/
│   │   ├── README.md
│   │
│   │── .github/workflows/               # GitHub Actions CI/CD workflows
│   │   ├── github-tf-plan.yaml
│   │   ├── github-tf-apply.yaml
│   │
│   │── tf-wrapper.sh                     # Terraform wrapper script
│   │── README.md
```

### **3. Rename Configuration Files**
```sh
mv ./cb.tf ./cb.tf.example
mv ./github.tf.example ./github.tf
mv ./terraform.example.tfvars ./terraform.tfvars
mv common.auto.example.tfvars common.auto.tfvars
mv shared.auto.example.tfvars shared.auto.tfvars
```

### **4. Update Variables**
- Update `terraform.tfvars`.
- If `shared.auto.tfvars` exists, update target_name_server_addresses.
- Update `common/shared/development/production/nonproduction.auto.tfvars` if present.
- Extract Access Context Manager ID:
```sh
export ORGANIZATION_ID=$(terraform -chdir="../gcp-bootstrap/envs/shared/" output -json common_config | jq '.org_id' --raw-output)
export ACCESS_CONTEXT_MANAGER_ID=$(gcloud access-context-manager policies list --organization ${ORGANIZATION_ID} --format="value(name)")
echo "access_context_manager_policy_id = ${ACCESS_CONTEXT_MANAGER_ID}"
sed -i'' -e "s/ACCESS_CONTEXT_MANAGER_ID/${ACCESS_CONTEXT_MANAGER_ID}/" ./access_context.auto.tfvars
```

### **5. Update Remote State Bucket**
```sh
export backend_bucket=$(terraform -chdir="../gcp-bootstrap/envs/shared" output -raw gcs_bucket_tfstate)
echo "remote_state_bucket = ${backend_bucket}"
sed -i'' -e "s/REMOTE_STATE_BUCKET/${backend_bucket}/" ./envs/shared/terraform.tfvars
```

### **6. Commit & Merge**
Push to `plan` branch, validate changes, then merge into `nonproduction` and finally `production`.

### **7. Run Terraform Commands (Network Step Only)**
```sh
export CICD_PROJECT_ID=$(terraform -chdir="../gcp-bootstrap/envs/shared/" output -raw cicd_project_id)
export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=$(terraform -chdir="../gcp-bootstrap/envs/shared/" output -raw networks_step_terraform_service_account_email)

./tf-wrapper.sh init shared
./tf-wrapper.sh plan shared
./tf-wrapper.sh validate shared $(pwd)/policy-library ${CICD_PROJECT_ID}
./tf-wrapper.sh apply shared
git push --set-upstream origin plan
```

### **8. Cleanup**
Before moving to the next step:
```sh
unset GOOGLE_IMPERSONATE_SERVICE_ACCOUNT
```

