variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "network_name" {
  type = string
}

variable "subnet_name" {
  type        = string
  description = "作成するサブネットの名前"
  default     = "main-subnet"
}

variable "subnet_ip_cidr_range" {
  type        = string
  description = "サブネットの CIDR (例: 10.0.0.0/24)"
  default     = "10.0.0.0/24"
}
