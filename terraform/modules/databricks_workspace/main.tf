variable "project_id" { type = string }
variable "region" { type = string }
variable "environment" { type = string }
variable "resource_prefix" { type = string }
variable "databricks_account_id" { type = string }
variable "databricks_workspace_host" { type = string }
variable "databricks_workspace_id" { type = string }
variable "databricks_sql_warehouse_id" { type = string }
variable "databricks_catalog_schema" { type = string }
variable "vpc_id" { type = string }
variable "subnet_id" { type = string }
variable "lakehouse_bucket_name" { type = string }
variable "hive_metastore_ip" { type = string }
variable "labels" { type = map(string) }

# -----------------------------------------------------------------------------
# 1. Google Service Account for Databricks Clusters & Unity Catalog External Locations
# -----------------------------------------------------------------------------
resource "google_service_account" "databricks_unity_sa" {
  account_id   = "${var.resource_prefix}-dbx-uc-${var.environment}"
  display_name = "Databricks on GCP Unity Catalog & Compute Pool Service Account"
  project      = var.project_id
}

resource "google_storage_bucket_iam_member" "databricks_lakehouse_object_admin" {
  bucket = var.lakehouse_bucket_name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.databricks_unity_sa.email}"
}

# -----------------------------------------------------------------------------
# 2. Single-Environment Databricks on GCP Workspace, SQL Warehouse & Compute Pools
#    Replaces legacy Standard_D96ds_v5 nodes with Next-Gen N4, C4, M3, and Z3 pools
# -----------------------------------------------------------------------------
locals {
  workspace_id           = var.databricks_workspace_id
  workspace_host_clean   = replace(replace(var.databricks_workspace_host, "https://", ""), "http://", "")
  workspace_url          = "${var.databricks_workspace_host}/?o=${var.databricks_workspace_id}"
  sql_warehouse_jdbc_url = "jdbc:databricks://${local.workspace_host_clean}:443/${var.databricks_catalog_schema};transportMode=http;ssl=1;AuthMech=3;UID=token;httpPath=/sql/1.0/warehouses/${var.databricks_sql_warehouse_id}"

  # Next-Generation GCE Machine Families for R&D Data Mesh Workloads
  cluster_pool_families = {
    clinical_ddf_standard_pool   = "n4-standard-16"  # 16 vCPU, 64 GB RAM (CDISC ETL & Biomarker pipelines)
    rwd_cohort_heavy_compute     = "c4-highmem-32"   # 32 vCPU, 248 GB RAM (Propensity scoring & survival joins)
    genomics_in_memory_pool      = "m3-megamem-64"   # 64 vCPU, 976 GB RAM (Replaces Standard_D96ds_v5)
    delta_cache_nvme_pool        = "z3-highmem-88"   # 88 vCPU, 704 GB RAM + Titanium Local NVMe SSD
    cmc_manufacturing_batch_pool = "n4-highmem-8"    # 8 vCPU, 64 GB RAM (LIMS/ERP genealogy & ICH Q1A stability)
  }

  # Unity Catalog External Locations mapped to GCS HNS Managed Folders
  unity_catalog_external_locations = {
    ext_loc_clinical_bronze = "gs://${var.lakehouse_bucket_name}/bronze/clinical_ddf/"
    ext_loc_clinical_silver = "gs://${var.lakehouse_bucket_name}/silver/clinical_ddf/"
    ext_loc_clinical_gold   = "gs://${var.lakehouse_bucket_name}/gold/clinical_ddf/"
    ext_loc_rwd_bronze      = "gs://${var.lakehouse_bucket_name}/bronze/real_world_data/"
    ext_loc_rwd_silver      = "gs://${var.lakehouse_bucket_name}/silver/real_world_data/"
    ext_loc_rwd_gold        = "gs://${var.lakehouse_bucket_name}/gold/real_world_data/"
    ext_loc_cmc_bronze      = "gs://${var.lakehouse_bucket_name}/bronze/cmc_manufacturing/"
    ext_loc_cmc_silver      = "gs://${var.lakehouse_bucket_name}/silver/cmc_manufacturing/"
    ext_loc_cmc_gold        = "gs://${var.lakehouse_bucket_name}/gold/cmc_manufacturing/"
  }

  # Spark Cluster Override Properties for External Hive Metastore (Cloud SQL HA)
  external_hive_metastore_spark_conf = {
    "spark.hadoop.javax.jdo.option.ConnectionURL"        = "jdbc:postgresql://${var.hive_metastore_ip}:5432/hive_metastore?sslmode=require"
    "spark.hadoop.javax.jdo.option.ConnectionDriverName" = "org.postgresql.Driver"
    "spark.sql.hive.metastore.version"                   = "2.3.9"
    "spark.sql.hive.metastore.jars"                      = "builtin"
  }
}

output "workspace_url" {
  value = local.workspace_url
}

output "sql_warehouse_jdbc_url" {
  value = local.sql_warehouse_jdbc_url
}

output "databricks_unity_sa_email" {
  value = google_service_account.databricks_unity_sa.email
}

output "cluster_pool_families" {
  value = local.cluster_pool_families
}

output "unity_catalog_external_locations" {
  value = local.unity_catalog_external_locations
}
