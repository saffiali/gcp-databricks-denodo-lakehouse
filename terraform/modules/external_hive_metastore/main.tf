variable "project_id" { type = string }
variable "region" { type = string }
variable "environment" { type = string }
variable "resource_prefix" { type = string }
variable "vpc_id" { type = string }
variable "hive_metastore_tier" { type = string }
variable "kms_crypto_key_id" { type = string }
variable "labels" { type = map(string) }

# -----------------------------------------------------------------------------
# 1. Regional High-Availability Cloud SQL for PostgreSQL 15 (External Hive Metastore)
#    Hosts rewritten SDS.LOCATION and DBS.DB_LOCATION_URI paths (abfss:// -> gs://)
# -----------------------------------------------------------------------------
resource "google_sql_database_instance" "external_hive_metastore" {
  name                = "${var.resource_prefix}-hive-metastore-${var.environment}"
  project             = var.project_id
  region              = var.region
  database_version    = "POSTGRES_15"
  encryption_key_name = var.kms_crypto_key_id
  deletion_protection = true

  settings {
    tier              = var.hive_metastore_tier
    availability_type = "REGIONAL"
    disk_type         = "PD_SSD"
    disk_size         = 100
    disk_autoresize   = true
    user_labels       = var.labels

    ip_configuration {
      ipv4_enabled    = false
      private_network = var.vpc_id
      ssl_mode        = "ENCRYPTED_ONLY"
    }

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "02:00"
      transaction_log_retention_days = 7
    }

    insights_config {
      query_insights_enabled  = true
      query_string_length     = 1024
      record_application_tags = true
    }
  }
}

resource "google_sql_database" "hive_metastore_db" {
  name     = "hive_metastore"
  project  = var.project_id
  instance = google_sql_database_instance.external_hive_metastore.name
}

# -----------------------------------------------------------------------------
# 2. Google Cloud Secret Manager (Replaces Legacy Key Vaults for JDBC & Tokens)
# -----------------------------------------------------------------------------
resource "google_secret_manager_secret" "hive_metastore_jdbc_secret" {
  secret_id = "${var.resource_prefix}-hive-metastore-jdbc-${var.environment}"
  project   = var.project_id
  labels    = var.labels

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "denodo_databricks_oauth_secret" {
  secret_id = "${var.resource_prefix}-denodo-dbx-oauth-${var.environment}"
  project   = var.project_id
  labels    = var.labels

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

output "private_ip_address" {
  value = google_sql_database_instance.external_hive_metastore.private_ip_address
}

output "instance_connection_name" {
  value = google_sql_database_instance.external_hive_metastore.connection_name
}

output "hive_jdbc_secret_id" {
  value = google_secret_manager_secret.hive_metastore_jdbc_secret.id
}
