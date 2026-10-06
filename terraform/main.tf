provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# -----------------------------------------------------------------------------
# 1. Network Controls, Multi-Subnet Zero-Trust VPC, PSC, Restricted APIs & VPC-SC
# -----------------------------------------------------------------------------
module "network_and_psc" {
  source = "./modules/network_and_psc"

  project_id               = var.project_id
  region                   = var.region
  environment              = var.environment
  resource_prefix          = var.resource_prefix
  vpc_subnet_cidr          = var.vpc_subnet_cidr
  gke_pods_cidr            = var.gke_pods_cidr
  gke_services_cidr        = var.gke_services_cidr
  denodo_subnet_cidr       = var.denodo_subnet_cidr
  denodo_gke_pods_cidr     = var.denodo_gke_pods_cidr
  denodo_gke_services_cidr = var.denodo_gke_services_cidr
  denodo_gke_master_cidr   = var.denodo_gke_master_cidr
  psc_subnet_cidr          = var.psc_subnet_cidr
  ilb_proxy_subnet_cidr    = var.ilb_proxy_subnet_cidr
  access_policy_id         = var.access_policy_id
  labels                   = var.labels
}

# -----------------------------------------------------------------------------
# 2. Storage Accounts (GCP Service Accounts), Cloud KMS CMEK, GCS HNS Buckets,
#    30-Year GxP WORM Archive & Subfolder Managed Folders (Bronze/Silver/Gold)
# -----------------------------------------------------------------------------
module "gcs_hns_lakehouse" {
  source = "./modules/gcs_hns_lakehouse"

  project_id                     = var.project_id
  project_number                 = var.project_number
  region                         = var.region
  environment                    = var.environment
  resource_prefix                = var.resource_prefix
  lakehouse_bucket_name          = var.lakehouse_bucket_name
  vpc_id                         = module.network_and_psc.vpc_id
  enable_filestore_posix_scratch = var.enable_filestore_posix_scratch
  labels                         = var.labels
}

# -----------------------------------------------------------------------------
# 3. External Hive Metastore (Regional HA Cloud SQL PostgreSQL 15 + Secret Mgr)
# -----------------------------------------------------------------------------
module "external_hive_metastore" {
  source = "./modules/external_hive_metastore"

  project_id          = var.project_id
  region              = var.region
  environment         = var.environment
  resource_prefix     = var.resource_prefix
  vpc_id              = module.network_and_psc.vpc_id
  hive_metastore_tier = var.hive_metastore_tier
  kms_crypto_key_id   = module.gcs_hns_lakehouse.kms_crypto_key_id
  labels              = var.labels
}

# -----------------------------------------------------------------------------
# 4. Databricks on GCP Workspace, Compute Pools (N4/C4/M3/Z3) & Unity Catalog
# -----------------------------------------------------------------------------
module "databricks_workspace" {
  source = "./modules/databricks_workspace"

  project_id                  = var.project_id
  region                      = var.region
  environment                 = var.environment
  resource_prefix             = var.resource_prefix
  databricks_account_id       = var.databricks_account_id
  databricks_workspace_host   = var.databricks_workspace_host
  databricks_workspace_id     = var.databricks_workspace_id
  databricks_sql_warehouse_id = var.databricks_sql_warehouse_id
  databricks_catalog_schema   = var.databricks_catalog_schema
  vpc_id                      = module.network_and_psc.vpc_id
  subnet_id                   = module.network_and_psc.databricks_subnet_id
  lakehouse_bucket_name       = module.gcs_hns_lakehouse.lakehouse_bucket_name
  hive_metastore_ip           = module.external_hive_metastore.private_ip_address
  labels                      = var.labels
}

# -----------------------------------------------------------------------------
# 5. BigQuery Denodo 8.0 VDP Caching Layer ONLY (Strictly Scoped to Denodo Cache)
# -----------------------------------------------------------------------------
module "bigquery_biglake" {
  source = "./modules/bigquery_biglake"

  project_id              = var.project_id
  region                  = var.region
  bq_location             = var.bq_location
  environment             = var.environment
  resource_prefix         = var.resource_prefix
  lakehouse_bucket_name   = module.gcs_hns_lakehouse.lakehouse_bucket_name
  denodo_cache_dataset_id = var.denodo_cache_dataset_id
  kms_crypto_key_id       = module.gcs_hns_lakehouse.kms_crypto_key_id
  labels                  = var.labels
}

# -----------------------------------------------------------------------------
# 6. Denodo 8.0 Trial Server on GKE (Private GKE + Artifact Registry + ILB)
# -----------------------------------------------------------------------------
module "denodo_vdp_platform" {
  source = "./modules/denodo_vdp_platform"

  project_id                 = var.project_id
  region                     = var.region
  environment                = var.environment
  resource_prefix            = var.resource_prefix
  vpc_id                     = module.network_and_psc.vpc_id
  subnet_id                  = module.network_and_psc.denodo_subnet_id
  denodo_gke_master_cidr     = var.denodo_gke_master_cidr
  denodo_machine_type        = var.denodo_machine_type
  denodo_container_image_tag = var.denodo_container_image_tag
  denodo_cache_dataset_id    = module.bigquery_biglake.denodo_cache_dataset_id
  lakehouse_bucket_name      = module.gcs_hns_lakehouse.lakehouse_bucket_name
  denodo_cache_bucket        = module.gcs_hns_lakehouse.denodo_delta_cache_bucket_name
  databricks_jdbc_url        = module.databricks_workspace.sql_warehouse_jdbc_url
  kms_crypto_key_id          = module.gcs_hns_lakehouse.kms_crypto_key_id
  labels                     = var.labels
}
