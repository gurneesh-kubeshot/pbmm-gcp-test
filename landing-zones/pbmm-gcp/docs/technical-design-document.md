# Technical  Design Document

En Français: [Document de conception technique](./document-de-conception-technique.md)

## PBMM (Protected B, Medium Integrity/Medium Availability) Landing Zone

#### Contents

* [Documentation overview](#documentation-overview)
  * [Intended audience](#intended-audience)
  * [ITSG-33/PBMM compliance disclaimer](#itsg)
* [1\. Landing Zone Overview](#landing-zone-overview)
* [2\. Prerequisite for deployment](#prerequisite-for-deployment)
  * [2.1  Setup your Organization](#setup-your-organization)
  * [2.2 Authentication and authorization](#authentication-and-authorization)
  * [2.3 Billing](#billing)
  * [2.4 Other Considerations](#other-considerations)
* [3\. Landing Zone Deployment Stages](#landing-zone-deployment-stages)
  * [The Environment's Bootstrap (0-bootstrap)](#bootstrap)
  * [Organization (1-org)](#organization)
  * [Environments (2-environments)](#environments)
  * [Networks (3-network-hub-and-spoke)](#networks)
  * [Projects (4-projects)](#projects)
  * [Organizational Policies (6-org-polices)](#organizational-policies)
  * [Network Virtual Appliance (7-fortigate)](#network-virtual-appliance)
* [4\. Landing Zone Features](#landing-zone-features) 
  * [4.1 Identity and Access Management (IAM)](#identity-and-access-management)
  * [4.3 Hub and Spoke Networking](#hub-and-spoke-networking)
  * [4.4 DNS](#dns)
  * [4.5 Firewall Policies](#firewall-policies)
  * [4.6 Fortigate Firewall: 2 Appliances](#fortigate-firewallliances)
  * [4.7 VPC Service Controls](#vpc-service-controls)
  * [4.8 Centralized Logging](#centralized-logging)
  * [4.9 Security Command Center](#security-command-center)
  * [4.10 Secret Management](#secret-management)
* [5\. Landing Zone Deployment Options](#landing-zone-deployment-options)
  * [5.1 Cloud Build](#cloud-build)
  * [5.2 Manual Deployment](#manual-deployment)
  * [5.3 Azure Devops Pipeline](#azure-devops-pipeline)
* [Day 2 Tasks and Operational Best Practices](#day-2-tasks-and-operational-best-practices)
  * [After IAC has been deployed](#after-iac-has-been-deployed)
  * [Operational Best Practices](#operational-best-practices)
* [Appendix 1: Naming Conventions](#naming-conventions)
* [Appendix 2: Mapping Controls to Code](#mapping-controls-to-code)
* [Appendix 3: Reference Materials](#reference-materials)

# Documentation overview <a name="documentation-overview"></a>

This document assists Google Cloud customers with implementing and formalizing Protected B, Medium Integrity, Medium Availability (PBMM) security controls for information systems deployed on Google Cloud Platform (GCP). Customers can use this document and the associated code repository to accelerate creation of a cloud foundation that meets Canadian governmental security requirements. The codebase forms a starting point to build your own foundations with pragmatic defaults that you can customize to meet your own specific needs. 

The Communications Security Establishment (CSE) has provided Government of Canada (GC) departments and agencies with an Information Security Risk Management framework published as the Information Technology Security Guidance (ITSG-33).  [Annex 3A of ITSG-33 documents](https://www.cyber.gc.ca/en/guidance/annex-3a-security-control-catalogue-itsg-33) suggests security controls and control enhancements. ITSG-33 is aligned with [version 4 of NIST 800-53](https://csrc.nist.gov/pubs/sp/800/53/r4/upd3/final). The Canadian Centre for Cyber Security (CCS) has published various Profiles as a set of Cloud security controls for different data classification levels.  [Profile 1 (Protected B / Medium Integrity / Medium Availability)](https://www.cyber.gc.ca/en/guidance/annex-4a-profile-1-protected-b-medium-integrity-medium-availability-itsg-33) and [Profile 3 (SECRET / Medium Integrity / Medium Availability)](https://www.cyber.gc.ca/en/guidance/annex-4a-profile-3-secret-medium-integrity-medium-availability-itsg-33). For environments with information having the PBMM security category, this document captures the details of a cloud-hosted information system, including the system architecture specifications and security controls implementation. 

Google provides two primary artifacts to assist GC departments and agencies with their PBMM posture \- a Landing Zone (LZ) code repository and this Technical Design Document (TDD) inclusive of an appendix to help map PBMM controls and the methods by which the Landing Zone addresses them:

* **The Landing Zone,** which is a GitHub-hosted, Terraform-based, PBMM compliant Google Cloud Landing Zone that GC can clone to their own repository, set variables, and deploy.   
* **The TDD** (this document) details the system architecture specifications. The included PBMM security control mapping outlines the security control implementation, and documents which controls the Landing Zone environment has inherited from Google, and which controls the department or agency has implemented.  

GC departments and agencies can use these two artifacts to provide ITSG-33/PBMM details to any interested parties for their GCP-hosted information system. 

The PBMM LZ is built using the [Enterprise Foundation Blueprint](https://cloud.google.com/architecture/security-foundations) and [Terraform Example Foundation](https://github.com/terraform-google-modules/terraform-example-foundation) v4 repo.

## Intended audience <a name="intended-audience"></a>

This document, along with the included PBMM mapping, are intended to be used by the following personnel within a customer’s organization:

* Information System Owner \- *primary Google Stakeholder*  
* Department or Agency Independent Assessor or 3rd Party Assessment Organization  
* GCP Administrators for the Information System  
* Department, Ministry or Agency Security Personnel: CIOs, CTOs, ISSMs, ISSOs, etc.

## ITSG-33/PBMM compliance disclaimer <a name="itsg"></a>

Google maintains alignment to compliance standards on many cloud services to allow customers to build compliant applications and general support systems; however, individual departments and agencies are ultimately responsible for assuring that their IT systems are ITSG-33/PBMM compliant when required.

This Technical Design Document (TDD) outlines the ITSG-33/PBMM aligned Landing Zone implementation and configuration components.

# 1\. Landing Zone Overview <a name="landing-zone-overview"></a>

A cloud foundation is the essential starting point for Canadian public sector organizations adopting Google Cloud. It encompasses the core resources, standardized configurations, and capabilities that empower agencies to leverage Google Cloud securely and effectively. Landing Zones are made up of several components including Security Policy, Identity and Access Management (IAM), Automation Pipelines, Organizational Policy, Networking, Logging and Monitoring. A visual representation can be found below with more details offered later in this document and in supporting documentation.

![][image1]

To separate the teams and technology stacks that are responsible for managing different layers of your environment the deployment code has been separated into different layers that are intended to map to different personas that are responsible for your environment ([Deployment Methodology Link](https://cloud.google.com/architecture/security-foundations/deployment-methodology)). 

The PBMM landing zone consists of 7 stages as follows:

| Stage | Description |
| :---- | :---- |
| 0-bootstrap | Bootstrap prepares your Google Cloud organization for the subsequent deployment stages. This step also configures a CI/CD pipeline for the blueprint code in subsequent stages. Configuring the correct service accounts and permissions The CICD project contains the Cloud Build foundation pipeline for deploying resources. The seed project includes the Cloud Storage buckets that contain the Terraform state of the foundation infrastructure and includes highly privileged service accounts that are used by the foundation pipeline to create resources. The Terraform state is protected through storage Object Versioning. When the CI/CD pipeline runs, it acts as the service accounts that are managed in the seed project. |
| 1-org | Sets up top-level shared folders, projects for shared services, organization-level logging, and baseline security settings through organization policies. |
| 2-environments | Sets up development, non-production, and production environments within the Google Cloud organization that you've created. |
| 3-networks-hub-and-spoke | Sets up shared VPCs in your chosen topology and the associated network resources. |
| 4-projects | Sets up a folder structure for different business units, service projects in each of the environments. Out of the box there are example projects and can be adjusted to support the needs of your organization.  |
| 5-app-infra | Deploys workload projects with a Compute Engine instance using the infrastructure pipeline as an example. |
| 6-org-policies | Once the policies are implemented at 1-Org level, developers can use the "6-org-policies" package to customize policies whether they are needed or are to be overridden at environment specific level. This is where many of the Protected B specific policies are put in place. |
| 7-fortigate | Installs a redundant pair of Fortigate security appliances into prj-net-hub-base, the landing zone transit VPC. |

#### *Example architecture with Fortigate appliances*

![][image2]

[Google Cloud resources](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy) are organized hierarchically. At the lowest level, resources are the fundamental components that make up all Google Cloud services. Examples of resources include Compute Engine Virtual Machines (VMs), Pub/Sub topics, Cloud Storage buckets, and App Engine instances. All these lower level resources can only exist within a project  A project is the first grouping mechanism of the Google Cloud resource hierarchy.

**Folders are an additional grouping mechanism to organize projects**. You are required to have an Organization resource as a prerequisite to use folders. Folders and projects are all mapped under the Organization resource.

**The Organization resource is the top-level node** of the Google Cloud resource hierarchy and all resources that belong to an organization are grouped under the organization node. This provides for central visibility and control over every resource that belongs to an organization. The following diagram shows the folders and projects that are deployed as part of the PBMM landing zone deployment code.  
![][image3]

# 2\. Prerequisite for deployment <a name="prerequisite-for-deployment"></a>

Although much of the landing zone deployment is automated via pipelines and terraform code there are a number of prerequisites that are required in order to have a successful deployment and to align to the security requirement of Protected B.

## 2.1  Setup your Organization  <a name="setup-your-organization"></a>

An organization resource in Google Cloud represents your business, and serves as the top level node of your hierarchy. To create your organization, you set up a Google identity service and associate it with your domain. When you complete this process, an organization resource is automatically created.  Detailed information on setting up your organization is outside the scope of this document and can be found [here](https://cloud.google.com/resource-manager/docs/creating-managing-organization).

## 2.2 Authentication and authorization <a name="authentication-and-authorization"></a>

Google Cloud requires the use of Cloud Identity or Google Workspace in order to control Identity and Access management within the cloud platform. As a best practice, we recommend federating your Cloud Identity account with your existing identity provider. Federation helps you ensure that your existing account management processes apply to Google Cloud and other Google services. If you're already using Google Workspace, Cloud Identity uses the same console, administrative controls, and user accounts as your Google Workspace account.

The process of federating identity is NOT covered in the PBMM landing zone terraform codebase as it will be dependent on individual organizations specific needs, policies and provisioning practices. It is strongly recommended you complete federation prior to proceeding with a landing zone deployment. 

The following diagram shows a high-level view of identity federation and single sign-on (SSO). It uses Microsoft Active Directory, located in the on-premises environment, as the example identity provider.  
![][image4]

The following table provides links to setup guidance for identity providers.

| Identity Provider | Guidance |
| :---- | :---- |
| Microsoft Entra ID  (formerly Azure AD) | [Federating Google Cloud with Microsoft Entra ID](https://cloud.google.com/architecture/identity/federating-gcp-with-azure-active-directory) |
| Active Directory | [Active Directory user account provisioning](https://cloud.google.com/architecture/identity/federating-gcp-with-active-directory-synchronizing-user-accounts) [Active Directory single sign-on](https://cloud.google.com/architecture/identity/federating-gcp-with-active-directory-configuring-single-sign-on) |
| Other external identity providers (for example, Ping or Okta) | [Integrating Ping Identity Solutions with Google Identity Services](https://www.pingidentity.com/en/resources/content-library/white-papers/3034-integrate-ping-identity-solutions-google-identity-services.html) [Using Okta with Google Cloud Providers](https://www.okta.com/sites/default/files/UsingOktaWithGCP.pdf) [Best practices for federating Google Cloud with an external identity provider](https://cloud.google.com/architecture/identity/best-practices-for-federating) |

We strongly recommend that you enforce multi-factor authentication at your identity provider with a phishing-resistant mechanism such as a [Titan Security Key](https://cloud.google.com/titan-security-key). 

The recommended settings for Cloud Identity aren't automated through the Terraform code in this blueprint. See [administrative controls for Cloud Identity](https://cloud.google.com/architecture/security-foundations/printable#administrative-controls-for-cloud-identity) for the recommended security settings that you must configure in addition to deploying the Terraform code.

## 2.3 Billing <a name="billing"></a>

Many government agencies and organizations already have procurement relationships in place with Google Cloud, typically these come in the form of a Billing Account.  If you are unsure, we’d suggest you start with your procurement or purchasing department to use any existing vehicles that currently exist.  Alternatively, you can [Apply for an invoiced billing account](https://cloud.google.com/billing/docs/how-to/invoiced-billing) with your Google Cloud sales team or create a [self-service billing account](https://cloud.google.com/billing/docs/how-to/create-billing-account) using a credit card.

## 2.4 Other Considerations <a name="other-considerations"></a>

The following items are recommended both as best practice and to ensure alignment with any security control requirement.

* If you are using a self-service billing account, you must [request additional project quota](https://github.com/terraform-google-modules/terraform-example-foundation/blob/4d7e822b85d6c21c28389e82b3794b9e1554ebc6/docs/FAQ.md?plain=1#L9) before proceeding to the next stage.  
* Enforce [security best practices](https://support.google.com/a/answer/9011373) for administrator accounts.  
* Verify and reconcile [issues with consumer user accounts](https://cloud.google.com/architecture/security-foundations/authentication-authorization#issues_with_consumer_user_accounts).

To connect to an an existing on-premises environment, prepare the following:

* Plan your [IP address allocation](https://cloud.google.com/architecture/security-foundations/networking#ip-address-allocation) based on the number and size of ranges that are required by the blueprint.  
* Order your [Dedicated Interconnect](https://cloud.google.com/interconnect/docs/concepts/dedicated-overview) connections.

# 

# 3\. Landing Zone Deployment Stages <a name="landing-zone-deployment-stages"></a>

## The Environment's Bootstrap (0-bootstrap) <a name="bootstrap"></a>

Bootstrapping is the process of setting up initial resources for further cloud deployment. The purpose of this step is to bootstrap a Google Cloud organization, creating all the required resources and permissions to start using the PBMM Landing zone code. This step can also configure a [CI/CD Pipeline](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/tef_0724_merged/docs/GLOSSARY.md#foundation-cicd-pipeline) for subsequent stages.  
This module sets up the initial permissions structure against the Organization Node and enables core GCP services such as Google Cloud Storage so that a repository can be instantiated for Terraform to validate and run the Plan. 

This is hosted in subdirectory:   
../0-bootstrap/  
../automation-scripts/0-bootstrap/

## Organization (1-org) <a name="organization"></a>

The purpose of this step is to set up top-level shared folders, monitoring and networking projects, organization-level logging, and baseline security settings through organizational policies.

This is hosted in subdirectory:   
../1-org/

## Environments (2-environments) <a name="environments"></a>

The purpose of this step is to set up development, nonproduction, and production environments within the Google Cloud organization that you've created.

This is hosted in subdirectory:   
../2-environments/

## Networks (3-network-hub-and-spoke) <a name="networks"></a>

The purpose of this step is to set up the global [DNS Hub](https://cloud.google.com/blog/products/networking/cloud-forwarding-peering-and-zones), per environment Hubs and their corresponding Spokes. With default DNS, NAT (optional), Private Service networking, VPC service controls, on-premises Dedicated or Partner Interconnect, and baseline firewall rules for each environment.  
	  
This is hosted in subdirectory:   
../3-networks-hub-and-spoke/

## Projects (4-projects) <a name="projects"></a>

The purpose of this step is to set up the folder structure, projects, and infrastructure pipelines for applications that are connected as service projects to the shared VPC created in the previous stage.

For each business unit, a shared infra-pipeline project is created along with Cloud Build triggers, cloud source repositories (CSRs) for application infrastructure code and Google Cloud Storage buckets for state storage.

This step follows the same [conventions](https://github.com/terraform-google-modules/terraform-example-foundation#branching-strategy) as the Foundation pipeline deployed in [0-bootstrap](https://github.com/terraform-google-modules/terraform-example-foundation/blob/master/0-bootstrap/README.md). A custom [workspace](https://github.com/terraform-google-modules/terraform-google-bootstrap/blob/master/modules/tf_cloudbuild_workspace/README.md) (bu1-example-app) is created by this pipeline and necessary roles are granted to the Terraform Service Account of this workspace by enabling variable sa\_roles as shown in this [example](https://github.com/terraform-google-modules/terraform-example-foundation/blob/master/4-projects/modules/base_env/example_base_shared_vpc_project.tf).

This pipeline is utilized to deploy resources in projects across the environments in step [5-app-infra](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/tef_0724_merged/5-app-infra/README.md). Other Workspaces can also be created to isolate deployments if needed.  
	  
This is hosted in subdirectory:   
../4-network-hub-and-spoke/

## 

## Organizational Policies (6-org-polices) <a name="organizational-policies"></a>

[Organization Policy Constraints](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints) enforce compliance at the GCP Organization, folder, or project level. They are a set of predefined rules that prevent certain actions from happening. These built-in policies are defined by Google and enabled by the organization consuming GCP. These policies help protect the security boundary of the platform.

In total, 26 Org Policies have been implemented and details can be found in the table below.  

| Constraint Name | Constraint Description | Control References |
| :---- | :---- | :---- |
| essentialcontacts.allowedContactDomains | This policy limits Essential Contacts to only allow managed user identities in selected domains to receive platform notifications. | AC-2(4) |
| compute.disableNestedVirtualization | This policy disables nested virtualization to decrease security risk due to unmonitored nested instances. | AC-3, AC-6(9), AC-6(10) |
| compute.disableSerialPortAccess | This policy prevents users from accessing the VM serial port which can be used for backdoor access from the Compute Engine API control plane. | AC-3, AC-6(9), AC-6(10) |
| compute.requireOsLogin | This policy requires OS Login on newly created VMs to more easily manage SSH keys, provide resource-level permission with IAM policies, and log user access. | AC-3, AU-12 |
| compute.restrictVpcPeering | Enables you to implement network segmentation and control the flow of information within your GCP environment. | SC-7, SC-7(5), SC-7 (7), SC-7(8), SC-7(18) |
| compute.vmCanIpForward | This permission controls whether a VM instance can act as a network router, forwarding IP packets between different network interfaces. Enabling IP forwarding on a VM essentially turns it into a router, which can have significant security implications.  | SC-7, SC-7(5), SC-7 (7), SC-7(8), SC-7(18), SC-8, SC-8(1) |
| compute.restrictLoadBalancerCreationForTypes |  This permission allows you to restrict the types of load balancers that can be created in your project. This helps prevent unauthorized or accidental creation of load balancers that could expose your services to unnecessary risks or attacks. | SC-8, SC-8(1) |
| compute.requireTlsForLoadBalancers | This constraint enforces the use of Transport Layer Security (TLS) for communication with load balancers in GCP. It aligns with several key principles and controls outlined in NIST. | SC-8, SC-8(1) |
| compute.skipDefaultNetworkCreation | This policy disables the automatic creation of a default VPC network and default firewall rules in each new project, ensuring that network and firewall rules are intentionally created. | AC-3, AC-6(9), AC-6(10) |
| compute.restrictXpnProjectLienRemoval | This policy prevents the accidental deletion of Shared VPC host projects by restricting the removal of project liens. | AC-3, AC-6(9), AC-6(10) |
| compute.disableVpcExternalIpv6 | This policy prevents the creation of external IPv6 subnets, which can be exposed to incoming and outgoing internet traffic. | AC-3, AC-6(9), AC-6(10) |
| compute.setNewProjectDefaultToZonalDNSOnly | This policy restricts application developers from choosing legacy DNS settings for Compute Engine instances that have lower service reliability than modern DNS settings. | AC-3, AC-6(9), AC-6(10) |
| compute.vmExternalIpAccess | This policy prevents the creation of Compute Engine instances with a public IP address, which can expose them to incoming internet traffic and outgoing internet traffic. | AC-3, AC-6(9), AC-6(10) |
| sql.restrictPublicIp | This policy prevents the creation of Cloud SQL instances with public IP addresses, which can expose them to incoming internet traffic and outgoing internet traffic. | AC-3, AC-6(9), AC-6(10) |
| sql.restrictAuthorizedNetworks | This policy prevents public or non-RFC 1918 network ranges from accessing Cloud SQL databases. | AC-3, AC-6(9), AC-6(10) |
| storage.uniformBucketLevelAccess | This policy prevents Cloud Storage buckets from using per-object ACL (a separate system from IAM policies) to provide access, enforcing consistency for access management and auditing. | AC-3, AC-6(9), AC-6(10) |
| storage.publicAccessPrevention | This policy prevents Cloud Storage buckets from being open to unauthenticated public access. | AC-3, AC-6(9), AC-6(10) |
| iam.disableServiceAccountKeyCreation | This constraint prevents users from creating persistent keys for service accounts to decrease the risk of exposed service account credentials. | AC-2(4) |
| iam.disableServiceAccountKeyUpload | This constraint avoids the risk of leaked and reused custom key material in service account keys. | AC-6(9), AC-6(10) |
| iam.allowedPolicyMemberDomains | This policy limits IAM policies to only allow managed user identities in selected domains to access resources inside this organization. | AC-2(4) |
| compute.disableGuestAttributesAccess | This permission controls whether a user or service account can modify guest attributes on a virtual machine (VM) instance. Guest attributes can contain metadata or configuration data that could potentially impact the security or operation of the VM. | AC-2(4) |
| iam.automaticIamGrantsForDefaultServiceAccounts | This constraint prevents default service accounts from receiving the overly-permissive Identity and Access Management (IAM) role Editor at creation. | AC-3 |
| compute.trustedImageProjects | This constraint helps enforce software and firmware integrity and configuration management. This permission controls which projects can be used as trusted sources for VM images. By limiting this to a select set of projects, you reduce the risk of deploying VMs from untrusted or potentially compromised sources. | SI-3 (2), SI-3 (7) |

This is hosted in subdirectory:   
../6-org-policies/

## Network Virtual Appliance (7-fortigate) <a name="network-virtual-appliance"></a>

This module can be customized to support third-party NGFW vendors or [Google’s Cloud NGFW](https://cloud.google.com/firewall/docs/about-firewalls). This implementation is currently designed and tested to install a redundant pair of Fortigate security appliances into prj-net-hub-base, the landing zone transit VPC, as the following diagram demonstrates.  
![][image5]  
For more information, see the following document for an architectural overview of [Fortigate appliances on GCP.](https://cloud.google.com/architecture/partners/fortigate-architecture-in-cloud)

This is hosted in subdirectory:   
../7-fortigate/

# 4\. Landing Zone Features <a name="landing-zone-features"></a>

The section largely focuses on the features and tools that are used as part of the landing zone and touches on some of the security controls that are put in place as part of a deployment. 

The landing zone uses [projects](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy#projects) to group individual resources based on their functionality and intended boundaries for access control. This following table describes the projects that are included in the blueprint.

| Folder | Project | Description |
| :---- | :---- | :---- |
| `bootstrap` | `prj-b-cicd` | Contains the deployment pipeline that's used to build out the foundation components of the organization. For more information, see [deployment methodology](https://cloud.google.com/architecture/security-foundations/deployment-methodology). |
|  | `prj-b-seed` | Contains the Terraform state of your infrastructure and the Terraform service account that is required to run the pipeline. For more information, see [deployment methodology](https://cloud.google.com/architecture/security-foundations/deployment-methodology). |
| `common` | `prj-c-secrets` | Contains organization-level secrets. For more information, see [store application credentials with Secret Manager](https://cloud.google.com/architecture/security-foundations/operation-best-practices#store-and). |
|  | `prj-c-logging` | Contains the aggregated log sources for audit logs. For more information, see [centralized logging for security and audit](https://cloud.google.com/architecture/security-foundations/detective-controls#centralized-logging). |
|  | `prj-c-scc` | Contains resources to help configure Security Command Center alerting and other custom security monitoring. For more information, see [threat monitoring with Security Command Center](https://cloud.google.com/architecture/security-foundations/detective-controls#threat-monitoring). |
|  | `prj-c-billing-export` | Contains a BigQuery dataset with the organization's [billing exports](https://cloud.google.com/billing/docs/how-to/export-data-bigquery). For more information, see [allocate costs between internal cost centers](https://cloud.google.com/architecture/security-foundations/operation-best-practices#allocate-costs). |
|  | `prj-c-infra-pipeline` | Contains an infrastructure pipeline for deploying resources like VMs and databases to be used by workloads. For more information, see [pipeline layers](https://cloud.google.com/architecture/security-foundations/deployment-methodology#pipeline-layers). |
|  | `prj-c-kms` | Contains organization-level encryption keys. For more information, see [manage encryption keys](https://cloud.google.com/architecture/security-foundations/operation-best-practices#manage-encryption). |
| `networking` | `prj-net-{env}-shared-base` | Contains the host project for a Shared VPC network for workloads that don't require VPC Service Controls. For more information, see [network topology](https://cloud.google.com/architecture/security-foundations/networking#network_topology). |
|  | `prj-net-{env}-shared-restricted` | Contains the host project for a Shared VPC network for workloads that do require VPC Service Controls. For more information, see [network topology](https://cloud.google.com/architecture/security-foundations/networking#network_topology). |
|  | `prj-net-interconnect` | Contains the Cloud Interconnect connections that provide connectivity between your on-premises environment and Google Cloud. For more information, see [hybrid connectivity](https://cloud.google.com/architecture/security-foundations/networking#hybrid-connectivity). |
|  | `prj-net-dns-hub` | Contains resources for a central point of communication between your on-premises DNS system and Cloud DNS. For more information, see [centralized DNS setup](https://cloud.google.com/architecture/security-foundations/networking#dns-setup). |
| `prj-{env}-secrets` | Contains folder-level secrets. For more information, see [store and audit application credentials with Secret Manager](https://cloud.google.com/architecture/security-foundations/operation-best-practices#store-and). |  |
| `prj-{env}-kms` | Contains folder-level encryption keys. For more information, see [manage encryption keys](https://cloud.google.com/architecture/security-foundations/operation-best-practices#manage-encryption). |  |
| application projects | Contains various projects in which you create resources for applications. For more information, see [project deployment patterns](https://cloud.google.com/architecture/security-foundations/networking#project_deployment_patterns) and [pipeline layers](https://cloud.google.com/architecture/security-foundations/deployment-methodology#pipeline-layers). |  |

## 4.1 Identity and Access Management (IAM) <a name="identity-and-access-management"></a>

Google Cloud Identity is the product used for managing users, groups, and domain-wide security settings for Workspace and Google Cloud Platform. Cloud Identity is tied to a unique DNS domain that needs to be enabled for receiving email (for example, has an appropriate MX configured) so that users and groups configured with responsibilities in GCP can receive generated notifications.

Cloud Identity configurations are made in the Admin Console. Existing Workspace customers can use their Workspace Admin Console for Cloud Identity. Customers without an existing Workspace account can create a Cloud Identity in the "IAM" section of the GCP Cloud Console.

IAM policies are available for configuration in the Google Cloud Console. IAM roles are available for users, groups of users, and service accounts that allow granular control of permissions to access resources. The organization resource provides a way to unify all projects under a single organization with permission inheritance across the organization. 

Identity Aware Proxy (IAP) provides an authenticated proxy that verifies all connections against an access control policy (See [Reference: Identity Aware Proxy](https://cloud.google.com/iap/docs/concepts-overview)). It can be used to access resources in a VPC where the source system does not have a route to the destination system, or a firewall rule blocks direct access. All connections through IAP are required to authenticate, and once authenticated, will be routed to the destination service where they can interact with it. This interaction can be simple TCP traffic such as a web service, or more complex like an RDP or SSH session where a credential to access the system would also be required. All IAP traffic is encrypted via TLS.

Access is controlled through IAM roles and is assigned directly to groups, users, or service accounts. This enables granularity in controlling access to systems and ensures that the principle of least privilege is adhered to. Thus, instead of managing bastion hosts, SSH keys, and other components that can cause operational burden, the Landing Zone will be taking advantage of IAP capabilities.

## 4.3 Hub and Spoke Networking <a name="hub-and-spoke-networking"></a>

Google’s worldwide infrastructure consists of regions and, within those regions, zones. Google offers several connectivity options for physical connectivity through direct peering or Google Carrier Interconnect across multiple geographies. Virtual private networks can be built on top of this physical layer and the Cloud Router is available to manage dynamic routes using BGP once that connection is configured. The use of Shared VPCs allows you to centralize networking infrastructure in a single host project and allow other service projects to consume networking resources from the host project. 

The PBMM landing zone design makes use of a hub-and-spoke network topology.

![][image6]

* This model adds a hub network, and each of the development, non-production, and production networks (spokes) are connected to the hub network through VPC Network Peering. Alternatively, if you anticipate exceeding the VPC peering quota limit (25), you can use an HA VPN gateway instead.  
* Connectivity to on-premises networks is allowed only through the hub network. All spoke networks can communicate with shared resources in the hub network and use this path to connect to on-premises networks.  
* The hub networks include a network virtual appliance (NVA)for each region, deployed redundantly behind internal Network Load Balancer instances. This NVA serves as the gateway to allow or deny traffic to communicate between spoke networks.  
* The hub network also hosts tooling that requires connectivity to all other networks. For example, you might deploy tools on VM instances for configuration management to the common environment.  
* The hub-and-spoke model is duplicated for a base version and restricted version of each network.

To enable spoke-to-spoke traffic, the blueprint deploys NVAs on the hub Shared VPC network that act as gateways between networks. Routes are exchanged from hub-to-spoke VPC networks through custom routes exchange. In this scenario, connectivity between spokes must be routed through the NVA because VPC Network Peering is non-transitive, and therefore, spoke VPC networks can't exchange data with each other directly. You must configure the virtual appliances to selectively allow traffic between spokes.

## 

## 4.4 DNS <a name="dns"></a>

Cloud DNS supports both public (internet resolvable) and private zones (See [Reference: DNS Overview](https://cloud.google.com/dns/docs/overview)). For DNS resolution between Google Cloud and on-premises environments, we recommend that you use a hybrid approach with two authoritative DNS systems. In this approach, Cloud DNS handles authoritative DNS resolution for your Google Cloud environment and your existing on-premises DNS servers handle authoritative DNS resolution for on-premises resources. Your on-premises environment and Google Cloud environment perform DNS lookups between environments through forwarding requests.

The following diagram demonstrates the DNS topology across the multiple VPC networks that are used in the landing zone.

![][image7]

* The DNS hub project in the common folder is the central point of DNS exchange between the on-premises environment and the Google Cloud environment. DNS forwarding uses the same Dedicated Interconnect instances and Cloud Routers that are already configured in your network topology.  
  * In the dual Shared VPC topology, the DNS hub uses the base production Shared VPC network.  
  * In the hub-and-spoke topology, the DNS hub uses the base hub Shared VPC network.  
* Servers in each Shared VPC network can resolve DNS records from other Shared VPC networks through [DNS forwarding](https://cloud.google.com/dns/docs/overview#dns-forwarding-methods), which is configured between Cloud DNS in each Shared VPC host project and the DNS hub.  
* On-premises servers can resolve DNS records in Google Cloud environments using [DNS server policies](https://cloud.google.com/dns/docs/best-practices#use_dns_server_policies_to_allow_queries_from_on-premises) that allow queries from on-premises servers. The blueprint configures an inbound server policy in the DNS hub to allocate IP addresses, and the on-premises DNS servers forward requests to these addresses. All DNS requests to Google Cloud reach the DNS hub first, which then resolves records from DNS peers.  
* Servers in Google Cloud can resolve DNS records in the on-premises environment using [forwarding zones](https://cloud.google.com/dns/docs/best-practices#use_forwarding_zones_to_query_on-premises_servers) that query on-premises servers. All DNS requests to the on-premises environment originate from the DNS hub. The DNS request source is 35.199.192.0/19.

## 4.5 Firewall Policies <a name="firewall-policies"></a>

Google Cloud has multiple [firewall policy](https://cloud.google.com/firewall/docs/firewall-policies-overview) types. Hierarchical firewall policies are enforced at the organization or folder level to inherit firewall policy rules consistently across all resources in the hierarchy. In addition, you can configure network firewall policies for each VPC network. The landing zone combines these firewall policies to enforce common configurations across all environments using Hierarchical firewall policies and to enforce more specific configurations at each individual VPC network using network firewall policies.

### Hierarchical firewall policies

The blueprint defines a single [hierarchical firewall policy](https://cloud.google.com/firewall/docs/firewall-policies) and attaches the policy to each of the production, non-production, development, bootstrap, and common folders. This hierarchical firewall policy contains the rules that should be enforced broadly across all environments, and delegates the evaluation of more granular rules to the network firewall policy for each individual environment.

The following table describes the hierarchical firewall policy rules deployed by the landing zone.

| Rule description | Direction of traffic | Filter (IPv4 range) | Protocols and ports | Action |
| :---- | :---- | :---- | :---- | :---- |
| Delegate the evaluation of inbound traffic from RFC 1918 to lower levels in the hierarchy. | Ingress | 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12 | all | Go to next |
| Delegate the evaluation of outbound traffic to RFC 1918 to lower levels in the hierarchy. | Egress | 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12 | all | Go to next |
| [IAP for TCP forwarding](https://cloud.google.com/iap/docs/using-tcp-forwarding) | Ingress | 35.235.240.0/20 | tcp:22,3390 | Allow |
| [Windows server activation](https://cloud.google.com/compute/docs/instances/windows/creating-managing-windows-instances) | Egress | 35.190.247.13/32 | tcp:1688 | Allow |
| [Health checks](https://cloud.google.com/load-balancing/docs/health-checks#fw-rule) for Cloud Load Balancing | Ingress | 130.211.0.0/22, 35.191.0.0/16, 209.85.152.0/22, 209.85.204.0/22 | tcp:80,443 | Allow |

### Network firewall policies

The landing zone configures a [network firewall policy](https://cloud.google.com/vpc/docs/network-firewall-policies) for each network. Each network firewall policy starts with a minimum set of rules that allow access to Google Cloud services and deny egress to all other IP addresses.

In the hub-and-spoke model, the network firewall policies contain additional rules to allow communication between spokes. The network firewall policy allows outbound traffic from one to the hub or another spoke, and allows inbound traffic from the NVA in the hub network.

The following table describes the rules in the global network firewall policy deployed for each VPC network in the landing zone.

| Rule description | Direction of traffic | Filter | Protocols and ports |
| :---- | :---- | :---- | :---- |
| Allow outbound traffic to Google Cloud APIs. | Egress | The Private Service Connect endpoint that is configured for each individual network. See [Private access to Google APIs](https://cloud.google.com/architecture/security-foundations/networking#private-access-to-google-cloud-apis). | tcp:443 |
| Deny outbound traffic not matched by other rules. | Egress | all | all |
| Allow outbound traffic from one spoke to another spoke (for hub-and-spoke model only). | Egress | The aggregate of all IP addresses used in the hub-and-spoke topology. Traffic that leaves a spoke VPC is routed to the NVA in the hub network first. | all |
| Allow inbound traffic to a spoke from the NVA in the hub network (for hub-and-spoke model only). | Ingress | Traffic originating from the NVAs in the hub network. | all |

When you first deploy the blueprint, a VM instance in a VPC network can communicate with Google Cloud services, but not to other infrastructure resources in the same VPC network. To allow VM instances to communicate, you must add additional rules to your network firewall policy and [tags](https://cloud.google.com/resource-manager/docs/tags/tags-overview) that explicitly allow the VM instances to communicate. Tags are added to VM instances, and traffic is evaluated against those tags. Tags additionally have IAM controls so that you can define them centrally and delegate their use to other teams.

## 4.6 Fortigate Firewall: 2 Appliances <a name="fortigate-firewall"></a>

This optional module is available if a Fortigate firewall appliance is desired. This type of NVA firewall will provide functionality including, but not limited to:

* Deep packet inspection  
* IDS Capabilities  
* WAF Capabilities  
* FQDN Filtering

If used, all traffic will first flow through the virtual appliance, before exiting to the public Internet. Traffic which is destined for on-premises will also flow through the NVA before egress to the on-premises environment. In order to facilitate this the landing zone makes use of [Policy Based Routing](https://cloud.google.com/vpc/docs/policy-based-routes) in order to steer traffic through the firewall VMs. 

## 4.7 VPC Service Controls <a name="vpc-service-controls"></a>

This landing zone helps prepare your environment for VPC Service Controls by separating the base and restricted networks. However, by default, the Terraform code doesn't enable VPC Service Controls because this enablement can be a disruptive process. To enable the restricted networks there is a flag in the variables in the 3-networks component.

A perimeter denies access to restricted Google Cloud services from traffic that originates outside the perimeter, which includes the console, developer workstations, and the foundation pipeline used to deploy resources. If you use VPC Service Controls, you must design exceptions to the perimeter that allow the access paths that you intend.

A VPC Service Controls perimeter is intended for exfiltration controls between your Google Cloud organization and external sources. The perimeter isn't intended to replace or duplicate allow policies for granular access control to individual projects or resources. When you [design and architect a perimeter](https://cloud.google.com/vpc-service-controls/docs/architect-perimeters), we recommend using a common unified perimeter for lower management overhead.

## 4.8 Centralized Logging <a name="centralized-logging"></a>

Monitoring and Logging within GCP is provided by two different products, Cloud Monitoring (See [Reference: Cloud Monitoring](https://cloud.google.com/monitoring/docs/monitoring-overview)) and Cloud Logging (See [Reference: Cloud Logging](https://cloud.google.com/logging/docs)). These GCP services, in conjunction with Security Command Center, enable a holistic view of resource health in all GCP projects. 

The landing zone configures logging capabilities to track and analyze changes to your Google Cloud resources with logs that are aggregated to a single project.

The following diagram shows how the blueprint aggregates logs from multiple sources in multiple projects into a centralized log sink.

![][image8]

* Log sinks are configured at the organization node to aggregate logs from all projects in the resource hierarchy.  
* Multiple log sinks are configured to send logs that match a filter to different destinations for storage and analytics.  
* The prj-c-logging project contains all the resources for log storage and analytics.  
* Optionally, you can configure additional tooling to export logs to a SIEM.

## 4.9 Security Command Center <a name="security-command-center"></a>

We strongly recommend that you activate [Security Command Center Premium](https://cloud.google.com/security-command-center/docs/concepts-security-command-center-overview) for your organization as it plays a critical part in compliance by detect threats, vulnerabilities, and misconfigurations in your Google Cloud resources. Security Command Center creates security findings from multiple sources including the following:

* [Security Health Analytics](https://cloud.google.com/security-command-center/docs/how-to-use-security-health-analytics): detects common vulnerabilities and misconfigurations across Google Cloud resources.

* [Attack path exposure](https://cloud.google.com/security-command-center/docs/attack-exposure-learn): shows a simulated path of how an attacker could exploit your high-value resources, based on the vulnerabilities and misconfigurations that are detected by other Security Command Center sources.

* [Event Threat Detection](https://cloud.google.com/security-command-center/docs/how-to-use-event-threat-detection): applies detection logic and proprietary threat intelligence against your logs to identify threats in near-real time.

* [Container Threat Detection](https://cloud.google.com/security-command-center/docs/how-to-use-container-threat-detection): detects common container runtime attacks.

* [Virtual Machine Threat Detection](https://cloud.google.com/security-command-center/docs/how-to-use-vm-threat-detection): detects potentially malicious applications that are running on virtual machines.

* [Web Security Scanner](https://cloud.google.com/security-command-center/docs/how-to-use-web-security-scanner): scans for OWASP Top Ten vulnerabilities in your web-facing applications on Compute Engine, App Engine, or Google Kubernetes Engine.

For more information on the vulnerabilities and threats addressed by Security Command Center, see [Security Command Center sources](https://cloud.google.com/security-command-center/docs/concepts-security-sources).

You must activate Security Command Center after you deploy the landing zone. For instructions, see [Activate Security Command Center for an organization](https://cloud.google.com/security-command-center/docs/activate-scc-for-an-organization).

After you activate Security Command Center, we recommend that you export the findings that are produced by Security Command Center to your existing tools or processes for triaging and responding to threats. The blueprint creates the prj-c-scc project with a Pub/Sub topic to be used for this integration. Depending on your existing tools, use one of the following methods to export findings:

* If you use the console to manage security findings directly in Security Command Center, configure [folder-level and project-level roles](https://cloud.google.com/security-command-center/docs/access-control-org#folder-level_and_project-level_roles) for Security Command Center to let teams view and manage security findings just for the projects for which they are responsible.

* If you use Google SecOps as your SIEM,  follow this article: [ingest Google Cloud data to Google SecOps](https://cloud.google.com/chronicle/docs/ingestion/cloud/ingest-gcp-logs).

* If you use a SIEM or SOAR tool with integrations to Security Command Center, read the following relevant articles: [Cortex XSOAR](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-cortex-xsoar), [Elastic Stack](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-elastic-stack-docker), [ServiceNow](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-servicenow), [Splunk](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-splunk), or [QRadar](https://cloud.google.com/security-command-center/docs/how-to-configure-scc-qradar).

* If you use an external tool that can ingest findings from Pub/Sub, configure [continuous exports](https://cloud.google.com/security-command-center/docs/how-to-export-data#continuous_exports) to Pub/Sub and configure your existing tools to ingest findings from the Pub/Sub topic.

## 4.10 Secret Management <a name="secret-management"></a>

We recommend that you never commit sensitive secrets such as API keys, passwords, and private certificates to source code repositories. Commit the secret to [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) and grant the [Secret Manager Secret Accessor](https://cloud.google.com/secret-manager/docs/access-control#secretmanager.secretAccessor) IAM role to the user or service account that needs to access the secret. We recommend that you grant the IAM role to an individual secret, not to all secrets in the project.

When possible, you should generate production secrets automatically within the CI/CD pipelines and keep them inaccessible to human users except in breakglass situations. In this scenario, ensure that you don't grant IAM roles to view these secrets to any users or groups.

The landing zone provides a single *prj-c-secrets* project in the common folder and a *prj-{env}-secrets* project in each environment folder for managing secrets centrally. This approach lets a central team audit and manage secrets used by applications in order to meet regulatory and compliance requirements.

Depending on your operational model, you might prefer a single centralized instance of Secret Manager under the control of a single team, or you might prefer to manage secrets separately in each environment, or you might prefer multiple distributed instances of Secret Manager so that each workload team can manage their own secrets. Modify the Terraform code sample as needed to fit your operational model.

Platform operators should have access to project level access to secrets in platform team managed projects, but they should not have access to application secrets. Application operators will have access to manage application secrets, which includes creating, updating, or decommissioning secrets in Secrets Manager. In addition to this, the application’s own service accounts will have access to individual secret/secret versions, but these service accounts will not be able to read any other secrets.

Secrets Manager has encryption at rest by default using Google Managed Encryption keys. The option to use Customer Managed Encryption Keys is also available and recommended (See [Reference: Secrets Manager \- Customer Managed Encryption Keys](https://cloud.google.com/secret-manager/docs/cmek)).

# 

# 5\. Landing Zone Deployment Options <a name="landing-zone-deployment-options"></a>

There are a few options for deploying the Protected B landing zone that can be considered depending on the desired future operating model and an organization’s technology preferences. We recommend that you use declarative infrastructure to deploy your foundation in a consistent and controllable manner. This approach helps enable consistent governance by enforcing policy controls about acceptable resource configurations into your pipelines. 

## 5.1 Cloud Build <a name="cloud-build"></a>

In this model, the landing zone is deployed using a GitOps flow with Terraform used to define infrastructure as code (IaC), a Git repository for version control and approval of code, and Cloud Build for CI/CD automation in the deployment pipeline. Terraform commitsare picked up by Cloud Build and a Terraform "plan" operation is performed to plan the impact on the environment. Terraform changes merged to the main branch of the bootstrap repository are picked up by Cloud Build, and a Terraform "apply" operation is performed.

## 5.2 Manual Deployment <a name="manual-deployment"></a>

This mode of deployment you will need to deploy each of the individual 7 stages by hand.  You will still be using Terraform as the Infrastructure as code engine however the terraform plan and apply steps will need to be run in the various directories related to the various stages from 1-7.

A link to the specific deployment instructions can be found below.  
[Manual PBMM Installation](https://docs.google.com/document/d/1iF-y9kQwVk4xs0bNhdX6kogHU-b8b1BbWl6AdbCJAUY/edit?usp=sharing)

## 5.3 Azure Devops Pipeline <a name="azure-devops-pipeline"></a>

Similar in approach to the Cloud Build model that is described above however this method is for those organizations who prefer to use Azure DevOps as their preferred deployment.

A link to the specific deployment instruction can be found below:  
[ADO Pipeline Documentation](https://docs.google.com/document/d/1gnbcEDA070Cqey-0-bO7KxMvOTcxTuZd-QNmBrceEmA/edit?usp=sharing&resourcekey=0-c_rRkhdtnYWl8P8683zPIw)

# Day 2 Tasks and Operational Best Practices <a name="day-2-tasks-and-operational-best-practices"></a>

## After IAC has been deployed <a name="after-iac-has-been-deployed"></a>

After your Terraform code has completed you should complete the following additional steps in order to complete your setup and ensure the highest level of compliance.

* Complete the [on-premises configuration changes](https://cloud.google.com/architecture/security-foundations/networking#on-premises_configuration_changes).  
* [Activate Security Command Center Premium](https://cloud.google.com/security-command-center/docs/activate-scc-overview).  
* [Export Cloud Billing data to BigQuery](https://cloud.google.com/billing/docs/how-to/export-data-bigquery).  
* Sign up for a [Cloud Customer Care plan](https://cloud.google.com/support).  
* [Enable Access Transparency](https://cloud.google.com/assured-workloads/access-transparency/docs/enable) logs.  
* [Share data from Cloud Identity with Google Cloud](https://support.google.com/a/answer/9320190).

 

## Operational Best Practices <a name="operational-best-practices"></a>

### Branching Strategy for your IAC repos

After deployment, you will have 7 repos corresponding to the steps above. Changes and additions to your infrastructure should be done through code. We recommend ongoing maintenance of your infrastructure as code should follow the best practices as outlined below. 

We recommend a [persistent branch](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows) strategy for submitting code to your Git system and deploying resources through the foundation pipeline. The following diagram describes the persistent branch strategy.

The diagram below shows three persistent branches in Git (development, non-production, and production) that reflect the corresponding Google Cloud environments. There are also multiple ephemeral feature branches that don't correspond to resources that are deployed in your Google Cloud environments.

![][image9]

We recommend that you enforce a [pull request (PR)](https://git-scm.com/docs/git-request-pull) process into your Git system so that any code that is merged to a persistent branch has an approved PR.

To develop code with this persistent branch strategy, follow these high-level steps:

1. When you're developing new capabilities or working on a bug fix, create a new branch based off of the development branch. Use a naming convention for your branch that includes the type of change, a ticket number or other identifier, and a human-readable description, like feature/123456-org-policies.

2. When you complete the work in the feature branch, open a PR that targets the development branch.

3. When you submit the PR, the PR triggers the foundation pipeline to perform terraform plan and terraform validate to stage and verify the changes.

4. After you validate the changes to the code, merge the feature or bug fix into the development branch.

5. The merge process triggers the foundation pipeline to run terraform apply to deploy the latest changes in the development branch to the development environment.

6. Review the changes in the development environment using any manual reviews, functional tests, or end-to-end tests that are relevant to your use case. Then promote changes to the non-production environment by opening a PR that targets the non-production branch and merge your changes.

7. To deploy resources to the production environment, repeat the same process as step 6: review and validate the deployed resources, open a PR to the production branch, and merge.

### Use the Active Assist Portfolio

In addition to IAM recommender, Google Cloud provides the [Active Assist](https://cloud.google.com/solutions/active-assist) portfolio of services to make recommendations about how to optimize your environment. For example, [firewall insights](https://cloud.google.com/network-intelligence-center/docs/firewall-insights/how-to/using-firewall-insights) or the [unattended project recommender](https://cloud.google.com/recommender/docs/unattended-project-recommender) provide actionable recommendations that can help tighten your security posture.

Design a process to periodically review recommendations or automatically apply recommendations into your deployment pipelines. Decide which recommendations should be managed by a central team and which should be the responsibility of workload owners, and apply IAM roles to access the recommendations accordingly.

### Grant exceptions to organization policies

The blueprint enforces a set of organization policy constraints that are recommended to most customers in most scenarios, but you might have legitimate use cases that require limited exceptions to the organization policies you enforce broadly.

For example, the blueprint enforces the [iam.disableServiceAccountKeyCreation](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts#disable_service_account_key_creation) constraint. This constraint is an important security control because a leaked service account key can have a significant negative impact, and most scenarios should use [more secure alternatives to service account keys](https://cloud.google.com/docs/authentication#auth-decision-tree) to authenticate. However, there might be use cases that can only authenticate with a service account key, such as an on-premises server that requires access to Google Cloud services and cannot use workload identity federation. In this scenario, you might decide to allow an exception to the policy, so long as additional compensating controls like [best practices for managing service account keys](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys) are enforced.

Therefore, you should design a process for workloads to request an exception to policies, and ensure that the decision makers who are responsible for granting exceptions have the technical knowledge to validate the use case and consult on whether additional controls must be in place to compensate. When you grant an exception to a workload, modify the organization policy constraint as narrowly as possible. You can also [conditionally add constraints to an organization policy](https://cloud.google.com/resource-manager/docs/organization-policy/tags-organization-policy#conditionally_add_constraints_to_organization_policy) by defining a tag that grants an exception or enforcement for policy, then applying the tag to projects and folders.

# Appendix 1: Naming Conventions <a name="naming-conventions"></a>

We recommend that you have a standardized naming convention for your Google Cloud resources. The following table describes recommended conventions for resource names in the blueprint.

| Resource Type | Naming Convention |
| :---- | :---- |
| Folder | `fldr-environment environment` is a description of the folder-level resources within the Google Cloud organization. For example, `bootstrap`, `common`, `production`, `nonproduction`, `development`, or `network`. For example: `fldr-production` |
| Project ID | `prj-environmentcode-description-randomid environmentcode` is a short form of the environment field (one of `b`, `c`, `p`, `n`, `d`, or `net`). Shared VPC host projects use the `environmentcode` of the associated environment. Projects for networking resources that are shared across environments, like the `interconnect` project, use the `net` environment code. description is additional information about the project. You can use short, human-readable abbreviations. randomid is a randomized suffix to prevent collisions for resource names that must be globally unique and to mitigate against attackers guessing resource names. The blueprint automatically adds a random four-character alphanumeric identifier. For example: `prj-c-logging-a1b2` |
| VPC network | `vpc-environmentcode-vpctype-vpcconfig environmentcode` is a short form of the environment field (one of `b`, `c`, `p`, `n`, `d`, or `net`). vpctype is one of `shared`, `float`, or `peer`. vpcconfig is either `base` or `restricted` to indicate whether the network is intended to be used with VPC Service Controls or not. For example: `vpc-p-shared-base` |
| Subnet | `sn-environmentcode-vpctype-vpcconfig-region{-description`} environmentcode is a short form of the environment field (one of `b`, `c`, `p`, `n`, `d`, or `net`). vpctype is one of `shared`, `float`, or `peer`. vpcconfig is either `base` or `restricted` to indicate whether the network is intended to be used with VPC Service Controls or not. region is any valid [Google Cloud region](https://cloud.google.com/compute/docs/regions-zones) that the resource is located in. We recommend removing hyphens and using an abbreviated form of some regions and directions to avoid hitting character limits. For example, `au` (Australia), `na` (North America), `sa` (South America), `eu` (Europe), `se` (southeast), or `ne` (northeast). description is additional information about the subnet. You can use short, human-readable abbreviations. For example: `sn-p-shared-restricted-uswest1` |
| Firewall policies | `fw-firewalltype-scope-environmentcode{-description`} firewalltype is `hierarchical` or `network`. scope is `global` or the Google Cloud region that the resource is located in. We recommend removing hyphens and using an abbreviated form of some regions and directions to avoid reaching character limits. For example, `au` (Australia), `na` (North America), `sa` (South America), `eu` (Europe), `se` (southeast), or `ne` (northeast). environmentcode is a short form of the environment field (one of `b`, `c`, `p`, `n`, `d`, or `net`) that owns the policy resource. description is additional information about the hierarchical firewall policy. You can use short, human-readable abbreviations. For example: `fw-hierarchical-global-c-01 fw-network-uswest1-p-shared-base` |
| Cloud Router | `cr-environmentcode-vpctype-vpcconfig-region{-description`} environmentcode is a short form of the environment field (one of `b`, `c`, `p`, `n`, `d`, or `net`). vpctype is one of `shared`, `float`, or `peer`. vpcconfig is either `base` or `restricted` to indicate whether the network is intended to be used with VPC Service Controls or not. region is any valid Google Cloud region that the resource is located in. We recommend removing hyphens and using an abbreviated form of some regions and directions to avoid reaching character limits. For example, `au` (Australia), `na` (North America), `sa` (South America), `eu` (Europe), `se` (southeast), or `ne` (northeast). description is additional information about the Cloud Router. You can use short, human-readable abbreviations. For example: `cr-p-shared-base-useast1-cr1` |
| Cloud Interconnect connection | `ic-dc-colo dc` is the name of your data center to which a Cloud Interconnect is connected. colo is the [colocation facility name](https://cloud.google.com/interconnect/docs/concepts/colocation-facilities#locations-table) that the Cloud Interconnect from the on-premises data center is peered with. For example: `ic-mydatacenter-lgazone1` |
| Cloud Interconnect VLAN attachment | `vl-dc-colo-environmentcode-vpctype-vpcconfig-region{-description} dc` is the name of your data center to which a Cloud Interconnect is connected. colo is the colocation facility name that the Cloud Interconnect from the on-premises data center is peered with. environmentcode is a short form of the environment field (one of `b`, `c`, `p`, `n`, `d`, or `net`). vpctype is one of `shared`, `float`, or `peer`. vpcconfig is either `base` or `restricted` to indicate whether the network is intended to be used with VPC Service Controls or not. region is any valid Google Cloud region that the resource is located in. We recommend removing hyphens and using an abbreviated form of some regions and directions to avoid reaching character limits. For example, `au` (Australia), `na` (North America), `sa` (South America), `eu` (Europe), `se` (southeast), or `ne` (northeast). description is additional information about the VLAN. You can use short, human-readable abbreviations. For example: `vl-mydatacenter-lgazone1-p-shared-base-useast1-cr1` |
| Group | `grp-gcp-description@example.com` Where description is additional information about the group. You can use short, human-readable abbreviations. For example: `grp-gcp-billingadmin@example.com` |
| Custom role | `rl-description` Where description is additional information about the role. You can use short, human-readable abbreviations. For example: `rl-customcomputeadmin` |
| Service account | `sa-description@projectid.iam.gserviceaccount.com` Where: description is additional information about the service account. You can use short, human-readable abbreviations. projectid is the globally unique project identifier. For example: `sa-terraform-net@prj-b-seed-a1b2.iam.gserviceaccount.com` |
| Storage bucket | `bkt-projectid-description` Where: projectid is the globally unique project identifier. description is additional information about the storage bucket. You can use short, human-readable abbreviations. For example: `bkt-prj-c-infra-pipeline-a1b2-app-artifacts` |

# 

# Appendix 2: Mapping Controls to Code <a name="mapping-controls-to-code"></a>

Notes: 

* Meeting ITSG-33/PBMM requirements will require configuration(s) in additional Google systems (for example, user identities and attributes such as usernames, passwords, multi-factor authentication (MFA), 2-step verification (2SV), and single sign-on (SSO) are configured and managed via [Google Workspace](https://workspace.google.com/) or [Cloud Identity](https://cloud.google.com/identity)).   
* The controls listed in this document often do not have a 1:1 mapping between the control itself and a singular code block where it can be invoked.   
* The header row is automatically pinned so it will appear at the top of each page.

## Access Control (AC)

### AC-2 (2) \- ACCESS CONTROL

**Control Description:** The information system automatically removes; disables temporary and emergency accounts after no more than 30 days

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Customers are responsible for managing all aspects of access control for customer users of GCP. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Customers are responsible for disabling temporary and emergency information system accounts used to access GCP in accordance with customer policy.

Workspace Consideration(s):  
Temporary or emergency accounts cannot be created in Google's application authentication service.  
Customer agencies should not provision temporary or emergency accounts.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Google Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/)

### AC-2 (3)

**Control Description:** The information system automatically disables inactive accounts after 90 days for user accounts

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Customers are responsible for managing all aspects of access control for customer users of GCP. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Customers are responsible for disabling temporary and emergency information system accounts used to access GCP in accordance with customer policy.

Workspace Consideration(s):  
Through the implementation of the SAML-based SSO an agency can automatically disable Google accounts after 90 days of inactivity.  
The agency should consider automatically disabling inactive accounts through integration with the SAML-based SSO after an agency-defined time period not to exceed the FedRAMP control requirement of 90 days.

Chrome Sync login occurs through the Chrome browser installed locally on a user's machine, and the Chrome Sync login activity is independent from the current Workspace account an agency customer is using. For example, an agency customer may log into Chrome Sync using "alice@agency.gov" while simultaneously logged into Gmail as "bob@agency.gov." The Chrome Sync and Workspace accounts being used are not linked together. Agency customers using Chrome Sync should only log into Chrome Sync using their authorized agency accounts.

Agency customers should log out of Chrome Sync on browsers and devices which they are no longer using. 

Agency customers are responsible for only logging into Chrome Sync via their agency account, on their agency issued device and only doing agency work while signed in to their agency account to prevent accidental flow of information to other accounts. 

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Google Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/)

### AC-2 (4)

**Control Description:** The information system automatically audits account creation, modification, enabling, disabling, and removal actions, and notifies organization-defined personnel or roles.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Google Cloud Logs will audit account creation, modification, disablement, removal, and enablement actions. LZ centralizes these logs into Pub/Sub. It is the customer's responsibility to consume these audit events into a SIEM solution.

#### Resource Definitions

* \- 1-org/envs/shared/org\_policy.tf \- for organization and folder policies  
* \- 1-org/envs/shared/log\_sinks.tf \- for setting up capturing audit logs, centralized logging, real-time monitoring, long-term storage and analysis

#### Org Policies

* AC-2        iam.disableServiceAccountKeyCreation: This constraint prevents users from creating persistent keys for service accounts to decrease the risk of exposed service account credentials.  
* AC-2        essentialcontacts.allowedContactDomains: This policy limits Essential Contacts to only allow managed user identities in selected domains to receive platform notifications.  
* AC-2        iam.allowedPolicyMemberDomains: This policy limits IAM policies to only allow managed user identities in selected domains to access resources inside this organization.  
* AC-2        compute.disableGuestAttributesAccess: This permission controls whether a user or service account can modify guest attributes on a virtual machine (VM) instance. Guest attributes can contain metadata or configuration data that could potentially impact the security or operation of the VM.

#### Implementation Recommendations

Customers are responsible for managing all aspects of access control for customer users of GCP. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Customers are responsible for disabling temporary and emergency information system accounts used to access GCP in accordance with customer policy.                

Workspace Consideration(s):  
The agency is responsible for automatically auditing account creation, modification, disabling, and termination actions, and notifying, as required, appropriate individuals when using SAML-based SSO.  
Customer agencies are required to determine organization-defined roles and responsibilities to fulfill their obligations for the following FedRAMP requirements. Customer agencies must define personnel or roles to notify when automatically auditing account creation, modification, enabling, disabling and removal actions.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/) 

Google Workspace \- Easily add users, manage devices, and configure security and settings so your data stays safe. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite' FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)

### AC-2 (10)

**Control Description:** The information system terminates shared/group account credentials when members leave the group.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM.

#### Implementation Recommendations

Customers are responsible for managing all aspects of access control for customer users of GCP. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Customers are responsible for disabling temporary and emergency information system accounts used to access GCP in accordance with customer policy.                

Workspace Consideration(s):  
Agencies are responsible for defining their own requirements around shared account access. Each Workspace account account is intended and designed for use by an individual user.  
If an agency provisions shared accounts, it is also responsible for terminating group credentials when a member leaves. Workspace Admin Console provides Admins with the option to change an account's password.

Chrome Sync login occurs through the Chrome browser installed locally on a user's machine, and the Chrome Sync login activity is independent from the current Workspace account an agency customer is using. For example, an agency customer may log into Chrome Sync using "alice@agency.gov" while simultaneously logged into Gmail as "bob@agency.gov." The Chrome Sync and Workspace accounts being used are not linked together. Agency customers using Chrome Sync should only log into Chrome Sync using their authorized agency accounts.

\- Agency customers should log out of Chrome Sync on browsers and devices which they are no longer using.

\- Agency customers are responsible for only logging into Chrome Sync via their agency account, on their agency issued device and only doing agency work while signed in to their agency account to prevent accidental flow of information to other accounts

### AC-3

**Control Description:** The information system enforces approved authorizations for logical access to information and system resources in accordance with applicable access control policies.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Customer would be responsible for adding users to the roles for system access.

IAM permissions and groups are used to enforce authorizations for the system. It is enforced via a combination of GCP standard roles, as well as custom roles.  Access enforcement is done for user and service accounts.

#### Resource Definitions

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf \- audit logging  
* \- 1-org/envs/shared/iam.tf \- custom roles  
* \- 1-org/envs/shared/projects.tf \- logical separation of projects for limited permissions  
* \- 1-org/envs/shared/folders.tf \- logical hierarchy of resources for limited permissions

#### Org Policies

* AC-3        iam.automaticIamGrantsForDefaultServiceAccounts: This constraint prevents default service accounts from receiving the overly-permissive Identity and Access Management (IAM) role Editor at creation.  
* AC-3, AC-6        compute.disableNestedVirtualization: This policy disables nested virtualization to decrease security risk due to unmonitored nested instances.  
* AC-3, AC-6        compute.disableSerialPortAccess: This policy prevents users from accessing the VM serial port which can be used for backdoor access from the Compute Engine API control plane.  
* AC-3, AC-6        compute.skipDefaultNetworkCreation: This policy disables the automatic creation of a default VPC network and default firewall rules in each new project, ensuring that network and firewall rules are intentionally created.  
* AC-3, AC-6        compute.restrictXpnProjectLienRemoval: This policy prevents the accidental deletion of Shared VPC host projects by restricting the removal of project liens.  
* AC-3, AC-6        compute.disableVpcExternalIpv6: This policy prevents the creation of external IPv6 subnets, which can be exposed to incoming and outgoing internet traffic.  
* AC-3, AC-6        compute.setNewProjectDefaultToZonalDNSOnly: This policy restricts application developers from choosing legacy DNS settings for Compute Engine instances that have lower service reliability than modern DNS settings.  
* AC-3, AC-6        sql.restrictPublicIp: This policy prevents the creation of Cloud SQL instances with public IP addresses, which can expose them to incoming internet traffic and outgoing internet traffic.  
* AC-3, AC-6        sql.restrictAuthorizedNetworks: This policy prevents public or non-RFC 1918 network ranges from accessing Cloud SQL databases.  
* AC-3, AC-6        storage.uniformBucketLevelAccess: This policy prevents Cloud Storage buckets from using per-object ACL (a separate system from IAM policies) to provide access, enforcing consistency for access management and auditing.  
* AC-3, AC-6        storage.publicAccessPrevention: This policy prevents Cloud Storage buckets from being open to unauthenticated public access.  
* AC-3, AC-6        compute.disableVpcExternalIpv6: This policy prevents the creation of external IPv6 subnets, which can be exposed to incoming and outgoing internet traffic.  
* AC-3, AC-6        compute.vmExternalIpAccess: This policy prevents the creation of Compute Engine instances with a public IP address, which can expose them to incoming internet traffic and outgoing internet traffic.  
* AC-3, AU-12        compute.requireOsLogin: This policy requires OS Login on newly created VMs to more easily manage SSH keys, provide resource-level permission with IAM policies, and log user access.

#### Implementation Recommendations

Customers are responsible for managing all aspects of access control for customer users of GCP. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Customers are responsible for disabling temporary and emergency information system accounts used to access GCP in accordance with customer policy.   

Workspace Consideration(s):  
Workspace enforces administrator authorization for logical access to the agency's domain. Workspace allows administrators to establish administrator roles and groups within a domain, and access to the roles and groups can be restricted based on required authorization. Within the Admin Console domain settings there are established administrator roles, as well as, the option for customer created roles. For each administrator role, specific privileges are defined controlling what administrators are authorized to access within Admin Console. Administrators establish groups by setting a group name, group email and a brief explanation of the group.  
The administrator determines the permission presets for the group by determining if the group should be for the public, announcements, the team, or custom. A public group is for topics of general interest and email is unrestricted. An announcement group is for broadcasting to a wide audience and email is restricted to group owners.  A team group is for teams and other working groups and email is restricted to domain users.  A custom group allows fine-grained control of group permission.  Users can also establish groups and be administrators of their own content and the sub-groups within the groups they create.

Separating user access within your domain:

To manage user permissions, the admin can simply create organizational units to logically segregate end user accounts. Once these units are set up, the admin can turn specific services on or off for users.

To learn more, please refer to our Support resources that discuss "how to setup organizational units" and "how to turn services on and off".

Google Vault:

Administrator privileges related to Google Vault are assigned to users within Admin Console. Domain Administrators with the Super Administrator role by default have access to all Vault access privileges. Customers can also assign any combination of Vault privileges to users via custom created roles within Admin Console. Google Vault is only available to customers with Workspace for Business or Workspace for Enterprise editions, or as a paid addition to Workspace Basic. It is the customer's responsibility to purchase Google Vault if they are a Workspace Basic customer.

The agency is responsible for establishing user created administrator roles, groups, and permissions in Workspace, ensuring that authorizations are approved, and ensuring the process is performed in accordance with applicable agency policy. (Customer Responsibility \#2)             

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/) 

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)  

Google Workspace \- Easily add users, manage devices, and configure security and settings so your data stays safe. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/)

### AC-4

**Control Description:** The information system enforces approved authorizations for controlling the flow of information within the system and between interconnected systems based on the customer's organization-defined information flow control policies.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

This Landing Zone uses the Hub and Spoke architecture mode. The Landing Zone template uses DNS-zones, Network Virtual Appliance Firewalls, Virtual Private Cloud (VPC) networking, and VPC service controls to satisfy this requirement. More details can be found at the Networking section of the Google cloud security foundations guide ([https://cloud.google.com/architecture/security-foundations/networking\#hub-and-spoke](https://cloud.google.com/architecture/security-foundations/networking#hub-and-spoke)).

Detailed description of implementation can be found in 3\. networks-dual-svpc ([https://github.com/terraform-google-modules/terraform-example-foundation\#3-networks-dual-svpc](https://github.com/terraform-google-modules/terraform-example-foundation#3-networks-dual-svpc)) and 3\. networks-hub-and-spoke ([https://github.com/terraform-google-modules/terraform-example-foundation\#3-networks-hub-and-spoke](https://github.com/terraform-google-modules/terraform-example-foundation#3-networks-hub-and-spoke));

Fortinet’s Fortigate will be the next generation firewall appliance in use.  

Firewall rules are implemented by default to prevent connections outside of the system boundary. Information/data is not present on the solution (it is an infrastructure only solution) prior to client workload onboarding. Any rules allowing the release of information outside the system boundaries would be the responsibility of the information/data owner as part of their response to this control.

IAM Asset Inventory allows for automated discovery/export of currently deployed services across the organization or individual projects.

Refer to Architecture ([https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md\#system-architecture-high-level-workload-overview](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md#system-architecture-high-level-workload-overview))

#### Resource Definitions

* \- 3-networks-hub-and-spoke/modules/base\_env/main.tf for base definition of network, service controls, policies and logging  
* \- 3-networks-hub-and-spoke/envs/shared/dns-hub.tf \- dns definition

#### Implementation Recommendations

Customers are responsible for controlling the flow of information within the customer's system, including components built in GCP, and between the customer's system and other interconnected systems. Customers may elect to use the Virtual Private Cloud (VPC) service within the GCP Networking product family to help address this requirement. VPC is a comprehensive set of Google-managed networking capabilities, including granular IP address range selection, routes, firewalls and Virtual Private Network (VPN). VPC allows customers to provision their GCP resources, connect them to each other, and isolate them from one another in a Virtual Private Cloud (VPC).

Workspace Consideration(s):  
Agency customers with data location requirements are responsible for disabling Chrome Sync. Chrome Sync is not a data located product and syncs data from the user's browser, which may contain data localized data.  
Chrome Sync login occurs through the Chrome browser installed locally on a user's machine, and the Chrome Sync login activity is independent from the current Workspace account an agency customer is using. For example, an agency customer may log into Chrome Sync using "alice@agency.gov" while simultaneously logged into Gmail as "bob@agency.gov." The Chrome Sync and Workspace accounts being used are not linked together. Agency customers using Chrome Sync should only log into Chrome Sync using their authorized agency accounts.

Agency customers are responsible for only logging into Chrome Sync via their agency account, on their agency issued device and only doing agency work while signed in to their agency account to prevent accidental flow of information to other accounts.

Customer agencies are responsible for configuring their client-side browsers and connections on applicable workstations, servers, and mobile devices to enable connections using encryption. Customers should enforce USGCB settings on government furnished workstations to establish connections with FIPS-approved ciphers. Customers should enable the list of functions requiring a trusted path connection should be reviewed and approved by the agency AO or FedRAMP JAB.

Best Practice: Implement VPC Service Controls (link) to block external access to services protected by the perimeter.  
Best Practice: Enable VPC Flow Logs (link) to monitor network traffic sent to/from VM instances

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/)  

Google Cloud Load Balancing \- Implement global network autoscaling, HTTP(S), TCP, SSL, and Internal Load Balancing   
[https://cloud.google.com/load-balancing/](https://cloud.google.com/load-balancing/) 

Cloud DNS \- Scalable, reliable, resilient and managed authoritative Domain Name System (DNS) service. Easily publish and manage millions of DNS zones and records.  
[https://cloud.google.com/dns/](https://cloud.google.com/dns/) 

VPC Service Controls \- A VPC feature to protect sensitive data in Google Cloud Platform services using security perimeters.  
[https://cloud.google.com/vpc-service-controls/](https://cloud.google.com/vpc-service-controls/) 

### AC-4 (21)

**Control Description:** The information system separates information flows logically or physically using organization-defined mechanisms and/or techniques to accomplish organization- defined required separations by types of information.

**Requirements:** PBMM Profile 1: No, Profile 3: Yes

#### Implementation Notes

Resources are logically separated for the organization and downstream for workloads. Separate projects, and roles for access, are created across types of information and business role such as billing, auditing, logging, kms, secrets and network.  Projects are created for teams and workloads

#### Resource Definitions

* \- 3-networks-hub-and-spoke/modules/base\_env/main.tf for base definition of network, service controls, policies and logging  
* \- 3-networks-hub-and-spoke/modules/hierarchical\_firewall\_policy for contextual access policies including ingress and egress

#### Implementation Recommendations

Customers are responsible for controlling the flow of information within the customer's system, including separating data flows logically according to customer requirements.

Best Practice: Implement VPC Service Controls ([https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters](https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters)) to block external access to services protected by the perimeter.  
Best Practice: Enable VPC Flow Logs ([https://cloud.google.com/vpc/docs/using-flow-logs](https://cloud.google.com/vpc/docs/using-flow-logs)) to monitor network traffic sent to/from VM instances \- App/Project Owner function 

### AC-6 (9)

**Control Description:** The information system audits the execution of privileged functions.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The Landing Zone defines roles and logical separation of resources for limited permissions.

#### Resource Definitions

* \- 1-org/envs/shared/iam.tf \- custom roles  
* \- 1-org/envs/shared/projects.tf \- logical separation of projects for limited permissions  
* \- 1-org/envs/shared/folders.tf \- logical hierarchy of resources for limited permissions

#### Org Policies

* AC-3, AC-6        compute.disableNestedVirtualization: This policy disables nested virtualization to decrease security risk due to unmonitored nested instances.  
* AC-3, AC-6        compute.disableSerialPortAccess: This policy prevents users from accessing the VM serial port which can be used for backdoor access from the Compute Engine API control plane.  
* AC-3, AC-6        compute.skipDefaultNetworkCreation: This policy disables the automatic creation of a default VPC network and default firewall rules in each new project, ensuring that network and firewall rules are intentionally created.  
* AC-3, AC-6        compute.restrictXpnProjectLienRemoval: This policy prevents the accidental deletion of Shared VPC host projects by restricting the removal of project liens.  
* AC-3, AC-6        compute.disableVpcExternalIpv6: This policy prevents the creation of external IPv6 subnets, which can be exposed to incoming and outgoing internet traffic.  
* AC-3, AC-6        compute.setNewProjectDefaultToZonalDNSOnly: This policy restricts application developers from choosing legacy DNS settings for Compute Engine instances that have lower service reliability than modern DNS settings.  
* AC-3, AC-6        sql.restrictPublicIp: This policy prevents the creation of Cloud SQL instances with public IP addresses, which can expose them to incoming internet traffic and outgoing internet traffic.  
* AC-3, AC-6        sql.restrictAuthorizedNetworks: This policy prevents public or non-RFC 1918 network ranges from accessing Cloud SQL databases.  
* AC-3, AC-6        storage.uniformBucketLevelAccess: This policy prevents Cloud Storage buckets from using per-object ACL (a separate system from IAM policies) to provide access, enforcing consistency for access management and auditing.  
* AC-3, AC-6        storage.publicAccessPrevention: This policy prevents Cloud Storage buckets from being open to unauthenticated public access.  
* AC-3, AC-6        compute.disableVpcExternalIpv6: This policy prevents the creation of external IPv6 subnets, which can be exposed to incoming and outgoing internet traffic.  
* AC-3, AC-6        compute.vmExternalIpAccess: This policy prevents the creation of Compute Engine instances with a public IP address, which can expose them to incoming internet traffic and outgoing internet traffic.  
* AC-6        iam.disableServiceAccountKeyUpload: This constraint avoids the risk of leaked and reused custom key material in service account keys.

#### Implementation Recommendations

Customers are responsible for auditing the execution of privileged functions for all customer controlled components hosted on GCP.

Workspace Consideration(s):  
Workspace provides access to privileged account event logging reports. The Admin console audit log shows a history of every task performed in your Google Admin console and who performed the task, at what time, and from which IP address. Reports can be accessed by going to Admin console \\ Reports \\ Admin.

Audit reports are filterable by event attributes.

More details and guidance related to privileged account event logging can be found here ([https://support.google.com/a/answer/4579579](https://support.google.com/a/answer/4579579))

Optional Best Practice: It may be useful to turn on Data Access audit logs for the specific system components managed by the system owners, to further log resource access ([https://cloud.google.com/logging/docs/audit/configure-data-access](https://cloud.google.com/logging/docs/audit/configure-data-access))

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/) 

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)    

Google Workspace \- Easily add users, manage devices, and configure security and settings so your data stays safe. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

### AC-6 (10)

**Control Description:** The information system prevents non-privileged users from executing privileged functions to include disabling, circumventing, or altering implemented security safeguards/countermeasures.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The Landing Zone defines roles and logical separation of resources for limited permissions. 

The Landing Zone template uses GCP Service Account access to these privileged accounts. The Organizational Administrator role should be used sparingly in alignment with the breakglass strategy.

#### Resource Definitions

* \- 1-org/envs/shared/iam.tf \- custom roles  
* \- 1-org/envs/shared/projects.tf \- logical separation of projects for limited permissions  
* \- 1-org/envs/shared/folders.tf \- logical hierarchy of resources for limited permissions

#### Org Policies

* AC-3, AC-6        compute.disableNestedVirtualization: This policy disables nested virtualization to decrease security risk due to unmonitored nested instances.  
* AC-3, AC-6        compute.disableSerialPortAccess: This policy prevents users from accessing the VM serial port which can be used for backdoor access from the Compute Engine API control plane.  
* AC-3, AC-6        compute.skipDefaultNetworkCreation: This policy disables the automatic creation of a default VPC network and default firewall rules in each new project, ensuring that network and firewall rules are intentionally created.  
* AC-3, AC-6        compute.restrictXpnProjectLienRemoval: This policy prevents the accidental deletion of Shared VPC host projects by restricting the removal of project liens.  
* AC-3, AC-6        compute.disableVpcExternalIpv6: This policy prevents the creation of external IPv6 subnets, which can be exposed to incoming and outgoing internet traffic.  
* AC-3, AC-6        compute.setNewProjectDefaultToZonalDNSOnly: This policy restricts application developers from choosing legacy DNS settings for Compute Engine instances that have lower service reliability than modern DNS settings.  
* AC-3, AC-6        sql.restrictPublicIp: This policy prevents the creation of Cloud SQL instances with public IP addresses, which can expose them to incoming internet traffic and outgoing internet traffic.  
* AC-3, AC-6        sql.restrictAuthorizedNetworks: This policy prevents public or non-RFC 1918 network ranges from accessing Cloud SQL databases.  
* AC-3, AC-6        storage.uniformBucketLevelAccess: This policy prevents Cloud Storage buckets from using per-object ACL (a separate system from IAM policies) to provide access, enforcing consistency for access management and auditing.  
* AC-3, AC-6        storage.publicAccessPrevention: This policy prevents Cloud Storage buckets from being open to unauthenticated public access.  
* AC-3, AC-6        compute.disableVpcExternalIpv6: This policy prevents the creation of external IPv6 subnets, which can be exposed to incoming and outgoing internet traffic.  
* AC-3, AC-6        compute.vmExternalIpAccess: This policy prevents the creation of Compute Engine instances with a public IP address, which can expose them to incoming internet traffic and outgoing internet traffic.  
* AC-6        iam.disableServiceAccountKeyUpload: This constraint avoids the risk of leaked and reused custom key material in service account keys.

#### Implementation Recommendations

Customers are responsible for preventing non-privileged users from executing privileged functions for all customer controlled components hosted on GCP. GCP allows customers to assign administrative and non-administrative roles to customer accounts within GCP. Non-administrative roles cannot perform privileged functions within the customer's GCP project, including disabling, circumventing, or altering implemented security safeguards/countermeasures.

Workspace Consideration(s):  
Agency customers are responsible for establishing conditions for group membership based on agency-defined criteria, including identifying authorized users of Workspace and specifying access privileges/roles.  
Grant access to the system based on valid access authorization and intended system usage.

Authorize and establish user created administrator roles, groups, and permissions, ensuring authorizations are approved and assigned in accordance with agency policy.

Best Practice: Have identity admin check and re-calibrate IAM permissions based on Cloud IAM Recommender ([https://cloud.google.com/iam/docs/recommender-overview](https://cloud.google.com/iam/docs/recommender-overview))

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/) 

### AC-7

**Control Description:** The information system:

 a. Enforces a limit of not more than 3 consecutive invalid logon attempts by a user, during a 15 minute time period; and

 b. Automatically locks the account/node for 30 minutes; or  
locks the account/node until released by an administrator; or  
delays next logon prompt according to an organization-defined delay algorithm when the maximum number of unsuccessful attempts is exceeded.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Customers are responsible for enforcing a limit of consecutive invalid logon attempts for customer user accounts and automatically locks the account until unlocked by an administrator. 

Google Workspace Consideration(s):

When logging into a Google account, Google's application authentication service does not by default enforce account lockout settings after a certain number of invalid log-in attempts. Google's application authentication service does institute the use of a Login Challenge such as a Captcha (type of challenge-response test used to determine if the user is a computer or a human) after an algorithm defined number of invalid log-in attempts. If a user responds to the Captcha incorrectly the user is presented with Captchas until the Captcha and password are entered correctly. Additionally, Google may send a secondary authentication code to an account the user included in their Google domain profile, such as an SMS sent to a backup cell phone number. Note: in order for a security code to be sent to a user’s cell phone, a user must provide that information in their Google Workspace Account Settings and complete the enrollment process, which includes saving the phone number in their Account Settings, receiving a test code and correctly entering the test code at the Google Account Settings prompt.  
For agencies using SAML based Single Sign-on, the account lockout settings are controlled by the agency's account management system which can be configured to enforce a limit of not more than three (3) consecutive invalid access attempts by a user during a 15 minute time period and automatically locks the account/node for a 30 minute time period.

For agencies using SAML-based SSO the agency should consider: (a) enforcing an agency-defined limit of consecutive invalid access attempts by a user during an agency-defined time period; (b) automatically locking the account for an agency-defined time period, locking the account until it is released by an administrator, or delaying the next login prompt for an agency-defined delay when the maximum number of unsuccessful attempts is exceeded. This control should apply regardless of whether the login occurs via a local or network connection. Agency administrators should configure their authentication service to enforce a limit of no more than three (3) invalid login attempts in a period of 15 minutes and lock the account/node for a minimum of 30 minutes.

Google also offers 2 factor authentication, either OTP or Security Key authentication options, for administrators to enable in the Admin Console. The 2 factor authentication implementation provides a second layer of verification for customer administrators and users. Once enabled, users or customer administrators must enroll in the 2 factor verification process to receive a six-digit verification code (OTP) or tap their USB token (Security Key) required to sign-in to Google Workspace in addition to their regular username and password credentials. If agencies choose to use Google 2 factor authentication and choose the Security Key authentication option, agencies should note that Domain-wide admin managed security keys and security key management is only available for Google Workspace Business and Google Workspace Enterprise Edition Customers.

If an agency does not choose to use SAML SSO, the agency is responsible for defining a time period of expected inactivity. Google Workspace Enterprise and Business Customers can configure a Google Session Termination duration as short as one (1) hour (https://support.google.com/a/answer/7576830?hl=en). It should be noted that in order for these settings to take effect, Agency users must log out and log back in to initiate the new session duration enforcement. It is also possible for Agency Administrators to manually reset a user’s sign-in cookies for each user (https://support.google.com/a/answer/178854?hl=en). Agencies that decide to implement a session termination duration shorter than one(1) hour should implement USGCB for agency workstations that will timeout the user at the workstation level after a period of inactivity specified by the agency.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)    

Google Workspace \- Easily add users, manage devices, and configure security and settings so your data stays safe. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

### AC-8

**Control Description:** The information system:

 a. Displays to users an organization-defined system use notification message or banner before granting access to the system that provides privacy and security notices consistent with applicable federal laws, Executive Orders, directives, policies, regulations, standards, and guidance and states that:  
   1\. Users are accessing a U.S. Government information system;  
   2\. Information system usage may be monitored, recorded, and subject to audit;  
   3\. Unauthorized use of the information system is prohibited and subject to criminal and civil penalties; and  
   4\. Use of the information system indicates consent to monitoring and recording;

 b. Retains the notification message or banner on the screen until users acknowledge the usage conditions and take explicit actions to log on to or further access the information system; and 

 c. For publicly accessible systems:  
   1\. Displays system use information based on organization-defined conditions, before granting further access;  
   2\. Displays references, if any, to monitoring, recording, or auditing that are consistent with privacy accommodations for such systems that generally prohibit those activities; and  
   3\. Includes a description of the authorized uses of the system.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Part a:  
Customers are responsible for displaying the appropriate system use banner to customer users before granting access to any customer systems. The system use banner should provide privacy and security notices consistent with applicable federal laws, Executive Orders, directives, policies, regulations, standards, and guidance.

Parb b:  
Customers are responsible for retaining the notification message or banner on the screen until customer users acknowledge the usage conditions and take explicit actions to log on to or further access the customer information system.

Part c:  
Customers are responsible for:

Displaying system use information for publicly accessible customer systems before granting further access  
Displaying references, if any, to monitoring, recording, or auditing that are consistent with privacy accommodations for such systems that generally prohibit those activities  
Including a description of the authorized uses of the system.

Workspace Consideration(s):  
In order to use System Use Notification controls, the agency is responsible for implementing SSO and approving a system use notification message or banner that is displayed on an agency-controlled SSO sign-in page. The agency should use SAML-based SSO to display the agency's approved system use notification when agency users attempt to authenticate to the agency domain and use the Admin Console to configure SSO for agency authentication. The agency is responsible for identifying, verifying and approving the system use notification or banner and the appropriate periodicity of the check.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Google App Engine \- Leverage Google App Engine and Google Compute Engine to serve websites, setup static websites for notifications, and to build scalable applications.  
[https://cloud.google.com/solutions/websites/](https://cloud.google.com/solutions/websites/) 

Cloud Pub/Sub \-Global messaging and even ingestion at scale  
[https://cloud.google.com/pubsub/](https://cloud.google.com/pubsub/)

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)  

Google Workspace \- Easily add users, manage devices, and configure security and settings so your data stays safe. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

Cloud Functions \- Event-driven serverless compute platform.  
[https://cloud.google.com/functions/](https://cloud.google.com/functions/) 

### AC-10

**Control Description:** The information system limits the number of concurrent sessions for privileged accounts to (3), and non-privileged account sessions to (2).

**Requirements:** PBMM Profile 1: No, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Customers are responsible for limiting the number of concurrent sessions for customer users according to customer account type.

Workspace Consideration(s):  
Agency customers should periodically review their Account Settings Recent Activity to determine whether their account activity is appropriate and notify an agency domain administrator if suspicious activity is detected. Additionally, agency customers should implement 2-step verification (2SV) to help limit the ability of a successful malicious login because users would need to provide a username, password and 2SV token delivered to a device (OTP) or tap their USB device (Security Key) that is in the physical possession of the user attempting to login. Furthermore, users can configure Notifications & Alerts to further monitor concurrent sessions

Chrome Sync login occurs through the Chrome browser installed locally on a user's machine, and the Chrome Sync login activity is independent from the current Workspace account an agency customer is using. For example, an agency customer may log into Chrome Sync using "alice@agency.gov" while simultaneously logged into Gmail as "bob@agency.gov." The Chrome Sync and Workspace accounts being used are not linked together. Agency customers using Chrome Sync should only log into Chrome Sync using their authorized agency accounts.

If agencies choose to use Google 2-Step Verification and choose the Security Key authentication option, agencies should note that Domain-wide admin managed security keys and security key management is only available for Workspace Business and Workspace Enterprise Edition Customers.

GSA has reviewed and accepted this alternative implementation

Agency customers should log out of Chrome Sync sessions when they are no longer using a browser or device

Best Practice: Configure Cloud Identity to limit session length for Google services (https://support.google.com/cloudidentity/answer/7576830?hl=en). By default, the session length for Google services is 14 days

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)  

Google Workspace \- Easily add users, manage devices, and configure security and settings so your data stays safe. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/) 

### AC-11

**Control Description:** The information system:  
   
a. Prevents further access to the system by initiating a session lock after a 15 minute time period of inactivity or upon receiving a request from a user; and

 b. Retains the session lock until the user reestablishes access using established identification and authentication procedures.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Part a:  
Customers are responsible for initiating a session lock for customer sessions after 15 minutes of inactivity or upon receiving a request from a user.

Part b:  
Customers are responsible for retaining session locks until the customer user reestablishes access using established customer identification and authentication procedures.

Workspace Consideration(s):  
The agency should use screensavers to (a) enable session lock after an agency-defined frequency of inactivity and (b) retain the session lock until the user reestablishes access using established identification and authentication procedures. In addition, where applicable, the agency should instruct users to log-out of the Google Services after completing a session on an unsecured workstation/laptop or upon removing a workstation/laptop from an unsecured facility.

Additionally, customers accessing Workspace from non-workstation devices, such as mobile devices, should enforce a mobile device management policy to lockout devices after 15 minutes of inactivity and require a passcode to unlock. The session lock should not exceed the FedRAMP requirement of 15 minutes of inactivity.

Best Practice: Configure Cloud Identity to limit session length for Google services (https://support.google.com/cloudidentity/answer/7576830?hl=en). By default, the session length for Google services is 14 days

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)  

Google Workspace \- Easily add users, manage devices, and configure security and settings so your data stays safe. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/) 

### AC-11 (1)

**Control Description:** The information system conceals, via the session lock, information previously visible on the display with a publicly viewable image.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Customers are responsible for ensuring customer systems conceal, via a session lock, information previously visible on the display with a publicly viewable image.

Workspace Consideration(s):  
The agency should use screensavers to enable session lock to conceal information previously visible on the display with a publicly viewable image and retain the session lock until the user reestablishes access using established identification and authentication procedures.

Best Practice: Configure Cloud Identity to limit session length for Google services (https://support.google.com/cloudidentity/answer/7576830?hl=en). By default, the session length for Google services is 14 days

### AC-12

**Control Description:** The information system automatically terminates a user session after organization-defined conditions or trigger events require a session disconnect.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM.

#### Implementation Recommendations

Customers are responsible for ensuring that customer systems automatically terminate a user session after a customer defined condition occurs.

Workspace Consideration(s):  
Workspace does not terminate a connection after a period of inactivity. As a compensating control agencies should implement SAML-based SSO as well as USGCB for agency workstations that will timeout the user at the workstation level after a period of inactivity specified by the agency.

Chrome Sync login occurs through the Chrome browser installed locally on a user's machine, and the Chrome Sync login activity is independent from the current Workspace account an agency customer is using. For example, an agency customer may log into Chrome Sync using "alice@agency.gov" while simultaneously logged into Gmail as "bob@agency.gov." The Chrome Sync and Workspace accounts being used are not linked together. Agency customers using Chrome Sync should only log into Chrome Sync using their authorized agency accounts.

Agency customers should log out of Chrome Sync on browsers and devices which they are no longer using.   
GSA has accepted this Alternative Implementation.  
Agencies should implement SAML-based SSO as well as USGCB for agency workstations that will timeout the user at the workstation level after a period of inactivity specified by the agency.

Best Practice: Configure Cloud Identity to limit session length for Google services (https://support.google.com/cloudidentity/answer/7576830?hl=en). By default, the session length for Google services is 14 days

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Key Management Service \- Manage, generate, use, rotate, and destroy AES256, RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 cryptographic keys on Google Cloud  
[https://cloud.google.com/kms/](https://cloud.google.com/kms/) 

Cloud HSM \- Protect your encryption keys in the cloud using a fully hosted, FIPS 140-2 Level 3 compliant hardware security model  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/) 

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/) 

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/)     

### AC-17 (1)

**Control Description:** The information system monitors and controls remote access methods.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system. 

he Landing Zone template deploys an immutable log bunker for collecting logging data. Organizations can use these logs for performing automated actions. The Landing Zone template also uses the Identity Aware Proxy, a feature that uses identity and context to guard access to services and VMs.

#### Implementation Recommendations

Customers are responsible for auditing the execution of privileged functions for all customer controlled components hosted on GCP.

Workspace Consideration(s):  
Workspace provides access to privileged account event logging reports. The Admin console audit log shows a history of every task performed in your Google Admin console and who performed the task, at what time, and from which IP address. Reports can be accessed by going to Admin console \\ Reports \\ Admin.

Audit reports are filterable by event attributes.

More details and guidance related to privileged account event logging can be found here

Optional Best Practice: It may be useful to turn on Data Access audit logs for the specific system components managed by the system owners, to further log resource access (link)

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/) 

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/)     
 

### AC-17 (2)

**Control Description:** The information system implements cryptographic mechanisms to protect the confidentiality and integrity of remote access sessions.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Customers are responsible for implementing cryptographic mechanisms to protect the confidentiality and integrity of remote access sessions to customer systems. Additionally, customers are required to ensure that machines connecting to Google Cloud are configured to use appropriate encryption for Google-to-agency communications.

Google uses encryption in transit with TLS ([https://cloud.google.com/security/encryption-in-transit\#encryption\_in\_transit\_by\_default](https://cloud.google.com/security/encryption-in-transit#encryption_in_transit_by_default)) by default from end users (the Internet) to all Google Services.  
Describe any additional the system owners configured encryption (e.g. Managed SSL certs, HTTPS LBs, etc.) \- User configurable encryption ([https://cloud.google.com/security/encryption-in-transit\#user\_config\_encrypt](https://cloud.google.com/security/encryption-in-transit#user_config_encrypt))  
Best Practice: Implement Dedicated Interconnect to isolate your organization's data and traffic from the public internet ([https://cloud.google.com/interconnect/docs/concepts/overview](https://cloud.google.com/interconnect/docs/concepts/overview))  \- the system owners function  
Best Practice: Configure Cloud VPN to further protect information in transit ([https://cloud.google.com/vpn/docs/concepts/overview](https://cloud.google.com/vpn/docs/concepts/overview)) \- IC function  
Best Practice: Implement Cloud Load Balancer(s) for additional encryption protection to applications ([https://cloud.google.com/load-balancing/docs/choosing-load-balancer](https://cloud.google.com/load-balancing/docs/choosing-load-balancer)) \- App/Project Owner function

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Key Management Service \- Manage, generate, use, rotate, and destroy AES256, RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 cryptographic keys on Google Cloud  
[https://cloud.google.com/kms/](https://cloud.google.com/kms/) 

Cloud HSM \- Protect your encryption keys in the cloud using a fully hosted, FIPS 140-2 Level 3 compliant hardware security model  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/) 

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/) 

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/)     

### AC-17 (3)

**Control Description:** The information system routes all remote accesses through an organization-defined number of managed network access control points.

Supplemental Guidance: Organizations consider the Trusted Internet Connections (TIC) initiative requirements for external network connections.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Customers are responsible for ensuring that all customer remote accesses to the information system are via a customer defined number of managed network access control points.

Describe how Google secures data in transit ([https://cloud.google.com/security/overview/whitepaper\#securing\_data\_in\_transit](https://cloud.google.com/security/overview/whitepaper#securing_data_in_transit)) using Google Front End servers (GFEs) and TLS ([https://cloud.google.com/security/encryption-in-transit\#user\_to\_google\_front\_end\_encryption](https://cloud.google.com/security/encryption-in-transit#user_to_google_front_end_encryption)).  
Best Practice: Implement Dedicated Interconnect to isolate your organization's data and traffic from the public internet ([https://cloud.google.com/interconnect/docs/concepts/overview](https://cloud.google.com/interconnect/docs/concepts/overview))  
Best Practice: Configure Cloud VPN to further protect information in transit ([https://cloud.google.com/vpn/docs/concepts/overview](https://cloud.google.com/vpn/docs/concepts/overview))  
Best Practice: Implement Cloud Load Balancer(s) for additional encryption protection to applications ([https://cloud.google.com/load-balancing/docs/choosing-load-balancer](https://cloud.google.com/load-balancing/docs/choosing-load-balancer))  
Optional Best Practice: Enable Cloud Identity Aware Proxy ([https://cloud.google.com/iap/docs/concepts-overview](https://cloud.google.com/iap/docs/concepts-overview)) to manage and restrict remote access to FedRAMP applications 

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Key Management Service \- Manage, generate, use, rotate, and destroy AES256, RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 cryptographic keys on Google Cloud  
[https://cloud.google.com/kms/](https://cloud.google.com/kms/)

Cloud HSM \- Protect your encryption keys in the cloud using a fully hosted, FIPS 140-2 Level 3 compliant hardware security model  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/)

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/)

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/)     

Context Aware Access \- A feature of Cloud IAP that allows you to manage access to apps and infrastructure based on a user’s identity and context. [https://cloud.google.com/context-aware-access/](https://cloud.google.com/context-aware-access/) 

## Audit and Accountability (AU)

### AU-3 \- AUDIT AND ACCOUNTABILITY

**Control Description:** The information system generates audit records containing information that establishes what type of event occurred, when the event occurred, where the event occurred, the source of the event, the outcome of the event, and the identity of any individuals or subjects associated with the event.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Google Cloud Logs will audit account creation, modification, disablement, removal, and enablement actions. LZ centralizes these logs into Pub/Sub. It is the customer's responsibility to consume these audit events into a SIEM solution.

The Landing Zone template deploys a locked storage bucket as an immutable log bunker for storing forensic log data (for audit purposes) by using an organizational log sink. The retention length is configurable.

#### Resource Definitions

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf for audit logging

#### Implementation Recommendations

GCP allows agency customer developers to write code and manage cloud resources to determine what audit records are generated and what information is contained within customer audit records. The GCP admin activity log produces audit records that contain sufficient information to, at a minimum, establish what type of event occurred, when (date and time) the event occurred, the source of the event, the outcome of the event, and the identity of any user/subject associated with the event. In the case of the admin activity log, "where the event occurred" is implied as occurring within the customer's GCP projects, folders or organizations. In addition to the admin log available through the GCP Cloud Console, application logs on application activity are available through the GCP Cloud Console and customers have the option to customize logs for their applications.

Customers may elect to use several GCP tools like Admin Audit Logs and Data Access Logs to ensure that adequate logging exists to establish what type of event occurred, when (date and time) the event occurred, where the event occurred, the source of the event, the outcome (success or failure) of the event, and the identity of any user/subject associated with the event. Customers should ensure that they properly configure appropriate GCP audit logs where applicable and set up additional logs where needed.

Workspace Consideration(s):

The agency should review the log content provided by the Admin SDK Reports API and the revision histories to determine whether the content meets the logging requirements defined by the agency. Additionally, the agency can use the SAML-based SSO for authorizing access to Workspace and can log additional events.

Best Practice: It may be useful to turn on Data Access audit logs for the specific system components managed by the system owners, to further log resource access ([https://cloud.google.com/logging/docs/audit/configure-data-access](https://cloud.google.com/logging/docs/audit/configure-data-access))  
Optional Best Practice: Enable access transparency logs to see when Google admin access your cloud data ([https://cloud.google.com/logging/docs/audit/access-transparency-overview](https://cloud.google.com/logging/docs/audit/access-transparency-overview))

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Access Transparency \- A feature enabled in Stackdriver Logging that allows users to get visibility into cloud provider actions on your data through near real-time logs.  
[https://cloud.google.com/access-transparency/](https://cloud.google.com/access-transparency/) 

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/) 

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)    

Google Workspace Security Center \- A Google Workspace feature; Actionable security insights for Google Workspace. Unified security dashboard. Get insights into external file sharing, visibility into spam and malware targeting users within your organization, and metrics to demonstrate your security effectiveness in a single, comprehensive dashboard.  
[https://workspace.google.com/products/admin/security-center/](https://workspace.google.com/products/admin/security-center/) 

### AU-3 (1)

**Control Description:** The information system generates audit records containing the following additional information: session, connection, transaction, or activity duration; for client-server transactions, the number of bytes received and bytes sent; additional informational messages to diagnose or identify the event; characteristics that describe or identify the object or resource being acted upon

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Google Cloud Logs will audit account creation, modification, disablement, removal, and enablement actions. LZ centralizes these logs into Pub/Sub. It is the customer's responsibility to consume these audit events into a SIEM solution.

#### Resource Definitions

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf for audit logging  
* \- 2-environments/modules/env\_baseline/monitoring.tf \- shared monitoring project  
* \- 3-networks-hub-and-spoke/modules/base\_env \- network flog log 

#### Implementation Recommendations

GCP allows agency customer developers to write code and manage cloud resources to determine what audit records are generated and what information is contained within customer audit records. The GCP admin activity log produces audit records that contain sufficient information to, at a minimum, establish what type of event occurred, when (date and time) the event occurred, the source of the event, the outcome of the event, and the identity of any user/subject associated with the event. In the case of the admin activity log, "where the event occurred" is implied as occurring within the customer's GCP projects, folders or organizations. In addition to the admin log available through the GCP Cloud Console, application logs on application activity are available through the GCP Cloud Console and customers have the option to customize logs for their applications.

Customers may elect to use several GCP tools like Admin Audit Logs and Data Access Logs to ensure that adequate logging exists to establish what type of event occurred, when (date and time) the event occurred, where the event occurred, the source of the event, the outcome (success or failure) of the event, and the identity of any user/subject associated with the event. Customers should ensure that they properly configure appropriate GCP audit logs where applicable and set up additional logs where needed.

Workspace Consideration(s):

The agency should review the log content provided by the Admin SDK Reports API and the revision histories to determine whether the content meets the logging requirements defined by the agency. Additionally, the agency can use the SAML-based SSO for authorizing access to Workspace and can log additional events.

Best Practice: It may be useful to turn on Data Access audit logs for the specific system components managed by the system owners, to further log resource access ([https://cloud.google.com/logging/docs/audit/configure-data-access](https://cloud.google.com/logging/docs/audit/configure-data-access))  
Optional Best Practice: Enable access transparency logs to see when Google admin access your cloud data ([https://cloud.google.com/logging/docs/audit/access-transparency-overview](https://cloud.google.com/logging/docs/audit/access-transparency-overview))

### AU-5

**Control Description:** The information system:

 a. Alerts organization-defined personnel or roles in the event of an audit processing failure; and

 b. Takes the following additional actions, as defined by the organization: (e.g., shut down information system, overwrite oldest audit records, stop generating audit records).

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Logs and controls are available from the selected IdM platform, e.g. Google Workspace or Cloud Identity.

Google Cloud system and audit logs are managed in the operations suite. 

In the event of an audit processing task failure, Google's infrastructure automatically re-assigns the failed task to another available resource. This usually results in no actual audit processing failure. Manual intervention in this process is rarely required.

If manual intervention is required, alerting is performed to allow responsible groups to fix the audit processing components that fail. The GCP Site Reliability Engineering (SRE) Team is alerted. As a first line of action, the SRE Team isolates the failed components and disconnects them from the network.

#### Resource Definitions

* \- 1-org/envs/shared/scc\_notification.tf \- SCC Notification for all active findings

#### Implementation Recommendations

Customers are responsible for monitoring and remediating audit processing failure for their systems and applications.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)  

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)      

Google Workspace Security Center \- A Google Workspace feature; Actionable security insights for Google Workspace. Unified security dashboard. Get insights into external file sharing, visibility into spam and malware targeting users within your organization, and metrics to demonstrate your security effectiveness in a single, comprehensive dashboard.  
[https://workspace.google.com/products/admin/security-center/](https://workspace.google.com/products/admin/security-center/)    

Cloud Pub/Sub \-Global messaging and even ingestion at scale  
[https://cloud.google.com/pubsub/](https://cloud.google.com/pubsub/) 

Cloud Functions \- Event-driven serverless compute platform.  
[https://cloud.google.com/functions/](https://cloud.google.com/functions/) 

### AU-7 (1)

**Control Description:** The information system provides the capability to process audit records for events of interest based on organization-defined audit fields within audit records.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Google Cloud Logs will audit account creation, modification, disablement, removal, and enablement actions. LZ centralizes these logs into Pub/Sub. It is the customer's responsibility to consume these audit events into a SIEM solution.

Cloud Asset Inventory Notification: Uses Google Cloud Asset Inventory to create a feed of IAM Policy change events, then process them to detect when a roles (from a preset list) is given to a member (service account, user or group). Then generates a SCC Finding with the member, role, resource where it was granted and the time that was granted.

#### Resource Definitions

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf for audit logging  
* \- 2-environments/modules/env\_baseline/monitoring.tf \- shared monitoring project  
* \- 3-networks-hub-and-spoke/modules/base\_env \- network flog log   
* \- 1-org/modules/cai-monitoring \- for Cloud Asset Inventory Notification

#### Implementation Recommendations

Customers are responsible for providing the capability to process audit records for events of interest based on audit fields within audit records.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/) 

### AU-8

**Control Description:** The information system:

 a. Uses internal system clocks to generate time stamps for audit records; and

 b. Records time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT) and meets an organization-defined granularity of time measurement.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The solution provides for detailed audit logs of system activity, allowing for comprehensive tracking and review. Additionally, Google Cloud's robust Identity and Access Management (IAM) capabilities enable fine-grained control over user actions, ensuring accountability for all interactions within the cloud environment.

#### Implementation Recommendations

GCP allows agency customer developers to write code and manage cloud resources. This includes using the internal system clocks of Google’s servers to generate time stamps for audit logs that are generated by customer systems hosted in GCP.

Customers should record timestamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT) and should define the granularity of time measurement.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)  

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)     

Google Workspace Security Center \- A Google Workspace feature; Actionable security insights for Google Workspace. Unified security dashboard. Get insights into external file sharing, visibility into spam and malware targeting users within your organization, and metrics to demonstrate your security effectiveness in a single, comprehensive dashboard.  
[https://workspace.google.com/products/admin/security-center/](https://workspace.google.com/products/admin/security-center/)  

### AU-9

**Control Description:** The information system protects audit information and audit tools from unauthorized access, modification, and deletion.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Google Cloud Logs will audit account creation, modification, disablement, removal, and enablement actions. LZ centralizes these logs into Pub/Sub. It is the customer's responsibility to consume these audit events into a SIEM solution.

#### Resource Definitions

* \- 1-org/envs/shared/iam.tf \- roles for privileged access to logs   
* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf for audit logging  
* \- 2-environments/modules/env\_baseline/monitoring.tf \- shared monitoring project  
* \- 3-networks-hub-and-spoke/modules/base\_env \- network flog log 

#### Implementation Recommendations

\- Supports on-demand audit review, analysis, and reporting requirements and after-the-fact investigations of security incidents; and

### AU-9 (2)

**Control Description:** The information system backs up audit records at least weekly onto a physically different system or system component than the system or component being audited.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Google Cloud Logs will audit account creation, modification, disablement, removal, and enablement actions. LZ centralizes these logs into Pub/Sub. It is the customer's responsibility to consume these audit events into a SIEM solution.

#### Resource Definitions

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf for audit logging  
* \- 2-environments/modules/env\_baseline/monitoring.tf \- shared monitoring project  
* \- 3-networks-hub-and-spoke/modules/base\_env \- network flog log 

#### Implementation Recommendations

GCP allows agency customer developers to write code and manage cloud resources. Many GCP services generate audit logs for customer systems built on those GCP services. The audit logs are retained on GCP for a fixed period of time, after which they are deleted. Customers can configure a backup destination for these audit logs, to increase the retention period and increase the number of replicate copies of logs for backup purposes. The backup destination can be configured as a physically different service on GCP, or a service/system outside of GCP.

Google Workspace Consideration(s)  
CUSTOMER should determine whether the frequency, location and availability of Google-provided audit log backups meets their requirements and implement processes to backup Google-provided audit records via the Admin Console and agency-provided audit logs to a different system or media at least weekly.  
If audit information is stored outside of the application the agency is responsible for protecting the audit information from unauthorized access, modification, and deletion.

### AU-12

**Control Description:** The information system:

 a. Provides audit record generation capability for the auditable events defined in AU-2 a. at all information system and network components where audit capability is deployed/available;

 b. Allows organization-defined personnel or roles to select which auditable events are to be audited by specific components of the information system; and  
   
c. Generates audit records for the events defined in AU-2 d. with the content defined in AU-3.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The Google Security Team requires that all components of the production environment and applications are capable of generating the defined auditable events as described in AU-2. This is accomplished via the Security Logging Policy.

OS Login simplifies SSH access management by linking your Linux user account to your Google identity. Administrators can easily manage access to instances at either an instance or project level by setting IAM permissions.

#### Resource Definitions

* \- 1-org/envs/shared/org\_policy.tf  
* \- 1-org/envs/shared/log\_sinks.tf for audit logging  
* \- 2-environments/modules/env\_baseline/monitoring.tf \- shared monitoring project  
* \- 3-networks-hub-and-spoke/modules/base\_env \- network flog log   
* \- 1-org/envs/shared/iam.tf \- roles for privileged access to logs 

#### Org Policies

* AC-3, AU-12        compute.requireOsLogin: This policy requires OS Login on newly created VMs to more easily manage SSH keys, provide resource-level permission with IAM policies, and log user access. \- This policy requires OS Login on newly created VMs to more easily manage SSH keys, provide resource-level permission with IAM policies, and log user access.

#### Implementation Recommendations

a, b,c . Customers are responsible to determine the roles and responsibilities to select which auditable events are to be audited by specific components of the information system to fulfill their obligations for the following FedRAMP requirements.

## Configuration Management (CM)

### CM-5 (1)

**Control Description:** The information system enforces access restrictions and supports auditing of the enforcement actions.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The Landing Zone code base is built with Terraform and controlled by GitHub. Any changes to the code base are handled via a merge/pull review process, preventing arbitrary modification to the core IaC. Changes to code are not reflected in the infrastructure until the code is actually deployed via terraform.

However, once the code is deployed, modification to the infrastructure via out-of-band changes (i.e., a privileged user modifying the infrastructure through the Google Cloud console) is possible, but would likely break inheritance. All changes to the infrastructure should be made via the merge/pull review process, and out of band changes should be disallowed by policy.

#### Implementation Recommendations

Customers are responsible for enforcing access restrictions and supports auditing of the enforcement actions.

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/) 

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)  

Cloud Source Repositories \- Store, manage, and track code in a fully managed, private git repository. Review code commits and automate builds.  
[https://cloud.google.com/source-repositories/](https://cloud.google.com/source-repositories/)  

Cloud Build \- Build, test, and deploy software quickly. Define custom workflows for building, testing, and deploying across multiple environments.   
[https://cloud.google.com/cloud-build/](https://cloud.google.com/cloud-build/)  

Cloud Resource Manager \- Hierarchically manage resources by project, folder, and organization. Centrally control org & access policies and asset inventories. Label resources for better management.   
[https://cloud.google.com/resource-manager/](https://cloud.google.com/resource-manager/)   

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)  

### CM-5 (3)

**Control Description:** The information system prevents the installation of organization-defined software and firmware components without verification that the component has been digitally signed using a certificate that is recognized and approved by the organization.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Customer responsibility.

#### Implementation Recommendations

Customers are responsible for preventing the installation of software and firmware components without verification that the component has been digitally signed using a certificate that is recognized and approved by the customer organization.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Key Management Service \- Manage, generate, use, rotate, and destroy AES256, RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 cryptographic keys on Google Cloud  
[https://cloud.google.com/kms/](https://cloud.google.com/kms/) 

Cloud HSM \- Protect your encryption keys in the cloud using a fully hosted, FIPS 140-2 Level 3 compliant hardware security model  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/) 

Google Managed SSL Certificates \- An element of Cloud Load Balancing; Google-managed SSL certificates are provisioned, renewed, and managed for your domain names.  
[https://cloud.google.com/load-balancing/docs/ssl-certificates](https://cloud.google.com/load-balancing/docs/ssl-certificates) 

Customer Managed SSL Certificates \- An element of Cloud Load Balancing; Provide your own SSL certificates to manage secure access to your GCP domains. Self-managed certificates can support wildcards and multiple subject alternative names (SANs).  
[https://cloud.google.com/load-balancing/docs/ssl-certificates\#working-self-managed](https://cloud.google.com/load-balancing/docs/ssl-certificates#working-self-managed) 

### CM-7 (2)

**Control Description:** The information system prevents program execution in accordance with organization-defined policies, regarding software program usage and restrictions; and/or rules authorizing the terms and conditions of software program usage.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Customer responsibility.

#### Implementation Recommendations

Customers are responsible for configuring their information system in order to prevent program execution in accordance with policies regarding software program usage and restrictions; rules authorizing the terms and conditions of software program usage.

## Contingency Planning (CP)

### CP-10(2)

**Control Description:** The information system implements transaction recovery for systems that are transaction-based.

Supplemental Guidance:  Transaction-based information systems include, for example, database management systems and transaction processing systems. Mechanisms supporting transaction recovery include, for example, transaction rollback and transaction journaling.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Customer responsibility.

#### Implementation Recommendations

Customers are responsible for implementing transaction recovery for their systems that are transaction-based.

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Cloud Deployment Manager \- Create declarative templates that specify all resources needed for your cloud deployment. Establish a repeatable, template-driven deployment process.  
[https://cloud.google.com/deployment-manager/](https://cloud.google.com/deployment-manager/) 

Google's Disaster Recovery Planning Guide \- What you need to know to design and implement a DR plan. Specific DR use cases and implementations on GCP. Note: This is not a GCP product  
[https://cloud.google.com/solutions/dr-scenarios-planning-guide](https://cloud.google.com/solutions/dr-scenarios-planning-guide) 

Managed Instance Groups \- Maintain high availability of your apps by proactively keeping your instances in a RUNNING state. Managed instance groups support autoscaling, load balancing, rolling updates, autohealing.  
[https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances](https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances) 

## Identification and Authentication (IA)

### IA-2 \- IDENTIFICATION AND AUTHENTICATION

**Control Description:** The information system uniquely identifies and authenticates organizational users (or processes acting on behalf of organizational users).

Note: Organizations can satisfy the identification and authentication requirements in this control with MFA solutions.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Customer is recommended to implement SSO using their existing IDp provider and synchronizing it to Cloud Identity / Google Workspace. With the implementation of SSO any MFA procedures that are in place today will be inherited by the platform today. The configuration of Identity syncing is a process that requires manual setup, it cannot be automated using Terraform and as such needs to be configured outside of the flow of the automated landing zone.

MFA enforcement is a best practice when administering users. Google.com accounts always require hardware-based multi-factor authentication. Google believes enabling MFA is the best way to protect accounts from phishing and recommends partners and customers always enable it.

This control is typically addressed via breakglass strategy.

#### Implementation Recommendations

Customers are responsible for managing all aspects of authentication for customer users of GCP. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Workspace Consideration(s):  
By design, Google does not enforce the use of SAML SSO on the Admin Console because if the agency SSO solution is unavailable, agency domain administrators will be unable to administer the Workspace service. Google recommends that agencies use 2-step verification for domain administrators to restrict access to the Admin Console. If implementing SAML SSO authentication customers should ensure all Google login pages are configured to point to the agencies SSO portal. For FIPS 199 Moderate impact level systems multifactor authentication is required. When using SAML-SSO with a mobile device (e.g., Apple iOS, Android, Blackberry), desktop, or thick-client (e.g., Outlook) installations of Workspace, additional implementation considerations apply based on the configuration of the agency's AC and IA control implementation and may require passwords to be stored in Google's application authentication service as described above. In lieu of SAML, agencies also may choose to enable 2-step verification (outlined below).  
If agencies choose to use Google 2-Step Verification and choose the Security Key authentication option, agencies should note that Domain-wide admin managed security keys and security key management is only available for Workspace Business and Workspace Enterprise Edition Customers.

If an agency does not choose to use SAML SSO, the agency is responsible for defining a time period of expected inactivity or a description of when their organizational users are required to log out. Agency customers should train employees on the system logout functionality and adhering to expected system behavior, and require logout when the user's session is done or according to agency guidelines.

Describe how service account in GCP are viewed as both resources and identities ([https://cloud.google.com/iam/docs/understanding-service-accounts](https://cloud.google.com/iam/docs/understanding-service-accounts)), and how Cloud IAM is used to authenticate and authorize service accounts to access cloud resources.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/) 

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)  

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/) 

### IA-2 (1)

**Control Description:** The information system implements multifactor authentication for network access to privileged accounts.

**Requirements:** PBMM Profile 1: No, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system. 

The Landing Zone uses predefined roles, custom IAM roles, and service accounts to appropriately restrict resource configuration. The Landing Zone template also uses the Identity Aware Proxy, a feature that uses identity and context to guard access to services and VMs. IAP can be used to provide a secure tunnel to GCP resources and replaces the Bastion Host concept (referenced in the project and firewall modules).

#### Implementation Recommendations

Customers are responsible for managing all aspects of authentication for customer users of GCP, including implementing multifactor authentication for access to privileged customer accounts. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Workspace Consideration(s):  
When using SAML-SSO with a mobile device (e.g., Apple iOS, Android, Blackberry), desktop, or thick-client (e.g., Outlook) installations of Workspace, additional implementation considerations apply based on the configuration of the agency's AC and IA control implementation and may require passwords to be stored in Google's application authentication service as described in IA-2. This SSP does not contemplate the use of "thick" clients and only address access through a web browser. In lieu of SAML, agencies also may choose to enable 2-step verification (outlined below) for access to Admin Console.  
If an agency does not choose to use SAML SSO, the agency is responsible for defining a time period of expected inactivity or a description of when their organizational users are required to log out. Agency customers should train employees on the system logout functionality and adhering to expected system behavior, and require logout when the user's session is done or according to agency guidelines.

Best Practice: Enforce MFA / 2SV for privileged access to Google Cloud ([https://cloud.google.com/identity/solutions/enforce-mfa](https://cloud.google.com/identity/solutions/enforce-mfa)) using Cloud Identity

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/) 

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)  

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/) 

### IA-2 (2)

**Control Description:** The information system implements multifactor authentication for network access to non- privileged accounts.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

The Landing Zone uses predefined roles, custom IAM roles, and service accounts to appropriately restrict resource configuration. The Landing Zone template also uses the Identity Aware Proxy, a feature that uses identity and context to guard access to services and VMs. IAP can be used to provide a secure tunnel to GCP resources and replaces the Bastion Host concept (referenced in the project and firewall modules).

#### Implementation Recommendations

Customers are responsible for managing all aspects of authentication for customer users of GCP, including implementing multifactor authentication for access to non-privileged customer accounts. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Workspace Consideration(s):  
When using SAML-SSO with mobile device (e.g., Apple iOS, Android, Blackberry), desktop, or thick-client (e.g., Outlook) installations of Workspace, additional implementation considerations apply based on the configuration of the agency's AC and IA control implementation and may require passwords to be stored in Google's application authentication service as described in IA-2. In lieu of SAML, agencies also may choose to enable 2-step verification (outlined below) for access to Admin Console.  
If an agency does not choose to use SAML SSO, the agency is responsible for defining a time period of expected inactivity or a description of when their organizational users are required to log out. Agency customers should train employees on the system logout functionality and adhering to expected system behavior, and require logout when the user's session is done or according to agency guidelines.

Best Practice: Enforce MFA / 2SV for non-privileged access to Google Cloud ([https://cloud.google.com/identity/solutions/enforce-mfa](https://cloud.google.com/identity/solutions/enforce-mfa)) using Cloud Identity

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Google Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/)

### IA-2 (8)

**Control Description:** The information system implements replay-resistant authentication mechanisms for network access to privileged accounts.

Supplemental Guidance:  Authentication processes resist replay attacks if it is impractical to achieve successful authentications by replaying previous authentication messages. Replay- resistant techniques include, for example, protocols that use nonces or challenges such as Transport Layer Security (TLS) and time synchronous or challenge-response one-time authenticators.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Customers are responsible for managing all aspects of authentication for customer users of GCP, including ensuring that replay-resistant authentication mechanisms are used for authentication of users. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Google Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/)

### IA-2 (11)

**Control Description:** The information system implements multifactor authentication for remote access to privileged and non-privileged accounts such that one of the factors is provided by a device separate from the system gaining access and the device meets FIPS 140-2, NIAP Certification, or NSA approval.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system. 

The Landing Zone uses predefined roles, custom IAM roles, and service accounts to appropriately restrict resource configuration. The Landing Zone template also uses the Identity Aware Proxy, a feature that uses identity and context to guard access to services and VMs. IAP can be used to provide a secure tunnel to GCP resources and replaces the Bastion Host concept (referenced in the project and firewall modules).

#### Implementation Recommendations

Customers are responsible for managing all aspects of authentication for customer users of GCP, including implementing multifactor authentication for customer users and ensuring that the devices used by their multifactor authentication system for access to the Google Cloud is provided by a device separate from the system gaining access and that the device meets FIPS 140-2, NIAP Certification, or NSA approval. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Customers are responsible for using multifactor authentication for customer users and ensuring that the devices used by their multifactor authentication system for access to the Google Cloud is provided by a device separate from the system gaining access and that the device meets FIPS 140-2, NIAP Certification, or NSA approval.

Workspace Consideration(s):  
The agency must use the Admin Console to configure the 2 step verification to provide remote access to privileged and non-privileged accounts.  
The agency should implement multifactor authentication using SAML-based SSO. Multifactor authentication would be established with the entity issuing the SAML assertion to Google. Users would authenticate via the SAML provider to their domain and privileged users, such as administrators, could then access the domain's Admin Console. If the agency chooses to implement the 2-step verification capability, all users must enroll in 2-step verification, and select the method for receiving their verification code on their mobile phone: the Google Authenticator app, text message, or phone call. If implementing SAML SSO authentication customers should ensure all Google login pages are configured to point to the agencies SSO portal. For FIPS 199 Moderate impact level systems multifactor authentication is required.

If an agency does not choose to use SAML SSO, the agency is responsible for defining a time period of expected inactivity or a description of when their organizational users are required to log out. Agency customers should also train employees on the previously described logout functionality and adhering to expected system behavior.

Best Practice: Enforce MFA / 2SV for non-privileged access to Google Cloud ([https://cloud.google.com/identity/solutions/enforce-mfa](https://cloud.google.com/identity/solutions/enforce-mfa)) using Cloud Identity

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/) 

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)  

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/) 

### IA-2 (12)

**Control Description:** The information system accepts and electronically verifies Personal Identity Verification (PIV) credentials.

Supplemental Guidance: Personal Identity Verification (PIV) credentials are those credentials issued by federal agencies that conform to FIPS Publication 201 and supporting guidance documents.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

Customers are responsible for managing all aspects of authentication for customer users of GCP, including ensuring that the information system accepts and electronically verifies PIV credentials in their agency authentication systems for customer users. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Workspace Consideration(s):  
Agency customers should configure and use SAML-based SSO to authenticate to Workspace services, which allows them to inherit second factor authenticators implemented at their agency, such as PIV. The agency should consider employing automated mechanisms such as LDAP, SSO, etc to support the management of Workspace.

Best Practice: Enforce MFA / 2SV for non-privileged access to Google Cloud ([https://cloud.google.com/identity/solutions/enforce-mfa](https://cloud.google.com/identity/solutions/enforce-mfa)) using Cloud Identity

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/) 

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

### IA-3

**Control Description:** The information system uniquely identifies and authenticates organization-defined, specific and/or types of devices before establishing a local, remote, or network connection.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Google describes this control as Not Applicable for GCP and/or Workspace.

How Google meets this control for the Google Common Infrastructure (GCI):  
The Google Security Team requires that all devices in the production environment are assigned a unique IP address in private name space for identification. Machines within the production environment are assigned a unique hostname upon installation. VLAN IP restrictions permit only authorized devices to establish network connections. As part of set-up, machine-specific certificates are generated and installed on each machine; a machine certificate is required for laptops and workstations to connect to the Google corporate network

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/) 

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)  

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/) 

### IA-5 (1)

**Control Description:** The information system, for password-based authentication:

 (a)   Enforces minimum password complexity of organization-defined requirements for case sensitivity, number of characters, mix of upper-case letters, lower-case letters, numbers, and special characters, including minimum requirements for each type;

 (b)   Enforces at least one changed character when new passwords are created;

 (c)   Stores and transmits only encrypted representations of passwords;

 (d)   Enforces password minimum and maximum lifetime restrictions of organization- defined numbers for lifetime minimum, lifetime maximum;

 (e)   Prohibits password reuse for 24 generations; and

 (f) Allows the use of a temporary password for system logons with an immediate change to a permanent password.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Part a:  
Customers are responsible for managing all aspects of authentication for customer users of GCP, including enforcing a minimum password complexity for password based authentication. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Part b:  
Customers are responsible for managing all aspects of authentication for customer users of GCP, including ensuring that at least one character has changed when new passwords are created. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Part c:  
Customers are responsible for managing all aspects of authentication for customer users of GCP, including ensuring that passwords are cryptographically protected in storage and transmission. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Part d:  
Customers are responsible for managing all aspects of authentication for customer users of GCP, including ensuring that passwords are cryptographically protected in storage and transmission. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Part e:  
Customers are responsible for managing all aspects of authentication for customer users of GCP, including ensuring that customer passwords are not reused for 24 generations. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Part f:  
Customers are responsible for managing all aspects of authentication for customer users of GCP. This includes, if temporary passwords are used in the customer system, issuing temporary passwords for system logons with an immediate change to a permanent password. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Workspace Consideration(s):  
Agencies should use the Admin SDK Directory API /SAML-based SSO to meet the FIPS 199 Moderate impact level.  
The agency is responsible for managing password-based authentication including:

Establishing a minimum 12 character password length and enforcing minimum password complexity of at least one of each: case sensitivity, mix of uppercase letters, lowercase letters, numbers and special characters;  
Enforcing at least a one (1) changed password character when new passwords are created;  
ensuring that TLS is enabled on the domain to help ensure secure transmission over HTTPS; and,  
Enforcing one (1) day password minimum and 60 day maximum lifetime restrictions set by the agency; and  
Prohibiting password reuse for 24 generations.  
Allows the use of a temporary password for system logons with an immediate change to a permanent password.  
Mobile devices are excluded from the password complexity requirement.

If an agency does not choose to use SAML SSO, the agency is responsible for defining a time period of expected inactivity or a description of when their organizational users are required to log out. Agency customers should train employees on the system logout functionality and adhering to expected system behavior, and require logout when the user's session is done or according to agency guidelines.

Best Practice: Use Cloud Identity to setup password policies for cloud-managed identities (https://support.google.com/cloudidentity/answer/139399?hl=en)  
Best Practice: Enable Single Sign On (SSO) for cloud-based applications ([https://cloud.google.com/identity/solutions/enable-sso](https://cloud.google.com/identity/solutions/enable-sso))

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)   

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

### IA-5 (2)

**Control Description:** The information system, for PKI-based authentication:

 (a)   Validates certifications by constructing and verifying a certification path to an accepted trust anchor including checking certificate status information;

 (b)   Enforces authorized access to the corresponding private key;

 (c)   Maps the authenticated identity to the account of the individual or group; and

 (d)   Implements a local cache of revocation data to support path discovery and validation in case of inability to access revocation information via the network.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Part a:  
Customers are responsible for the management of customer PKI infrastructure and authentication in their systems. This includes validating certificates by constructing and verifying the certification path to an accepted trust anchor. Customers may elect to use the Cloud Key Management Service (Cloud KMS) within the GCP Identity & Security product family to help address this requirement. Cloud KMS is a cloud-hosted key management service that allows customers to manage encryption for their cloud services.

Part b:  
Customers are responsible for the management of customer PKI infrastructure and authentication in their systems. This includes enforcing authorized access to customer private keys. Customers can use the Cloud Key Management Service to help manage customer keys.

Part c:  
Customers are responsible for the management of customer PKI infrastructure and authentication in their systems. This includes mapping authenticated identities of customer identifiers to customer individuals or groups. Customers can use the Cloud Key Management Service to help manage customer keys.

Part d:  
Customers are responsible for the management of customer PKI infrastructure and authentication in their systems. This includes implementing a local cache of revocation data for user PKI. Customers can use the Cloud Key Management Service to help manage customer keys.

Workspace  Consideration(s):  
Customer agencies are responsible for meeting the FedRAMP requirements when configuring access through the SAML-based SSO. Agencies should use the SAML-based SSO Admin Console configuration. For agency customer PKI-based authentication, agency customers should (a) validate certificates by constructing a certification path with status information to an accepted trust anchor, (b) enforce authorized access to the corresponding private key and (c) map the authenticated identity to the user account, d) Implement a local cache of revocation data to support path discovery and validation in case of inability to access revocation information via the network

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Key Management Service \- Manage, generate, use, rotate, and destroy AES256, RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 cryptographic keys on Google Cloud  
[https://cloud.google.com/kms/](https://cloud.google.com/kms/) 

Google Trust Services \- The Google Public Key Infrastructure (“Google PKI”) enables reliable and secure identity authentication and facilitates the preservation of confidentiality and integrity of data in electronic transactions. Note: This is not a GCP product.  
[https://pki.goog/](https://pki.goog/) 

### IA-5 (11)

**Control Description:** The information system, for hardware token-based authentication, employs mechanisms that satisfy organization-defined token quality requirements.

Supplemental Guidance:  Hardware token-based authentication typically refers to the use of PKI-based tokens, such as the U.S. Government Personal Identity Verification (PIV) card. Organizations define specific requirements for tokens, such as working with a particular PKI.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

Customers are responsible for managing all aspects of authentication for customer users of GCP, including employing hardware tokens that satisfy customer requirements. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Best Practice: Enforce MFA / 2SV for privileged GCP users via Titan Security Keys ([https://cloud.google.com/titan-security-key](https://cloud.google.com/titan-security-key)) as additional hardware authentication in the cloud.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/)   

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

### IA-6

**Control Description:** The information system obscures feedback of authentication information during the authentication process to protect the information from possible exploitation/use by unauthorized individuals.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Customers are responsible for managing all aspects of authentication for customer users of GCP, including ensuring that authenticator feedback is obscured during the customer authentication process. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Workspace Consideration(s):  
The agency should ensure that SAML assertions sent to Google are secured during transmission to protect information from possible exploitation/use by unauthorized individuals.

Google uses encryption in transit with TLS by default from end users (the Internet) to all Google Services.

Best Practice: Implement Dedicated Interconnect to isolate your organization's data and traffic from the public internet (link)  
Best Practice: Configure Cloud VPN to further protect information in transit (link)  
Best Practice: Leverage Cloud KMS to encrypt data with symmetric and asymmetric encryption keys (link)

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Google Cloud Console \- FedRAMP compliant, integrated management console for GCP. Secure administrative interface for to connect to all GCP resources and services.  
[https://cloud.google.com/cloud-console/](https://cloud.google.com/cloud-console/) 

Google Application Layer Transport Security \- Google’s Application Layer Transport Security (ALTS) is a mutual authentication and transport encryption system typically used for securing Remote Procedure Call (RPC) communications within Google’s infrastructure. Note: This is not a GCP product.  
[https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security/](https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security/) 

Google Infrastructure Security \- Whitepaper that gives an overview of Google's infrastructure security for hardware, services, user identity, storage, communications, and operations. Note: This is not a GCP product.  
https://cloud.google.com/security/infrastructure/design/resources/google\_infrastructure\_whitepaper\_fa.pdf?utm\_medium=et\&utm\_source=google.com%2Fcloud\&utm\_campaign=multilayered\_security\&utm\_content=download\_the\_whitepaper   

### IA-7

**Control Description:** The information system implements mechanisms for authentication to a cryptographic module that meet the requirements of applicable federal laws, Executive Orders, directives, policies, regulations, standards, and guidance for such authentication.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Customers are responsible for managing all aspects of authentication for customer users of GCP. This may be achieved by using a customer managed, SAML-based, Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Customers are responsible for implementing mechanisms for authentication that meet all applicable requirements for such authentication. Additionally, customers are required to ensure that customer machines connecting to Google Cloud are configured to use appropriate encryption for Google-to-agency communications.

Workspace Consideration(s):  
Customer agencies are responsible for configuring their client-side browsers and connections on applicable workstations, servers, and mobile devices to enable connections using encryption. Customers should enforce USGCB settings on government furnished workstations to establish connections with FIPS-approved ciphers.

Google uses BoringSSL (a Google-maintained TLS implementation with FIPS 140-2 Level 1 validated BoringCrypto (link)  
Best Practice:Leverage Cloud KMS and/or Cloud HSM to create, enforce, manage, and protect cryptographic keys in the cloud in alignment with FIPS 140-2 Level 3 (link)

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Key Management Service \- Manage, generate, use, rotate, and destroy AES256, RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 cryptographic keys on Google Cloud  
[https://cloud.google.com/kms/](https://cloud.google.com/kms/) 

Cloud HSM \- Protect your encryption keys in the cloud using a fully hosted, FIPS 140-2 Level 3 compliant hardware security model  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/) 

### IA-8

**Control Description:** The information system uniquely identifies and authenticates non-organizational users (or processes acting on behalf of non-organizational users).

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Out of scope of landing zone. Customer managed SSO system. 

The Landing Zone template deploys an organizational policy to enforce domain restricted sharing. This will only allow directory IDs within the allowed domain list as a GCP IAM entity, effectively blocking all other organizational accounts, such as and not limited to Gmail accounts.

#### Implementation Recommendations

Customers are responsible for managing all aspects of authentication for customer users of GCP. This includes uniquely identifying and authenticating non-organizational customer users (or processes acting on behalf of non-organizational customer users). This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Workspace Consideration(s):  
The agency should enable/disable the public/private settings for each application in Admin Console in accordance with agency specifications.

Optional Best Practice: Implement Cloud IAP ([https://cloud.google.com/iap](https://cloud.google.com/iap)) to guard access to applications and VMs \- Project/App Owners

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/)

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/) 

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

### IA-8 (1)

**Control Description:** The information system accepts and electronically verifies Personal Identity Verification (PIV) credentials from other federal agencies.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

This control is not applicable to GCP as GCP does not directly accept or verify Government customer PIV credentials. GCP accepts SAML assertions to authenticate users that have authenticated to a customer authentication system via PIV.

Customers are responsible for managing all aspects of authentication for customer users of GCP, including accepting and electronically verifying PIV credentials in their agency authentication systems for customer users. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Workspace Consideration(s):  
Agency customers should configure and use SAML-based SSO to authenticate to Workspace services, which allows them to inherit second factor authenticators implemented at their agency, such as PIV. The agency should consider employing automated mechanisms such as LDAP, SSO, etc to support the management of Workspace.

### IA-8 (2)

**Control Description:** The information system accepts only FICAM-approved third-party credentials.

Supplemental Guidance: Third-party credentials are those credentials issued by nonfederal government entities approved by the Federal Identity, Credential, and Access Management (FICAM) Trust Framework Solutions initiative. Approved third-party credentials meet or exceed the set of minimum federal government-wide technical, security, privacy, and organizational maturity requirements.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

This control is not applicable to GCP as GCP does not directly accept or verify Government customer FICAM credentials. GCP accepts SAML assertions to authenticate users that have authenticated to a customer authentication system via FICAM approved third-party credentials.

Customers are responsible for managing all aspects of authentication for customer users of GCP. This includes accepting only FICAM-approved third party credentials in their agency authentication systems for customer users. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Workspace Consideration(s):  
If customer domain administrators provision access to their Workspace domain to non-organizational users, agencies are responsible for accepting only FICAM-approved third party credentials and configuring Single Sign-On using SAML 2.0 or Web SSO to inherit their agency's authentication controls

### IA-8 (4)

**Control Description:** The information system conforms to FICAM-issued profiles.

Supplemental Guidance: FICAM-issued implementation profiles of approved protocols (e.g., FICAM authentication protocols such as SAML 2.0 and OpenID 2.0, as well as other protocols such as the FICAM Backend Attribute Exchange).

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

This control is not applicable to GCP as GCP does not directly accept or verify Government customer FICAM credentials. GCP accepts SAML assertions to authenticate users that have authenticated to a customer authentication system via FICAM approved third-party credentials.

Customer Responsibility:  
Customers are responsible for managing all aspects of authentication for customer users of GCP. This includes conforming to FICAM-issued profiles in their agency authentication systems for customer users. This may be achieved by using a customer managed SAML-based Single Sign-On system and synchronizing this system with GCP via Google Cloud Directory Sync.

Workspace Consideration(s):  
If customer domain administrators provision access to their Workspace domain to non-organizational users, agencies are responsible for accepting only FICAM-approved third party credentials and configuring Single Sign-On using SAML 2.0 or Web SSO to inherit their agency's authentication controls

Best Practices: Enable Single Sign On for your organization to manage access to cloud apps / SaaS ([https://cloud.google.com/identity/solutions/enable-sso](https://cloud.google.com/identity/solutions/enable-sso))

## undefined (RA)

### RA-5 (5)

**Control Description:** The information system implements privileged access authorization to operating systems / web applications / database for all vulnerability scanning activities.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

The CUSTOMER is responsible for implementing access authorization to operating systems / web applications / database for all vulnerability scanning activities.

## System and Communications Protection (SC)

### SC-2

**Control Description:** The information system separates user functionality (including user interface services) from information system management functionality.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Customer responsibility. 

Applications and information/data are not present in the solution (it is an infrastructure only solution) prior to client workload onboarding. Any policies needed for application partitioning would be the responsibility of the application/information/data owner and addressed in their response to this control.

#### Implementation Recommendations

The customer is responsible for  separating user functionality from information system management functionality.

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/)

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/) 

Google Workspace \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://workspace.google.com/](https://workspace.google.com/) 

### SC-4

**Control Description:** The information system prevents unauthorized and unintended information transfer via shared system resources.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

The CUSTOMER is responsible for preventing unauthorized and unintended information transfer via shared system resources.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

VPC Service Controls \- A VPC feature to protect sensitive data in Google Cloud Platform services using security perimeters.  
[https://cloud.google.com/vpc-service-controls/](https://cloud.google.com/vpc-service-controls/)

Private Google Access \-A component of Cloud VPC used to securely access Google services and 3rd party SaaS from on-premise to the cloud, using Cloud Interconnect or VPN  
[https://cloud.google.com/vpc/docs/private-access-options](https://cloud.google.com/vpc/docs/private-access-options)

Context Aware Access \- A feature of Cloud IAP that allows you to manage access to apps and infrastructure based on a user’s identity and context.  
[https://cloud.google.com/context-aware-access/](https://cloud.google.com/context-aware-access/)

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/)

### SC-5 \- SYSTEM AND COMMUNICATIONS PROTECTION

**Control Description:** The information system protects against or limits the effects of organization-defined types of denial of service attacks or reference to source for such information by employing organization-defined security safeguards.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The GCP infrastructure (GCP console, APIs, etc.) is protected by the Google Front End service ([https://cloud.google.com/docs/security/infrastructure/design](https://cloud.google.com/docs/security/infrastructure/design))

Google Cloud Armor Helps protect your applications and websites against denial of service and web attacks.

Client applications can make use of Google Cloud Armour within the solution infrastructure to provide application level DoS protection. A portion of this control would be addressed in the client application security assessment

Customers have to deploy Cloud Armor for additional default protection in the form of ML based L7 DDoS attack mitigation, OWASP top 10, LB attacks and Bot management via reCAPTCHA

#### Implementation Recommendations

Customers are responsible for ensuring that their information systems resources built on GCP are protected against or limits the effects of denial of service attacks. Customer VMs are not behind the Google Front End (GFE) and require additional protection from DDOS attacks. Customers may elect to use the GCP multi-region load balancer in the Compute Engine product to get DDoS protection from Google; enable Google Cloud HTTP(s) and SSL proxy load balancing for their GCE instances to mitigate DDoS attacks; enable Cloud Armor for HTTP(s) load balancers or GKE; or purchase and configure another commercial product. Google Cloud Load balancers can handle a sudden spike in traffic by distributing the traffic across all the back ends with available capacity.

GCP provides native network security and denial of service protection using Google Front Ends (GFEs). GFEs terminate traffic for incoming HTTP(S), TCP and TLS proxy traffic, provides DDoS attack countermeasures, and routes and load balances traffic to Google Cloud services ([https://cloud.google.com/security/encryption-in-transit\#how\_traffic\_gets\_routed](https://cloud.google.com/security/encryption-in-transit#how_traffic_gets_routed)).  
Best Practice: Configure Cloud Armor to further protect your services against denial of service and web attacks ([https://cloud.google.com/armor](https://cloud.google.com/armor)). Configure Cloud Armor security policies to filter incoming traffic ([https://cloud.google.com/armor/docs/configure-security-policies](https://cloud.google.com/armor/docs/configure-security-policies)).

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Armor \- Protect your infrastructure and web applications from Distributed Denial of Service (DDoS) attacks  
[https://cloud.google.com/armor/](https://cloud.google.com/armor/)

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

Google Cloud Load Balancing \- Implement global network autoscaling, HTTP(S), TCP, SSL, and Internal Load Balancing   
[https://cloud.google.com/load-balancing/](https://cloud.google.com/load-balancing/)

VPC Service Controls \- A VPC feature to protect sensitive data in Google Cloud Platform services using security perimeters.  
[https://cloud.google.com/vpc-service-controls/](https://cloud.google.com/vpc-service-controls/)

### SC-6

**Control Description:** The information system protects the availability of resources by allocating organization-defined resources by priority or quota, and organization-defined security safeguards.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

The CUSTOMER is responsible for  protecting against or limits the effects of organization-defined types of denial of service attacks or reference to source for such information by employing organization-defined security safeguards.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Resource Manager \- Hierarchically manage resources by project, folder, and organization. Centrally control org & access policies and asset inventories. Label resources for better management.   
[https://cloud.google.com/resource-manager/](https://cloud.google.com/resource-manager/)

Google Cloud Storage \- Object storage with global edge-caching. Multi-regional, regional, nearline \- low frequency access, and coldline \- archive storage options.   
[https://cloud.google.com/storage/](https://cloud.google.com/storage/)

Managed Instance Groups \- Maintain high availability of your apps by proactively keeping your instances in a RUNNING state. Managed instance groups support autoscaling, load balancing, rolling updates, autohealing.  
[https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances](https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances)

Global, Regional, Zonal Resources \- Build in high availability by leveraging global, zonal, and regional Google Cloud resources. Note: This is not a GCP Product  
[https://cloud.google.com/compute/docs/regions-zones/global-regional-zonal-resources](https://cloud.google.com/compute/docs/regions-zones/global-regional-zonal-resources)

Google Cloud Resource Quotas \- Manage your GCP rate quotas for API requests and resource allocation quotas. Note: This is not a GCP Product  
[https://cloud.google.com/docs/quota](https://cloud.google.com/docs/quota)

### SC-7

**Control Description:** The information system:

 a. Monitors and controls communications at the external boundary of the system and at key internal boundaries within the system;

 b. Implements subnetworks for publicly accessible system components that are physically and logically separated from internal organizational networks; and

 c. Connects to external networks or information systems only through managed interfaces consisting of boundary protection devices arranged in accordance with an organizational security architecture.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The VPC network allows for incoming and outgoing firewall rules to allow or limit the flow of information based on layer 4 IPs or Ports.

Network and resource configuration is defined in 3-networks-hub-and-spoke. This LZ uses Fortigate devices as front end devices, this is defined in 7-fortigate. 

Boundary protection provided by VPC service controls, Private Google Access and 1p or 3p NGFW.  

Access Context Manager (ACM) helps in securing your Google Cloud resources by providing a framework for defining and enforcing fine-grained access control policies based on various contextual attributes. 

Refer to Architecture ([https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md\#system-architecture-high-level-workload-overview](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md#system-architecture-high-level-workload-overview))

#### Resource Definitions

* \- 3-networks-hub-and-spoke/modules/base\_env \- defines network architecture and network flog log configuration  
* \- 3-networks-hub-and-spoke/modules/restricted\_shared\_vpc/service\_control.tf \- defines access policies and membership  
* \- 7-fortigate \- front end device definition

#### Org Policies

* SC-7        compute.restrictVpcPeering: Enables you to implement network segmentation and control the flow of information within your GCP environment. \- Enables you to implement network segmentation and control the flow of information within your GCP environment.  
* SC-7, SC-8        compute.vmCanIpForward: This permission controls whether a VM instance can act as a network router, forwarding IP packets between different network interfaces. Enabling IP forwarding on a VM essentially turns it into a router, which can have significant security implications.  \- This permission controls whether a VM instance can act as a network router, forwarding IP packets between different network interfaces. Enabling IP forwarding on a VM essentially turns it into a router, which can have significant security implications. 

#### Implementation Recommendations

Part a:  
Customers are responsible for ensuring that their GCP customer systems resources are connected to external network systems through managed interfaces that are consistent with organization's security architecture. Not all user and application traffic is monitored by Google. Applications hosted on GCP may bypass the GFE if they are using Cloud VPN, Cloud Interconnect, or a single instance VM (since it uses a public IP address by default). Customers can segment their networks with global distributed firewalls to restrict access to certain instances.

Part b:  
Customers are responsible for ensuring that their GCP information systems resources are connected to external network systems only through managed interfaces. Customer VMs have public IPs and can connect to the Internet by default. Customers may elect to use the Virtual Private Cloud located in the Networking product. Customers can provision GCP resources segmenting their networks with a global distributed firewalls to restrict access to certain instances.

Part c:  
Customers are responsible for ensuring that their GCP customer systems resources are connected to external network systems through managed interfaces that are consistent with organization's security architecture. Not all user and application traffic is monitored by Google. Applications hosted on GCP may bypass the GFE if they are using Cloud VPN, Cloud Interconnect, or a single instance VM (since it uses a public IP address by default). Customers can segment their networks with a global distributed firewalls to restrict access to certain instances.

Best Practice: Implement VPC Service Controls ([https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters](https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters)) to block external access to services protected by the perimeter.  
Best Practice: Enable VPC Flow Logs ([https://cloud.google.com/vpc/docs/using-flow-logs](https://cloud.google.com/vpc/docs/using-flow-logs)) to monitor network traffic sent to/from VM instances  
Best Practice: It may be useful to turn on Data Access audit logs for the specific system components managed by the system owners, to further log resource access ([https://cloud.google.com/logging/docs/audit\#admin-activity](https://cloud.google.com/logging/docs/audit#admin-activity))

#### Service Notes

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

VPC Service Controls \- A VPC feature to protect sensitive data in Google Cloud Platform services using security perimeters.  
[https://cloud.google.com/vpc-service-controls/](https://cloud.google.com/vpc-service-controls/)

Private Google Access \-A component of Cloud VPC used to securely access Google services and 3rd party SaaS from on-premise to the cloud, using Cloud Interconnect or VPN  
[https://cloud.google.com/vpc/docs/private-access-options](https://cloud.google.com/vpc/docs/private-access-options)

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)

### SC-7 (5)

**Control Description:** The information system at managed interfaces denies network communications traffic by default and allows network communications traffic by exception (i.e., deny all, permit by exception).

Supplemental Guidance:  This control enhancement applies to both inbound and outbound network communications traffic. A deny-all, permit-by-exception network communications traffic policy ensures that only those connections which are essential and approved are allowed.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The VPC network allows for incoming and outgoing firewall rules to allow or limit the flow of information based on layer 4 IPs or Ports.

The Landing Zone template has a default deny posture for the VPC firewall rules; a rule match must exist to allow for traffic to traverse the VPC. The ingress/egress to the environment is restricted via the perimeter project and VPC. Traffic is blocked by default, and specific rules must be created to allow communication ([https://cloud.google.com/vpc/docs/vpc\#communications\_and\_access](https://cloud.google.com/vpc/docs/vpc#communications_and_access))

Network and resource configuration is defined in 3-networks-hub-and-spoke. This LZ uses Fortigate devices as front end devices, this is defined in 7-fortigate. 

Boundary protection provided by VPC service controls, Private Google Access and 1p or 3p NGFW. 

Refer to Architecture ([https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md\#system-architecture-high-level-workload-overview](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md#system-architecture-high-level-workload-overview))

#### Resource Definitions

* \- 3-networks-hub-and-spoke/modules/base\_env \- defines network architecture and network flog log configuration  
* \- 3-networks-hub-and-spoke/modules/base\_shared\_vpc \- defines egress deny-all by default  
* \- 7-fortigate \- front end device definition

#### Org Policies

* SC-7        compute.restrictVpcPeering: Enables you to implement network segmentation and control the flow of information within your GCP environment. \- Enables you to implement network segmentation and control the flow of information within your GCP environment.  
* SC-7, SC-8        compute.vmCanIpForward: This permission controls whether a VM instance can act as a network router, forwarding IP packets between different network interfaces. Enabling IP forwarding on a VM essentially turns it into a router, which can have significant security implications.  \- This permission controls whether a VM instance can act as a network router, forwarding IP packets between different network interfaces. Enabling IP forwarding on a VM essentially turns it into a router, which can have significant security implications. 

#### Implementation Recommendations

Customers are responsible for implementing a deny all; permit by exception policy at their managed interfaces.

Optional Best Practice: Verify and/or enable firewall rules logging ([https://cloud.google.com/vpc/docs/firewall-rules-logging](https://cloud.google.com/vpc/docs/firewall-rules-logging)) to audit, verify, and analyze the effects of your firewall rules.  
Best Practice: Implement VPC Service Controls ([https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters](https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters)) to block external access to services protected by the perimeter.  
Best Practice: Enable VPC Flow Logs ([https://cloud.google.com/vpc/docs/using-flow-logs](https://cloud.google.com/vpc/docs/using-flow-logs)) to monitor network traffic sent to/from VM instances \- App/Project Owner function

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

### SC-7 (7)

**Control Description:** The information system, in conjunction with a remote device, prevents the device from simultaneously establishing non-remote connections with the system and communicating via some other connection to resources in external networks.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Cloud VPN services, along with device-level configurations, prevent split tunneling for remote devices. Identity Aware Proxy enforces granular access controls based on user identity and context, such as device security status, location, and network.

All connections by devices to solution resources are remote; there are no direct (non-local) connections possible as Google does not permit direct (local) connections to GCP

#### Resource Definitions

* \- 3-networks-dual-svpc/modules/vpn-ha \- A sample configuration for VPN is provided.   
* \- 4-projects/modules/base\_env/example\_peering\_project.tf \- Sample IAP firewall rules.  IAP resources are not created by default. 

#### Org Policies

* SC-7        compute.restrictVpcPeering: Enables you to implement network segmentation and control the flow of information within your GCP environment.   
* SC-7, SC-8        compute.vmCanIpForward: This permission controls whether a VM instance can act as a network router, forwarding IP packets between different network interfaces. Enabling IP forwarding on a VM essentially turns it into a router, which can have significant security implications. 

#### Implementation Recommendations

The CUSTOMER is responsible for preventing the device from simultaneously establishing non-remote connections with the system and communicating via some other connection to resources in external networks.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

VPC Service Controls \- A VPC feature to protect sensitive data in Google Cloud Platform services using security perimeters.  
[https://cloud.google.com/vpc-service-controls/](https://cloud.google.com/vpc-service-controls/)

Private Google Access \- A component of Cloud VPC used to securely access Google services and 3rd party SaaS from on-premise to the cloud, using Cloud Interconnect or VPN  
[https://cloud.google.com/vpc/docs/private-access-options](https://cloud.google.com/vpc/docs/private-access-options)

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/)

### SC-7 (8)

**Control Description:** The information system routes organization-defined internal communications traffic to organization-defined external networks through authenticated proxy servers at managed interfaces.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The VPC network allows for incoming and outgoing firewall rules to allow or limit the flow of information based on layer 4 IPs or Ports.

Network and resource configuration is defined in 3-networks-hub-and-spoke. This LZ uses Fortigate devices as front end devices, this is defined in 7-fortigate. 

Boundary protection provided by VPC service controls, Private Google Access and 1p or 3p NGFW. 

Refer to Architecture ([https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md\#system-architecture-high-level-workload-overview](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md#system-architecture-high-level-workload-overview))

#### Resource Definitions

* \- 3-networks-hub-and-spoke/modules/base\_env \- defines network architecture and network flog log configuration  
* \- 3-networks-hub-and-spoke/modules/base\_shared\_vpc \- defines egress deny-all by default  
* \- 7-fortigate \- front end device definition

#### Org Policies

* SC-7        compute.restrictVpcPeering: Enables you to implement network segmentation and control the flow of information within your GCP environment.   
* SC-7, SC-8        compute.vmCanIpForward: This permission controls whether a VM instance can act as a network router, forwarding IP packets between different network interfaces. Enabling IP forwarding on a VM essentially turns it into a router, which can have significant security implications. 

#### Implementation Recommendations

Customers are responsible for managing authenticated proxy servers at customer managed interfaces. Proxy servers should be configured to route internal and external traffic in agreement with Agency requirements.

Google Front Ends (GFEs) are globally distributed to proxy traffic incoming to Google Services ([https://cloud.google.com/security/encryption-in-transit\#how\_traffic\_gets\_routed](https://cloud.google.com/security/encryption-in-transit#how_traffic_gets_routed)).  
Best Practice: Configure Cloud Armor to further protect your services against denial of service and web attacks ([https://cloud.google.com/armor](https://cloud.google.com/armor)). Configure Cloud Armor security policies to filter incoming traffic ([https://cloud.google.com/armor/docs/configure-security-policies](https://cloud.google.com/armor/docs/configure-security-policies)).  
Best Practice: Configure Google Load Balancer(s) to help route and manage global, regional, external and internal traffic ([https://cloud.google.com/load-balancing/docs/choosing-load-balancer](https://cloud.google.com/load-balancing/docs/choosing-load-balancer)).

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

VPC Service Controls \- A VPC feature to protect sensitive data in Google Cloud Platform services using security perimeters.  
[https://cloud.google.com/vpc-service-controls/](https://cloud.google.com/vpc-service-controls/)

Private Google Access \- A component of Cloud VPC used to securely access Google services and 3rd party SaaS from on-premise to the cloud, using Cloud Interconnect or VPN  
[https://cloud.google.com/vpc/docs/private-access-options](https://cloud.google.com/vpc/docs/private-access-options)

Cloud Identity Aware Proxy \- Use identity and context to guard access to your applications and VMs.  
[https://cloud.google.com/iap/](https://cloud.google.com/iap/)

### SC-7 (18)

**Control Description:** The information system fails securely in the event of an operational failure of a boundary protection device.  
   
Supplemental Guidance: Failures of boundary protection devices cannot lead to, or cause information external to the devices to enter the devices, nor can failures permit unauthorized information releases.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The VPC network allows for incoming and outgoing firewall rules to allow or limit the flow of information based on layer 4 IPs or Ports.

Network and resource configuration is defined in 3-networks-hub-and-spoke. This LZ uses Fortigate devices as front end devices, this is defined in 7-fortigate. 

Boundary protection provided by VPC service controls, Private Google Access and 1p or 3p NGFW. 

Refer to Architecture ([https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md\#system-architecture-high-level-workload-overview](https://github.com/GoogleCloudPlatform/pbmm-on-gcp-onboarding/blob/main/docs/architecture.md#system-architecture-high-level-workload-overview))

#### Resource Definitions

* \- 3-networks-hub-and-spoke/modules/base\_env \- defines network architecture and network flog log configuration  
* \- 3-networks-hub-and-spoke/modules/base\_shared\_vpc \- defines egress deny-all by default  
* \- 7-fortigate \- front end device definition

#### Org Policies

* SC-7        compute.restrictVpcPeering: Enables you to implement network segmentation and control the flow of information within your GCP environment.   
* SC-7, SC-8        compute.vmCanIpForward: This permission controls whether a VM instance can act as a network router, forwarding IP packets between different network interfaces. Enabling IP forwarding on a VM essentially turns it into a router, which can have significant security implications. 

#### Implementation Recommendations

Customers are responsible for configuring all customer managed boundary protection devices to fail in a secure state.

Best Practice: Implement Cloud Interconnect and Cloud Load Balancing for networking DR capabilities and high availability ([https://cloud.google.com/solutions/dr-scenarios-building-blocks\#networking\_and\_data\_transfer](https://cloud.google.com/solutions/dr-scenarios-building-blocks#networking_and_data_transfer)). 

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

### SC-8

**Control Description:** The information system protects the confidentiality and integrity of transmitted information.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

All communication to Google resources is via TLS 1.2 or above (https is specified for all connection strings, and Google Consoles all redirect http to https automatically) providing confidentiality and integrity of information in transit. Organization managed desktops are mandated for access which are configured with up-to-date browser versions and ciphers.

All communication to Azure DevOps (repo) and Entra ID is via TLS 1.2 or above.

VPC Service Controls are configured to block external access to services protected by the perimeter.  
VPC Flow Logs are configured to monitor network traffic sent to/from VM instances  
Audit logs are configured for the specific system components managed by the system owners, to further log resource access.

#### Org Policies

* SC-7, SC-8        compute.vmCanIpForward: This permission controls whether a VM instance can act as a network router, forwarding IP packets between different network interfaces. Enabling IP forwarding on a VM essentially turns it into a router, which can have significant security implications.   
* SC-8        compute.restrictLoadBalancerCreationForTypes:  This permission allows you to restrict the types of load balancers that can be created in your project. This helps prevent unauthorized or accidental creation of load balancers that could expose your services to unnecessary risks or attacks.  
* SC-8        compute.requireTlsForLoadBalancers: This constraint enforces the use of Transport Layer Security (TLS) for communication with load balancers in GCP. It aligns with several key principles and controls outlined in NIST.

#### Implementation Recommendations

Part a:  
Customers are responsible for ensuring that their GCP customer systems resources are connected to external network systems through managed interfaces that are consistent with organization's security architecture. Not all user and application traffic is monitored by Google. Applications hosted on GCP may bypass the GFE if they are using Cloud VPN, Cloud Interconnect, or a single instance VM (since it uses a public IP address by default). Customers can segment their networks with global distributed firewalls to restrict access to certain instances.

Part b:  
Customers are responsible for ensuring that their GCP information systems resources are connected to external network systems only through managed interfaces. Customer VMs have public IPs and can connect to the Internet by default. Customers may elect to use the Virtual Private Cloud located in the Networking product. Customers can provision GCP resources segmenting their networks with a global distributed firewalls to restrict access to certain instances.

Part c:  
Customers are responsible for ensuring that their GCP customer systems resources are connected to external network systems through managed interfaces that are consistent with organization's security architecture. Not all user and application traffic is monitored by Google. Applications hosted on GCP may bypass the GFE if they are using Cloud VPN, Cloud Interconnect, or a single instance VM (since it uses a public IP address by default). Customers can segment their networks with a global distributed firewalls to restrict access to certain instances.

Best Practice: Implement VPC Service Controls ([https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters](https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters)) to block external access to services protected by the perimeter.  
Best Practice: Enable VPC Flow Logs ([https://cloud.google.com/vpc/docs/using-flow-logs](https://cloud.google.com/vpc/docs/using-flow-logs)) to monitor network traffic sent to/from VM instances  
Best Practice: It may be useful to turn on Data Access audit logs for the specific system components managed by the system owners, to further log resource access ([https://cloud.google.com/logging/docs/audit\#admin-activity](https://cloud.google.com/logging/docs/audit#admin-activity))

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/)   

Cloud CDN \- Low latency, low cost content delivery network. Leverages Google's globally distributed edge points of presence to accelerate content delivery for websites and applications served out of Google Compute Engine and Google Cloud Storage. Secures content using SSL/TLS.  
[https://cloud.google.com/cdn/](https://cloud.google.com/cdn/)

### SC-8 (1)

**Control Description:** The information system implements cryptographic mechanisms to prevent unauthorized disclosure of information and detect changes to information during transmission unless otherwise protected by a hardened or alarmed carrier Protective Distribution System (PDS).

Supplemental Guidance: Encrypting information for transmission protects information from unauthorized disclosure and modification. Cryptographic mechanisms implemented to protect information integrity include, for example, cryptographic hash functions which have common application in digital signatures, checksums, and message authentication codes. Alternative physical security safeguards include, for example, protected distribution systems.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

All communication to Google resources is via TLS 1.2 or above (https is specified for all connection strings, and Google Consoles all redirect http to https automatically) providing confidentiality and integrity of information in transit. Organization managed desktops are mandated for access which are configured with up-to-date browser versions and ciphers.

All communication to Azure DevOps (repo) and Entra ID is via TLS 1.2 or above.

GCP incorporates default L4 encryption in transit between all google services. L7 encryption is available.

#### Org Policies

* SC-7, SC-8        compute.vmCanIpForward: This permission controls whether a VM instance can act as a network router, forwarding IP packets between different network interfaces. Enabling IP forwarding on a VM essentially turns it into a router, which can have significant security implications.   
* SC-8 compute.restrictLoadBalancerCreationForTypes:  This permission allows you to restrict the types of load balancers that can be created in your project. This helps prevent unauthorized or accidental creation of load balancers that could expose your services to unnecessary risks or attacks.   
* SC-8 compute.requireTlsForLoadBalancers: This constraint enforces the use of Transport Layer Security (TLS) for communication with load balancers in GCP. It aligns with several key principles and controls outlined in NIST.

#### Implementation Recommendations

Customers are required to ensure that machines connecting to GCP are configured to use appropriate encryption for Google-to-agency communications. It is the responsibility of federal customers to configure their browsers to meet federal encryption standards.

Workspace Considerations:  
Customer agencies are responsible for configuring their client-side browsers and connections on applicable workstations, servers, and mobile devices to enable connections using encryption. Customers should enforce USGCB settings on government furnished workstations to establish connections with FIPS-approved ciphers.

Google uses encryption in transit with TLS ([https://cloud.google.com/security/encryption-in-transit\#encryption\_in\_transit\_by\_default](https://cloud.google.com/security/encryption-in-transit#encryption_in_transit_by_default)) by default from end users (the Internet) to all Google Services. If not already configured, enable Cloud KMS encryption for data managed by the system owners (e.g. audit logs/GCS buckets).  
Best Practice: Implement Dedicated Interconnect to isolate your organization's data and traffic from the public internet ([https://cloud.google.com/interconnect/docs/concepts/overview](https://cloud.google.com/interconnect/docs/concepts/overview))   
Best Practice: Configure Cloud VPN to further protect information in transit ([https://cloud.google.com/vpn/docs/concepts/overview](https://cloud.google.com/vpn/docs/concepts/overview))   
Best Practice: Leverage Cloud KMS to encrypt data with symmetric and asymmetric encryption keys ([https://cloud.google.com/kms/docs/encrypt-decrypt](https://cloud.google.com/kms/docs/encrypt-decrypt))

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Key Management Service \- Manage, generate, use, rotate, and destroy AES256, RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 cryptographic keys on Google Cloud  
[https://cloud.google.com/kms/](https://cloud.google.com/kms/)

Cloud HSM \- Protect your encryption keys in the cloud using a fully hosted, FIPS 140-2 Level 3 compliant hardware security model  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/) 

Google Managed SSL Certificates \- A Cloud Load Balancing feature; Google-managed SSL certificates are provisioned, renewed, and managed for your domain names.  
[https://cloud.google.com/load-balancing/docs/ssl-certificates](https://cloud.google.com/load-balancing/docs/ssl-certificates)

Customer Managed SSL Certificates \- A Cloud Load Balancing feature; Provide your own SSL certificates to manage secure access to your GCP domains. Self-managed certificates can support wildcards and multiple subject alternative names (SANs).  
[https://cloud.google.com/load-balancing/docs/ssl-certificates\#working-self-managed](https://cloud.google.com/load-balancing/docs/ssl-certificates#working-self-managed)

Shielded VMs \- Shielded VM offers verifiable integrity of your Compute Engine VM instances, so you can be confident your instances haven't been compromised by boot- or kernel-level malware or rootkits. Shielded VM's verifiable integrity is achieved through the use of Secure Boot, virtual trusted platform module (vTPM)-enabled Measured Boot, and integrity monitoring.  
[https://cloud.google.com/security/shielded-cloud/shielded-vm](https://cloud.google.com/security/shielded-cloud/shielded-vm)

### SC-10

**Control Description:** The information system terminates the network connection associated with a communications session at the end of the session or after no longer than 30 minutes for RAS-based sessions or no longer than 60 minutes for non-interactive user sessions of inactivity.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Given the SAML and transactional nature of HTTPS and API calls there are no specific "sessions" to terminate. Account reauthentication is required every 16 hours ([https://cloud.google.com/blog/products/identity-security/improve-security-posture-with-time-bound-session-length](https://cloud.google.com/blog/products/identity-security/improve-security-posture-with-time-bound-session-length)) which serves a similar purpose and will satisfy this control.

Out of scope of landing zone. Customer managed SSO system.

#### Implementation Recommendations

Google Workspace Consideration(s):  
Google Workspace Enterprise and Business Customers can configure a Google Session Termination duration (cookie lifetime) as short as one (1) hour (https://support.google.com/a/answer/7576830?hl=en). It should be noted that in order for these settings to take effect, Agency users must log out and log back in to initiate the new session duration enforcement. It is also possible for Agency Administrators to manually reset a user’s sign-in cookies for each user (https://support.google.com/a/answer/178854?hl=en). Agencies that decide to implement a session termination duration shorter than one (1) hour should implement SAML-based SSO as well as USGCB for agency workstation/laptops that will timeout the user at the workstation/laptop level after a period of inactivity specified by the agency.  
Agency customers should log out of Chrome Sync on browsers and devices which they are no longer using.

Agency customers are responsible for only logging into Chrome Sync via their agency account, on their agency issued device and only doing agency work while signed in to their agency account to prevent accidental flow of information to other accounts.

GSA has accepted the Alternative Implementation statement below (See Attachment 14, \#42): POA\&M \#39 \- This Alternative Implementation has been accepted by GSA.

Agencies should implement SAML-based SSO as well as USGCB for agency workstation/laptops that will timeout the user at the workstation/laptop level after a period of inactivity specified by the agency.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Connection Draining \- A Cloud Load Balancing feature; You can enable connection draining on backend services. To enable connection draining, you set a connection draining timeout on the backend service. This timeout instructs the backend service to gracefully migrate traffic away from VM instances in its backends.  
[https://cloud.google.com/load-balancing/docs/enabling-connection-draining](https://cloud.google.com/load-balancing/docs/enabling-connection-draining)

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/) 

Cloud Shell: Session Limitations \- Non-interactive sessions will be ended automatically after a warning. Cloud shell also has weekly usage limits  
[https://cloud.google.com/shell/docs/limitations](https://cloud.google.com/shell/docs/limitations)

### SC-13

**Control Description:** The information system implements FIPS-validated or NSA-approved cryptography in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

All communication to Google resources is via TLS 1.2 or above (https is specified for all connection strings, and Google Consoles all redirect http to https automatically) providing confidentiality and integrity of information in transit. Organization managed desktops are mandated for access which are configured with up-to-date browser versions and ciphers.

All communication to Azure DevOps (repo) and Entra ID is via TLS 1.2 or above.

GCP incorporates default L4 encryption in transit between all google services. L7 encryption is available.

GCP incorporates default rotated google managed security keys for storage encryption. Customer supplied and customer managed security keys solutions are also available.

Resources:   
\- 2-environments/modules/env\_baseline/kms.tf \- separated key management project

#### Implementation Recommendations

Customers are required to ensure that machines connecting to Google Cloud are configured to use appropriate encryption for Google-to-agency communications.

Workspace Consideration(s)  
To establish an encrypted connection with FIPS 140-2 approved algorithms, customer agencies are responsible for and configuring their client-side browsers and connections on applicable workstations, servers, and mobile devices to enable connections using encryption. Google enforces TLS on all Workspace server to agency customer connections. Customers who enforce USGCB settings on government furnished workstations will achieve strong encryption with FIPS approved algorithms.

Google uses BoringSSL (a Google-maintained TLS implementation) with FIPS 140-2 Level 1 validated BoringCrypto ([https://cloud.google.com/security/encryption-in-transit\#boringssl](https://cloud.google.com/security/encryption-in-transit#boringssl)).  
Google's BoringCrypto Cryptographic Module Security Policy ([https://csrc.nist.gov/csrc/media/projects/cryptographic-module-validation-program/documents/security-policies/140sp2964.pdf](https://csrc.nist.gov/csrc/media/projects/cryptographic-module-validation-program/documents/security-policies/140sp2964.pdf))  
Best Practice: Leverage Cloud KMS and/or Cloud HSM to create, enforce, manage, and protect cryptographic keys in the cloud in alignment with FIPS 140-2 Level 3 ([https://cloud.google.com/kms/docs/hsm](https://cloud.google.com/kms/docs/hsm))

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Cloud Key Management Service \- Manage, generate, use, rotate, and destroy AES256, RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 cryptographic keys on Google Cloud  
[https://cloud.google.com/kms/](https://cloud.google.com/kms/)

Cloud HSM \- Protect your encryption keys in the cloud using a fully hosted, FIPS 140-2 Level 3 compliant hardware security model  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/)

### SC-20

**Control Description:** The information system:

 a. Provides additional data origin and integrity artifacts along with the authoritative name resolution data the system returns in response to external name/address resolution queries; and

 b. Provides the means to indicate the security status of child zones and (if the child supports secure resolution services) to enable verification of a chain of trust among parent and child domains, when operating as part of a distributed, hierarchical namespace.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

Part a:  
Customers are responsible for configuring web browsers to require secure connections when opening connections to GCP. Additionally, customers must configure end user devices to only use trusted DNS servers for handling domain name resolution.

Best Practice: Configure Cloud DNS with managed zones ([https://cloud.google.com/dns/docs/overview](https://cloud.google.com/dns/docs/overview)). Implement DNSSEC ([https://cloud.google.com/dns/docs/dnssec](https://cloud.google.com/dns/docs/dnssec)) to enforce authentication of domain name lookups. When enabled, Cloud DNS logging tracks queries that are resolved by name servers for VPC networks ([https://cloud.google.com/dns/docs/monitoring](https://cloud.google.com/dns/docs/monitoring)).  
Best Practice: Create Private DNS Zones to perform internal DNS resolution for private GCP networks ([https://cloud.google.com/dns/zones\#create-private-zone](https://cloud.google.com/dns/zones#create-private-zone))

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud DNS \- Scalable, reliable, resilient and managed authoritative Domain Name System (DNS) service. Easily publish and manage millions of DNS zones and records.  
[https://cloud.google.com/dns/](https://cloud.google.com/dns/)

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

### SC-21

**Control Description:** The information system requests and performs data origin authentication and data integrity verification on the name/address resolution responses the system receives from authoritative sources.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

Customers are responsible for configuring web browsers to require secure connections when opening connections to GCP. Additionally, customers must configure end user devices to only use trusted DNS servers for handling domain name resolution.

Workspace Consideration(s):  
Google does not provide a DNS as part of our Workspace offering, and the DNS Google uses is not within the scope of the GCI and Workspace authorization boundaries.  
Agencies should perform data origin authentication and data integrity verification on the name/address resolution responses from authoritative sources when requested by client systems.

Security implementations of Google's public DNS ([https://developers.google.com/speed/public-dns/docs/security](https://developers.google.com/speed/public-dns/docs/security)).    
Best Practice: Configure Cloud DNS with managed zones ([https://cloud.google.com/dns/docs/overview](https://cloud.google.com/dns/docs/overview)). Implement DNSSEC ([https://cloud.google.com/dns/docs/dnssec](https://cloud.google.com/dns/docs/dnssec)) to enforce authentication of domain name lookups. When enabled, Cloud DNS logging tracks queries that are resolved by name servers for VPC networks ([https://cloud.google.com/dns/docs/monitoring](https://cloud.google.com/dns/docs/monitoring)).  
Best Practice: Create Private DNS Zones to perform internal DNS resolution for private GCP networks ([https://cloud.google.com/dns/zones\#create-private-zone](https://cloud.google.com/dns/zones#create-private-zone))

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud DNS \- Scalable, reliable, resilient and managed authoritative Domain Name System (DNS) service. Easily publish and manage millions of DNS zones and records.  
[https://cloud.google.com/dns/](https://cloud.google.com/dns/)

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

VPC Service Controls \- A VPC feature to protect sensitive data in Google Cloud Platform services using security perimeters.  
[https://cloud.google.com/vpc-service-controls/](https://cloud.google.com/vpc-service-controls/)

### SC-22

**Control Description:** The information systems that collectively provide name/address resolution service for an organization are fault-tolerant and implement internal/external role separation.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

As part of the solution infrastructure the GCP Cloud DNS component is implemented for use by clients for their workloads. This includes fault-tolerance by default with 100% uptime availability advertised by Google ([https://cloud.google.com/dns](https://cloud.google.com/dns))

The client will configure DNS resolution as part of their application deployment, and would address this control as part of their security assessment

#### Resource Definitions

* \- 3-networks-hub-and-spoke/modules/base\_env/main.tf for base definition of network, service controls, policies and logging  
* \- 3-networks-hub-and-spoke/envs/shared/dns-hub.tf \- dns definition

#### Implementation Recommendations

The customer is responsible for providing systems that collectively provide name/address resolution service for an organization are fault-tolerant and implement internal/external role separation.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud DNS \- Scalable, reliable, resilient and managed authoritative Domain Name System (DNS) service. Easily publish and manage millions of DNS zones and records.  
[https://cloud.google.com/dns/](https://cloud.google.com/dns/)

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/)

### SC-23

**Control Description:** The information system protects the authenticity of communications sessions.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

All communication to Google resources is via TLS 1.2 or above (https is specified for all connection strings, and Google Consoles all redirect http to https automatically) providing confidentiality and integrity of information in transit. Organization managed desktops are mandated for access which are configured with up-to-date browser versions and ciphers.

All communication to Azure DevOps (repo) and Entra ID is via TLS 1.2 or above.

TLS 1.2+ provides the necessary authenticity of communications sessions (by way of certificate authentication) including guarding against man-in-the-middle type attacks, hijacking, etc.

#### Implementation Recommendations

Customers are responsible for configuring web browsers to use an encryption protocol that meets or exceeds Agency requirements. Customers are advised that United States Government Configuration Baseline (USGCB) standard restricts federal desktop client-side TLS handshake initiation to FIPS approved algorithms.

Workspace Considerations:  
Customer agencies are responsible for configuring their client-side browsers and connections on applicable workstations, servers, and mobile devices to enable connections using encryption. Customers should enforce USGCB settings on government furnished workstations to establish connections with FIPS-approved ciphers.

Google uses a custom Application Layer Transport Security (ALTS) ([https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security](https://cloud.google.com/security/encryption-in-transit/application-layer-transport-security)) protocol for authentication and encryption. ALTS performs authentication primarily by identity rather than host, and is similar to mutually authenticated TLS. ALTS does not allow zero round trip time (0-RTT) session resumption/handshakes, relies on a handshake protocol and a record protocol. ALTS is replay-resistant.  
Best Practice: Implement Dedicated Interconnect to isolate your organization's data and traffic from the public internet ([https://cloud.google.com/interconnect/docs/concepts/overview](https://cloud.google.com/interconnect/docs/concepts/overview))  
Best Practice: Configure Cloud VPN to further protect information in transit ([https://cloud.google.com/vpn/docs/concepts/overview](https://cloud.google.com/vpn/docs/concepts/overview))  
Best Practice: Leverage Cloud KMS to encrypt data with symmetric and asymmetric encryption keys ([https://cloud.google.com/kms/docs/encrypt-decrypt](https://cloud.google.com/kms/docs/encrypt-decrypt))

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Google Cloud Security \- Whitepaper covering Google's cloud services security, including Google's security culture, operational security, technology & data center security, data center environmental controls, data security and compliance.  
[https://services.google.com/fh/files/misc/google\_security\_wp.pdf](https://services.google.com/fh/files/misc/google_security_wp.pdf) 

Google Infrastructure Security \- Whitepaper that gives an overview of Google's infrastructure security for hardware, services, user identity, storage, communications, and operations. Note: This is not a GCP Product  
https://cloud.google.com/security/infrastructure/design/resources/google\_infrastructure\_whitepaper\_fa.pdf?utm\_medium=et\&utm\_source=google.com%2Fcloud\&utm\_campaign=multilayered\_security\&utm\_content=download\_the\_whitepaper 

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/)  

### SC-28

**Control Description:** The information system protects the confidentiality and integrity of organization-defined information at rest.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

GCP incorporates default rotated google managed security keys for storage encryption. Customer supplied and customer managed security keys solutions are also available.

Resources:   
\- 2-environments/modules/env\_baseline/kms.tf \- separated key management project

#### Implementation Recommendations

Agencies should evaluate their information storage practices and take measures to protect agency information. Information stored in Google Workspace should be restricted to FIPS 199 High baseline or lower. Agencies should evaluate and implement appropriate cryptographic mechanisms for any data extracted from the Google Workspace service, such as audit logs or other data needed for reporting. There is no prerequisite for external services to be FedRAMP-authorized for inclusion in the Cloud Identity product and Google Workspace's boundary does not extend to these third-party services. As a result, agencies must perform due diligence in authorizing these services prior to establishing third-party authentication via Cloud Identity. Any external services that an agency chooses to manage with Cloud Identity are outside of the scope of the Google Workspace system boundary and must be secured in accordance with agency requirements.

For additional information on configuring Cloud Identity Auto Provisioning relationships, please see the following articles:

Set up SSO with Google as your Identity Provider: https://support.google.com/cloudidentity/topic/7558768?hl=en\&ref\_topic=7558174

Automated user provisioning and deprovisioning: [https://support.google.com/cloudidentity/topic/7661972](https://support.google.com/cloudidentity/topic/7661972)

Set up your own customer SAML application: https://support.google.com/cloudidentity/answer/6087519?hl=en\&ref\_topic=7558947

6Off the record chats are not kept, hence encryption at rest is not applicable. Please see https://support.google.com/chat/answer/29291?hl=en for more information on Hangouts chatting off the record.

7Google allows agency customers the ability to host Google Sites in the following two ways:

Google Sites hosted from custom domains (Please see https://support.google.com/sites/answer/99448?hl=en for more information on custom domains); or,  
Google Sites hosted from a Google domain, such as sites.google.com or sites.google.com/site/.  
Agency customer Google Sites must be hosted on a Google domain to receive the TLS transmission integrity implementation described in the Apps SSP SC-8 Transmission Integrity control. Agency customers should not consider Google Sites SSL during transmission to and from individual users and the Google Sites service to be implemented when an agency customer is hosting Google Sites from a custom domain.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Google Cloud Security \- Whitepaper covering Google's cloud services security, including Google's security culture, operational security, technology & data center security, data center environmental controls, data security and compliance.  
[https://services.google.com/fh/files/misc/google\_security\_wp.pdf](https://services.google.com/fh/files/misc/google_security_wp.pdf) 

Google Infrastructure Security \- Whitepaper that gives an overview of Google's infrastructure security for hardware, services, user identity, storage, communications, and operations. Note: This is not a GCP Product  
[https://cloud.google.com/security/infrastructure/design/resources/google\_infrastructure\_whitepaper\_fa.pdf](https://cloud.google.com/security/infrastructure/design/resources/google_infrastructure_whitepaper_fa.pdf) 

Google Cloud Storage \- Object storage with global edge-caching. Multi-regional, regional, nearline \- low frequency access, and coldline \- archive storage options.   
[https://cloud.google.com/storage/](https://cloud.google.com/storage/)

Cloud Key Management Service \- Manage, generate, use, rotate, and destroy AES256, RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 cryptographic keys on Google Cloud  
[https://cloud.google.com/kms/](https://cloud.google.com/kms/)

Cloud HSM \- Protect your encryption keys in the cloud using a fully hosted, FIPS 140-2 Level 3 compliant hardware security model  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/)

Shielded VMs \- Shielded VM offers verifiable integrity of your Compute Engine VM instances, so you can be confident your instances haven't been compromised by boot- or kernel-level malware or rootkits. Shielded VM's verifiable integrity is achieved through the use of Secure Boot, virtual trusted platform module (vTPM)-enabled Measured Boot, and integrity monitoring.  
[https://cloud.google.com/security/shielded-cloud/shielded-vm](https://cloud.google.com/security/shielded-cloud/shielded-vm)

### SC-28 (1)

**Control Description:** The information system implements cryptographic mechanisms to prevent unauthorized disclosure and modification of organization-defined information on organization-defined information system components.

Supplemental Guidance: This control enhancement applies to significant concentrations of digital media in organizational areas designated for media storage and also to limited quantities of media generally associated with information system components in operational environments (e.g., portable storage devices, mobile devices). Organizations have the flexibility to either encrypt all information on storage devices (i.e., full disk encryption) or encrypt specific data structures (e.g., files, records, or fields). Organizations employing cryptographic mechanisms to protect information at rest also consider cryptographic key management solutions.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The solution is deployed as infrastructure configurations within GCP. Integrity of the GCP equipment, networking and services used within the solution is the responsibility of Google. The assessment of its capabilities to address this control have been previously examined by CCCS as part of the approval issued to host PB workload, and is being inherited here to partially address this control. 

The solution is deployed using infrastructure as code and deployed from a Azure DevOps repository and CI/CD platform.  The integrity of Azure DevOps has been assessed previously.   
   
The client will configure mechanisms to prevent unauthorized disclosure, notification, etc. as part of their application deployment, and would address this control as part of their security assessment

#### Implementation Recommendations

There is no prerequisite for external services to be FedRAMP-authorized for inclusion in the Cloud Identity product and Google Workspace's boundary does not extend to these third-party services. As a result, agencies must perform due diligence in authorizing these services prior to establishing third-party authentication via Cloud Identity. Any external services that an agency chooses to manage with Cloud Identity are outside of the scope of the Google Workspace system boundary and must be secured in accordance with agency requirements.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Titan Security Key \- Prevent account hacks, phishing attacks, and enforce MFA/2SV using Titan Security Keys  
[https://cloud.google.com/titan-security-key/](https://cloud.google.com/titan-security-key/)

Cloud Key Management Service \- Manage, generate, use, rotate, and destroy AES256, RSA 2048, RSA 3072, RSA 4096, EC P256, and EC P384 cryptographic keys on Google Cloud  
[https://cloud.google.com/kms/](https://cloud.google.com/kms/)

Cloud HSM \- Protect your encryption keys in the cloud using a fully hosted, FIPS 140-2 Level 3 compliant hardware security model  
[https://cloud.google.com/hsm/](https://cloud.google.com/hsm/)

Google Managed SSL Certificates \- A Cloud Load Balancing feature; Google-managed SSL certificates are provisioned, renewed, and managed for your domain names.  
[https://cloud.google.com/load-balancing/docs/ssl-certificates](https://cloud.google.com/load-balancing/docs/ssl-certificates)

Customer Managed SSL Certificates \- A Cloud Load Balancing feature; Provide your own SSL certificates to manage secure access to your GCP domains. Self-managed certificates can support wildcards and multiple subject alternative names (SANs).  
[https://cloud.google.com/load-balancing/docs/ssl-certificates\#working-self-managed](https://cloud.google.com/load-balancing/docs/ssl-certificates#working-self-managed)

### SC-39

**Control Description:** The information system maintains a separate execution domain for each executing process.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

The CUSTOMER is responsible for maintaining a separate execution domain for each executing process.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Resource Manager \- Hierarchically manage resources by project, folder, and organization. Centrally control org & access policies and asset inventories. Label resources for better management.   
[https://cloud.google.com/resource-manager](https://cloud.google.com/resource-manager)

## System and Information Integrity (SI)

### SI-3 (2)

**Control Description:** The information system automatically updates malicious code protection mechanisms.

Supplemental Guidance:  Malicious code protection mechanisms include, for example, signature definitions.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Security Command Center is configured to provide monitoring, and has threat intelligence to detect malicious activity. 

SCC integrates with Cloud Audit Logs to capture audit records of security-relevant events. These logs can be used for analysis and investigations.

#### Org Policies

* SI-3	compute.trustedImageProjects: This constraint helps enforce software and firmware integrity and configuration management. This permission controls which projects can be used as trusted sources for VM images. By limiting this to a select set of projects, you reduce the risk of deploying VMs from untrusted or potentially compromised sources.

#### Implementation Recommendations

For additional information on configuring Cloud Identity Auto Provisioning relationships, please see the following articles:

### SI-3 (7)

**Control Description:** The information system implements nonsignature-based malicious code detection mechanisms.

Supplemental Guidance:  Nonsignature-based detection mechanisms include, for example, the use of heuristics to detect, analyze, and describe the characteristics or behavior of malicious code and to provide safeguards against malicious code for which signatures do not yet exist or for which existing signatures may not be effective. This includes polymorphic malicious code (i.e., code that changes signatures when it replicates). This control enhancement does not preclude the use of signature-based detection mechanisms.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Security Command Center is configured to provide monitoring, and has threat intelligence to detect malicious activity. 

SCC can help you track and manage planned security events like penetration tests and vulnerability scans, ensuring that they are properly authorized and documented.

#### Org Policies

* SI-3	compute.trustedImageProjects: This constraint helps enforce software and firmware integrity and configuration management. This permission controls which projects can be used as trusted sources for VM images. By limiting this to a select set of projects, you reduce the risk of deploying VMs from untrusted or potentially compromised sources.

#### Implementation Recommendations

The customers is responsible for implementing nonsignature-based malicious code detection mechanisms.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Google Workspace Phishing & Malware Protection \- An element of Google Workspace that provides advanced phishing and malware protection. Place emails in quarantine, protect against anomalous attachments, protect Google Groups from inbound email spoofing.  
[https://support.google.com/a/answer/7577854](https://support.google.com/a/answer/7577854)

### SI-4 (2)

**Control Description:** The organization employs automated tools to support near real-time analysis of events.

Supplemental Guidance:  Automated tools include, for example, host-based, network-based, transport-based, or storage-based event monitoring tools or Security Information and Event Management (SIEM) technologies that provide real time analysis of alerts and/or notifications generated by organizational information systems.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Security Command Center is configured to provide monitoring, and has threat intelligence to detect malicious activity.

#### Implementation Recommendations

Set up SSO with Google as your Identity Provider: [https://support.google.com/cloudidentity/topic/7558768](https://support.google.com/cloudidentity/topic/7558768)

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Google Workspace Security Center \- Actionable security insights for Google Workspace. Unified security dashboard. Get insights into external file sharing, visibility into spam and malware targeting users within your organization, and metrics to demonstrate your security effectiveness in a single, comprehensive dashboard.  
[https://workspace.google.com/products/admin/security-center/](https://workspace.google.com/products/admin/security-center/)

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)

### SI-4 (4)

**Control Description:** The information system monitors inbound and outbound communications traffic continuously for unusual or unauthorized activities or conditions.

Supplemental Guidance:  Unusual/unauthorized activities or conditions related to information system inbound and outbound communications traffic include, for example, internal traffic that indicates the presence of malicious code within organizational information systems or propagating among system components, the unauthorized exporting of information, or signaling to external information systems. Evidence of malicious code is used to identify potentially compromised information systems or information system components.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Security Command Center is configured to provide monitoring, and has threat intelligence to detect malicious activity.

#### Implementation Recommendations

The CUSTOMER is responsible for defining what is considered a privileged function, reviewing auditable information provided by various Google Workspace editions, and determining whether available audit logging features are sufficient for organization-specific auditing needs.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)

Google Cloud Network Telemetry \- Network Telemetry provides both network and security operations with in-depth, responsive VPC Flow Logs for Google Cloud Platform networking services. Identify traffic and access patterns that may impose security or operational risks to your organization in near real time. VPC Firewall Logs allows users to log firewall access and deny events with the same responsiveness of VPC Flow Logs.  
[https://cloud.google.com/network-telemetry/](https://cloud.google.com/network-telemetry/)

### SI-4 (5)

**Control Description:** The information system alerts organization-defined personnel or roles when organization-defined indicators of compromise or potential compromise occur

Supplemental Guidance:  Alerts may be generated from a variety of sources, including, for example, audit records or inputs from malicious code protection mechanisms, intrusion detection or prevention mechanisms, or boundary protection devices such as firewalls, gateways, and routers. Alerts can be transmitted, for example, telephonically, by electronic mail messages, or by text messaging. Organizational personnel on the notification list can include, for example, system administrators, mission/business owners, system owners, or information system security officers.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Security Command Center is configured to provide monitoring, and has threat intelligence to detect malicious activity and compromise. Alerting is configured to notify operational personnel when indicators of unusual usage, possible attack, potential compromise have been identified.

#### Implementation Recommendations

Automated user provisioning and deprovisioning: [https://support.google.com/cloudidentity/topic/7661972](https://support.google.com/cloudidentity/topic/7661972)

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)

Google Cloud Network Telemetry \- Network Telemetry provides both network and security operations with in-depth, responsive VPC Flow Logs for Google Cloud Platform networking services. Identify traffic and access patterns that may impose security or operational risks to your organization in near real time. VPC Firewall Logs allows users to log firewall access and deny events with the same responsiveness of VPC Flow Logs.  
[https://cloud.google.com/network-telemetry/](https://cloud.google.com/network-telemetry/)

### SI-4 (16)

**Control Description:** The organization correlates information from monitoring tools employed throughout the information system.

Supplemental Guidance:  Correlating information from different monitoring tools can provide a more comprehensive view of information system activity. The correlation of monitoring tools that usually work in isolation (e.g., host monitoring, network monitoring, anti-virus software) can provide an organization-wide view and in so doing, may reveal otherwise unseen attack patterns.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

The CUSTOMER is responsible for deploying tools correlates information employed throughout the information system.

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Cloud Identity \- Easily manage user identities, devices, and applications from one console. Enforce SSO, MFA/2SV, and Mobile Device Management.  
[https://cloud.google.com/identity/](https://cloud.google.com/identity/) 

Cloud IAM \- Fine-grained identity and access management for GCP resources. Manage permissions, roles, service accounts, members & identities, org policies, and more.  
[https://cloud.google.com/iam/](https://cloud.google.com/iam/)

Cloud VPC \- Managed networking functionality for your Cloud Platform resources. VPC Network, Cloud Router, Cloud VPN, Firewalls, VPC Peering, Shared VPC, Routes, VPC Flow Logs.  
[https://cloud.google.com/vpc/](https://cloud.google.com/vpc/) 

Google Cloud Network Telemetry \- Network Telemetry provides both network and security operations with in-depth, responsive VPC Flow Logs for Google Cloud Platform networking services. Identify traffic and access patterns that may impose security or operational risks to your organization in near real time. VPC Firewall Logs allows users to log firewall access and deny events with the same responsiveness of VPC Flow Logs.  
[https://cloud.google.com/network-telemetry/](https://cloud.google.com/network-telemetry/)

### SI-4 (23)

**Control Description:** The organization implements organization-defined host-based monitoring mechanisms at organization-defined information system components.

Supplemental Guidance:  Information system components where host-based monitoring can be implemented include, for example, servers, workstations, and mobile devices. Organizations consider employing host-based monitoring mechanisms from multiple information technology product developers.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

Set up your own customer SAML application: [https://support.google.com/cloudidentity/answer/6087519](https://support.google.com/cloudidentity/answer/6087519)

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)

### SI-6

**Control Description:** The information system:

 a. Verifies the correct operation of organization-defined security functions;

 b. Performs this verification: organization-defined system transitional states, upon command by user with appropriate privilege, to include upon system startup and/or restart and at least monthly; and

 c. Notifies organization-defined personnel or roles of failed security verification tests \- to include system administrators and security personnel; and

 d. Shuts the information system down, restarts the information system, and performs organization-defined alternative action(s) when anomalies are discovered \- to include notification of system administrators and security personnel.

**Requirements:** PBMM Profile 1: No, Profile 3: No

#### Implementation Notes

Not required for PBMM

#### Implementation Recommendations

The CUSTOMER is responsible for all security functionality verification for their infrastructure and workloads.

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Google Workspace Security Center \- Actionable security insights for Google Workspace. Unified security dashboard. Get insights into external file sharing, visibility into spam and malware targeting users within your organization, and metrics to demonstrate your security effectiveness in a single, comprehensive dashboard.  
[https://workspace.google.com/products/admin/security-center/](https://workspace.google.com/products/admin/security-center/)

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)

### SI-7 (1)

**Control Description:** The information system performs an integrity check of organization-defined software, firmware, and information at startup and/or at organization-defined security-relevant events at least monthly

Supplemental Guidance:  Security-relevant events include, for example, the identification of a new threat to which organizational information systems are susceptible, and the installation of new hardware, software, or firmware. Transitional states include, for example, system startup, restart, shutdown, and abort.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

Security Command Center is configured to provide monitoring, and has threat intelligence to detect malicious activity. 

The solution is deployed as infrastructure configurations within GCP. Integrity of the GCP equipment, networking and services used within the solution is the responsibility of Google. The assessment of its capabilities to address this control have been previously examined by CCCS as part of the approval issued to host PB workload, and is being inherited here to partially address this control. 

The solution is deployed using infrastructure as code and deployed from a separate repository and CI/CD platform.

#### Implementation Recommendations

The CUSTOMER and supported workloads are responsible for performing an integrity check of organization-defined software, firmware, and information at startup and/or at organization-defined security-relevant events at least monthly

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Shielded VMs \- Shielded VM offers verifiable integrity of your Compute Engine VM instances, so you can be confident your instances haven't been compromised by boot- or kernel-level malware or rootkits. Shielded VM's verifiable integrity is achieved through the use of Secure Boot, virtual trusted platform module (vTPM)-enabled Measured Boot, and integrity monitoring.  
[https://cloud.google.com/security/shielded-cloud/shielded-vm](https://cloud.google.com/security/shielded-cloud/shielded-vm)

Cloud Security Scanner \- Automatically scan App Engine, Compute Engine, and Kubernetes Engine applications for common vulnerabilities such as XXS, flash injection, mixed HTTP(S) content, outdated and insecure libraries  
[https://cloud.google.com/security-scanner/](https://cloud.google.com/security-scanner/)

Artifact Analysis \- Artifact Analysis is a family of services that provide software composition analysis, metadata storage and retrieval. Its detection points are built into a number of Google Cloud products such as Artifact Registry and Google Kubernetes Engine (GKE) for quick enablement. The service works with both Google Cloud's first-party products and also lets you store information from third-party sources. The scanning services leverage a common vulnerability store for matching files against known vulnerabilities.  
[https://cloud.google.com/artifact-analysis/docs/artifact-analysis](https://cloud.google.com/artifact-analysis/docs/artifact-analysis)

### SI-10

**Control Description:** The information system checks the validity of organization-defined information inputs.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The solution infrastructure has the following input points:  
\* Administrative Uis \- These are developed and maintained by Google who have responsibility for input validation  
\* Infrastructure as Code \- All configuration files validated by multiple reviewers (including examination for any abnormal inputs) prior to being accepted into the repo. Linting is also configured on the repo to ensure syntactical correctness.

Yet to be deployed client workloads may contain code that accepts user input; the client would be responsible to respond to this control as part of their assessment activities.

#### Implementation Recommendations

The CUSTOMER and supporting workloads are responsible for implementing system checks the validity of organization-defined information inputs.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Cloud Security Scanner \- Automatically scan App Engine, Compute Engine, and Kubernetes Engine applications for common vulnerabilities such as XXS, flash injection, mixed HTTP(S) content, outdated and insecure libraries  
[https://cloud.google.com/security-scanner/](https://cloud.google.com/security-scanner/)

Artifact Analysis \- Artifact Analysis is a family of services that provide software composition analysis, metadata storage and retrieval. Its detection points are built into a number of Google Cloud products such as Artifact Registry and Google Kubernetes Engine (GKE) for quick enablement. The service works with both Google Cloud's first-party products and also lets you store information from third-party sources. The scanning services leverage a common vulnerability store for matching files against known vulnerabilities.  
[https://cloud.google.com/artifact-analysis/docs/artifact-analysis](https://cloud.google.com/artifact-analysis/docs/artifact-analysis)

### SI-11 \- SYSTEM AND INFORMATION INTEGRITY

**Control Description:** The information system:

 a. Generates error messages that provide information necessary for corrective actions without revealing information that could be exploited by adversaries; and

 b. Reveals error messages only to organization-defined personnel or roles.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The solution infrastructure relies on error messages generated by GCP and associated services; there is no ability to replace/modify/remove any error messages. The assessment of the level of information contained has been previously examined by CCCS as part of the approval issued to host PB workload, and is being inherited here to partially address this control. 

Only privileged users have access to the administrative interfaces and are exposed to these error messages. Errors included in logs are similarly restricted to only privileged used via access control on logging buckets (inherited from the logging project)

Yet to be deployed client workloads may generate application specific error messages. The client would be responsible to respond to this control as part of their assessment activities.

#### Implementation Recommendations

Part a:  
Customers are responsible for ensuring applications built on GCP generate error messages that provide information necessary for corrective actions without revealing any potential information that can be misused by adversaries. Customers may use Cloud Error Reporting product located within Operations Tools to identify and report errors. Cloud Error Reporting is a centralized error management interface that displays the results with sorting and filtering capabilities. Customers can use the dedicated view to show error details such as time charts, occurrences, affected user counts, first and last seen dates and a cleaned exception stack trace.

Part b:  
Customers are responsible for ensuring applications built on GCP generate error messages that provide information necessary for corrective actions without revealing any potential information that can be misused by adversaries. Customers may use Cloud Error Reporting product located within Management Tools to identify and report errors. Cloud Error Reporting is a centralized error management interface that displays the results with sorting and filtering capabilities. Customers can use the dedicated view to show error details such as time charts, occurrences, affected user counts, first and last seen dates and a cleaned exception stack trace.

Google Cloud uses a small set of standard errors with a large number of resources, to communicate issues. The smaller state space reduces the complexity of documentation, affords better idiomatic mappings in client libraries, and reduces client logic complexity while not restricting the inclusion of actionable information. Google APIs must use the canonical error codes defined by google.rpc.Code. These error messages help users understand and resolve the API error easily and quickly ([https://cloud.google.com/apis/design/errors](https://cloud.google.com/apis/design/errors)).  
Note that these errors are only revealed to privileged personnel with Google APIs access.   
Best Practice: Encourage Server Developers to develop errors in alignment with google.rpc.Code ([https://cloud.google.com/apis/design/errors\#generating\_errors](https://cloud.google.com/apis/design/errors#generating_errors))

#### Service Notes

Policies, procedures and configurations for this control must be determined by the customer's internal organization, security and administrative teams, however these Google Cloud tools and services may be helpful.

Cloud Operations Suite \- Google's embedded observability suite designed to monitor, troubleshoot, and improve cloud infrastructure, software, and application performance. Cloud Operations Suite's FedRAMP compliant components include: Logging, Error Reporting, Debugger, Profiler, and Trace.  
[https://cloud.google.com/products/operations/](https://cloud.google.com/products/operations/)

### SI-16

**Control Description:** The information system implements organization-defined security safeguards to protect its memory from unauthorized code execution.

**Requirements:** PBMM Profile 1: Yes, Profile 3: Yes

#### Implementation Notes

The solution is deployed as infrastructure configurations within GCP using its services. Integrity of memory protections to preclude unauthorized code execution is the responsibility of Google. The assessment of its capabilities to address this control have been previously examined by CCCS as part of the approval issued to host PB workload, and is being inherited here to partially address this control. 

Yet to be deployed client workloads may involve client-developed components where memory protection is needed. The client would be responsible to respond to this control as part of their assessment activities.

#### Implementation Recommendations

The CUSTOMER is responsible for configurating and deploying organization-defined security safeguards to protect its memory from unauthorized code execution within their GCP workloads.

#### Service Notes

Customers and organizations can leverage or reference the following tools to help meet this requirement for their IT system(s) on Google Cloud

Google Cloud Security \- Whitepaper covering Google's cloud services security, including Google's security culture, operational security, technology & data center security, data center environmental controls, data security and compliance.  
[https://services.google.com/fh/files/misc/google\_security\_wp.pdf](https://services.google.com/fh/files/misc/google_security_wp.pdf) 

Google Infrastructure Security \- Whitepaper that gives an overview of Google's infrastructure security for hardware, services, user identity, storage, communications, and operations. Note: This is not a GCP Product  
[https://cloud.google.com/security/infrastructure/design/resources/google\_infrastructure\_whitepaper\_fa.pdf](https://cloud.google.com/security/infrastructure/design/resources/google_infrastructure_whitepaper_fa.pdf)

Cloud Memorystore \- Fully managed in-memory data store service for Redis, built on scalable, secure, and highly available infrastructure. Use Cloud Memorystore to build application caches that provides sub-millisecond data access. Cloud Memorystore instances are isolated and protected from the internet using private IPs and are further secured using IAM role-based access control.  
[https://cloud.google.com/memorystore/](https://cloud.google.com/memorystore/)

# Appendix 3: Reference Materials <a name="reference-materials"></a>

* [Enterprise Foundation Blueprint \- Documentation](https://cloud.google.com/architecture/security-foundations)  
* [GC Cloud Guardrails Checks for Google Cloud Platform](https://github.com/canada-ca/cloud-guardrails-gcp)  
* [Google Workspace and GCP Organization](https://cloud.google.com/resource-manager/docs/creating-managing-organization)  
* [Resource Hierarchy, Google Cloud Platform](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy)  
* [IAM Hierarchy, Google Cloud Platform](https://cloud.google.com/iam/docs/resource-hierarchy-access-control)  
* [Best Practices for Enterprise Organizations](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)  
* [Accepted GCP Authentication Members](https://cloud.google.com/iam/docs/overview#google_account)  
* [GCP IAM Roles](https://cloud.google.com/iam/docs/understanding-roles)  
* [Private Google Access](https://cloud.google.com/vpc/docs/configure-private-google-access)  
* [Dynamic Routing in VPC](https://cloud.google.com/vpc/docs/vpc#routing_for_hybrid_networks)  
* [Access to Google APIs](https://cloud.google.com/vpc/docs/configure-private-google-access#config-routing)  
* [VPC Firewall Rules](https://cloud.google.com/vpc/docs/firewalls)  
* [Identity Aware Proxy](https://cloud.google.com/iap/docs/concepts-overview)  
* [Forseti Security](https://forsetisecurity.org/)  
* [GCP Cloud Guardrails](https://github.com/canada-ca/cloud-guardrails-gcp)  
* [Security Command Center](https://cloud.google.com/security-command-center/docs/concepts-security-command-center-overview)  
* [VPC Service Control](https://cloud.google.com/vpc-service-controls/docs/overview)  
* [Secret Manager](https://cloud.google.com/secret-manager/docs/overview)  
* [Secrets Manager \- Customer Managed Encryption Keys](https://cloud.google.com/secret-manager/docs/cmek)  
* [Cloud Logging](https://cloud.google.com/logging/docs)  
* [Cloud Monitoring](https://cloud.google.com/monitoring/docs/monitoring-overview)  
* [DNS Overview](https://cloud.google.com/dns/docs/overview)

[image1]: ./images/efb-key-decisions.svg

[image2]: ./images/architecture-with-appliance.svg

[image3]: ./images/example-org-structure.svg

[image4]: ./images/example-identity-structure.svg

[image5]: ./images/traffic-flow-appliance.svg

[image6]: ./images/example-hub-spoke.svg

[image7]: ./images/example-dns-setup.svg

[image8]: ./images/example-logging-structure.svg

[image9]: ./images/example-deployment-branching.svg
