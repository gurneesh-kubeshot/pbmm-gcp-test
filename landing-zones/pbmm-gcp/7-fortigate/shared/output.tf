#
# Output  
#
output "External-Load-Balancer-Public-IP-Address" {
  value = google_compute_address.static.address
}

output "Internal-Load-Balancer-Public-IP-Address" {
  value = google_compute_address.internal_address.address
}

output "FortiGate-HA-Active-MGMT-IP" {
  value = google_compute_instance_from_template.active_fgt_instance.network_interface
}

output "FortiGate-HA-Passive-MGMT-IP" {
   value = google_compute_instance_from_template.passive_fgt_instance.network_interface
}

output "FortiGate-Username" {
  value = "admin"
}

output "FortiGate-Password" {
  value = google_compute_instance_from_template.active_fgt_instance.instance_id
}
