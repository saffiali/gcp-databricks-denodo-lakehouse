output "vpc_network_id" {
  description = "Customer-managed Zero-Trust VPC ID hosting Databricks on GCP and Denodo 8.0 VDP."
  value       = module.network_and_psc.vpc_id
}

output "databricks_compute_subnet_id" {
  description = "Dedicated /19 subnet ID for Databricks on GCP GKE Enterprise worker nodes."
  value       = module.network_and_psc.databricks_subnet_id
}

output "denodo_vdp_subnet_id" {
  description = "Dedicated /22 subnet ID for Denodo 8.0 VDP Shielded VM MIG and Internal Passthrough NLB."
  value       = module.network_and_psc.denodo_subnet_id
}

output "psc_subnet_id" {
  description = "Dedicated /24 Private Service Connect (PSC) subnet ID."
  value       = module.network_and_psc.psc_subnet_id
}

output "lakehouse_bucket_url" {
  description = "Primary GCS Hierarchical Namespace (HNS) Bucket URI for Bronze/Silver/Gold Medallion tables."
  value       = module.gcs_hns_lakehouse.lakehouse_bucket_url
}

output "sts_landing_bucket_url" {
  description = "Cross-cloud Storage Transfer Service (STS) landing bucket URI."
  value       = module.gcs_hns_lakehouse.sts_landing_bucket_url
}

output "denodo_delta_cache_bucket_url" {
  description = "Dedicated GCS HNS bucket URI for Denodo 8.0 Parquet/Delta caching."
  value       = module.gcs_hns_lakehouse.denodo_delta_cache_bucket_url
}

output "gxp_worm_archive_bucket_url" {
  description = "30-Year GxP WORM retention archive bucket URI for batch release and regulatory lock snapshots."
  value       = module.gcs_hns_lakehouse.gxp_worm_archive_bucket_url
}

output "domain_service_accounts" {
  description = "Dedicated least-privilege GCP Service Accounts replacing legacy storage account keys and managed identities."
  value       = module.gcs_hns_lakehouse.service_account_emails
}

output "hive_metastore_private_ip" {
  description = "Private IP of the Regional HA Cloud SQL PostgreSQL 15 External Hive Metastore."
  value       = module.external_hive_metastore.private_ip_address
}

output "databricks_workspace_url" {
  description = "Databricks on GCP Workspace URL."
  value       = module.databricks_workspace.workspace_url
}

output "databricks_sql_warehouse_jdbc_url" {
  description = "Simba Spark JDBC URL for Denodo 8.0 VDP to query the GCP Databricks SQL Warehouse."
  value       = module.databricks_workspace.sql_warehouse_jdbc_url
}

output "unity_catalog_external_locations" {
  description = "Unity Catalog External Location URIs mapped to GCS HNS Managed Folders."
  value       = module.databricks_workspace.unity_catalog_external_locations
}

output "bigquery_denodo_cache_dataset" {
  description = "BigQuery Dataset ID used STRICTLY and EXCLUSIVELY for the Denodo 8.0 VDP Native Cache Engine."
  value       = module.bigquery_biglake.denodo_cache_dataset_id
}

output "denodo_gke_cluster_name" {
  description = "Private Regional GKE Cluster name hosting the Denodo 8.0 Trial Server StatefulSet."
  value       = module.denodo_vdp_platform.denodo_gke_cluster_name
}

output "denodo_artifact_registry_uri" {
  description = "Private Google Artifact Registry Docker/OCI image URI mirroring harbor.open.denodo.com for the Denodo Trial Server."
  value       = module.denodo_vdp_platform.denodo_artifact_registry_uri
}

output "denodo_vdp_jdbc_endpoint" {
  description = "Internal Passthrough LoadBalancer JDBC endpoint for the Denodo 8.0 Trial Server on GKE (:9999)."
  value       = module.denodo_vdp_platform.vdp_jdbc_endpoint
}

output "denodo_design_studio_url" {
  description = "Internal LoadBalancer URL for Denodo Design Studio (:9090/denodo-design-studio)."
  value       = module.denodo_vdp_platform.vdp_design_studio_url
}

output "denodo_data_catalog_url" {
  description = "Internal LoadBalancer URL for Denodo Data Catalog / Marketplace (:9090/denodo-data-catalog)."
  value       = module.denodo_vdp_platform.vdp_data_catalog_url
}
