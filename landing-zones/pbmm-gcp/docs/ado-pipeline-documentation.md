

# ADO Pipeline Documentation

En Français: [Documentation du pipeline ADO](./documentation-du-pipeline-ado.md)

## PBMM (Protected B, Medium Integrity/Medium Availability) Landing Zone


#### Contents

* [Overview](#overview)
* [Architecture](#architecture)
* [ADO Pipeline Deployment Flowchart](#ado-pipeline-deployment-flowchart)
  * [Infrastructure Design Decisions](#infrastructure-design-decisions)
* [Preparing for Deployment](#preparing-for-deployment)
  * [Cloning the azure repository](#cloning-the-azure-repository)
  * [Create a GCP Project](#create-a-gcp-project)
  * [Groups](#groups)
  * [Service Account IAM Prerequisites](#service-account-iam-prerequisites)
  * [Azure Library](#azure-library)
* [The Azure Pipeline Yaml and Automation Scripts](#the-azure-pipeline-yaml-and-automation-scripts)
  * [0-Bootstrap Yaml and Script Execution](#0-bootstrap-yaml-and-script-execution)
  * [1-Org Yaml and Script Execution](#1-org-yaml-and-script-execution)
  * [2-Environments Yaml and Script Execution](#2-environments-yaml-and-script-execution)
  * [3-networks-hub-and-spoke Yaml and Script Execution](#3-networks-hub-and-spoke-yaml-and-script-execution)
  * [4-projects Yaml and Script Execution](#4-projects-yaml-and-script-execution)
  * [6-org-policies Yaml and Script Execution](#6-org-policies-yaml-and-script-execution)
  * [7-fortigate Yaml and Script Execution](#7-fortigate-yaml-and-script-execution)
  * [Error Detection in Bash Scripts](#error-detection-in-bash-scripts)
  * [Reference README Files](#reference-readme-files)
* [Steps for ADO Pipeline Execution](#steps-for-ado-pipeline-execution)
  * [ADO Pipeline Execution Time](#ado-pipeline-execution-time)
  * [Output: GCP Folder Structure](#gcp-folder-structure)
  * [Steps to Re-run Failed Jobs](#steps-to-re-run-failed-jobs)
  * [Re-run New Pipeline on Intermittent errors](#re-run-new-pipeline-on-intermittent-errors)


# Overview <a name="overview"></a>

This process will deploy a Landing Zone as outlined in the [Technical Design Document](./technical-design-document.md) for the Canada PBMM Landing Zone.  The Landing Zone is a GitHub-hosted, Terraform-based, PBMM compliant Google Cloud Landing Zone.  Any GC department or agency can clone to their own repository, set variables, and deploy.  The following methodology will guide users through the end-to-end process.

The documentation comprehensively outlines the Azure DevOps pipeline based deployment option, from its architectural foundation to execution and troubleshooting. It delves into the pipeline's structure, configuration, and the sequence of stages involved in provisioning resources. Key components like the Azure Library and automation scripts are explained, along with details on error handling and performance metrics. The document aims to guide users through the pipeline's setup, execution, and Intermittent issues.

# Architecture <a name="architecture"></a>

![][image1]

# ADO Pipeline Deployment Flowchart <a name="ado-pipeline-deployment-flowchart"></a>

Following Flowchart describes the resources to be deployed in each of the different stages.  
![][image2]

## Infrastructure Design Decisions <a name="infrastructure-design-decisions"></a>

There are decisions that need to be made at the outset of the project and set into configuration.

1. Workload   
   1. Changes can be made to folders in steps 4 and 5 that will be reflected in the names of the projects created.   
   2. The resources in step 5 are a set of VMs as examples.  The resource definitions should be changed to match your actual workload.   
   3. Please refer to the TDD for further direction and more resources.  
2. VPC Configuration   
   1. The vpc\_config.yaml is the consolidated point for configuration. 

# Preparing for Deployment <a name="preparing-for-deployment"></a>

Following are the Prerequisites required for the Deployment of the Ado Pipeline

## Cloning the azure repository <a name="cloning-the-azure-repository"></a>

There are two ways to clone the azure repository.

1\. Copy the HTTPS url and use the git clone command in your terminal.

```bash
git clone <repo_url> 
git checkout <branch>
```

2\. Click on the Button “Clone in VS Code”. Select the destination folder and paste the generated git credentials.

![][image3]

## Create a GCP Project <a name="create-a-gcp-project"></a>

Following service to be created in the gcp project

* The service account(super admin)  
* And the JSON Key of the service account used for gcp authentication from ADO to GCP Environment.   
* Api to be enabled in the setup gcp project.

```
accesscontextmanager.googleapis.com
analyticshub.googleapis.com
artifactregistry.googleapis.com
bigquery.googleapis.com
bigqueryconnection.googleapis.com
bigquerydatapolicy.googleapis.com
bigquerymigration.googleapis.com
bigqueryreservation.googleapis.com
bigquerystorage.googleapis.com
billingbudgets.googleapis.com
cloudapis.googleapis.com
cloudasset.googleapis.com
cloudbilling.googleapis.com
cloudbuild.googleapis.com
cloudfunctions.googleapis.com
cloudkms.googleapis.com
cloudresourcemanager.googleapis.com
cloudtrace.googleapis.com
compute.googleapis.com
containerregistry.googleapis.com
dataform.googleapis.com
dataplex.googleapis.com
datastore.googleapis.com
essentialcontacts.googleapis.com
iam.googleapis.com
iamcredentials.googleapis.com
iap.googleapis.com
logging.googleapis.com
monitoring.googleapis.com
oslogin.googleapis.com
policysimulator.googleapis.com
pubsub.googleapis.com
secretmanager.googleapis.com
securitycenter.googleapis.com
securitycentermanagement.googleapis.com
servicemanagement.googleapis.com
servicenetworking.googleapis.com
serviceusage.googleapis.com
source.googleapis.com
sourcerepo.googleapis.com
sql-component.googleapis.com
storage-api.googleapis.com
storage-component.googleapis.com
storage.googleapis.com

```

## Groups <a name="groups"></a>

Following are the Groups to be created at Organization IAM Level.
```
gcp-organization-admins@example.com
gcp-billing-admins@example.com 
gcp-billing-data@example.com 
gcp-audit-data@example.com 
gcp-monitoring-workspace@example.com
```

## Service Account IAM Prerequisites <a name="service-account-iam-prerequisites"></a>

| Service Account  | IAM Permission  | Level  |
| :---- | :---- | :---- |
| Super Admin Email<br />(The Setup Service Account to <br />Execute the ADO Pipeline) | Access Context Manager Editor | Organization |
|  | Billing Account User | Organization |
|  | Compute Admin | Organization |
|  | Compute Network Viewer | Organization |
|  | Create Service Accounts | Organization |
|  | Folder Creator | Organization |
|  | Folder Viewer | Organization |
|  | Organization Administrator | Organization |
|  | Organization Policy Administrator | Organization |
|  | Organization Viewer | Organization |
|  | Quota Administrator | Organization |
|  | Security Center Notification Configurations Editor | Organization |
|  | Service Account Token Creator | Organization |
|  | Service Usage Admin | Organization |
|  | Service Usage Consumer | Organization |
|  | Storage Admin | Organization |
|  | Project Creator | Organization |
|  | Owner | Project |
|  | Service Account Token Creator | Project |
|  | Service Account User | Project |
|  | Billing Administrator | Billing Account |

## Azure Library   <a name="azure-library"></a>

### **1\. Variable Group** <a name="1.-variable-group"></a>

The Azure Library stores environment variables used as inputs for the ADO pipeline. These variables include Billing\_ID, Org\_id, region, root\_folder\_id, super\_admin\_email, domain, and vpc-sc perimeter user. They are referenced within the YAML pipeline.

| Variable Name  | Description |
| :---- | :---- |
| BILLING\_ID  | The billing account ID is an 18-character alphanumeric value assigned to your GCP Cloud Billing account. |
| DOMAIN | The Domain Name of the Organization eg: google.com |
| GCP\_SA\_KEY | The Json File of the GCP Service account (super admin)which is used for setup of the ado pipeline.  |
| ORG\_ID | The organization resource ID is a unique identifier for an organization resource. |
| PERIMETER USER  | It is the admin user to be added in VPC-SC Perimeter(access level). At least one user to be added. |
| REGION | It is the region to deploy all resources within it. |
| ROOT\_FOLDER\_ID | The Parent gcp folder id where all resources like folders and projects,etc to be deployed.(It should be created already) |
| SUPER\_ADMIN\_EMAIL | The Email of the Admin Service Account required for setup of the Ado Pipeline. |

![][image4]

### **2\. Secure File** <a name="2.-secure-file"></a>

Upload the Service Account Json File into the Azure-\>Library-\>Secure file.The Secure file is further used for the GCP Authentication.

# The Azure Pipeline Yaml and Automation Scripts <a name="the-azure-pipeline-yaml-and-automation-scripts"></a>

The Azure Pipeline YAML defines a sequential workflow composed of multiple stages. Each stage relies on template YAML files to execute Bash scripts, which in turn orchestrate Terraform operations (init, plan, apply). These template YAML files incorporate the Azure Library as a variables group to access necessary environment variables and also install terraform and various tools.Additionally, the YAML files manage tool installation, GCP credential configuration, and export necessary environment variables for the pipeline's execution.

Yaml Path: azure-pipelines  
Scripts Path: automation-scripts

```yaml

trigger: none


variables:
 - group: 'GCP_ZA_ADO-baseline-stages'


stages:
 - stage: Setup
   displayName: 'Setup Tools'
   jobs:
     - job: Access_GCP_environment
       displayName: 'Access to GCP'
       pool:
         vmImage: 'ubuntu-latest'
       steps:
         - template: templates/securefile-template.yaml
     - job: InstallTools
       displayName: 'Install Terraform'
       dependsOn: Access_GCP_environment
       pool:
         vmImage: 'ubuntu-latest'
       steps:
         - script: |
             curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
             sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com              $(lsb_release -cs) main"
             sudo apt-get install -y wget unzip
             wget  https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
             unzip terraform_1.6.0_linux_amd64.zip
             sudo mv terraform /usr/local/bin/
             sudo chmod +x /usr/local/bin/terraform
             terraform version
             sudo apt-get update && sudo apt-get install dos2unix
             sudo apt-get update && sudo apt-get install google-cloud-sdk
             sudo apt-get install google-cloud-cli-terraform-tools -y
             sudo apt-get install jq -y
             sudo apt update && sudo apt install python3  
             ls -l
             python3 ./fix_tfvars_symlinks.py .
             find . -type f -name "*.sh" | xargs chmod a+x
             find . -type f -name "*.sh" | xargs dos2unix


           displayName: 'Install Terraform'
           continueOnError: false


 - template: bootstrap_stage/bootstrap.yaml
   parameters:
     stageName: bootstrap_stage
     continueOnError: false
 - template: org_stage/org.yaml
   parameters:
     stageName: org_stage
     continueOnError: false


 - template: environments_stage/environments.yaml
   parameters:
     stageName: environments_stage
     continueOnError: false


 - template: network_hub_spoke_stage/network_hub_spoke.yaml
   parameters:
     stageName: network_hub_spoke_stage
     continueOnError: false


 - template: projects_stage/projects.yaml
   parameters:
     stageName: projects_stage
     continueOnError: false


 - template: orgpolicies_stage/orgpolicies.yaml
   parameters:
     stageName: orgpolicies_stage
     continueOnError: false


 - template: fortigate_stage/fortigate.yaml
   parameters:
     stageName: fortigate_stage
     continueOnError: false

```

## 0-Bootstrap Yaml and Script Execution <a name="0-bootstrap-yaml-and-script-execution"></a>

The Bootstrap YAML file initializes the pipeline by exporting essential environment variables, configuring GCP credentials, and deploying the bootstrap script. To optimize efficiency and prevent symlink issues, the bootstrap artifact is published at the end of this stage and downloaded in subsequent stages. This approach isolates each stage in its own environment, ensuring a clean execution and reliable results.The bootstrap script leverages Terraform to provision the resources defined in the 0-bootstrap directory.

| Stage  | Description |
| :---- | :---- |
| <nobr>0-bootstrap</nobr> | Bootstrap is a Google Cloud organization. This step also configures a CI/CD pipeline for the blueprint code in subsequent stages. The CICD project contains the Cloud Build foundation pipeline for deploying resources. The seed project includes the Cloud Storage buckets that contain the Terraform state of the foundation infrastructure and includes highly privileged service accounts that are used by the foundation pipeline to create resources. The Terraform state is protected through storage Object Versioning. When the CI/CD pipeline runs, it acts as the service accounts that are managed in the seed project. |

## 1-Org Yaml and Script Execution <a name="1-org-yaml-and-script-execution"></a>

The deployment pipeline utilizes an Org YAML file to download a 0-Bootstrap Artifact. This artifact acts as a container, holding all the previously executed files. Following the download, the pipeline executes the 1-org shell script. This script is responsible for deploying resources defined within the 1-org directory.

To ensure consistency and prevent conflicts after completion of each script, a tar archive is created, essentially capturing its state. This archive is then extracted at the start of the subsequent script. This approach guarantees file integrity throughout the entire deployment pipeline. Finally, the process concludes with the publication of the 1-org artifact.

| Stage  | Description |
| :---- | :---- |
| 1-org | Sets up top-level shared folders, projects for shared services, organization-level logging, and baseline security settings through organization policies. |

## 2-Environments Yaml and Script Execution <a name="2-environments-yaml-and-script-execution"></a>

The deployment pipeline utilizes an environment YAML file to download an 1-Org Artifact. This artifact acts as a container, holding all the previously executed files. Following the download, the pipeline executes the 2-environments shell script. This script is responsible for deploying resources defined within the 2-environments directory.Finally, the process concludes with the publication of the 2-environments artifact.

| Stage | Description |
| :---- | :---- |
| <nobr>2-environments</nobr> | Sets up development, non-production, and production environments within the Google Cloud organization that you've created. |

## VPC Config YAML

This YAML file defines the network configuration for the LZ and is used by the networks section in 3-networks-hub-and-spoke. It outlines the structure for regions, spokes (for workload environments), common resources and on-site network connections. 

See the Technical Design Document for design-related information. 

### **Usage Notes**

* Populate this YAML file with your specific network requirements  
* Make sure to understand the implications of each configuration option and adjust them to match your security and connectivity needs.

### **Regions**

A list of configurations for each of the 2 supported regions

* name: (required) the name of the region e.g.  
* enabled: (optional) by default "true" for region1 and "false" for region2. Set to true to deploy in a region

### **Production, Non-production and Development Spokes**

The spokes sections contain a common configuration section for the "spokes" and similar configurations for each of the "spokes". By default, this section contains 3 "spoke" environments (development, nonproduction and production). You can add or remove spokes as necessary. 

The configuration elements are:

* al\_env\_ip\_range: a summarized CIDR for the "spoke" address ranges  
* spoke\_common\_routes: Contains (if applicable) the common routing for all "spokes", by default 2 optional routes  
  * rt\_nat\_to\_internet: route to the Internet through the NAT gateway  
  * rt\_windows\_activation: route to Windows activation servers provided by Google

These routes can be supplemented or overridden by routes defined at the "spoke" environment level or even lower at the sub-environment ("base" or "restricted") level using a higher priority.

### **Spoke Configuration**

For each of the "spoke" environments there is a common configuration part and separate configurations for each of the sub-environments (by default "base" and "restricted").

The difference between "base" and "restricted" is the level of security. The "restricted" sub-environments use perimeter-type service controls that secure workloads.

### **Common Configuration**

The following parameters are common for the "base" and "restricted" sub-environments

* env\_code: (required) a one-letter code for the environment, found in resource names. By default it is "d" for development, "n" for nonproduction and "p" for production  
* env\_enabled: (optional) by default false, set to true to provision the "spoke" environment  
* nat\_igw\_enabled: (optional) controls the provisioning of the NAT function, by default false, set to true to configure the NAT gateways. Also implicitly conditions the provisioning of the NAT route to the Internet and the associated "cloud router" resources  
* windows\_activation\_enabled: (optional) controls the provisioning of the rt\_windows\_activation route. By default false.  
* enable\_hub\_and\_spoke\_transitivity: (optional) controls the deployment of VMs in shared VPCs to allow inter-spoke routing. By default false.  
* router\_ha\_enabled: (optional) controls the deployment of the second "cloud router" resource in each availability zone. The "cloud router" is free but not the BGP traffic through it. By default false.  
* mode: (optional) 2 possible values set "spoke" or "hub", this is used in the code. By default "spoke" at this level.

### **Configuration settings for "base" and "restricted"**

The configuration of the 2 sub-environments is the same, the routes and addressing could vary.

The following parameters are common:

* env\_type: (optional) This is a component of resource names. By default "shared-base" for "base" and "shared-restricted" for "restricted".  
* enabled: (optional) By default false. If true, the sub-environment is deployed.  
* private\_service\_cidr: (optional) This is in an address range in CIDR format which, if configured, allows the provisioning of "Private Service Access" connectivity, necessary to access services such as Cloud SQL or Cloud Filestore (file sharing).  
* private\_service\_connect\_ip: (required) this is the address that will be assigned to a private connection point, used to access Google API services in private mode.  
* subnets: (required) the configuration of the subnets. By default the subnet sets that are configured are as follows:  
  * id=primary: (optional) used for workloads, with address ranges for each region. It is optional to provision a subnet at the region level.  
    * secondary\_ranges: (optional) multiple secondary address ranges can be configured, again optionally in one or both regions, associated with the primary subnet. The only parameters provided (per region) are  
      * range\_suffix: (required) an arbitrary string that is used to generate the names of the secondary subnets  
      * ip\_cidr\_ranges: (required) the address range of the secondary subnet in CIDR format, for each region where you want to provision a secondary subnet.  
    * id: (required) a unique identifier for the subnet, which appears in the generated name of the created resource. We can provision  
    * description: (optional) a description of the function of the subnet  
    * ip\_ranges: (required) a subnet address space per region in CIDR format. For each region for which a CIDR range is specified, a separate subnet will be provisioned.  
    * subnet\_suffix: (optional) a string that will be appended to the end of the generated subnet name  
    * flow\_logs: (optional) custom "flow-log" settings compared to default values. The following fields can be specified:  
      * enable: (optional) default "false". If true, flow\_logs are enabled for the subnet  
      * interval: (optional) default 5 seconds  
      * medatata: (optional) default INCLUDE\_ALL\_METADATA  
      * metadata\_fields (optional) default empty  
    * private\_access: (optional) default false. Controls whether Google Private Access (PGA) is enabled at the subnet level. As this involves provisioning a "forwarding-rule" type resource, activation incurs costs.  
  * id=proxy: (optional) used for resources that use the Envoy proxy deployed in a VPC. Examples: application load balancer or internal "TCP proxy", API Gateway. There are parameters  
    * id: (required) a unique identifier for the subnet, which appears in the generated name of the created resource. We can provision  
    * description: (optional) a description of the function of the subnet  
    * ip\_ranges: (required) a subnet address space per region in CIDR format. For each region for which a CIDR range is specified, a separate subnet will be provisioned.  
    * subnet\_suffix: (optional) a string that will be appended to the end of the generated subnet name  
    * flow\_logs: (optional) custom "flow-log" settings compared to default values. The following fields can be specified:  
      * enable: (optional) default "false". If true, flow\_logs are enabled for the subnet  
      * interval: (optional) default 5 seconds  
      * medatata: (optional) default INCLUDE\_ALL\_METADATA  
      * metadata\_fields (optional) default empty  
    * role and purpose are required and specific to "proxy" type subnets. Leave the default values (role \= ACTIVE and purpose \= REGIONAL\_MANAGED\_PROXY)

### **The configuration of shared resources (common section)**

By default the "common" environment contains 2 sub-environments:

* dns-hub: (required) hosts the shared DNS zones with "DNS peering" as well as for DNS resolution between the cloud and the "on-site"  
* net-hub: (required) hosts the shared "hub" type VPCs, one per environment (production, nonproduction and development) and sub-environment (base and restricted)

For the "net-hub" sub-environment there are specific configurations, see the yaml configuration for details.

### **Example vpc\_config.yaml**

## 3-networks-hub-and-spoke Yaml and Script Execution  <a name="3-networks-hub-and-spoke-yaml-and-script-execution"></a>

The deployment pipeline utilizes an environment YAML file to download an 2-Environments Artifact. This artifact acts as a container, holding all the previously executed files. Following the download, the pipeline executes the 3-networks-hub-and-spoke shell script. This script is responsible for deploying resources defined within the 3-networks-hub-and-spoke directory.Finally, the process concludes with the publication of the 3-networks-hub-and-spoke artifact.

| Stage | Description |
| :---- | :---- |
| <nobr>3-networks-hub-and-spoke</nobr> | Sets up shared VPCs in your chosen topology and the associated network resources. |

## 4-projects Yaml and Script Execution <a name="4-projects-yaml-and-script-execution"></a>

The deployment pipeline utilizes an environment YAML file to download an 3-networks-hub-and-spoke Artifact. This artifact acts as a container, holding all the previously executed files. Following the download, the pipeline executes the 4-projects shell script. This script is responsible for deploying resources defined within the 4-projects directory.Finally, the process concludes with the publication of the 4-projects artifact.

| Stage | Description |
| :---- | :---- |
| 4-projects | Sets up a folder structure for different business units, service projects in each of the environments. |

##### 

## 5-app-infra Yaml and Script Execution 

The purpose of this step is to deploy a simple Compute Engine instance in one of the business unit projects using the infra pipeline set up in 4-projects.  These resources are not created as part of the Landing Zone full-pipeline automation. The pipeline does not run any automation for step 5\. 

## 6-org-policies Yaml and Script Execution <a name="6-org-policies-yaml-and-script-execution"></a>

The deployment pipeline utilizes an environment YAML file to download an 4-projects Artifact. This artifact acts as a container, holding all the previously executed files. Following the download, the pipeline executes the 6-org-policies shell script. This script is responsible for deploying resources defined within the 6-org-policies directory. Finally, the process concludes with the publication of the 6-org-policies artifact.

| Stage  | Description |
| :---- | :---- |
| 6-org-policies | Once the policies are implemented at 1-Org level, developers can use the "6-org-policies" package to customize policies whether they are needed or are to be overridden at environment specific level.  This is where many of the Protected B specific policies are put in place. |

## 7-fortigate Yaml and Script Execution <a name="7-fortigate-yaml-and-script-execution"></a>

The deployment pipeline utilizes an environment YAML file to download an 6-org-policies Artifact. This artifact acts as a container, holding all the previously executed files. Following the download, the pipeline executes the 7-fortigate shell script. This script is responsible for deploying resources defined within the 7-fortigate directory.Finally, the process concludes with the publication of the 7-fortigate artifact.

| Stage | Description |
| :---- | :---- |
| 7-fortigate |   Installs a redundant pair of Fortigate security appliances into prj-net-hub-base, the landing zone transit VPC.  |

## Error Detection in Bash Scripts <a name="error-detection-in-bash-scripts"></a>

The Command set \-xe is used for the Error Detection in the All the Shell Script files:

\-x (Print commands and their arguments)

* Echoes each command before it's executed, along with its arguments.  
* Helps in understanding the script's flow and identifying unexpected behavior.  
* Output is prefixed with \+ to differentiate it from regular script output.

\-e (Exit on error)

* Causes the script to exit immediately if any command returns a non-zero exit status.  
* Helps in catching errors early and preventing unexpected behavior.

The Command set \+e is used to disable the \-e option where some errors are to be expected.

* Definition: It instructs the Bash shell to continue execution even if a command fails with a non-zero exit status.  
* Behavior: In essence, it reverts the shell's behavior back to the default where errors are ignored.  
* Purpose: It is used to allow specific commands or sections of a script to fail without causing the entire script to terminate.

## Reference README Files: <a name="reference-readme-files:"></a>

1. TEF-GCP-LZ-HS/README.md

**README files for Each Stages:**

1. /TEF-GCP-LZ-HS/0-bootstrap/README.md  
2. /TEF-GCP-LZ-HS/1-org/README.md  
3. /TEF-GCP-LZ-HS/2-environments/README.md  
4. /TEF-GCP-LZ-HS/3-networks-hub-and-spoke/README.md  
5. /TEF-GCP-LZ-HS/4-projects/README.md  
6. /TEF-GCP-LZ-HS/6-org-policies/readme.md  
7. /TEF-GCP-LZ-HS/7-fortigate/README.md


# Steps for ADO Pipeline Execution <a name="steps-for-ado-pipeline-execution"></a>

When initiating the ADO pipeline, specify the desired branch according to the following criteria:

![][image6]

Select the stages to be executed ,for the end to end exectuion of the whole pipeline all stages to be selected and click on the run button. 

![][image8]

## ADO Pipeline Execution Time: <a name="ado-pipeline-execution-time"></a>

Following are the Approx Execution Time for the ADO Pipeline Jobs/Stages.The approx overall time is around 1 hour 45 minutes.   
![][image10]

## Output: GCP Folder Structure  <a name="gcp-folder-structure"></a>

The following is a sample output of an executed ADO pipeline, showcasing the various resources organized within their corresponding directories.  
![][image11]

## Steps to Re-run Failed Jobs: <a name="steps-to-re-run-failed-jobs"></a>

Following are two ways to execute/rerun the Failed jobs : 

1. **Rerun Single Job**:To Re-execute the single failed job click on the “Rerun failed jobs” .  
2. **Rerun Remaining Failed Jobs**:To Re-execute all remaining failed jobs click on the “Rerun all jobs”,for eg like below example it will re-execute the following network stage then projects and so on. 

## Re-run New Pipeline on Intermittent errors <a name="re-run-new-pipeline-on-intermittent-errors"></a>

The ADO pipeline can cause  intermittent errors, particularly provider issues arising during the early 0-bootstrap or 1-org stages. In such instances, a complete pipeline rerun is necessary to ensure data integrity and prevent subsequent failures. Furthermore, if a job within the pipeline encounters a 'resource already exists' error, it indicates an underlying conflict that necessitates a fresh pipeline execution from the beginning to avoid unexpected outcomes and maintain deployment stability. 


[image1]: ./images/architecture-with-appliance.svg

[image2]: ./images/deployment-flowchart.svg

[image3]: ./images/ado-clone.png

[image4]: ./images/ado-library.png

[image6]: ./images/ado-run.png

[image8]: ./images/ado-run-stages.png

[image10]: ./images/ado-jobs.png

[image11]: ./images/resource-structure.png
