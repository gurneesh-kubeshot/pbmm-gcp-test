# Configuration for vpc_config.yaml

The configuration file contains several sections

## Regions (section regions)

A list of configurations for each of the 2 supported regions

* name : (required) the name of the region e.g.
* enabled : (optional) by default "true" for region1 and "false" for region2. Set to true for the deployment to be done in a region

## The prod, non-prod and dev "Spokes" (section spokes)

Contains a configuration section common to the "spokes" and more or less similar configurations for each of the "spokes". By default contains 3 "spoke" environments (development, nonproduction and production) but it is optional - we can add more, change the names or remove them.

### Common configuration (common section)

By default the only configuration elements (optional) are:

* al_env_ip_range: a CIDR summary for the spoke address ranges
* spoke_common_routes: Contains (if any) the common routing for all spokes, by default 2 optional routes
* rt_nat_to_internet: route to Internet through the NAT gateway
* rt_windows_activation: route to the Windows activation servers provided by Google

These routes can be complemented or invalidated by routes defined at the level of a spoke environment or even lower at the level of a sub-environment ("base" or "restricted") by using a higher priority

### Configuration by "spoke"

For each of the spoke environments there is a common configuration part and separate configurations for each of the sub-environments (by default "base" and "restricted")

The difference between "base" and "restricted" is the security level. "Restricted" sub-environments use perimeter-based service controls that secure workloads.

#### Common Configuration

The following settings are common to both "base" and "restricted" sub-environments

* env_code: (required) a one-letter code for the environment, found in resource names. Defaults to "d" for development, "n" for nonproduction, and "p" for production
* env_enabled: (optional) defaults to false, set to true to provision the "spoke" environment
* nat_igw_enabled: (optional) controls NAT provisioning, defaults to false, set to true to configure NAT gateways. Also implicitly conditions the provisioning of the NAT route to the Internet and the associated "cloud router" resources
* windows_activation_enabled: (optional) controls the provisioning of the rt_windows_activation route. Default is false.
* enable_hub_and_spoke_transitivity: (optional) controls the deployment of VMs in shared VPCs to enable inter-spoke routing. Default is false.
* router_ha_enabled: (optional) controls the deployment of the second "cloud router" resource in each availability zone. The "cloud router" is free but not the BGP traffic through it. Default is false.
* mode: (optional) 2 possible values put "spoke" or "hub", it is used in the code. Default is "spoke" at this level.

#### Configuration settings for "base" and "restricted"

The settings of the 2 sub-environments are the same, the routes and addressing could vary.

The following parameters are common:

* env_type: (optional) This is a component of the resource names. By default "shared-base" for "base" and "shared-restricted" for "restricted".
* enabled: (optional) By default false. If true, the subenvironment is deployed.
* private_service_cidr: (optional) This is in a range of addresses in a CIDR format that, if configured, allows to provision the "Private Service Access" connectivity, necessary to access services like Cloud SQL or Cloud Filestore (file sharing).
* private_service_connect_ip: (required) this is the address that will be assigned to a private connection point, used to access Google API services in private mode.
* subnets: (required) the subnets setting. By default the subnet sets that are configured are the following:

* id=primary: (optional) used for workloads, with address ranges for each region. It is optional to provision a subnet at the region level.

* secondary_ranges: (optional) multiple secondary address ranges can be configured, again optionally in one or both regions, associated with the primary subnet. The only parameters provided (per region) are
* range_suffix: (required) an arbitrary string that is used to generate the names of the secondary subnets
* ip_cidr_ranges: (required) the address range of the secondary subnet in CIDR format, for each region where we want to provision a secondary subnet.
* id: (required) a unique identifier of the subnet, which appears in the generated name of the resource created. Can be provisioned
* description: (optional) a description of the subnet's function
* ip_ranges: (required) a subnet address range per region in CIDR format. For each region for which a CIDR range is specified, a separate subnet will be provisioned.
* subnet_suffix: (optional) a string that will be appended to the end of the generated subnet name
* flow_logs: (optional) a custom setting for flow-logs compared to the default values. The following fields can be specified:
* enable: (optional) default "false". If true, flow_logs are enabled for the subnet
* interval: (optional) default 5 seconds
* medatata: (optional) default INCLUDE_ALL_METADATA
* metadata_fields (optional) default empty
* private_access: (optional) default false. Controls whether Private Google Access (PGA) is enabled at the subnet level. Since this is provisioning a forwarding-rule resource, enabling it involves costs.
* id=proxy: (optional) used for resources that use the Envoy proxy deployed in a VPC. Examples: application balancer or internal "TCP proxy", API Gateway. There are parameters

* id: (required) a unique identifier of the subnet, which appears in the generated name of the resource created. It can be provisioned
* description: (optional) a description of the function of the subnet
* ip_ranges: (required) a subnet address range per region in CIDR format. For each region for which a CIDR range is specified, a separate subnet will be provisioned.
* subnet_suffix: (optional) a string that will be appended to the end of the generated subnet name
* flow_logs: (optional) a custom setting for flow-logs compared to the default values. The following fields can be specified:
* enable: (optional) default "false". If true, flow_logs are enabled for the subnet
* interval: (optional) default 5 seconds
* medatata: (optional) default INCLUDE_ALL_METADATA
* metadata_fields (optional) default empty
* role and purpose are required and specific to proxy subnets. Leave the default values (role = ACTIVE and purpose = REGIONAL_MANAGED_PROXY)

## Shared resources settings (common section)

By default the "common" environment contains 2 sub-environments:

* dns-hub: (required) hosts the DNS zones shared with "DNS peering" as well as for DNS resolution between the cloud and the "on-site"
* net-hub: (required) hosts the shared VPCs of type "hub", one per environment (production, nonproduction and development) and sub-environment (base and restricted)

For the "net-hub" sub-environment there are specific configurations, see the yaml configuration for details.
