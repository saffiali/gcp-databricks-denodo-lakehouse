variable "project_id" { type = string }
variable "region" { type = string }
variable "environment" { type = string }
variable "resource_prefix" { type = string }
variable "vpc_id" { type = string }
variable "subnet_id" { type = string }
variable "denodo_machine_type" { type = string }
variable "denodo_cache_dataset_id" { type = string }
variable "lakehouse_bucket_name" { type = string }
variable "denodo_cache_bucket" { type = string }
variable "databricks_jdbc_url" { type = string }
variable "kms_crypto_key_id" { type = string }
variable "labels" { type = map(string) }

# -----------------------------------------------------------------------------
# 1. Dedicated Denodo 8.0 VDP Service Account & Least-Privilege Cache IAM
# -----------------------------------------------------------------------------
resource "google_service_account" "denodo_vdp_sa" {
  account_id   = "${var.resource_prefix}-denodo-vdp-${var.environment}"
  display_name = "Denodo 8.0 Virtual DataPort Service Account"
  project      = var.project_id
}

# Allows Denodo VDP to execute BigQuery cache load/query jobs
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

# Bucket-scoped access for Denodo GCS Parquet/Delta Cache
resource "google_storage_bucket_iam_member" "denodo_delta_cache_admin" {
  bucket = var.denodo_cache_bucket
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# -----------------------------------------------------------------------------
# 2. Hardened Shielded VM Instance Template for Denodo 8.0 VDP Nodes
#    Private IP only (no public IP), Hyperdisk Balanced, CMEK encrypted
# -----------------------------------------------------------------------------
resource "google_compute_instance_template" "denodo_vdp_node_template" {
  name_prefix  = "${var.resource_prefix}-denodo-vdp-80-"
  project      = var.project_id
  region       = var.region
  machine_type = var.denodo_machine_type
  tags         = ["denodo-vdp-node"]
  labels       = var.labels

  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }

  disk {
    source_image = "projects/debian-cloud/global/images/family/debian-12"
    auto_delete  = true
    boot         = true
    disk_type    = "hyperdisk-balanced"
    disk_size_gb = 200

    disk_encryption_key {
      kms_key_self_link = var.kms_crypto_key_id
    }
  }

  network_interface {
    network    = var.vpc_id
    subnetwork = var.subnet_id
    # Omit access_config block to enforce 100% private IP (zero public IP exposure)
  }

  service_account {
    email  = google_service_account.denodo_vdp_sa.email
    scopes = ["cloud-platform"]
  }

  metadata = {
    DENODO_VDP_VERSION      = "8.0.202409"
    DATABRICKS_JDBC_URL     = var.databricks_jdbc_url
    BIGQUERY_CACHE_DATASET  = "${var.project_id}.${var.denodo_cache_dataset_id}"
    DELTA_CACHE_GCS_URI     = "gs://${var.lakehouse_bucket_name}/denodo_cache/"
    ENABLE_STORAGE_READ_API = "true"
  }
}

# -----------------------------------------------------------------------------
# 3. Regional Managed Instance Group (HA Multi-Zone) & Internal Load Balancer
# -----------------------------------------------------------------------------
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

resource "google_compute_region_instance_group_manager" "denodo_vdp_mig" {
  name                      = "${var.resource_prefix}-denodo-vdp-mig-${var.region}"
  project                   = var.project_id
  region                    = var.region
  base_instance_name        = "${var.resource_prefix}-denodo-vdp"
  distribution_policy_zones = ["${var.region}-a", "${var.region}-b"]
  target_size               = 2

  version {
    instance_template = google_compute_instance_template.denodo_vdp_node_template.id
  }

  auto_healing_policies {
    health_check      = google_compute_region_health_check.denodo_vdp_tcp_health_check.id
    initial_delay_sec = 300
  }
}

resource "google_compute_region_backend_service" "denodo_vdp_internal_lb" {
  name                  = "${var.resource_prefix}-denodo-vdp-ilb-${var.region}"
  project               = var.project_id
  region                = var.region
  protocol              = "TCP"
  load_balancing_scheme = "INTERNAL"
  health_checks         = [google_compute_region_health_check.denodo_vdp_tcp_health_check.id]

  backend {
    group          = google_compute_region_instance_group_manager.denodo_vdp_mig.instance_group
    balancing_mode = "CONNECTION"
  }
}

resource "google_compute_forwarding_rule" "denodo_vdp_forwarding_rule" {
  name                  = "${var.resource_prefix}-denodo-vdp-fwd-${var.region}"
  project               = var.project_id
  region                = var.region
  load_balancing_scheme = "INTERNAL"
  backend_service       = google_compute_region_backend_service.denodo_vdp_internal_lb.id
  ip_protocol           = "TCP"
  ports                 = ["9090", "9443", "9996", "9999"]
  network               = var.vpc_id
  subnetwork            = var.subnet_id
}

output "vdp_jdbc_endpoint" {
  value = "jdbc:vdb://denodo-vdp-internal.${var.region}.rd-lakehouse.internal:9999/rd_unified_vdb"
}

output "denodo_vdp_sa_email" {
  value = google_service_account.denodo_vdp_sa.email
}
