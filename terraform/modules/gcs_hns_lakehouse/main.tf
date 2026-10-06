variable "project_id" { type = string }
variable "project_number" { type = string }
variable "region" { type = string }
variable "environment" { type = string }
variable "resource_prefix" { type = string }
variable "lakehouse_bucket_name" { type = string }
variable "vpc_id" { type = string }
variable "enable_filestore_posix_scratch" { type = bool }
variable "labels" { type = map(string) }

# -----------------------------------------------------------------------------
# 1. Cloud KMS CMEK KeyRing & CryptoKey (90-Day Automatic Rotation)
# -----------------------------------------------------------------------------
resource "google_kms_key_ring" "lakehouse_keyring" {
  name     = "${var.resource_prefix}-kms-ring-${var.region}-${var.environment}"
  project  = var.project_id
  location = var.region
}

resource "google_kms_crypto_key" "lakehouse_cmek" {
  name            = "${var.resource_prefix}-cmek-key"
  key_ring        = google_kms_key_ring.lakehouse_keyring.id
  rotation_period = "7776000s" # 90 days
  labels          = var.labels
}

# -----------------------------------------------------------------------------
# 2. Dedicated Least-Privilege GCP Service Accounts ("Storage Accounts")
#    Replaces legacy shared Storage Account keys and cross-cloud identities
# -----------------------------------------------------------------------------
resource "google_service_account" "sa_sts_ingest" {
  account_id   = "${var.resource_prefix}-sa-sts-ingest"
  display_name = "Storage Transfer Service (STS) Cross-Cloud Ingestion Identity"
  project      = var.project_id
}

resource "google_service_account" "sa_unity_catalog_master" {
  account_id   = "${var.resource_prefix}-sa-uc-master"
  display_name = "Databricks Unity Catalog Storage Credential Master Identity"
  project      = var.project_id
}

resource "google_service_account" "sa_domain_clinical_ddf" {
  account_id   = "${var.resource_prefix}-sa-clinical-ddf"
  display_name = "Data Mesh Node 1: Clinical Development & Biomarkers Identity"
  project      = var.project_id
}

resource "google_service_account" "sa_domain_real_world_data" {
  account_id   = "${var.resource_prefix}-sa-rwd-cohorts"
  display_name = "Data Mesh Node 2: Real-World Evidence (RWD) Cohorts Identity"
  project      = var.project_id
}

resource "google_service_account" "sa_domain_cmc_manufacturing" {
  account_id   = "${var.resource_prefix}-sa-cmc-mfg"
  display_name = "Data Mesh Node 3: CMC Biologics & Stability Manufacturing Identity"
  project      = var.project_id
}

# -----------------------------------------------------------------------------
# 3. Purpose-Built GCS Buckets (STS Landing, HNS Lakehouse, Denodo Cache, WORM)
# -----------------------------------------------------------------------------

# 3a. Cross-Cloud Storage Transfer Service (STS) Landing Bucket
resource "google_storage_bucket" "sts_landing_bucket" {
  name                        = "${var.lakehouse_bucket_name}-sts-landing"
  project                     = var.project_id
  location                    = upper(var.region)
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false
  labels                      = var.labels

  encryption {
    default_kms_key_name = google_kms_crypto_key.lakehouse_cmek.id
  }
}

# 3b. Primary Medallion Lakehouse Bucket with Hierarchical Namespace (HNS)
#     Provides atomic O(1) directory renames and high QPS for Spark/Delta Lake
resource "google_storage_bucket" "rd_lakehouse_hns" {
  name                        = var.lakehouse_bucket_name
  project                     = var.project_id
  location                    = upper(var.region)
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false
  labels                      = var.labels

  hierarchical_namespace {
    enabled = true
  }

  versioning {
    enabled = false
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.lakehouse_cmek.id
  }
}

# 3c. Dedicated GCS HNS Bucket for Denodo 8.0 Parquet/Delta Caching Spike
resource "google_storage_bucket" "denodo_delta_cache_hns" {
  name                        = "${var.lakehouse_bucket_name}-denodo-cache"
  project                     = var.project_id
  location                    = upper(var.region)
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false
  labels                      = var.labels

  hierarchical_namespace {
    enabled = true
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.lakehouse_cmek.id
  }
}

# 3d. GxP 30-Year WORM Regulatory Archive Bucket (21 CFR Part 11 / EU Annex 11)
resource "google_storage_bucket" "gxp_worm_archive_bucket" {
  name                        = "${var.lakehouse_bucket_name}-gxp-worm-archive"
  project                     = var.project_id
  location                    = upper(var.region)
  storage_class               = "ARCHIVE"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false
  labels                      = var.labels

  versioning {
    enabled = true
  }

  retention_policy {
    is_locked        = false # Set true in production after validation sign-off
    retention_period = 946728000 # 30 Years (in seconds)
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.lakehouse_cmek.id
  }
}

# -----------------------------------------------------------------------------
# 4. Granular GCS Managed Folders & Subfolder IAM (Replicating ADLS POSIX ACLs)
#    Structured across Medallion Tiers (bronze/, silver/, gold/) & 3 Mesh Nodes
# -----------------------------------------------------------------------------
locals {
  medallion_domain_folders = toset([
    "bronze/clinical_ddf/",
    "silver/clinical_ddf/",
    "gold/clinical_ddf/",
    "bronze/real_world_data/",
    "silver/real_world_data/",
    "gold/real_world_data/",
    "bronze/cmc_manufacturing/",
    "silver/cmc_manufacturing/",
    "gold/cmc_manufacturing/",
    "hive_warehouse/",
    "unity_catalog/",
    "denodo_cache/",
  ])
}

resource "google_storage_managed_folder" "lakehouse_managed_folders" {
  for_each      = local.medallion_domain_folders
  bucket        = google_storage_bucket.rd_lakehouse_hns.name
  name          = each.value
  force_destroy = true
}

# Subfolder IAM: Domain 1 (Clinical DDF) Service Account -> */clinical_ddf/ only
resource "google_storage_managed_folder_iam_member" "clinical_ddf_subfolder_iam" {
  for_each       = toset(["bronze/clinical_ddf/", "silver/clinical_ddf/", "gold/clinical_ddf/"])
  bucket         = google_storage_bucket.rd_lakehouse_hns.name
  managed_folder = google_storage_managed_folder.lakehouse_managed_folders[each.value].name
  role           = "roles/storage.objectAdmin"
  member         = "serviceAccount:${google_service_account.sa_domain_clinical_ddf.email}"
}

# Subfolder IAM: Domain 2 (Real-World Data) Service Account -> */real_world_data/ only
resource "google_storage_managed_folder_iam_member" "real_world_data_subfolder_iam" {
  for_each       = toset(["bronze/real_world_data/", "silver/real_world_data/", "gold/real_world_data/"])
  bucket         = google_storage_bucket.rd_lakehouse_hns.name
  managed_folder = google_storage_managed_folder.lakehouse_managed_folders[each.value].name
  role           = "roles/storage.objectAdmin"
  member         = "serviceAccount:${google_service_account.sa_domain_real_world_data.email}"
}

# Subfolder IAM: Domain 3 (CMC Manufacturing) Service Account -> */cmc_manufacturing/ only
resource "google_storage_managed_folder_iam_member" "cmc_manufacturing_subfolder_iam" {
  for_each       = toset(["bronze/cmc_manufacturing/", "silver/cmc_manufacturing/", "gold/cmc_manufacturing/"])
  bucket         = google_storage_bucket.rd_lakehouse_hns.name
  managed_folder = google_storage_managed_folder.lakehouse_managed_folders[each.value].name
  role           = "roles/storage.objectAdmin"
  member         = "serviceAccount:${google_service_account.sa_domain_cmc_manufacturing.email}"
}

# -----------------------------------------------------------------------------
# 5. Optional Filestore Enterprise (POSIX flock/fcntl for SAS / Legacy HPC)
# -----------------------------------------------------------------------------
resource "google_filestore_instance" "posix_statistical_scratch" {
  count    = var.enable_filestore_posix_scratch ? 1 : 0
  name     = "${var.resource_prefix}-posix-scratch-${var.environment}"
  project  = var.project_id
  location = var.region
  tier     = "ENTERPRISE"
  labels   = var.labels

  file_shares {
    capacity_gb = 1024
    name        = "rd_posix_scratch"
  }

  networks {
    network      = var.vpc_id
    modes        = ["MODE_IPV4"]
    connect_mode = "PRIVATE_SERVICE_ACCESS"
  }
}

output "kms_crypto_key_id" {
  value = google_kms_crypto_key.lakehouse_cmek.id
}

output "lakehouse_bucket_name" {
  value = google_storage_bucket.rd_lakehouse_hns.name
}

output "lakehouse_bucket_url" {
  value = "gs://${google_storage_bucket.rd_lakehouse_hns.name}"
}

output "sts_landing_bucket_url" {
  value = "gs://${google_storage_bucket.sts_landing_bucket.name}"
}

output "denodo_delta_cache_bucket_name" {
  value = google_storage_bucket.denodo_delta_cache_hns.name
}

output "denodo_delta_cache_bucket_url" {
  value = "gs://${google_storage_bucket.denodo_delta_cache_hns.name}"
}

output "gxp_worm_archive_bucket_url" {
  value = "gs://${google_storage_bucket.gxp_worm_archive_bucket.name}"
}

output "service_account_emails" {
  value = {
    sts_ingest            = google_service_account.sa_sts_ingest.email
    unity_catalog_master  = google_service_account.sa_unity_catalog_master.email
    domain_clinical_ddf   = google_service_account.sa_domain_clinical_ddf.email
    domain_real_world     = google_service_account.sa_domain_real_world_data.email
    domain_cmc_mfg        = google_service_account.sa_domain_cmc_manufacturing.email
  }
}
