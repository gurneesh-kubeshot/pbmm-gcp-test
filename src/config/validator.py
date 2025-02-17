"""Validator for the landing zone configuration YAML."""

import yaml
from jsonschema import validate, ValidationError
from typing import Dict, Any

from .lz_schemas.base import BASE_SCHEMA
from .lz_schemas.pbmm_gcp import SCHEMA as PBMM_GCP_SCHEMA
from .lz_schemas.gcp import SCHEMA as GCP_SCHEMA

# Registry of landing zone schemas
LANDING_ZONE_SCHEMAS = {
    "pbmm-gcp": PBMM_GCP_SCHEMA,
    "gcp": GCP_SCHEMA
}

class ConfigValidator:
    """Validator for the landing zone configuration."""

    @staticmethod
    def load_yaml(config_path: str) -> Dict[str, Any]:
        """Load YAML configuration from file.

        Args:
            config_path: Path to the YAML configuration file.

        Returns:
            Dict containing the configuration.

        Raises:
            yaml.YAMLError: If the YAML file is invalid.
            FileNotFoundError: If the configuration file is not found.
        """
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML file: {str(e)}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

    def validate_config(self, config: Dict[str, Any]) -> None:
        """Validate the configuration against the schema.

        Args:
            config: Dictionary containing the configuration.

        Raises:
            ValidationError: If the configuration is invalid.
        """
        try:
            # First validate against base schema
            validate(instance=config, schema=BASE_SCHEMA)
            
            # Get the landing zone type
            lz_type = config["landing_zone"]["type"]
            
            # Get the specific schema for this landing zone type
            if lz_type not in LANDING_ZONE_SCHEMAS:
                raise ValidationError(f"Unsupported landing zone type: {lz_type}")
            
            # Validate against the specific landing zone schema
            validate(instance=config, schema=LANDING_ZONE_SCHEMAS[lz_type])
            
        except ValidationError as e:
            # Create a more user-friendly error message
            path = " -> ".join(str(p) for p in e.path)
            message = f"Validation error in {path}: {e.message}"
            raise ValidationError(message)

    def validate_file(self, config_path: str) -> Dict[str, Any]:
        """Load and validate a configuration file.

        Args:
            config_path: Path to the YAML configuration file.

        Returns:
            Dict containing the validated configuration.

        Raises:
            ValidationError: If the configuration is invalid.
            ValueError: If the YAML file is invalid.
            FileNotFoundError: If the configuration file is not found.
        """
        config = self.load_yaml(config_path)
        self.validate_config(config)
        return config
