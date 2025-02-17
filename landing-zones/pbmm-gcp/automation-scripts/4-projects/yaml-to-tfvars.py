#!/usr/bin/env python3

import yaml
import json
import os
import sys
from pathlib import Path

def yaml_to_tfvars(yaml_file, output_file):
    """Convert YAML configuration to Terraform variables."""
    with open(yaml_file, 'r') as f:
        yaml_data = yaml.safe_load(f)
    
    # Convert YAML data to Terraform format
    tfvars = {}
    
    # Process business units
    if 'business_units' in yaml_data:
        tfvars['business_units'] = []
        for bu in yaml_data['business_units']:
            tfvars['business_units'].append({
                'business_code': bu.get('business_code', ''),
                'business_unit': bu.get('business_unit', ''),
                'location_kms': bu.get('location_kms', 'ca'),
                'location_gcs': bu.get('location_gcs', 'ca'),
                'tfc_org_name': bu.get('tfc_org_name', ''),
                'gcs_bucket_prefix': bu.get('gcs_bucket_prefix', 'bkt'),
                'folder_prefix': bu.get('folder_prefix', 'fldr'),
                'primary_contact': bu.get('primary_contact', 'none@no.ne'),
                'secondary_contact': bu.get('secondary_contact', 'none@no.ne'),
                # Environment specific configuration
                'environments': {
                    env: {
                        'env_code': env_config.get('env_code', ''),
                        'billing_code': env_config.get('billing_code', 'none'),
                        'env_enabled': env_config.get('env_enabled', False),
                        'windows_activation_enabled': env_config.get('windows_activation_enabled', False),
                        'firewall_logging_enabled': env_config.get('firewall_logging_enabled', False),
                        'optional_fw_rules_enabled': env_config.get('optional_fw_rules_enabled', False),
                        'vpc_flow_logs_enabled': env_config.get('vpc_flow_logs_enabled', False),
                        'peering_iap_fw_rules_enabled': env_config.get('peering_iap_fw_rules_enabled', False),
                        'key_ring_name': env_config.get('key_ring_name', 'simple-keyring'),
                        'key_name': env_config.get('key_name', 'simple-keyname'),
                        'key_rotation_period': env_config.get('key_rotation_period', '7776000s'),
                        'base': env_config.get('base', {}),
                        'restricted': env_config.get('restricted', {})
                    }
                    for env, env_config in bu.items()
                    if env in ['development', 'nonproduction', 'production']
                }
            })
    
    # Process regions if present
    if 'regions' in yaml_data:
        tfvars['regions'] = yaml_data['regions']
    
    # Write to tfvars file
    with open(output_file, 'w') as f:
        for key, value in tfvars.items():
            if isinstance(value, (dict, list)):
                f.write(f'{key} = {json.dumps(value, indent=2)}\n')
            else:
                f.write(f'{key} = "{value}"\n')

def main():
    if len(sys.argv) != 3:
        print("Usage: yaml-to-tfvars.py <yaml_file> <output_file>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(yaml_file):
        print(f"Error: YAML file {yaml_file} does not exist")
        sys.exit(1)
    
    yaml_to_tfvars(yaml_file, output_file)
    print(f"Successfully converted {yaml_file} to {output_file}")

if __name__ == '__main__':
    main() 