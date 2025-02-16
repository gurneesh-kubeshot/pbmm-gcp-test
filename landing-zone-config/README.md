# Landing Zone Configuration Tool

A tool for validating and managing landing zone configurations.

## Installation

### Development Installation
```bash
# Clone the repository
git clone <repository-url>
cd landing-zone-config

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Production Installation
```bash
pip install .
```

## Usage

### Validating a Configuration
```bash
# Using the installed command
lz-config validate path/to/config.yaml

# Or running directly
python src/main.py validate path/to/config.yaml
```

### Example Configuration
See the `examples/pbmm_config.yaml` for a complete example configuration.

## Development

### Running Tests
```bash
pip install pytest
pytest tests/
```

### Project Structure
```
landing-zone-config/
├── src/
│   ├── config/
│   │   ├── schema.py        # YAML schema definitions
│   │   └── validator.py     # Configuration validator
│   └── main.py             # CLI entry point
├── tests/
│   └── test_validator.py   # Validator tests
└── examples/
    └── pbmm_config.yaml    # Example configuration
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests
5. Submit a pull request

## License
[Your chosen license] 