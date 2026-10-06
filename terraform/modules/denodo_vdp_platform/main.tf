variable "project_id" { type = string }
variable "region" { type = string }
variable "environment" { type = string }
variable "resource_prefix" { type = string }
variable "vpc_id" { type = string }
variable "subnet_id" { type = string }
variable "denodo_gke_master_cidr" { type = string }
variable "denodo_machine_type" { type = string }
variable "denodo_container_image_tag" { type = string }
variable "denodo_cache_dataset_id" { type = string }
variable "lakehouse_bucket_name" { type = string }
variable "denodo_cache_bucket" { type = string }
variable "databricks_jdbc_url" { type = string }
variable "kms_crypto_key_id" { type = string }
variable "labels" { type = map(string) }

# -----------------------------------------------------------------------------
# 1. Dedicated Denodo 8.0 VDP GCP Service Account & GKE Workload Identity
# -----------------------------------------------------------------------------
resource "google_service_account" "denodo_vdp_sa" {
  account_id   = "${var.resource_prefix}-denodo-vdp-${var.environment}"
  display_name = "Denodo 8.0 Trial Server on GKE Service Account (Workload Identity)"
  project      = var.project_id
}

# GKE Workload Identity Binding: Maps Kubernetes SA (denodo-trial/denodo-vdp-ksa)
# directly to the GCP Service Account with ZERO static JSON keys inside containers.
resource "google_service_account_iam_member" "denodo_gke_workload_identity" {
  service_account_id = google_service_account.denodo_vdp_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[denodo-trial/denodo-vdp-ksa]"
}

# Allows Denodo Trial Server on GKE to execute BigQuery cache load/query jobs
resource "google_project_iam_member" "denodo_bq_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# Enables high-throughput Simba BigQuery Storage Read API (EnableHighThroughputAPI=1)
resource "google_project_iam_member" "denodo_bq_read_session_user" {
  project = var.project_id
  role    = "roles/bigquery.readSessionUser"
  member  = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# Dataset-scoped write/read permissions STRICTLY on the Denodo Cache dataset
resource "google_bigquery_dataset_iam_member" "denodo_cache_data_editor" {
  project    = var.project_id
  dataset_id = var.denodo_cache_dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# Bucket-scoped access for Denodo GCS Parquet/Delta Cache & JDBC Driver Artifacts
resource "google_storage_bucket_iam_member" "denodo_delta_cache_admin" {
  bucket = var.denodo_cache_bucket
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# -----------------------------------------------------------------------------
# 2. Private Google Artifact Registry for Denodo Trial Container & Helm Charts
#    Mirrors harbor.open.denodo.com/denodo-8.0/images/denodo-platform inside VPC-SC
# -----------------------------------------------------------------------------
resource "google_artifact_registry_repository" "denodo_trial_repo" {
  location      = var.region
  project       = var.project_id
  repository_id = "${var.resource_prefix}-denodo-trial"
  description   = "Private Docker/OCI Artifact Registry mirroring Denodo 8.0 Trial Server images & Helm charts from harbor.open.denodo.com"
  format        = "DOCKER"
  kms_key_name  = var.kms_crypto_key_id
  labels        = var.labels
}

resource "google_artifact_registry_repository_iam_member" "denodo_gke_image_puller" {
  project    = var.project_id
  location   = google_artifact_registry_repository.denodo_trial_repo.location
  repository = google_artifact_registry_repository.denodo_trial_repo.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# -----------------------------------------------------------------------------
# 3. Cloud Secret Manager Secrets for Denodo 30-Day Trial License & Harbor Auth
# -----------------------------------------------------------------------------
resource "google_secret_manager_secret" "denodo_trial_license" {
  secret_id = "${var.resource_prefix}-denodo-trial-license"
  project   = var.project_id
  labels    = var.labels

  replication {
    user_managed {
      replicas {
        location = var.region
        customer_managed_encryption {
          kms_key_name = var.kms_crypto_key_id
        }
      }
    }
  }
}

resource "google_secret_manager_secret" "denodo_harbor_cli_secret" {
  secret_id = "${var.resource_prefix}-denodo-harbor-cli-secret"
  project   = var.project_id
  labels    = var.labels

  replication {
    user_managed {
      replicas {
        location = var.region
        customer_managed_encryption {
          kms_key_name = var.kms_crypto_key_id
        }
      }
    }
  }
}

resource "google_secret_manager_secret" "denodo_admin_password" {
  secret_id = "${var.resource_prefix}-denodo-vdp-admin-pwd"
  project   = var.project_id
  labels    = var.labels

  replication {
    user_managed {
      replicas {
        location = var.region
        customer_managed_encryption {
          kms_key_name = var.kms_crypto_key_id
        }
      }
    }
  }
}

resource "google_secret_manager_secret_iam_member" "denodo_license_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.denodo_trial_license.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "denodo_admin_pwd_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.denodo_admin_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# -----------------------------------------------------------------------------
# 4. Private Regional GKE Cluster for Denodo 8.0 Trial Server
#    Deployed in Subnet B (snet-denodo-vdp 10.169.0.0/22) with Dataplane V2,
#    Shielded GKE Nodes, Workload Identity & CMEK Boot Disk Encryption
# -----------------------------------------------------------------------------
resource "google_container_cluster" "denodo_trial_gke" {
  name                     = "${var.resource_prefix}-denodo-trial-gke-${var.region}"
  project                  = var.project_id
  location                 = var.region
  network                  = var.vpc_id
  subnetwork               = var.subnet_id
  remove_default_node_pool = true
  initial_node_count       = 1
  networking_mode          = "VPC_NATIVE"
  datapath_provider        = "ADVANCED_DATAPATH" # GKE Dataplane V2 (eBPF / Cilium)
  resource_labels          = var.labels

  ip_allocation_policy {
    cluster_secondary_range_name  = "denodo-gke-pods-range"
    services_secondary_range_name = "denodo-gke-services-range"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = var.denodo_gke_master_cidr
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  database_encryption {
    state    = "ENCRYPTED"
    key_name = var.kms_crypto_key_id
  }

  release_channel {
    channel = "REGULAR"
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
    gce_persistent_disk_csi_driver_config {
      enabled = true
    }
  }
}

# -----------------------------------------------------------------------------
# 5. Hardened Next-Gen N4 Node Pool for Denodo 8.0 Trial StatefulSet Pods
#    (2x n4-standard-8 across Zones a & b, Shielded VM + Hyperdisk Balanced)
# -----------------------------------------------------------------------------
resource "google_container_node_pool" "denodo_vdp_node_pool" {
  name               = "${var.resource_prefix}-denodo-vdp-pool"
  project            = var.project_id
  location           = var.region
  cluster            = google_container_cluster.denodo_trial_gke.name
  node_locations     = ["${var.region}-a", "${var.region}-b"]
  initial_node_count = 1 # 1 per zone = 2 HA nodes for Denodo Trial Server + Design Studio

  autoscaling {
    min_node_count = 1
    max_node_count = 2
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    machine_type    = var.denodo_machine_type # n4-standard-8 (8 vCPU, 32 GB RAM)
    disk_type       = "hyperdisk-balanced"
    disk_size_gb    = 200
    boot_disk_kms_key = var.kms_crypto_key_id
    service_account = google_service_account.denodo_vdp_sa.email
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]
    tags            = ["denodo-gke-node", "denodo-vdp-node"]

    labels = merge(var.labels, {
      workload         = "denodo-vdp-trial"
      denodo_version   = "8-0-trial"
      databricks_ready = "true"
      bq_cache_enabled = "true"
    })

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    metadata = {
      disable-legacy-endpoints = "true"
      DENODO_VDP_VERSION       = var.denodo_container_image_tag
      DATABRICKS_JDBC_URL      = var.databricks_jdbc_url
      BIGQUERY_CACHE_DATASET   = "${var.project_id}.${var.denodo_cache_dataset_id}"
      DELTA_CACHE_GCS_URI      = "gs://${var.lakehouse_bucket_name}/denodo_cache/"
      ENABLE_STORAGE_READ_API  = "true"
    }
  }
}

# -----------------------------------------------------------------------------
# 6. Static Internal IP & Passthrough NLB Health Check for Denodo on GKE
#    Bound by Kubernetes Service (networking.gke.io/load-balancer-type: "Internal")
#    Exposes TCP :9999 (JDBC), :9996 (ODBC), :9090 (Design Studio/Catalog), :9443 (HTTPS)
# -----------------------------------------------------------------------------
resource "google_compute_address" "denodo_gke_ilb_ip" {
  name         = "${var.resource_prefix}-denodo-gke-ilb-ip"
  project      = var.project_id
  region       = var.region
  subnetwork   = var.subnet_id
  address_type = "INTERNAL"
  purpose      = "GCE_ENDPOINT"
  description  = "Static internal VIP in snet-denodo-vdp for the GKE Denodo Trial Server Internal LoadBalancer (:9999, :9996, :9090, :9443)"
}

resource "google_compute_region_health_check" "denodo_vdp_tcp_health_check" {
  name                = "${var.resource_prefix}-denodo-vdp-hc-${var.region}"
  project             = var.project_id
  region              = var.region
  check_interval_sec  = 15
  timeout_sec         = 5
  healthy_threshold   = 2
  unhealthy_threshold = 3

  tcp_health_check {
    port = 9999
  }
}

output "denodo_gke_cluster_name" {
  value = google_container_cluster.denodo_trial_gke.name
}

output "denodo_artifact_registry_uri" {
  value = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.denodo_trial_repo.repository_id}/denodo-platform:${var.denodo_container_image_tag}"
}

output "denodo_internal_lb_ip" {
  value = google_compute_address.denodo_gke_ilb_ip.address
}

output "vdp_jdbc_endpoint" {
  value = "jdbc:vdb://denodo-vdp-internal.${var.region}.rd-lakehouse.internal:9999/rd_unified_vdb"
}

output "vdp_design_studio_url" {
  value = "http://denodo-vdp-internal.${var.region}.rd-lakehouse.internal:9090/denodo-design-studio/#/uri=//denodo-vdp-trial-0.denodo-vdp-headless.denodo-trial.svc.cluster.local:9999/"
}

output "vdp_data_catalog_url" {
  value = "http://denodo-vdp-internal.${var.region}.rd-lakehouse.internal:9090/denodo-data-catalog"
}

output "denodo_vdp_sa_email" {
  value = google_service_account.denodo_vdp_sa.email
}
