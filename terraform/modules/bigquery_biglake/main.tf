variable "project_id" { type = string }
variable "region" { type = string }
variable "bq_location" { type = string }
variable "environment" { type = string }
variable "resource_prefix" { type = string }
variable "lakehouse_bucket_name" { type = string }
variable "denodo_cache_dataset_id" { type = string }
variable "kms_crypto_key_id" { type = string }
variable "labels" { type = map(string) }

# -----------------------------------------------------------------------------
# Architectural Separation Mandate:
# Google BigQuery is provisioned STRICTLY and EXCLUSIVELY as the Denodo 8.0 VDP
# Native Cache Layer (replacing legacy Snowflake caching). All Medallion
# Lakehouse tables (Bronze, Silver, Gold) reside in Databricks on GCP.
# -----------------------------------------------------------------------------

# 1. BigQuery Dataset for Denodo 8.0 VDP Full-View & Incremental Caching
resource "google_bigquery_dataset" "denodo_vdp_cache" {
  dataset_id                 = var.denodo_cache_dataset_id
  project                    = var.project_id
  location                   = var.bq_location
  friendly_name              = "Denodo 8.0 VDP Native Cache Engine (BigQuery Cache Layer Only)"
  description                = "Dedicated BigQuery dataset for Denodo 8.0 Virtual DataPort cached derived views and cache performance telemetry."
  delete_contents_on_destroy = false
  labels                     = var.labels

  default_encryption_configuration {
    kms_key_name = var.kms_crypto_key_id
  }
}

# 2. BigQuery BI Engine In-Memory Reservation for Sub-Second Denodo Cache Hits
resource "google_bigquery_bi_reservation" "denodo_cache_bi_engine" {
  project  = var.project_id
  location = var.bq_location
  size     = 53687091200 # 50 GB in-memory BI Engine acceleration
}

# 3. Cloud Resource Connection for BigLake / GCS Delta Cache Interoperability
resource "google_bigquery_connection" "biglake_gcs_connection" {
  connection_id = "${var.resource_prefix}-biglake-conn-${var.environment}"
  project       = var.project_id
  location      = var.bq_location
  friendly_name = "BigLake Connection for Denodo Delta Cache Interoperability"

  cloud_resource {}
}

# 4. Clustered Denodo Cache Table: Unified Cross-Domain Molecule 360 View
resource "google_bigquery_table" "cache_dv_rd_molecule_360" {
  dataset_id          = google_bigquery_dataset.denodo_vdp_cache.dataset_id
  table_id            = "cache_dv_rd_molecule_360"
  project             = var.project_id
  deletion_protection = false
  labels              = var.labels

  clustering = ["studyid", "molecule_id"]

  schema = jsonencode([
    { name = "studyid", type = "STRING", mode = "REQUIRED" },
    { name = "molecule_id", type = "STRING", mode = "REQUIRED" },
    { name = "usubjid", type = "STRING", mode = "REQUIRED" },
    { name = "country", type = "STRING", mode = "REQUIRED" },
    { name = "region_code", type = "STRING", mode = "REQUIRED" },
    { name = "arm_blinded", type = "STRING", mode = "REQUIRED" },
    { name = "arm_unblinded_treatment", type = "STRING", mode = "REQUIRED" },
    { name = "comet_lot_id", type = "STRING", mode = "REQUIRED" },
    { name = "sap_batch_charg", type = "STRING", mode = "REQUIRED" },
    { name = "manufacturing_site", type = "STRING", mode = "REQUIRED" },
    { name = "purity_sec_hplc_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "bioreactor_titer_g_l", type = "FLOAT64", mode = "REQUIRED" },
    { name = "ctdna_clearance_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "pd_l1_expression_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "clinical_response_recist", type = "STRING", mode = "REQUIRED" },
    { name = "rwd_synthetic_control_pfs_months", type = "FLOAT64", mode = "REQUIRED" }
  ])
}

# 5. Clustered Denodo Cache Table: CMC-to-Clinical Batch Lot Traceability View
resource "google_bigquery_table" "cache_dv_cmc_clinical_lot_trace" {
  dataset_id          = google_bigquery_dataset.denodo_vdp_cache.dataset_id
  table_id            = "cache_dv_cmc_clinical_lot_trace"
  project             = var.project_id
  deletion_protection = false
  labels              = var.labels

  clustering = ["studyid", "comet_lot_id"]

  schema = jsonencode([
    { name = "comet_lot_id", type = "STRING", mode = "REQUIRED" },
    { name = "sap_werks", type = "STRING", mode = "REQUIRED" },
    { name = "sap_matnr", type = "STRING", mode = "REQUIRED" },
    { name = "sap_batch_charg", type = "STRING", mode = "REQUIRED" },
    { name = "molecule_id", type = "STRING", mode = "REQUIRED" },
    { name = "studyid", type = "STRING", mode = "REQUIRED" },
    { name = "manufacturing_site", type = "STRING", mode = "REQUIRED" },
    { name = "purity_sec_hplc_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "release_status", type = "STRING", mode = "REQUIRED" },
    { name = "avg_24m_potency_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "has_stability_oos", type = "BOOL", mode = "REQUIRED" },
    { name = "dosed_clinical_subjects", type = "INT64", mode = "REQUIRED" },
    { name = "mean_week12_ctdna_clearance_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "grade3_plus_ae_rate_pct", type = "FLOAT64", mode = "REQUIRED" }
  ])
}

output "denodo_cache_dataset_id" {
  value = google_bigquery_dataset.denodo_vdp_cache.dataset_id
}
