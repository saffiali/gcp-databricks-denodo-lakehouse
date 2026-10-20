variable "project_id" { type = string }
variable "region" { type = string }
variable "environment" { type = string }
variable "resource_prefix" { type = string }
variable "vpc_id" { type = string }
variable "subnet_id" { type = string }
variable "denodo_source_image" {
  type    = string
  default = "projects/rhel-cloud/global/images/family/rhel-9"
}
variable "denodo_machine_type" { type = string }
variable "denodo_vmss_min_replicas" { type = number }
variable "denodo_vmss_max_replicas" { type = number }
variable "denodo_vmss_target_cpu" { type = number }
variable "denodo_cache_dataset_id" { type = string }
variable "lakehouse_bucket_name" { type = string }
variable "denodo_cache_bucket" { type = string }
variable "databricks_jdbc_url" { type = string }
variable "kms_crypto_key_id" { type = string }
variable "labels" { type = map(string) }

# -----------------------------------------------------------------------------
# 1. Dedicated Least-Privilege GCP Service Account for Denodo 9.0 VM Scale Set
#    Zero Static Keys: Attached natively to Shielded VMs in the Regional MIG
# -----------------------------------------------------------------------------
resource "google_service_account" "denodo_vdp_sa" {
  account_id   = "${var.resource_prefix}-denodo-vdp-${var.environment}"
  project      = var.project_id
  display_name = "Denodo 9.0 VM Scale Set Service Account (Base OS Image + Databricks JDBC + BigQuery Cache)"
}

# Project-level BigQuery Job & High-Throughput StorageReadAPI roles
resource "google_project_iam_member" "denodo_bq_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

resource "google_project_iam_member" "denodo_bq_read_session_user" {
  project = var.project_id
  role    = "roles/bigquery.readSessionUser"
  member  = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# Dataset-scoped Data Editor role ONLY on the Denodo Cache Dataset (denodo_vdp_cache)
resource "google_bigquery_dataset_iam_member" "denodo_bq_cache_dataset_editor" {
  project    = var.project_id
  dataset_id = var.denodo_cache_dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# Bucket-scoped Object Admin ONLY on the Denodo Cache & Installer Staging Bucket
resource "google_storage_bucket_iam_member" "denodo_delta_cache_bucket_admin" {
  bucket = var.denodo_cache_bucket
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# -----------------------------------------------------------------------------
# 2. Cloud Secret Manager (CMEK): Denodo 9.0 BYOL License & VDP Admin Password
#    Pulled at boot by the Base OS VM startup script to run the unattended
#    Denodo 9.0 silent installer (`installer_cli.sh install --xml ...`).
# -----------------------------------------------------------------------------
resource "google_secret_manager_secret" "denodo_license" {
  secret_id = "${var.resource_prefix}-denodo-license"
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

resource "google_secret_manager_secret" "denodo_vdp_admin_password" {
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

resource "google_secret_manager_secret_iam_member" "denodo_license_secret_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.denodo_license.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "denodo_admin_pwd_secret_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.denodo_vdp_admin_password.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.denodo_vdp_sa.email}"
}

# -----------------------------------------------------------------------------
# 3. Shielded VM Instance Template for Denodo 9.0 VM Scale Set on Base OS Images
#    - Boots from a hardened Enterprise Linux Base OS Image (var.denodo_source_image,
#      defaulting to `projects/rhel-cloud/global/images/family/rhel-9` or custom
#      CIS-hardened golden base image — NOT a Marketplace PAYG appliance).
#    - Runs `install_denodo_vmss_startup.sh` to install OpenJDK 17, pull the
#      Denodo 9.0 installer archive + Simba Spark/BQ JDBC drivers from GCS,
#      execute `installer_cli.sh install --xml denodo_silent_install.xml`,
#      configure BigQuery Native Cache (`EnableHighThroughputAPI=1`), and import VQL.
# -----------------------------------------------------------------------------
resource "google_compute_instance_template" "denodo_vmss_template" {
  name_prefix  = "${var.resource_prefix}-denodo-vmss-tpl-"
  project      = var.project_id
  region       = var.region
  machine_type = var.denodo_machine_type
  tags         = ["denodo-vdp-node"]

  labels = merge(var.labels, {
    component        = "denodo-vdp-vm-scaleset"
    denodo_build     = "9-0-base-image"
    databricks_ready = "true"
    bq_cache_enabled = "true"
  })

  disk {
    source_image = var.denodo_source_image
    auto_delete  = true
    boot         = true
    disk_type    = "hyperdisk-balanced"
    disk_size_gb = 200

    disk_encryption_key {
      kms_key_self_link = var.kms_crypto_key_id
    }
  }

  # Private VPC interface in snet-denodo-vdp (Zero Public IPs)
  network_interface {
    network    = var.vpc_id
    subnetwork = var.subnet_id
  }

  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }

  metadata = {
    enable-oslogin             = "TRUE"
    block-project-ssh-keys     = "TRUE"
    DENODO_VERSION             = "9.0"
    DENODO_INSTALLER_GCS_URI   = "gs://${var.denodo_cache_bucket}/installers"
    DENODO_LICENSE_SECRET_ID   = google_secret_manager_secret.denodo_license.secret_id
    DENODO_ADMIN_PWD_SECRET_ID = google_secret_manager_secret.denodo_vdp_admin_password.secret_id
    DATABRICKS_JDBC_URL        = var.databricks_jdbc_url
    BIGQUERY_CACHE_DATASET     = "${var.project_id}.${var.denodo_cache_dataset_id}"
    DELTA_CACHE_GCS_URI        = "gs://${var.denodo_cache_bucket}/vdp_cached_views/"
    ENABLE_STORAGE_READ_API    = "true"
  }

  metadata_startup_script = file("${path.module}/../../../scripts/install_denodo_vmss_startup.sh")

  service_account {
    email  = google_service_account.denodo_vdp_sa.email
    scopes = ["cloud-platform"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

# -----------------------------------------------------------------------------
# 4. Regional Managed Instance Group (VM Scale Set) + Regional Autoscaler
#    Distributes Shielded n4-standard-8 VMs across 3 availability zones with
#    auto-healing on TCP :9999 and CPU-based horizontal autoscaling (2..6 VMs)
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

resource "google_compute_region_instance_group_manager" "denodo_vmss_mig" {
  name                      = "${var.resource_prefix}-denodo-vmss-${var.region}"
  project                   = var.project_id
  region                    = var.region
  base_instance_name        = "${var.resource_prefix}-denodo-vdp"
  distribution_policy_zones = ["${var.region}-a", "${var.region}-b", "${var.region}-c"]

  version {
    name              = "denodo-9-0-base-image"
    instance_template = google_compute_instance_template.denodo_vmss_template.self_link
  }

  named_port {
    name = "vdp-jdbc"
    port = 9999
  }

  named_port {
    name = "vdp-odbc"
    port = 9996
  }

  named_port {
    name = "vdp-http"
    port = 9090
  }

  named_port {
    name = "vdp-https"
    port = 9443
  }

  named_port {
    name = "vdp-scheduler"
    port = 8000
  }

  auto_healing_policies {
    health_check      = google_compute_region_health_check.denodo_vdp_tcp_health_check.id
    initial_delay_sec = 300
  }

  update_policy {
    type                         = "PROACTIVE"
    instance_redistribution_type = "PROACTIVE"
    minimal_action               = "REPLACE"
    max_surge_fixed              = 3
    max_unavailable_fixed        = 0
  }
}

resource "google_compute_region_autoscaler" "denodo_vmss_autoscaler" {
  name    = "${var.resource_prefix}-denodo-vmss-autoscaler-${var.region}"
  project = var.project_id
  region  = var.region
  target  = google_compute_region_instance_group_manager.denodo_vmss_mig.id

  autoscaling_policy {
    min_replicas    = var.denodo_vmss_min_replicas
    max_replicas    = var.denodo_vmss_max_replicas
    cooldown_period = 180

    cpu_utilization {
      target = var.denodo_vmss_target_cpu
    }
  }
}

# -----------------------------------------------------------------------------
# 5. Internal Passthrough Network Load Balancer (ILB) Fronting the VM Scale Set
#    Exposes Denodo 9.0 ports:
#    - :9999 (VDP Server / JDBC)
#    - :9996 (VDP ODBC)
#    - :9090 (Design Studio `/denodo-design-studio/` & Scheduler Admin `/webadmin/denodo-scheduler-admin/`)
#    - :9443 (HTTPS Web Container)
#    - :8000 (Denodo Scheduler Server)
# -----------------------------------------------------------------------------
resource "google_compute_address" "denodo_ilb_vip" {
  name         = "${var.resource_prefix}-denodo-vmss-ilb-ip"
  project      = var.project_id
  region       = var.region
  subnetwork   = var.subnet_id
  address_type = "INTERNAL"
  purpose      = "GCE_ENDPOINT"
  description  = "Static internal VIP in snet-denodo-vdp for the Denodo 9.0 Base-Image VM Scale Set Internal Passthrough NLB"
}

resource "google_compute_region_backend_service" "denodo_vdp_ilb_backend" {
  name                  = "${var.resource_prefix}-denodo-vmss-ilb-backend"
  project               = var.project_id
  region                = var.region
  protocol              = "TCP"
  load_balancing_scheme = "INTERNAL"
  health_checks         = [google_compute_region_health_check.denodo_vdp_tcp_health_check.id]

  backend {
    group          = google_compute_region_instance_group_manager.denodo_vmss_mig.instance_group
    balancing_mode = "CONNECTION"
  }
}

resource "google_compute_forwarding_rule" "denodo_vdp_ilb_forwarding_rule" {
  name                  = "${var.resource_prefix}-denodo-vmss-ilb-fwd"
  project               = var.project_id
  region                = var.region
  load_balancing_scheme = "INTERNAL"
  backend_service       = google_compute_region_backend_service.denodo_vdp_ilb_backend.id
  ip_address            = google_compute_address.denodo_ilb_vip.address
  ip_protocol           = "TCP"
  ports                 = ["9999", "9996", "9090", "9443", "8000"]
  network               = var.vpc_id
  subnetwork            = var.subnet_id
  allow_global_access   = true
}

output "denodo_vmss_mig_name" {
  value = google_compute_region_instance_group_manager.denodo_vmss_mig.name
}

output "denodo_vmss_autoscaler_name" {
  value = google_compute_region_autoscaler.denodo_vmss_autoscaler.name
}

output "vdp_jdbc_endpoint" {
  value = "jdbc:vdb://${google_compute_address.denodo_ilb_vip.address}:9999/enterprise_data_mesh"
}

output "vdp_design_studio_url" {
  value = "http://${google_compute_address.denodo_ilb_vip.address}:9090/denodo-design-studio/"
}

output "vdp_scheduler_admin_url" {
  value = "http://${google_compute_address.denodo_ilb_vip.address}:9090/webadmin/denodo-scheduler-admin/"
}

output "vdp_data_catalog_url" {
  value = "https://${google_compute_address.denodo_ilb_vip.address}:9443/denodo-data-catalog"
}
