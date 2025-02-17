#!/usr/bin/env python3

"""Main entry point for the landing zone configuration tool."""

import argparse
import sys
import yaml
import json
import os
import time
from typing import Dict, Any
from pathlib import Path
from google.cloud.devtools import cloudbuild_v1
from config.validator import ConfigValidator
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from datetime import datetime

console = Console()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Landing Zone Configuration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Validate a configuration:
    %(prog)s validate path/to/config.yaml
  
  Deploy a configuration:
    %(prog)s deploy path/to/config.yaml --project-id=my-project [--progress]
  
  Convert YAML to Terraform variables:
    %(prog)s convert path/to/config.yaml path/to/output.tfvars [--common-only]
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a configuration file')
    validate_parser.add_argument('config_file', help='Path to the configuration YAML file')

    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy a configuration using Cloud Build')
    deploy_parser.add_argument('config_file', help='Path to the configuration YAML file')
    deploy_parser.add_argument('--project-id', required=True, help='GCP project ID')
    deploy_parser.add_argument('--progress', action='store_true', help='Show build progress')

    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert YAML configuration to Terraform variables')
    convert_parser.add_argument('config_file', help='Path to the configuration YAML file')
    convert_parser.add_argument('output_file', help='Path to the output .tfvars file')
    convert_parser.add_argument('--common-only', action='store_true', help='Extract only common configuration')

    return parser.parse_args()

def yaml_to_tfvars(yaml_file: str, output_file: str, common_only: bool = False) -> bool:
    """Convert YAML configuration to Terraform variables.
    
    Args:
        yaml_file: Path to the YAML configuration file.
        output_file: Path to the output .tfvars file.
        common_only: Whether to extract only common configuration.
    
    Returns:
        bool: True if conversion succeeds, False otherwise.
    """
    try:
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
        
        # Convert YAML data to Terraform format
        tfvars = {}
        
        # Process regions (common configuration)
        if 'regions' in yaml_data:
            tfvars['regions'] = yaml_data['regions']
        
        # Process business units if not common_only or if we need their common attributes
        if 'business_units' in yaml_data:
            tfvars['business_units'] = []
            for bu in yaml_data['business_units']:
                # Common business unit configuration
                bu_config = {
                    'business_code': bu.get('business_code', ''),
                    'business_unit': bu.get('business_unit', ''),
                    'location_kms': bu.get('location_kms', 'ca'),
                    'location_gcs': bu.get('location_gcs', 'ca'),
                    'tfc_org_name': bu.get('tfc_org_name', ''),
                    'gcs_bucket_prefix': bu.get('gcs_bucket_prefix', 'bkt'),
                    'folder_prefix': bu.get('folder_prefix', 'fldr'),
                    'primary_contact': bu.get('primary_contact', 'none@no.ne'),
                    'secondary_contact': bu.get('secondary_contact', 'none@no.ne'),
                }
                
                # Add environment-specific configuration if not common_only
                if not common_only:
                    env_keys = ['development', 'nonproduction', 'production']
                    bu_config['environments'] = {}
                    
                    for env in env_keys:
                        if env in bu:
                            env_config = bu[env]
                            bu_config['environments'][env] = {
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
                
                tfvars['business_units'].append(bu_config)
        
        # Write to tfvars file
        with open(output_file, 'w') as f:
            for key, value in tfvars.items():
                if isinstance(value, (dict, list)):
                    f.write(f'{key} = {json.dumps(value, indent=2)}\n')
                else:
                    f.write(f'{key} = "{value}"\n')
        
        print(f"✅ Successfully converted {yaml_file} to {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error converting YAML to Terraform variables: {str(e)}", file=sys.stderr)
        return False

def validate_config(config_file: str) -> tuple[bool, Dict[str, Any] | None]:
    """Validate the configuration file.
    
    Args:
        config_file: Path to the configuration file.
    
    Returns:
        Tuple of (success, config) where success is True if validation succeeds,
        and config is the validated configuration if successful.
    """
    try:
        validator = ConfigValidator()
        config = validator.validate_file(config_file)
        print(f"✅ Configuration file {config_file} is valid")
        print("\nConfiguration details:")
        print(f"Landing Zone Type: {config['landing_zone']['type']}")
        print(f"Version: {config['version']}")
        return True, config
    except Exception as e:
        print(f"❌ Error validating configuration: {str(e)}", file=sys.stderr)
        return False, None

def format_build_step(step: cloudbuild_v1.BuildStep, status: str) -> str:
    """Format a build step for display.
    
    Args:
        step: The build step to format
        status: The status of the step
    
    Returns:
        str: Formatted step string
    """
    status_icons = {
        'SUCCESS': '✅',
        'FAILURE': '❌',
        'WORKING': '🔄',
        'QUEUED': '⏳',
    }
    icon = status_icons.get(status, '⚪')
    return f"{icon} {step.name}"

def monitor_build_progress(operation, project_id: str):
    """Monitor build progress and display in terminal.
    
    Args:
        operation: The build operation to monitor
        project_id: GCP project ID
    """
    client = cloudbuild_v1.CloudBuildClient()
    build_id = operation.metadata.build.id
    
    with Live(console=console, refresh_per_second=1) as live:
        while True:
            build = client.get_build(project_id=project_id, id=build_id)
            
            # Create progress display
            status = f"[bold]Build Status:[/bold] {build.status.name}"
            if build.status == cloudbuild_v1.Build.Status.WORKING:
                status += f" ({len([s for s in build.steps if s.status == cloudbuild_v1.Build.Status.SUCCESS])}/{len(build.steps)} steps complete)"
            
            steps_display = []
            for step in build.steps:
                step_status = step.status.name if step.status else 'QUEUED'
                steps_display.append(format_build_step(step, step_status))
                if step.status == cloudbuild_v1.Build.Status.WORKING and hasattr(step, 'timing'):
                    steps_display.append(f"  > {step.timing.start_time.strftime('%H:%M:%S')}: Running...")
            
            # Update display
            live.update(
                Panel(
                    "\n".join([
                        status,
                        "",
                        *steps_display,
                        "",
                        f"[bold]Time Elapsed:[/bold] {build.timing.start_time.strftime('%H:%M:%S') if build.timing and build.timing.start_time else 'Not started'}"
                    ]),
                    title=f"Build ID: {build_id}",
                    border_style="blue"
                )
            )
            
            # Check if build is complete
            if build.status in [
                cloudbuild_v1.Build.Status.SUCCESS,
                cloudbuild_v1.Build.Status.FAILURE,
                cloudbuild_v1.Build.Status.CANCELLED,
                cloudbuild_v1.Build.Status.TIMEOUT
            ]:
                break
            
            time.sleep(5)  # Poll every 5 seconds

def convert_environment_configs(base_dir: str) -> bool:
    """Convert YAML configurations for all environments to Terraform variables.
    
    Args:
        base_dir: Base directory containing the business_units directory
        
    Returns:
        bool: True if conversion succeeds, False otherwise
    """
    try:
        business_units_dir = os.path.join(base_dir, '4-projects/business_units')
        environments = ['development', 'nonproduction', 'production']
        
        for env in environments:
            env_dir = os.path.join(business_units_dir, env)
            if not os.path.exists(env_dir):
                continue
                
            config_file = os.path.join(env_dir, 'config.yaml')
            if not os.path.exists(config_file):
                continue
            
            # Convert to environment-specific tfvars
            env_tfvars = os.path.join(env_dir, f'{env}.auto.tfvars')
            if not yaml_to_tfvars(config_file, env_tfvars, False):
                return False
            
            # Extract common configuration
            common_tfvars = os.path.join(env_dir, 'common.auto.tfvars')
            if not yaml_to_tfvars(config_file, common_tfvars, True):
                return False
    
        return True
    except Exception as e:
        print(f"❌ Error converting environment configurations: {str(e)}", file=sys.stderr)
        return False

def submit_build(project_id: str, config: Dict[str, Any], show_progress: bool = False) -> bool:
    """Submit a Cloud Build job using the existing cloudbuild.yaml.
    
    Args:
        project_id: GCP project ID
        config: Validated configuration
        show_progress: Whether to show build progress
        
    Returns:
        bool: True if submission succeeds, False otherwise
    """
    try:
        # First convert all environment configurations
        if not convert_environment_configs('landing-zones/pbmm-gcp'):
            return False

        # Create the Cloud Build client
        client = cloudbuild_v1.CloudBuildClient()

        # Read the cloudbuild.yaml file
        with open('landing-zones/pbmm-gcp/cloudbuild.yaml', 'r') as f:
            yaml_config = yaml.safe_load(f)

        # Create the build request
        build = cloudbuild_v1.Build()
        
        # Add steps
        for step in yaml_config.get('steps', []):
            build_step = cloudbuild_v1.BuildStep()
            build_step.name = step['name']
            if 'entrypoint' in step:
                build_step.entrypoint = step['entrypoint']
            if 'args' in step:
                build_step.args = step['args']
            if 'env' in step:
                build_step.env = step['env']
            if 'secretEnv' in step:
                build_step.secret_env = step['secretEnv']
            build.steps.append(build_step)

        # Add substitutions
        build.substitutions = {
            "_PROJECT_ID": project_id,
            "_SUPER_ADMIN_EMAIL": config["bootstrap"]["groups"]["required_groups"]["group_org_admins"],
            "_REGION": config["bootstrap"]["default_region"],
            "_ORG_ID": config["bootstrap"]["org_id"],
            "_ROOT_FOLDER_ID": config["org"]["parent_folder"],
            "_BILLING_ID": config["bootstrap"]["billing_account"],
            "_DOMAIN": "www.neosecai.com"  # This could be made configurable if needed
        }

        # Add secrets
        available_secrets = cloudbuild_v1.types.Secrets()
        secret_manager_secret = cloudbuild_v1.types.SecretManagerSecret()
        secret_manager_secret.version_name = f"projects/816268782019/secrets/sa-111-secops/versions/latest"
        secret_manager_secret.env = 'SECRET'  # Specify which env var will use this secret
        available_secrets.secret_manager = [secret_manager_secret]
        build.available_secrets = available_secrets

        # Create the build
        operation = client.create_build(
            project_id=project_id,
            build=build
        )
        
        print("\n✅ Build submitted successfully:")
        print(f"Build ID: {operation.metadata.build.id}")
        print(f"Build Name: {operation.metadata.build.name}")
        
        if show_progress:
            print("\nMonitoring build progress...")
            monitor_build_progress(operation, project_id)
        else:
            print("\nYou can monitor the build progress in the Cloud Console")
        
        return True

    except Exception as e:
        print(f"❌ Error submitting build: {str(e)}", file=sys.stderr)
        return False

def main():
    """Main entry point."""
    args = parse_args()

    if not args.command:
        print("Error: No command specified", file=sys.stderr)
        sys.exit(1)

    if args.command == 'validate':
        success, _ = validate_config(args.config_file)
        sys.exit(0 if success else 1)
    elif args.command == 'deploy':
        # First validate the configuration
        success, config = validate_config(args.config_file)
        if not success:
            sys.exit(1)
        
        # Then submit the build
        success = submit_build(args.project_id, config, args.progress)
        sys.exit(0 if success else 1)
    elif args.command == 'convert':
        success = yaml_to_tfvars(args.config_file, args.output_file, args.common_only)
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 