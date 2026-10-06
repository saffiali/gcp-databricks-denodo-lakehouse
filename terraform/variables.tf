variable "project_id" {
  description = "Target Google Cloud Project ID for the single-environment Databricks on GCP Lakehouse and Denodo 8.0 VDP platform."
  type        = string
  default     = "gke-demos-363017"
}

variable "project_number" {
  description = "Target Google Cloud Project Number (used for KMS CMEK service agent IAM bindings and VPC-SC perimeters)."
  type        = string
  default     = "157995042458"
}

variable "region" {
  description = "Primary GCP region for Databricks on GCP, GCS HNS buckets, HA Cloud SQL Hive Metastore, and Denodo 8.0 VDP."
  type        = string
  default     = "europe-west2"
}

variable "bq_location" {
  description = "BigQuery dataset location for the Denodo 8.0 VDP Native Cache layer."
  type        = string
  default     = "EU"
}

variable "environment" {
  description = "Single-environment deployment identifier (e.g., mvp, dual-run, prod)."
  type        = string
  default     = "mvp"
}

variable "resource_prefix" {
  description = "Customer-agnostic naming prefix for all VPC, storage, compute, and IAM resources."
  type        = string
  default     = "rd-lakehouse"
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
  description = "Dedicated /22 primary subnet CIDR for the Denodo 8.0 Trial GKE Cluster nodes and Internal Passthrough LoadBalancer."
  type        = string
  default     = "10.169.0.0/22"
}

variable "denodo_gke_pods_cidr" {
  description = "Secondary CIDR range (/18) on snet-denodo-vdp for Denodo 8.0 Trial GKE Cluster pods."
  type        = string
  default     = "10.178.0.0/18"
}

variable "denodo_gke_services_cidr" {
  description = "Secondary CIDR range (/20) on snet-denodo-vdp for Denodo 8.0 Trial GKE Cluster services."
  type        = string
  default     = "10.179.0.0/20"
}

variable "denodo_gke_master_cidr" {
  description = "Private /28 IPv4 CIDR block for the Denodo Trial GKE Control Plane master endpoint."
  type        = string
  default     = "172.16.0.16/28"
}

variable "psc_subnet_cidr" {
  description = "Dedicated /24 subnet CIDR for Private Service Connect (PSC) endpoints (Databricks Private Link & Google APIs)."
  type        = string
  default     = "10.169.4.0/24"
}

variable "ilb_proxy_subnet_cidr" {
  description = "Dedicated /24 Regional Managed Proxy subnet CIDR for internal L7 load balancers (Denodo Design Studio / Data Catalog HTTPS)."
  type        = string
  default     = "10.169.5.0/24"
}

variable "access_policy_id" {
  description = "Optional Organization Access Context Manager Policy ID for VPC Service Controls (VPC-SC) perimeter enforcement."
  type        = string
  default     = ""
}

variable "lakehouse_bucket_name" {
  description = "Primary GCS Hierarchical Namespace (HNS) bucket for the 3 R&D Data Mesh domains (Bronze, Silver, Gold)."
  type        = string
  default     = "gke-demos-363017-rd-lakehouse-hns"
}

variable "enable_filestore_posix_scratch" {
  description = "Whether to provision a Filestore Enterprise NFSv4.1 instance for POSIX file-locking (SAS / legacy HPC statistical workloads)."
  type        = bool
  default     = false
}

variable "denodo_cache_dataset_id" {
  description = "BigQuery dataset ID used STRICTLY and EXCLUSIVELY as the Denodo 8.0 VDP Native Cache Engine."
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
  default     = "https://8259555750233451.1.gcp.databricks.com"
}

variable "databricks_workspace_id" {
  description = "Databricks on GCP Workspace numeric ID."
  type        = string
  default     = "8259555750233451"
}

variable "databricks_sql_warehouse_id" {
  description = "Databricks Serverless/Pro SQL Warehouse ID queried by Denodo 8.0 VDP over Simba Spark JDBC."
  type        = string
  default     = "0154a901254a4f17"
}

variable "databricks_catalog_schema" {
  description = "Primary Unity Catalog schema hosting the R&D Medallion Lakehouse tables in Databricks."
  type        = string
  default     = "rd_lakehouse_medallion"
}

variable "hive_metastore_tier" {
  description = "Regional HA Cloud SQL PostgreSQL 15 machine tier for the External Hive Metastore."
  type        = string
  default     = "db-custom-4-16384"
}

variable "denodo_machine_type" {
  description = "GKE node pool machine family for Denodo 8.0 Trial Server pods (Next-Gen N4 family)."
  type        = string
  default     = "n4-standard-8"
}

variable "denodo_container_image_tag" {
  description = "Denodo Platform Trial Server container image tag mirrored from harbor.open.denodo.com into GCP Artifact Registry."
  type        = string
  default     = "8.0-trial"
}

variable "labels" {
  description = "Standard enterprise resource labels for FinOps, GxP governance, and Dual-Run cost attribution."
  type        = map(string)
  default = {
    programme      = "rd-data-unification"
    architecture   = "databricks-denodo-gcp"
    lakehouse_tier = "medallion-hns"
    virtualizer    = "denodo-8-trial-gke"
    cache_engine   = "bigquery-native-cache"
    managed_by     = "terraform"
  }
}
