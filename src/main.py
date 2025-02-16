#!/usr/bin/env python3

"""Main entry point for the landing zone configuration tool."""

import argparse
import sys
import yaml
import time
from typing import Dict, Any
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

    return parser.parse_args()

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

if __name__ == '__main__':
    main() 