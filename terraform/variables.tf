variable "project_id" {
  description = "Target Google Cloud Project ID for the single-environment Databricks on GCP Lakehouse and Denodo 9.0 VDP platform."
  type        = string
  default     = "your-gcp-project-id"
}

variable "project_number" {
  description = "Target Google Cloud Project Number (used for KMS CMEK service agent IAM bindings and VPC-SC perimeters)."
  type        = string
  default     = "123456789012"
}

variable "region" {
  description = "Primary GCP region for Databricks on GCP, standard GCS Medallion buckets, HA Cloud SQL Hive Metastore, and Denodo 9.0 VM Scale Set."
  type        = string
  default     = "europe-west2"
}

variable "bq_location" {
  description = "BigQuery dataset location for the Denodo 9.0 VDP Native Cache layer."
  type        = string
  default     = "EU"
}

variable "environment" {
  description = "Single-environment deployment identifier (e.g., dev, uat, prod)."
  type        = string
  default     = "prod"
}

variable "resource_prefix" {
  description = "Naming prefix for all VPC, storage, compute, and IAM resources."
  type        = string
  default     = "ent-lakehouse"
}

variable "vpc_subnet_cidr" {
  description = "Customer-managed /19 primary subnet CIDR for Databricks on GCP Compute Plane (GKE Enterprise worker nodes)."
  type        = string
  default     = "10.168.0.0/19"
}

variable "gke_pods_cidr" {
  description = "Secondary CIDR range (/16) for Databricks GKE Enterprise pods."
  type        = string
  default     = "10.176.0.0/16"
}

variable "gke_services_cidr" {
  description = "Secondary CIDR range (/20) for Databricks GKE Enterprise services."
  type        = string
  default     = "10.177.0.0/20"
}

variable "denodo_subnet_cidr" {
  description = "Dedicated /22 primary subnet CIDR for the Denodo 9.0 VM Scale Set (Regional MIG on Base OS images) and Internal Passthrough LoadBalancer."
  type        = string
  default     = "10.169.0.0/22"
}

variable "psc_subnet_cidr" {
  description = "Dedicated /24 subnet CIDR for Private Service Connect (PSC) endpoints (Databricks Private Link & Google APIs)."
  type        = string
  default     = "10.169.4.0/24"
}

variable "ilb_proxy_subnet_cidr" {
  description = "Dedicated /24 Regional Managed Proxy subnet CIDR for internal L7 load balancers."
  type        = string
  default     = "10.169.5.0/24"
}

variable "access_policy_id" {
  description = "Optional Organization Access Context Manager Policy ID for VPC Service Controls (VPC-SC) perimeter enforcement."
  type        = string
  default     = ""
}

variable "lakehouse_bucket_name" {
  description = "Primary Standard GCS bucket (Uniform Bucket-Level Access, HNS disabled for Databricks compatibility) hosting Medallion Managed Folders (Bronze, Silver, Gold)."
  type        = string
  default     = "your-gcp-project-id-ent-lakehouse"
}

variable "enable_filestore_posix_scratch" {
  description = "Whether to provision a Filestore Enterprise NFSv4.1 instance for POSIX file-locking workloads."
  type        = bool
  default     = false
}

variable "denodo_cache_dataset_id" {
  description = "BigQuery dataset ID used STRICTLY and EXCLUSIVELY as the Denodo 9.0 VDP Native Cache Engine."
  type        = string
  default     = "denodo_vdp_cache"
}

variable "databricks_account_id" {
  description = "Databricks Account ID for GCP Workspace and Unity Catalog provisioning."
  type        = string
  default     = "00000000-0000-0000-0000-000000000000"
}

variable "databricks_workspace_host" {
  description = "Databricks on GCP Workspace URL."
  type        = string
  default     = "https://1234567890123456.1.gcp.databricks.com"
}

variable "databricks_workspace_id" {
  description = "Databricks on GCP Workspace numeric ID."
  type        = string
  default     = "1234567890123456"
}

variable "databricks_sql_warehouse_id" {
  description = "Databricks Serverless/Pro SQL Warehouse ID queried by Denodo 9.0 VDP over Simba Spark JDBC."
  type        = string
  default     = "0123456789abcdef"
}

variable "databricks_catalog_schema" {
  description = "Primary Unity Catalog schema hosting the Medallion Lakehouse tables in Databricks."
  type        = string
  default     = "lakehouse_medallion"
}

variable "hive_metastore_tier" {
  description = "Regional HA Cloud SQL PostgreSQL 15 machine tier for the External Hive Metastore."
  type        = string
  default     = "db-custom-4-16384"
}

variable "denodo_source_image" {
  description = "Hardened Enterprise Linux Base OS image (e.g., RHEL 9, Rocky Linux 9, or custom golden base image) on which Denodo Platform 9.0 is installed via unattended silent installer."
  type        = string
  default     = "projects/rhel-cloud/global/images/family/rhel-9"
}

variable "denodo_machine_type" {
  description = "GCE machine family for Denodo 9.0 VM Scale Set (Regional MIG) nodes (Next-Gen N4 family)."
  type        = string
  default     = "n4-standard-8"
}

variable "denodo_vmss_min_replicas" {
  description = "Minimum number of Shielded VMs in the Denodo 9.0 Regional VM Scale Set (multi-zone HA)."
  type        = number
  default     = 2
}

variable "denodo_vmss_max_replicas" {
  description = "Maximum number of Shielded VMs in the Denodo 9.0 Regional VM Scale Set under autoscaling."
  type        = number
  default     = 6
}

variable "denodo_vmss_target_cpu" {
  description = "Target CPU utilization ratio (0.0 - 1.0) for the Denodo 9.0 Regional VM Scale Set autoscaler."
  type        = number
  default     = 0.70
}

variable "labels" {
  description = "Standard enterprise resource labels for FinOps, governance, and cost attribution."
  type        = map(string)
  default = {
    programme      = "enterprise-data-unification"
    architecture   = "databricks-denodo-gcp"
    lakehouse_tier = "medallion-standard-gcs"
    virtualizer    = "denodo-9-base-image-vmss"
    cache_engine   = "bigquery-native-cache"
    managed_by     = "terraform"
  }
}
