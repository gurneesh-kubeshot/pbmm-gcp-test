changequote(,)
# 5-app-infra

This repo is part of a multi-part guide that shows how to configure and deploy
the example.com reference architecture described in
[Google Cloud security foundations guide](https://services.google.com/fh/files/misc/google-cloud-security-foundations-guide.pdf)
(PDF). The following table lists the parts of the guide.

<table>
<tbody>
<tr>
<td><a href="../0-bootstrap">0-bootstrap</a></td>
<td>Bootstraps a Google Cloud organization, creating all the required resources
and permissions to start using the Cloud Foundation Toolkit (CFT). This
step also configures a CI/CD pipeline for foundations code in subsequent
stages.</td>
</tr>
<tr>
<td><a href="../1-org">1-org</a></td>
<td>Sets up top-level shared folders, monitoring and networking projects,
organization-level logging, and baseline security settings through
organizational policies.</td>
</tr>
<tr>
<td><a href="../2-environments"><span style="white-space: nowrap;">2-environments</span></a></td>
<td>Sets up development, non-production, and production environments within the
Google Cloud organization that you've created.</td>
</tr>
<tr>
<td><a href="../3-networks">3-networks</a></td>
<td>Sets up base and restricted shared VPCs with default DNS, NAT (optional),
Private Service networking, VPC service controls, on-premises Dedicated
Interconnect, and baseline firewall rules for each environment. It also sets
up the global DNS hub.</td>
</tr>
<tr>
<td><a href="../4-projects">4-projects</a></td>
<td>Sets up a folder structure, projects, and an application infrastructure pipeline for applications,
 which are connected as service projects to the shared VPC created in the previous stage.</td>
</tr>
<tr>
<td>5-app-infra (this file)</td>
<td>Deploy a simple [Compute Engine](https://cloud.google.com/compute/) instance in one of the business unit projects using the infra pipeline set up in 4-projects.</td>
</tr>
</tbody>
</table>

For an overview of the architecture and the parts, see the
[terraform-example-foundation README](https://github.com/terraform-google-modules/terraform-example-foundation)
file.

## Purpose

The purpose of this step is to deploy a simple [Compute Engine](https://cloud.google.com/compute/) instance in one of the business unit projects using the infra pipeline set up in 4-projects.
The infra pipeline is created in step `4-projects` within the shared env and has a [Cloud Build](https://cloud.google.com/build/docs) pipeline configured to manage infrastructure within projects.
To enable deployment via this pipeline, the projects deployed should [enable](https://github.com/terraform-google-modules/terraform-example-foundation/blob/master/4-projects/business_unit_1/development/example_base_shared_vpc_project.tf#L31-L32) the `enable_cloudbuild_deploy` flag and provide the Cloud Build service account value via `cloudbuild_sa`.

This enables the Cloud Build service account to impersonate the project service account and use it to deploy infrastructure. The roles required for the project SA can also be [managed](https://github.com/terraform-google-modules/terraform-example-foundation/blob/master/4-projects/business_unit_1/development/example_base_shared_vpc_project.tf#L30) via `sa_roles`. (Note: This requires per project SA impersonation. If you would like to have a single SA managing an environment and all associated projects, that is also possible by [granting](https://github.com/terraform-google-modules/terraform-example-foundation/blob/master/4-projects/modules/single_project/main.tf#L62-L68) `roles/iam.serviceAccountTokenCreator` to an SA with the right roles in `4-projects/env`.)

There is also a [Source Repository](https://cloud.google.com/source-repositories) configured with build triggers similar to the [foundation pipeline](https://github.com/terraform-google-modules/terraform-example-foundation#0-bootstrap) setup in `0-bootstrap`.
This Compute Engine instance is created using the base network from step `3-networks` and is used to access private services.

## Prerequisites

1. 0-bootstrap executed successfully.
1. 1-org executed successfully.
1. 2-environments executed successfully.
1. 3-networks executed successfully.
1. 4-projects executed successfully.

### Troubleshooting

Please refer to [troubleshooting](../docs/TROUBLESHOOTING.md) if you run into issues during this step.
