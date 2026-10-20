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

resource "google_service_account" "sa_domain_customer_analytics" {
  account_id   = "${var.resource_prefix}-sa-cust-analytics"
  display_name = "Data Mesh Domain 1: Customer & Commercial Analytics Identity"
  project      = var.project_id
}

resource "google_service_account" "sa_domain_supply_chain" {
  account_id   = "${var.resource_prefix}-sa-supply-chain"
  display_name = "Data Mesh Domain 2: Global Supply Chain & Inventory Identity"
  project      = var.project_id
}

resource "google_service_account" "sa_domain_enterprise_finance" {
  account_id   = "${var.resource_prefix}-sa-ent-finance"
  display_name = "Data Mesh Domain 3: Enterprise Finance & Risk Operations Identity"
  project      = var.project_id
}

# -----------------------------------------------------------------------------
# 3. Purpose-Built Standard GCS Buckets (Uniform Bucket-Level Access, No HNS)
#    IMPORTANT: Hierarchical Namespace (HNS) is intentionally NOT enabled
#    because Databricks on GCP / Unity Catalog does not support HNS buckets.
#    Subfolder isolation is enforced via GCS Managed Folders & Unity Catalog.
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

# 3b. Primary Medallion Lakehouse Bucket (Standard Flat Namespace, UBLA = true)
resource "google_storage_bucket" "medallion_lakehouse_bucket" {
  name                        = var.lakehouse_bucket_name
  project                     = var.project_id
  location                    = upper(var.region)
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false
  labels                      = var.labels

  versioning {
    enabled = false
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.lakehouse_cmek.id
  }
}

# 3c. Dedicated Standard GCS Bucket for Denodo 9.0 Installer Staging & Parquet/Delta Cache
resource "google_storage_bucket" "denodo_delta_cache_bucket" {
  name                        = "${var.lakehouse_bucket_name}-denodo-cache"
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

# 3d. Long-Term WORM Compliance Archive Bucket
resource "google_storage_bucket" "worm_archive_bucket" {
  name                        = "${var.lakehouse_bucket_name}-worm-archive"
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
    is_locked        = false     # Set true in production after compliance sign-off
    retention_period = 946728000 # 30 Years (in seconds)
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.lakehouse_cmek.id
  }
}

# -----------------------------------------------------------------------------
# 4. Granular GCS Managed Folders & Subfolder IAM on Standard UBLA Bucket
#    Structured across Medallion Tiers (bronze/, silver/, gold/) & 3 Mesh Domains
# -----------------------------------------------------------------------------
locals {
  medallion_domain_folders = toset([
    "bronze/customer_analytics/",
    "silver/customer_analytics/",
    "gold/customer_analytics/",
    "bronze/supply_chain/",
    "silver/supply_chain/",
    "gold/supply_chain/",
    "bronze/enterprise_finance/",
    "silver/enterprise_finance/",
    "gold/enterprise_finance/",
    "hive_warehouse/",
    "unity_catalog/",
    "denodo_cache/",
  ])
}

resource "google_storage_managed_folder" "lakehouse_managed_folders" {
  for_each      = local.medallion_domain_folders
  bucket        = google_storage_bucket.medallion_lakehouse_bucket.name
  name          = each.value
  force_destroy = true
}

# Subfolder IAM: Domain 1 (Customer Analytics) Service Account -> */customer_analytics/ only
resource "google_storage_managed_folder_iam_member" "customer_analytics_subfolder_iam" {
  for_each       = toset(["bronze/customer_analytics/", "silver/customer_analytics/", "gold/customer_analytics/"])
  bucket         = google_storage_bucket.medallion_lakehouse_bucket.name
  managed_folder = google_storage_managed_folder.lakehouse_managed_folders[each.value].name
  role           = "roles/storage.objectAdmin"
  member         = "serviceAccount:${google_service_account.sa_domain_customer_analytics.email}"
}

# Subfolder IAM: Domain 2 (Supply Chain) Service Account -> */supply_chain/ only
resource "google_storage_managed_folder_iam_member" "supply_chain_subfolder_iam" {
  for_each       = toset(["bronze/supply_chain/", "silver/supply_chain/", "gold/supply_chain/"])
  bucket         = google_storage_bucket.medallion_lakehouse_bucket.name
  managed_folder = google_storage_managed_folder.lakehouse_managed_folders[each.value].name
  role           = "roles/storage.objectAdmin"
  member         = "serviceAccount:${google_service_account.sa_domain_supply_chain.email}"
}

# Subfolder IAM: Domain 3 (Enterprise Finance) Service Account -> */enterprise_finance/ only
resource "google_storage_managed_folder_iam_member" "enterprise_finance_subfolder_iam" {
  for_each       = toset(["bronze/enterprise_finance/", "silver/enterprise_finance/", "gold/enterprise_finance/"])
  bucket         = google_storage_bucket.medallion_lakehouse_bucket.name
  managed_folder = google_storage_managed_folder.lakehouse_managed_folders[each.value].name
  role           = "roles/storage.objectAdmin"
  member         = "serviceAccount:${google_service_account.sa_domain_enterprise_finance.email}"
}

# -----------------------------------------------------------------------------
# 5. Optional Filestore Enterprise (POSIX flock/fcntl for Legacy Shared Scratch)
# -----------------------------------------------------------------------------
resource "google_filestore_instance" "posix_shared_scratch" {
  count    = var.enable_filestore_posix_scratch ? 1 : 0
  name     = "${var.resource_prefix}-posix-scratch-${var.environment}"
  project  = var.project_id
  location = var.region
  tier     = "ENTERPRISE"
  labels   = var.labels

  file_shares {
    capacity_gb = 1024
    name        = "ent_posix_scratch"
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
  value = google_storage_bucket.medallion_lakehouse_bucket.name
}

output "lakehouse_bucket_url" {
  value = "gs://${google_storage_bucket.medallion_lakehouse_bucket.name}"
}

output "sts_landing_bucket_url" {
  value = "gs://${google_storage_bucket.sts_landing_bucket.name}"
}

output "denodo_delta_cache_bucket_name" {
  value = google_storage_bucket.denodo_delta_cache_bucket.name
}

output "denodo_delta_cache_bucket_url" {
  value = "gs://${google_storage_bucket.denodo_delta_cache_bucket.name}"
}

output "worm_archive_bucket_url" {
  value = "gs://${google_storage_bucket.worm_archive_bucket.name}"
}

output "service_account_emails" {
  value = {
    sts_ingest           = google_service_account.sa_sts_ingest.email
    unity_catalog_master = google_service_account.sa_unity_catalog_master.email
    domain_analytics     = google_service_account.sa_domain_customer_analytics.email
    domain_supply_chain  = google_service_account.sa_domain_supply_chain.email
    domain_finance       = google_service_account.sa_domain_enterprise_finance.email
  }
}
