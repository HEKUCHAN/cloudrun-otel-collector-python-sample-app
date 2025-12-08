terraform {
  required_version = ">= 1.14.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 7.12.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "network" {
  source = "./modules/network"

  project_id           = var.project_id
  region               = var.region
  network_name         = var.network_name
  subnet_name          = var.subnet_name
  subnet_ip_cidr_range = var.subnet_ip_cidr_range
}

module "cloudrun" {
  source = "./modules/cloudrun"

  project_id         = var.project_id
  region             = var.region
  service_name       = var.service_name
  artifact_repo_name = var.artifact_repo_name
  image_tag          = var.image_tag
  otel_secret_name   = var.otel_secret_name
  environment        = var.environment
  service_label_env  = var.service_label_env

  network_name    = module.network.network_name
  subnetwork_name = module.network.subnetwork_name
}
