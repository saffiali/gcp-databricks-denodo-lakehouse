output "vpc_network_id" {
  description = "Customer-managed Zero-Trust VPC ID hosting Databricks on GCP and Denodo 9.0 VDP."
  value       = module.network_and_psc.vpc_id
}

output "databricks_compute_subnet_id" {
  description = "Dedicated /19 subnet ID for Databricks on GCP GKE Enterprise worker nodes."
  value       = module.network_and_psc.databricks_subnet_id
}

output "denodo_vdp_subnet_id" {
  description = "Dedicated /22 subnet ID for Denodo 9.0 VM Scale Set (Regional MIG on Base OS images) and Internal Passthrough NLB."
  value       = module.network_and_psc.denodo_subnet_id
}

output "psc_subnet_id" {
  description = "Dedicated /24 Private Service Connect (PSC) subnet ID."
  value       = module.network_and_psc.psc_subnet_id
}

output "lakehouse_bucket_url" {
  description = "Primary Standard GCS Bucket URI (Uniform Bucket-Level Access, HNS disabled for Databricks compatibility) for Bronze/Silver/Gold Medallion tables."
  value       = module.gcs_medallion_lakehouse.lakehouse_bucket_url
}

output "sts_landing_bucket_url" {
  description = "Cross-cloud Storage Transfer Service (STS) landing bucket URI."
  value       = module.gcs_medallion_lakehouse.sts_landing_bucket_url
}

output "denodo_delta_cache_bucket_url" {
  description = "Dedicated Standard GCS bucket URI for Denodo 9.0 Parquet/Delta caching and silent installer staging."
  value       = module.gcs_medallion_lakehouse.denodo_delta_cache_bucket_url
}

output "worm_archive_bucket_url" {
  description = "Long-term immutable WORM retention archive bucket URI for compliance lock snapshots."
  value       = module.gcs_medallion_lakehouse.worm_archive_bucket_url
}

output "domain_service_accounts" {
  description = "Dedicated least-privilege GCP Service Accounts replacing legacy storage account keys and managed identities."
  value       = module.gcs_medallion_lakehouse.service_account_emails
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
  description = "Simba Spark JDBC URL for Denodo 9.0 VDP to query the GCP Databricks SQL Warehouse."
  value       = module.databricks_workspace.sql_warehouse_jdbc_url
}

output "unity_catalog_external_locations" {
  description = "Unity Catalog External Location URIs mapped to Standard GCS Managed Folders."
  value       = module.databricks_workspace.unity_catalog_external_locations
}

output "bigquery_denodo_cache_dataset" {
  description = "BigQuery Dataset ID used STRICTLY and EXCLUSIVELY for the Denodo 9.0 VDP Native Cache Engine."
  value       = module.bigquery_biglake.denodo_cache_dataset_id
}

output "denodo_vmss_mig_name" {
  description = "Regional Managed Instance Group (VM Scale Set) name hosting Denodo 9.0 Shielded VMs built on Enterprise Base OS images."
  value       = module.denodo_vdp_platform.denodo_vmss_mig_name
}

output "denodo_vmss_autoscaler_name" {
  description = "Regional Autoscaler name scaling Denodo 9.0 VM Scale Set between 2 and 6 Shielded VMs."
  value       = module.denodo_vdp_platform.denodo_vmss_autoscaler_name
}

output "denodo_vdp_jdbc_endpoint" {
  description = "Internal Passthrough LoadBalancer JDBC endpoint for the Denodo 9.0 VM Scale Set (:9999)."
  value       = module.denodo_vdp_platform.vdp_jdbc_endpoint
}

output "denodo_design_studio_url" {
  description = "Internal LoadBalancer URL for Denodo 9.0 Design Studio Web Tool (:9090/denodo-design-studio/)."
  value       = module.denodo_vdp_platform.vdp_design_studio_url
}

output "denodo_scheduler_admin_url" {
  description = "Internal LoadBalancer URL for Denodo 9.0 Scheduler Admin Web Tool (:9090/webadmin/denodo-scheduler-admin/)."
  value       = module.denodo_vdp_platform.vdp_scheduler_admin_url
}

output "denodo_data_catalog_url" {
  description = "Internal LoadBalancer HTTPS URL for Denodo 9.0 Data Catalog (:9443/denodo-data-catalog)."
  value       = module.denodo_vdp_platform.vdp_data_catalog_url
}
