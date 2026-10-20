-- =============================================================================
-- Databricks on GCP Unity Catalog — Enterprise Data Mesh Medallion Lakehouse DDL
-- =============================================================================
-- Target Engine: Databricks on GCP Serverless/Pro SQL Warehouse (Delta Lake)
-- Storage Backing: Standard GCS Bucket (UBLA = true, HNS Disabled) + Managed Folders
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS workspace.lakehouse_medallion
  COMMENT 'Enterprise Data Mesh Medallion Lakehouse on Databricks on GCP';

CREATE SCHEMA IF NOT EXISTS workspace.customer_analytics
  COMMENT 'Data Mesh Domain 1: Customer & Commercial Analytics';

CREATE SCHEMA IF NOT EXISTS workspace.supply_chain
  COMMENT 'Data Mesh Domain 2: Global Supply Chain, Orders & Inventory';

CREATE SCHEMA IF NOT EXISTS workspace.enterprise_finance
  COMMENT 'Data Mesh Domain 3: Enterprise Finance, Revenue & Risk Operations';

-- 1. Silver Supply Chain Order Genealogy (Delta Lake w/ Liquid Clustering)
CREATE TABLE IF NOT EXISTS workspace.supply_chain.silver_supply_chain_orders (
  order_batch_id STRING NOT NULL,
  erp_plant_code STRING NOT NULL,
  sku_material_id STRING NOT NULL,
  erp_order_number STRING NOT NULL,
  customer_id STRING NOT NULL,
  region_code STRING NOT NULL,
  fulfillment_center STRING NOT NULL,
  inventory_turnover_ratio DOUBLE NOT NULL,
  on_time_delivery_pct DOUBLE NOT NULL,
  defect_rate_ppm DOUBLE NOT NULL,
  shipment_release_status STRING NOT NULL,
  qa_release_timestamp TIMESTAMP NOT NULL
)
USING DELTA
CLUSTER BY (customer_id, region_code);

-- 2. Silver Customer Accounts & Segmentation (Delta Lake w/ Liquid Clustering)
CREATE TABLE IF NOT EXISTS workspace.customer_analytics.silver_customer_accounts (
  customer_id STRING NOT NULL,
  account_segment STRING NOT NULL,
  site_id STRING NOT NULL,
  country STRING NOT NULL,
  region_code STRING NOT NULL,
  tenure_months INT NOT NULL,
  pii_masked_tier STRING NOT NULL,
  account_executive_unmasked STRING NOT NULL,
  order_batch_id STRING NOT NULL,
  onboarding_date DATE NOT NULL
)
USING DELTA
CLUSTER BY (region_code, customer_id);

-- 3. Silver Enterprise Finance & Revenue Metrics (Delta Lake w/ Liquid Clustering)
CREATE TABLE IF NOT EXISTS workspace.enterprise_finance.silver_finance_revenue_metrics (
  customer_id STRING NOT NULL,
  region_code STRING NOT NULL,
  fiscal_quarter INT NOT NULL,
  net_retention_score_pct DOUBLE NOT NULL,
  annual_contract_value_usd DOUBLE NOT NULL,
  gross_margin_pct DOUBLE NOT NULL,
  credit_risk_rating STRING NOT NULL,
  forecasted_12m_ltv_usd DOUBLE NOT NULL,
  sla_exception_flag BOOLEAN NOT NULL
)
USING DELTA
CLUSTER BY (region_code, customer_id);
