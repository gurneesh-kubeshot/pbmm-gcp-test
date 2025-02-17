# Landing Zone Configuration Tool

A Python-based tool for managing and deploying Google Cloud Platform landing zones. This tool supports both standard GCP and PBMM GCP landing zone configurations.

## Features

- YAML-based configuration
- Multiple landing zone type support (GCP and PBMM-GCP)
- Automated Terraform variable file generation
- Cloud Build integration for deployment
- Progress monitoring for builds
- Configuration validation

## Prerequisites

- Python 3.7+
- Google Cloud SDK
- Terraform 1.6.0+
- Required Python packages:
  - pyyaml
  - google-cloud-devtools-cloudbuild
  - rich
  - jsonschema

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The tool provides three main commands:

### 1. Validate Configuration

Validates a YAML configuration file against the schema:

```bash
python3 src/main.py validate path/to/config.yaml [--landing-zone-type=<type>]
```

### 2. Convert YAML to Terraform Variables

Converts a YAML configuration to Terraform variables:

```bash
python3 src/main.py convert path/to/config.yaml path/to/output.tfvars [--common-only] [--landing-zone-type=<type>]
```

### 3. Deploy Configuration

Deploys a configuration using Cloud Build:

```bash
python3 src/main.py deploy path/to/config.yaml --project-id=<project-id> [--progress] [--landing-zone-type=<type>]
```

### Common Options

- `--landing-zone-type`: Specify the landing zone type (choices: 'pbmm-gcp', 'gcp')
- `--progress`: Show build progress (for deploy command)
- `--common-only`: Extract only common configuration (for convert command)

## Configuration Examples

### Standard GCP Landing Zone

```yaml
version: "1.0"
landing_zone:
  type: "gcp"

bootstrap:
  org_id: "123456789012"
  billing_account: "ABC123-DEF456-GHI789"
  default_region: "us-central1"

org:
  parent_folder: "folders/987654321"
  scc_notification_name: "security-alerts"

environments:
  - name: "development"
    environment_code: "d"
  - name: "production"
    environment_code: "p"

# ... additional configuration ...
```

### PBMM GCP Landing Zone

```yaml
version: "1.0"
landing_zone:
  type: "pbmm-gcp"

bootstrap:
  org_id: "123456789012"
  billing_account: "ABC123-DEF456-GHI789"
  default_region: "northamerica-northeast1"
  groups:
    create_required_groups: true
    required_groups:
      group_org_admins: "gcp-organization-admins@example.com"
      # ... additional groups ...

# ... additional configuration ...
```

## Directory Structure

```
.
├── src/
│   ├── main.py
│   └── config/
│       ├── validator.py
│       └── lz_schemas/
│           ├── base.py
│           ├── gcp.py
│           └── pbmm_gcp.py
├── landing-zones/
│   ├── gcp-landing-zone/
│   │   ├── cloudbuild.yaml
│   │   └── automation-scripts/
│   │       └── deploy.sh
│   └── pbmm-gcp/
│       ├── cloudbuild.yaml
│       └── automation-scripts/
│           └── deploy.sh
└── examples/
    ├── gcp_config.yaml
    └── pbmm_config.yaml
```

## Landing Zone Types

### Standard GCP Landing Zone
- Basic GCP organization structure
- Environment-based project organization
- Network and security controls
- Application infrastructure support

### PBMM GCP Landing Zone
- Enhanced security controls
- Business unit organization
- Compliance with Protected B, Medium Integrity, Medium Availability (PBMM)
- Additional security groups and IAM controls
- Fortigate integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here] 