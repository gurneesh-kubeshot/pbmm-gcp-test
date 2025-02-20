regions = {
  "primary": "northamerica-northeast1",
  "secondary": "northamerica-northeast2"
}
business_units = [
  {
    "business_code": "bu1",
    "business_unit": "Business Unit 1",
    "location_kms": "ca",
    "location_gcs": "ca",
    "tfc_org_name": "example-org",
    "gcs_bucket_prefix": "bkt",
    "folder_prefix": "fldr",
    "primary_contact": "admin@example.com",
    "secondary_contact": "backup@example.com",
    "environments": {
      "development": {
        "env_code": "d",
        "billing_code": "1234",
        "env_enabled": true,
        "windows_activation_enabled": true,
        "firewall_logging_enabled": true,
        "optional_fw_rules_enabled": true,
        "vpc_flow_logs_enabled": true,
        "peering_iap_fw_rules_enabled": true,
        "key_ring_name": "dev-keyring",
        "key_name": "dev-key",
        "key_rotation_period": "7776000s",
        "base": {
          "enabled": true,
          "ip_ranges": {
            "subnet1": "10.0.0.0/24",
            "subnet2": "10.0.1.0/24"
          },
          "projects": [
            {
              "id": "dev-project-1",
              "name": "Development Project 1",
              "services": [
                "compute.googleapis.com",
                "container.googleapis.com"
              ]
            }
          ]
        },
        "restricted": {
          "enabled": false,
          "ip_ranges": {},
          "projects": [],
          "vpc_scp": false
        }
      }
    }
  },
  {
    "business_code": "bu2",
    "business_unit": "Business Unit 2",
    "location_kms": "ca",
    "location_gcs": "ca",
    "tfc_org_name": "example-org",
    "gcs_bucket_prefix": "bkt",
    "folder_prefix": "fldr",
    "primary_contact": "admin2@example.com",
    "secondary_contact": "backup2@example.com",
    "environments": {
      "development": {
        "env_code": "d",
        "billing_code": "5678",
        "env_enabled": true,
        "windows_activation_enabled": false,
        "firewall_logging_enabled": true,
        "optional_fw_rules_enabled": true,
        "vpc_flow_logs_enabled": true,
        "peering_iap_fw_rules_enabled": false,
        "key_ring_name": "dev-keyring-2",
        "key_name": "dev-key-2",
        "key_rotation_period": "7776000s",
        "base": {
          "enabled": true,
          "ip_ranges": {
            "subnet1": "10.1.0.0/24",
            "subnet2": "10.1.1.0/24"
          },
          "projects": [
            {
              "id": "dev-project-2",
              "name": "Development Project 2",
              "services": [
                "compute.googleapis.com",
                "cloudfunctions.googleapis.com"
              ]
            }
          ]
        },
        "restricted": {
          "enabled": true,
          "ip_ranges": {
            "subnet1": "192.168.0.0/24"
          },
          "projects": [
            {
              "id": "dev-restricted-1",
              "name": "Development Restricted Project 1",
              "services": [
                "compute.googleapis.com"
              ]
            }
          ],
          "vpc_scp": true
        }
      }
    }
  }
]
