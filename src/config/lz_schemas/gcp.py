"""Schema definition for the basic GCP landing zone configuration."""

SCHEMA = {
    "type": "object",
    "required": ["bootstrap", "org", "environments", "networking", "projects", "app_infra"],
    "properties": {
        "bootstrap": {
            "type": "object",
            "required": ["org_id", "billing_account", "default_region"],
            "properties": {
                "org_id": {
                    "type": "string",
                    "pattern": "^\\d{12}$"
                },
                "billing_account": {
                    "type": "string",
                    "pattern": "^[A-Z0-9]{6}-[A-Z0-9]{6}-[A-Z0-9]{6}$"
                },
                "default_region": {
                    "type": "string"
                }
            }
        },
        "org": {
            "type": "object",
            "required": ["parent_folder"],
            "properties": {
                "parent_folder": {
                    "type": "string"
                },
                "scc_notification_name": {
                    "type": "string"
                }
            }
        },
        "environments": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["name", "environment_code"],
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": ["development", "non-production", "production"]
                    },
                    "environment_code": {
                        "type": "string",
                        "enum": ["d", "n", "p"]
                    }
                }
            }
        },
        "networking": {
            "type": "object",
            "required": ["enable_hub_and_spoke", "dns_enable_logging"],
            "properties": {
                "enable_hub_and_spoke": {
                    "type": "boolean"
                },
                "dns_enable_logging": {
                    "type": "boolean"
                },
                "shared_vpc_host_project_id": {
                    "type": "string"
                }
            }
        },
        "projects": {
            "type": "object",
            "required": ["common", "environments"],
            "properties": {
                "common": {
                    "type": "object",
                    "properties": {
                        "billing_account": {
                            "type": "string",
                            "pattern": "^[A-Z0-9]{6}-[A-Z0-9]{6}-[A-Z0-9]{6}$"
                        },
                        "parent_folder": {
                            "type": "string",
                            "pattern": "^folders/[0-9]+$"
                        }
                    }
                },
                "environments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["environment", "projects"],
                        "properties": {
                            "environment": {
                                "type": "string",
                                "enum": ["development", "non-production", "production"]
                            },
                            "projects": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["name", "apis", "labels"],
                                    "properties": {
                                        "name": {
                                            "type": "string"
                                        },
                                        "apis": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            }
                                        },
                                        "labels": {
                                            "type": "object",
                                            "additionalProperties": {
                                                "type": "string"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "app_infra": {
            "type": "object",
            "required": ["environments"],
            "properties": {
                "environments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["environment", "business_units"],
                        "properties": {
                            "environment": {
                                "type": "string",
                                "enum": ["development", "non-production", "production"]
                            },
                            "business_units": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["name", "gke_clusters"],
                                    "properties": {
                                        "name": {
                                            "type": "string"
                                        },
                                        "gke_clusters": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "required": ["name", "region", "network_config"],
                                                "properties": {
                                                    "name": {
                                                        "type": "string"
                                                    },
                                                    "region": {
                                                        "type": "string"
                                                    },
                                                    "network_config": {
                                                        "type": "object",
                                                        "required": ["network", "subnetwork", "ip_range_pods", "ip_range_services"],
                                                        "properties": {
                                                            "network": {
                                                                "type": "string"
                                                            },
                                                            "subnetwork": {
                                                                "type": "string"
                                                            },
                                                            "ip_range_pods": {
                                                                "type": "string"
                                                            },
                                                            "ip_range_services": {
                                                                "type": "string"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
} 