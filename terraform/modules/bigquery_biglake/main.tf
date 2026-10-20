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
# Google BigQuery is provisioned STRICTLY and EXCLUSIVELY as the Denodo 9.0 VDP
# Native Cache Layer (replacing legacy Snowflake caching). All Medallion
# Lakehouse tables (Bronze, Silver, Gold) reside in Databricks on GCP.
# -----------------------------------------------------------------------------

# 1. BigQuery Dataset for Denodo 9.0 VDP Full-View & Incremental Caching
resource "google_bigquery_dataset" "denodo_vdp_cache" {
  dataset_id                 = var.denodo_cache_dataset_id
  project                    = var.project_id
  location                   = var.bq_location
  friendly_name              = "Denodo 9.0 VDP Native Cache Engine (BigQuery Cache Layer Only)"
  description                = "Dedicated BigQuery dataset for Denodo 9.0 Virtual DataPort cached derived views and cache performance telemetry."
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

# 4. Clustered Denodo Cache Table: Unified Cross-Domain Customer 360 View
resource "google_bigquery_table" "cache_dv_enterprise_customer_360" {
  dataset_id          = google_bigquery_dataset.denodo_vdp_cache.dataset_id
  table_id            = "cache_dv_enterprise_customer_360"
  project             = var.project_id
  deletion_protection = false
  labels              = var.labels

  clustering = ["region_code", "customer_id"]

  schema = jsonencode([
    { name = "customer_id", type = "STRING", mode = "REQUIRED" },
    { name = "account_segment", type = "STRING", mode = "REQUIRED" },
    { name = "country", type = "STRING", mode = "REQUIRED" },
    { name = "region_code", type = "STRING", mode = "REQUIRED" },
    { name = "pii_masked_tier", type = "STRING", mode = "REQUIRED" },
    { name = "account_executive_unmasked", type = "STRING", mode = "REQUIRED" },
    { name = "order_batch_id", type = "STRING", mode = "REQUIRED" },
    { name = "erp_order_number", type = "STRING", mode = "REQUIRED" },
    { name = "fulfillment_center", type = "STRING", mode = "REQUIRED" },
    { name = "on_time_delivery_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "inventory_turnover_ratio", type = "FLOAT64", mode = "REQUIRED" },
    { name = "net_retention_score_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "annual_contract_value_usd", type = "FLOAT64", mode = "REQUIRED" },
    { name = "credit_risk_rating", type = "STRING", mode = "REQUIRED" },
    { name = "forecasted_12m_ltv_usd", type = "FLOAT64", mode = "REQUIRED" }
  ])
}

# 5. Clustered Denodo Cache Table: Supply Chain to Finance Order Traceability View
resource "google_bigquery_table" "cache_dv_supply_chain_order_trace" {
  dataset_id          = google_bigquery_dataset.denodo_vdp_cache.dataset_id
  table_id            = "cache_dv_supply_chain_order_trace"
  project             = var.project_id
  deletion_protection = false
  labels              = var.labels

  clustering = ["region_code", "order_batch_id"]

  schema = jsonencode([
    { name = "order_batch_id", type = "STRING", mode = "REQUIRED" },
    { name = "erp_plant_code", type = "STRING", mode = "REQUIRED" },
    { name = "sku_material_id", type = "STRING", mode = "REQUIRED" },
    { name = "erp_order_number", type = "STRING", mode = "REQUIRED" },
    { name = "customer_id", type = "STRING", mode = "REQUIRED" },
    { name = "region_code", type = "STRING", mode = "REQUIRED" },
    { name = "fulfillment_center", type = "STRING", mode = "REQUIRED" },
    { name = "quality_inspection_score_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "shipment_release_status", type = "STRING", mode = "REQUIRED" },
    { name = "invoice_reconciliation_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "has_sla_exception", type = "BOOL", mode = "REQUIRED" },
    { name = "fulfilled_line_items", type = "INT64", mode = "REQUIRED" },
    { name = "gross_margin_pct", type = "FLOAT64", mode = "REQUIRED" },
    { name = "dispute_rate_pct", type = "FLOAT64", mode = "REQUIRED" }
  ])
}

output "denodo_cache_dataset_id" {
  value = google_bigquery_dataset.denodo_vdp_cache.dataset_id
}
