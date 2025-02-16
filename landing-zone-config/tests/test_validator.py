"""Tests for the configuration validator."""

import os
import pytest
from jsonschema import ValidationError

from src.config.validator import ConfigValidator


def test_valid_config():
    """Test that a valid configuration passes validation."""
    validator = ConfigValidator()
    config_path = os.path.join(os.path.dirname(__file__), 
                              '../examples/pbmm_config.yaml')
    config = validator.validate_file(config_path)
    assert config['version'] == '1.0'
    assert config['landing_zone']['type'] == 'pbmm-gcp'


def test_invalid_version():
    """Test that an invalid version fails validation."""
    validator = ConfigValidator()
    invalid_config = {
        'version': 'invalid',
        'landing_zone': {'type': 'pbmm-gcp'}
    }
    with pytest.raises(ValidationError) as exc_info:
        validator.validate_config(invalid_config)
    assert 'version' in str(exc_info.value)


def test_missing_required_field():
    """Test that missing required fields fail validation."""
    validator = ConfigValidator()
    invalid_config = {
        'version': '1.0',
        'landing_zone': {'type': 'pbmm-gcp'}
        # Missing required fields
    }
    with pytest.raises(ValidationError) as exc_info:
        validator.validate_config(invalid_config)
    assert 'required' in str(exc_info.value)


def test_invalid_email():
    """Test that invalid email formats fail validation."""
    validator = ConfigValidator()
    invalid_config = {
        'version': '1.0',
        'landing_zone': {'type': 'pbmm-gcp'},
        'bootstrap': {
            'org_id': '123456789012',
            'billing_account': 'ABCDEF-GHIJKL-MNOPQR',
            'default_region': 'northamerica-northeast1',
            'groups': {
                'create_required_groups': True,
                'create_optional_groups': True,
                'billing_project': 'my-project',
                'required_groups': {
                    'group_org_admins': 'invalid-email',  # Invalid email
                    'group_billing_admins': 'gcp-billing-admins@example.com',
                    'billing_data_users': 'gcp-billing-data@example.com',
                    'audit_data_users': 'gcp-audit-data@example.com',
                    'monitoring_workspace_users': 'gcp-monitoring@example.com'
                },
                'optional_groups': {
                    'gcp_security_reviewer': 'gcp-security@example.com',
                    'gcp_network_viewer': 'gcp-network@example.com',
                    'gcp_scc_admin': 'gcp-scc@example.com',
                    'gcp_global_secrets_admin': 'gcp-secrets@example.com',
                    'gcp_kms_admin': 'gcp-kms@example.com'
                }
            }
        }
    }
    with pytest.raises(ValidationError) as exc_info:
        validator.validate_config(invalid_config)
    assert 'email' in str(exc_info.value) 