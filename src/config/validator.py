"""Validator for the landing zone configuration YAML."""

import yaml
from jsonschema import validate, ValidationError
from typing import Dict, Any

from .schema import LANDING_ZONE_SCHEMA


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
            validate(instance=config, schema=LANDING_ZONE_SCHEMA)
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
