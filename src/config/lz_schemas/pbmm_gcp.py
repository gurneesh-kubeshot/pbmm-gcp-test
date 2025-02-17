"""Schema definition for the PBMM GCP landing zone configuration."""

SCHEMA = {
    "type": "object",
    "required": ["bootstrap", "org", "environments", "networking", "projects", "app_infra", "org_policies", "fortigate"],
    "properties": {
        "bootstrap": {
            "type": "object",
            "required": ["org_id", "billing_account", "default_region", "groups"],
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
                },
                "groups": {
                    "type": "object",
                    "required": ["create_required_groups", "create_optional_groups", "billing_project", "required_groups", "optional_groups"],
                    "properties": {
                        "create_required_groups": {
                            "type": "boolean"
                        },
                        "create_optional_groups": {
                            "type": "boolean"
                        },
                        "billing_project": {
                            "type": "string"
                        },
                        "required_groups": {
                            "type": "object",
                            "required": [
                                "group_org_admins",
                                "group_billing_admins",
                                "billing_data_users",
                                "audit_data_users",
                                "monitoring_workspace_users"
                            ],
                            "properties": {
                                "group_org_admins": {
                                    "type": "string",
                                    "format": "email"
                                },
                                "group_billing_admins": {
                                    "type": "string",
                                    "format": "email"
                                },
                                "billing_data_users": {
                                    "type": "string",
                                    "format": "email"
                                },
                                "audit_data_users": {
                                    "type": "string",
                                    "format": "email"
                                },
                                "monitoring_workspace_users": {
                                    "type": "string",
                                    "format": "email"
                                }
                            }
                        },
                        "optional_groups": {
                            "type": "object",
                            "required": [
                                "gcp_security_reviewer",
                                "gcp_network_viewer",
                                "gcp_scc_admin",
                                "gcp_global_secrets_admin",
                                "gcp_kms_admin"
                            ],
                            "properties": {
                                "gcp_security_reviewer": {
                                    "type": "string",
                                    "format": "email"
                                },
                                "gcp_network_viewer": {
                                    "type": "string",
                                    "format": "email"
                                },
                                "gcp_scc_admin": {
                                    "type": "string",
                                    "format": "email"
                                },
                                "gcp_global_secrets_admin": {
                                    "type": "string",
                                    "format": "email"
                                },
                                "gcp_kms_admin": {
                                    "type": "string",
                                    "format": "email"
                                }
                            }
                        }
                    }
                }
            }
        },
        "org": {
            "type": "object",
            "required": ["parent_folder", "billing_data_users", "audit_data_users"],
            "properties": {
                "parent_folder": {
                    "type": "string"
                },
                "billing_data_users": {
                    "type": "string",
                    "format": "email"
                },
                "audit_data_users": {
                    "type": "string",
                    "format": "email"
                },
                "scc_notification_name": {
                    "type": "string"
                },
                "scc_notifications_filter": {
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
                    },
                    "monitoring": {
                        "type": "object",
                        "properties": {
                            "enable_monitoring": {
                                "type": "boolean"
                            },
                            "monitoring_workspace_users": {
                                "type": "string",
                                "format": "email"
                            }
                        }
                    }
                }
            }
        },
        "networking": {
            "type": "object",
            "required": ["enable_hub_and_spoke", "enable_vpn", "dns_enable_logging"],
            "properties": {
                "enable_hub_and_spoke": {
                    "type": "boolean"
                },
                "enable_vpn": {
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
        },
        "org_policies": {
            "type": "object",
            "required": ["policy_boolean", "policy_list"],
            "properties": {
                "policy_boolean": {
                    "type": "object",
                    "properties": {
                        "vmExternalIpAccess": {
                            "type": "boolean"
                        },
                        "skipDefaultNetworkCreation": {
                            "type": "boolean"
                        },
                        "disableSerialPortAccess": {
                            "type": "boolean"
                        },
                        "disableDefaultIamGrantsServiceAccounts": {
                            "type": "boolean"
                        }
                    }
                },
                "policy_list": {
                    "type": "object",
                    "properties": {
                        "restrictVpcPeering": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "restrictSharedVpcSubnetworks": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "restrictSharedVpcHostProjects": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        },
        "fortigate": {
            "type": "object",
            "required": ["enabled", "version"],
            "properties": {
                "enabled": {
                    "type": "boolean"
                },
                "version": {
                    "type": "string"
                },
                "license_type": {
                    "type": "string",
                    "enum": ["byol", "payg"]
                },
                "config": {
                    "type": "object",
                    "properties": {
                        "ha_enabled": {
                            "type": "boolean"
                        },
                        "regions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "machine_type": {
                            "type": "string"
                        },
                        "service_account": {
                            "type": "string",
                            "format": "email"
                        },
                        "networks": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["name", "cidr"],
                                "properties": {
                                    "name": {
                                        "type": "string"
                                    },
                                    "cidr": {
                                        "type": "string",
                                        "pattern": "^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}/\\d{1,2}$"
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