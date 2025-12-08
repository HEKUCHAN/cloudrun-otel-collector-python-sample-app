output "cloud_run_service_uri" {
  description = "デプロイされた Cloud Run サービスの URL"
  value       = module.cloudrun.service_uri
}

output "cloud_run_app_image" {
  description = "Cloud Run で使用しているコンテナイメージ"
  value       = module.cloudrun.app_image
}

output "vpc_network_self_link" {
  description = "作成された VPC ネットワークの self_link"
  value       = module.network.network_self_link
}

output "vpc_subnetwork_self_link" {
  description = "作成されたサブネットの self_link"
  value       = module.network.subnetwork_self_link
}

output "vpc_network_name" {
  description = "VPC ネットワーク名（Cloud Run の vpc_access.network に渡している値）"
  value       = module.network.network_name
}

output "vpc_subnetwork_name" {
  description = "サブネット名（Cloud Run の vpc_access.subnetwork に渡している値）"
  value       = module.network.subnetwork_name
}
