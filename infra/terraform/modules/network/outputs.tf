output "network_self_link" {
  description = "作成された VPC ネットワークの self_link"
  value       = google_compute_network.main_app_vpc.self_link
}

output "network_name" {
  description = "VPC ネットワーク名（Cloud Run の vpc_access.network に渡せる）"
  value       = google_compute_network.main_app_vpc.name
}

output "subnetwork_self_link" {
  description = "作成されたサブネットの self_link"
  value       = google_compute_subnetwork.main_app_subnet.self_link
}

output "subnetwork_name" {
  description = "サブネット名（Cloud Run の vpc_access.subnetwork に渡せる）"
  value       = google_compute_subnetwork.main_app_subnet.name
}
