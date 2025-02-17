{
  "environment": "development",
  "projects": [
    {
      "name": "app-dev-project",
      "apis": [
        "compute.googleapis.com",
        "container.googleapis.com"
      ],
      "labels": {
        "environment": "development",
        "application": "app1"
      }
    }
  ],
  "app_infra": {
    "environment": "development",
    "business_units": [
      {
        "name": "bu1",
        "gke_clusters": [
          {
            "name": "app-cluster-dev",
            "region": "us-central1",
            "network_config": {
              "network": "app-network",
              "subnetwork": "app-subnet",
              "ip_range_pods": "10.0.0.0/16",
              "ip_range_services": "10.1.0.0/16"
            }
          }
        ]
      }
    ]
  }
}