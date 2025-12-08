output "service_uri" {
  description = "Cloud Run サービスの URL"
  value       = google_cloud_run_v2_service.todo_app_cloud_run_service.uri
}

output "app_image" {
  description = "Cloud Run で使用しているコンテナイメージ"
  value       = local.app_image
}
