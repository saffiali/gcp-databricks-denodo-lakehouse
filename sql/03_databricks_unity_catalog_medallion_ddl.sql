-- =============================================================================
-- Databricks on GCP Unity Catalog — R&D Data Mesh Medallion Lakehouse DDL
-- =============================================================================
-- Target Engine: Databricks on GCP Serverless/Pro SQL Warehouse (Delta Lake)
-- Storage Backing: GCS Hierarchical Namespace (HNS) Managed Folders (`gs://...`)
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS workspace.rd_lakehouse_medallion
  COMMENT 'Enterprise R&D Data Mesh Medallion Lakehouse on Databricks on GCP';

CREATE SCHEMA IF NOT EXISTS workspace.clinical_development
  COMMENT 'Data Mesh Node 1: Clinical Development (CDISC SDTM/ADaM & PK/PD Biomarkers)';

CREATE SCHEMA IF NOT EXISTS workspace.real_world_evidence
  COMMENT 'Data Mesh Node 2: Real-World Evidence (RWD) Longitudinal Cohorts & Synthetic Control Arms';

CREATE SCHEMA IF NOT EXISTS workspace.cmc_manufacturing
  COMMENT 'Data Mesh Node 3: CMC Biologics Batch Genealogy, LIMS Quality & ICH Q1A Stability';

-- 1. Silver CMC Batch Genealogy (Delta Lake w/ Liquid Clustering)
CREATE TABLE IF NOT EXISTS workspace.cmc_manufacturing.silver_cmc_batch_genealogy (
  comet_lot_id STRING NOT NULL,
  sap_werks STRING NOT NULL,
  sap_matnr STRING NOT NULL,
  sap_batch_charg STRING NOT NULL,
  molecule_id STRING NOT NULL,
  studyid STRING NOT NULL,
  manufacturing_site STRING NOT NULL,
  bioreactor_titer_g_l DOUBLE NOT NULL,
  purity_sec_hplc_pct DOUBLE NOT NULL,
  endotoxin_eu_ml DOUBLE NOT NULL,
  release_status STRING NOT NULL,
  qa_release_timestamp TIMESTAMP NOT NULL
)
USING DELTA
CLUSTER BY (molecule_id, studyid);

-- 2. Silver CDISC SDTM Demographics & Dosing (Delta Lake w/ Liquid Clustering)
CREATE TABLE IF NOT EXISTS workspace.clinical_development.silver_cdisc_dm_subjects (
  studyid STRING NOT NULL,
  molecule_id STRING NOT NULL,
  usubjid STRING NOT NULL,
  siteid STRING NOT NULL,
  country STRING NOT NULL,
  region_code STRING NOT NULL,
  age INT NOT NULL,
  sex STRING NOT NULL,
  arm_blinded STRING NOT NULL,
  arm_unblinded_treatment STRING NOT NULL,
  comet_lot_id STRING NOT NULL,
  dosing_start_date DATE NOT NULL
)
USING DELTA
CLUSTER BY (studyid, molecule_id);

-- 3. Silver PK/PD & Genomic Biomarker Assays (Delta Lake w/ Liquid Clustering)
CREATE TABLE IF NOT EXISTS workspace.clinical_development.silver_biomarker_pkpd (
  usubjid STRING NOT NULL,
  studyid STRING NOT NULL,
  molecule_id STRING NOT NULL,
  visit_week INT NOT NULL,
  ctdna_clearance_pct DOUBLE NOT NULL,
  pd_l1_expression_pct DOUBLE NOT NULL,
  serum_auc_0_tau DOUBLE NOT NULL,
  clinical_response_recist STRING NOT NULL,
  grade3_plus_ae_flag BOOLEAN NOT NULL
)
USING DELTA
CLUSTER BY (studyid, molecule_id);

-- 4. Silver Real-World Evidence (RWD) Synthetic Control Cohorts (Delta Lake)
CREATE TABLE IF NOT EXISTS workspace.real_world_evidence.silver_rwd_synthetic_control (
  rwd_cohort_id STRING NOT NULL,
  molecule_id STRING NOT NULL,
  indication STRING NOT NULL,
  data_registry_source STRING NOT NULL,
  matched_patient_count INT NOT NULL,
  propensity_score_smd DOUBLE NOT NULL,
  rwd_synthetic_control_pfs_months DOUBLE NOT NULL,
  standard_of_care_hr DOUBLE NOT NULL
)
USING DELTA
CLUSTER BY (molecule_id);
