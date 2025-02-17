"""Base schema that all landing zone configurations must follow."""

BASE_SCHEMA = {
    "type": "object",
    "required": ["version", "landing_zone"],
    "properties": {
        "version": {
            "type": "string",
            "pattern": "^\\d+\\.\\d+$"
        },
        "landing_zone": {
            "type": "object",
            "required": ["type"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["pbmm-gcp", "gcp"]
                }
            }
        }
    }
} 