variable "project_id" {
  type        = string
  description = "デプロイ先の GCP プロジェクト ID"
}

variable "region" {
  type        = string
  description = "Cloud Run / VPC を作成するリージョン"
  default     = "asia-northeast1"
}

variable "service_name" {
  type        = string
  description = "Cloud Run サービス名"
  default     = "fastapi-todo"
}

variable "artifact_repo_name" {
  type        = string
  description = "Artifact Registry のリポジトリ名（例: app）"
  default     = "app"
}

variable "image_tag" {
  type        = string
  description = "コンテナイメージのタグ（例: latest, v1.0.0 など）"
  default     = "latest"
}

variable "otel_secret_name" {
  type        = string
  description = "Collector 用 config を格納した Secret Manager のシークレット名"
  default     = "otel-collector-config"
}

variable "environment" {
  type        = string
  description = "ENVIRONMENT 環境変数に入れる値 (dev / staging / prod など)"
  default     = "dev"
}

variable "service_label_env" {
  type        = string
  description = "Cloud Run サービスに付与する env ラベル値"
  default     = "dev"
}

variable "network_name" {
  type        = string
  description = "VPC ネットワーク名"
  default     = "main-vpc"
}

variable "subnet_name" {
  type        = string
  description = "アプリ用サブネットの名前"
  default     = "main-subnet"
}

variable "subnet_ip_cidr_range" {
  type        = string
  description = "アプリ用サブネットの CIDR (例: 10.0.0.0/24)"
  default     = "10.0.0.0/24"
}
