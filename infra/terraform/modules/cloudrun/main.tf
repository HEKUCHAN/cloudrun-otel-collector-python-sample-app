locals {
  app_image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_repo_name}/${var.service_name}:${var.image_tag}"
}

resource "google_artifact_registry_repository" "todo_app_repo" {
  location      = var.region
  repository_id = var.artifact_repo_name
  description   = "Container images for ${var.service_name}"
  format        = "DOCKER"
}

resource "google_service_account" "cloud_run_todo_app_sa" {
  account_id   = "cr-${var.service_name}"
  display_name = "Cloud Run service account for ${var.service_name}"
}

resource "google_secret_manager_secret" "otel_collector_config" {
  secret_id = var.otel_secret_name

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "otel_collector_config_version" {
  secret      = google_secret_manager_secret.otel_collector_config.id
  secret_data = file("${path.root}/../../otel/collector-config.yaml")
}

resource "google_secret_manager_secret_iam_binding" "otel_config_accessor_for_cloud_run_todo_app_sa" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.otel_collector_config.secret_id
  role      = "roles/secretmanager.secretAccessor"

  members = [
    "serviceAccount:${google_service_account.cloud_run_todo_app_sa.email}",
  ]

  depends_on = [google_secret_manager_secret.otel_collector_config]
}

resource "google_project_iam_binding" "artifact_registry_reader_for_cloud_run_todo_app_sa" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"

  members = [
    "serviceAccount:${google_service_account.cloud_run_todo_app_sa.email}",
  ]
}

resource "google_cloud_run_v2_service_iam_member" "public_access_todo_app_cloud_run_service" {
  project  = google_cloud_run_v2_service.todo_app_cloud_run_service.project
  location = google_cloud_run_v2_service.todo_app_cloud_run_service.location
  name     = google_cloud_run_v2_service.todo_app_cloud_run_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}


resource "google_cloud_run_v2_service" "todo_app_cloud_run_service" {
  name     = var.service_name
  location = var.region

  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.cloud_run_todo_app_sa.email

    annotations = {
      "run.googleapis.com/container-dependencies" = "{app:[collector]}"
      "run.googleapis.com/execution-environment"  = "gen2"
    }

    labels = {
      env = var.service_label_env
    }

    vpc_access {
      egress = "PRIVATE_RANGES_ONLY"

      network_interfaces {
        network    = var.network_name
        subnetwork = var.subnetwork_name
      }
    }

    containers {
      name  = "app"
      image = local.app_image

      ports {
        container_port = 8080
      }

      env {
        name  = "OTEL_EXPORTER_OTLP_ENDPOINT"
        value = "http://localhost:4317"
      }

      env {
        name  = "OTEL_EXPORTER_OTLP_INSECURE"
        value = "true"
      }

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }

      env {
        name  = "SERVICE_NAME"
        value = var.service_name
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }

    containers {
      name  = "collector"
      image = "us-docker.pkg.dev/cloud-ops-agents-artifacts/google-cloud-opentelemetry-collector/otelcol-google:0.137.0"

      args = [
        "--config=/etc/otelcol-google/config.yaml",
      ]

      volume_mounts {
        name       = "collector-config"
        mount_path = "/etc/otelcol-google"
      }

      startup_probe {
        http_get {
          path = "/"
          port = 13133
        }
        initial_delay_seconds = 10
        period_seconds        = 10
        timeout_seconds       = 10
        failure_threshold     = 10
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }

    volumes {
      name = "collector-config"

      secret {
        secret = google_secret_manager_secret.otel_collector_config.secret_id

        items {
          version = "latest"
          path    = "config.yaml"
        }
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 1
    }

    timeout = "60s"
  }

  # WARNIG: 本番環境で運用する場合は true に設定することを強く推奨します。
  deletion_protection = false

  depends_on = [
    google_artifact_registry_repository.todo_app_repo,
    google_secret_manager_secret_version.otel_collector_config_version,
  ]
}
