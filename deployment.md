Create different private repositries for each stage(Names need not to be same)
    Repo 1: gcp-0-bootstrap-repo 
    Repo 2: gcp-1-org-repo
    Repo 3: gcp-2-enviornments-repo
    Repo 4: gcp-3-networks-dual-repo
    Repo 5: gcp-3-networks-hubandspoke-repo

                DEPLOYING BOOTSTRAP
1. The repo should have the following structure
        /gcp-0-bootstrap-repo
            │── gcp-bootstrap/                        
            │   │── envs/                             
            │   │   ├── shared/                        # Contains Terraform bootstrap configurations
            │   │   │   ├── main.tf && otherfiles      # Contains all files from 0-bootstap from landing zone
            │   │
            │   │── policy-library/                     # Contains policy guardrails(copied from parent dir in LZ)
            │   │   ├── policies/
            │   │   ├── constraints/
            │   │   ├── README.md
            │   │
            │   │── .github/workflows/                  # GitHub Actions workflows for CI/CD(Copied from build dir in LZ)
            │   │   ├── github-tf-plan.yaml             ## Can use different file for other cicd platforms
            │   │   ├── github-tf-apply.yaml
            │   │
            │   │── tf-wrapper.sh                        # Terraform wrapper script
            │   │── README.md
3. Un-comment sections for your cicd platform from versions.tf,varialbes.tf, outputs.tf from each section
4. Rename following files
    mv ./cb.tf ./cb.tf.example
    mv ./github.tf.example ./github.tf
    mv ./terraform.example.tfvars ./terraform.tfvars
5. Variables- update values in terraform.tfvars
            - set your access token as env var (TF_VAR_gh_token)
6. Validations- 

    ../../../terraform-example-foundation/scripts/validate-requirements.sh  -o <ORGANIZATION_ID> -b <BILLING_ACCOUNT_ID> -u <END_USER_EMAIL> -e

    gcloud beta terraform vet

    terraform init
    terraform plan -input=false -out bootstrap.tfplan

    export VET_PROJECT_ID=A-VALID-PROJECT-ID
    terraform show -json bootstrap.tfplan > bootstrap.json
    gcloud beta terraform vet bootstrap.json --policy-library="../../policy-library" --project ${VET_PROJECT_ID}

7. terraform apply bootstrap.tfplan
8. Outputs-
        export network_step_sa=$(terraform output -raw networks_step_terraform_service_account_email)
        export projects_step_sa=$(terraform output -raw projects_step_terraform_service_account_email)
        export cicd_project_id=$(terraform output -raw cicd_project_id)

        echo "CI/CD Project ID = ${cicd_project_id}"
        echo "network step service account = ${network_step_sa}"
        echo "projects step service account = ${projects_step_sa}"
9. Migrate to remote backend

    export backend_bucket=$(terraform output -raw gcs_bucket_tfstate)
    echo "backend_bucket = ${backend_bucket}"

    cp backend.tf.example backend.tf
    cd ../../../

    for i in `find . -name 'backend.tf'`; do sed -i'' -e "s/UPDATE_ME/${backend_bucket}/" $i; done
    for i in `find . -name 'backend.tf'`; do sed -i'' -e "s/UPDATE_PROJECTS_BACKEND/${backend_bucket}/" $i; done

    cd gcp-bootstrap/envs/shared

10. Push to required branch and this will trigger the pipeline, check github actions output
     

            DEPLOYING FURTHER STAGES
1. Initialize and seed the repostries and change to non production branch
        git commit --allow-empty -m 'repository seed'
        git push --set-upstream origin main

        git checkout -b production
        git push --set-upstream origin production

        git checkout -b nonproduction
        git push --set-upstream origin nonproduction

        git checkout -b development
        git push --set-upstream origin development

        git checkout -b plan

2. The repo should have the following structure
        /gcp-0-{stage}-repo
            │── gcp-{stage}/                        
            │   │── envs/                             
            │   │   ├── shared/                        # Contains Terraform configurations
            │   │   │   ├── main.tf && otherfiles      # Contains all files from 0-bootstap from landing zone
            │   │
            │   │── policy-library/                     # Contains policy guardrails(copied from parent dir in LZ)
            │   │   ├── policies/
            │   │   ├── constraints/
            │   │   ├── README.md
            │   │
            │   │── .github/workflows/                  # GitHub Actions workflows for CI/CD(Copied from build dir in LZ)
            │   │   ├── github-tf-plan.yaml             ## Can use different file for other cicd platforms
            │   │   ├── github-tf-apply.yaml
            │   │
            │   │── tf-wrapper.sh                        # Terraform wrapper script
            │   │── README.md.

3. Rename following files(Some of them might not be present in all steps)
    mv ./cb.tf ./cb.tf.example
    mv ./github.tf.example ./github.tf
    mv ./terraform.example.tfvars ./terraform.tfvars
    mv common.auto.example.tfvars common.auto.tfvars
    mv shared.auto.example.tfvars shared.auto.tfvars
    mv access_context.auto.example.tfvars access_context.auto.tfvars
    mv development.auto.example.tfvars development.auto.tfvars
    mv nonproduction.auto.example.tfvars nonproduction.auto.tfvars
    mv production.auto.example.tfvars production.auto.tfvars

4. Variables- update values in terraform.tfvars
            - If shared.auto.tfvars is present update with values for target_name_server_addresses
            - update *common/shared/development/production/nonproduction*.auto.tfvars if present 
            - Update the file access_context.auto.tfvars with the organization's access_context_manager_policy_id if present
                    export ORGANIZATION_ID=$(terraform -chdir="../gcp-bootstrap/envs/shared/" output -json common_config | jq '.org_id' --raw-output)

                    export ACCESS_CONTEXT_MANAGER_ID=$(gcloud access-context-manager policies list --organization ${ORGANIZATION_ID} --format="value(name)")

                    echo "access_context_manager_policy_id = ${ACCESS_CONTEXT_MANAGER_ID}"

                    sed -i'' -e "s/ACCESS_CONTEXT_MANAGER_ID/${ACCESS_CONTEXT_MANAGER_ID}/" ./access_context.auto.tfvars

5. Update the remote_state_bucket variable with the backend bucket from previous step

        export backend_bucket=$(terraform -chdir="../gcp-bootstrap/envs/shared" output -raw gcs_bucket_tfstate)

        echo "remote_state_bucket = ${backend_bucket}"

        sed -i'' -e "s/REMOTE_STATE_BUCKET/${backend_bucket}/" ./envs/shared/terraform.tfvars

6. Commit changes and push to plan, if successfull merge the PR into non production branch, review and then merge into production branch
**** from network step Only *****
    export CICD_PROJECT_ID=$(terraform -chdir="../gcp-bootstrap/envs/shared/" output -raw cicd_project_id)
    echo ${CICD_PROJECT_ID}
    export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=$(terraform -chdir="../gcp-bootstrap/envs/shared/" output -raw networks_step_terraform_service_account_email)
    echo ${GOOGLE_IMPERSONATE_SERVICE_ACCOUNT}

    ./tf-wrapper.sh init shared
    ./tf-wrapper.sh plan shared
    ./tf-wrapper.sh validate shared $(pwd)/policy-library ${CICD_PROJECT_ID}
    ./tf-wrapper.sh apply shared
    git push --set-upstream origin plan

    Before moving to next step:

    unset GOOGLE_IMPERSONATE_SERVICE_ACCOUNT
