{
  "environment": "production",
  "projects": [
    {
      "name": "app-prod-project",
      "apis": [
        "compute.googleapis.com",
        "container.googleapis.com",
        "cloudbuild.googleapis.com"
      ],
      "labels": {
        "environment": "production",
        "application": "app1"
      }
    }
  ],
  "app_infra": {
    "environment": "production",
    "business_units": [
      {
        "name": "bu1",
        "gke_clusters": [
          {
            "name": "app-cluster-prod",
            "region": "us-central1",
            "network_config": {
              "network": "app-network",
              "subnetwork": "app-subnet",
              "ip_range_pods": "gke-pods-range",
              "ip_range_services": "gke-services-range"
            }
          }
        ]
      }
    ]
  }
}