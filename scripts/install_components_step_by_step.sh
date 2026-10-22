#!/usr/bin/env bash
# ==============================================================================
# Step-by-Step Component Installer:
#   Component 1: Networking (VPC, 4 Subnets, Cloud NAT, Private DNS, PSA, 5 Firewalls, VPC-SC)
#   Component 2: GCS Managed Folder & Bucket Structure (KMS CMEK, 5 SAs, 4 Standard Buckets [No HNS], 12 Managed Folders)
#   Component 3: Databricks VMs, Unity Catalog & External Hive Metastore (HA Cloud SQL PG15, N4/C4/M3/Z3 Pools, 9 UC Locations)
#   Component 4: Denodo 9.0 on GCE Managed Instance Group (BigQuery Cache + BI Engine, RHEL 9 Base OS Template, Regional MIG 2-6 VMs, NLB)
# ==============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TF_DIR="${REPO_ROOT}/terraform"

COMPONENT="all"
PROJECT_ID=""
REGION="europe-west2"
ENV_PREFIX="ent-prod-lakehouse"
DRY_RUN="false"
AUTO_APPROVE="-auto-approve"

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Installs the Enterprise Lakehouse & Denodo 9.0 platform component-by-component:
  1 | networking           Component 1: Custom VPC, 4 Subnets, Cloud NAT, Private DNS (199.36.153.4/30), PSA, 5 Firewalls & VPC-SC
  2 | gcs-managed-folders  Component 2: 90-Day KMS CMEK, 5 Zero-Key SAs, 4 Standard GCS Buckets (No HNS) & 12 Managed Folders
  3 | databricks-vms       Component 3: Regional HA Cloud SQL Hive Metastore, Databricks N4/C4/M3/Z3 VM Pools & Unity Catalog
  4 | denodo-mig           Component 4: BigQuery VDP Cache (50 GB BI Engine) + Denodo 9.0 on GCE Regional MIG (RHEL 9 Base OS)
  all                      Run Components 1 -> 2 -> 3 -> 4 sequentially (default)

Options:
  --component <1|2|3|4|all>   Component to install (default: all)
  --project-id <id>           Target Google Cloud Project ID (required for live apply)
  --region <region>           Target GCP region (default: europe-west2)
  --prefix <prefix>           Resource naming prefix (default: ent-prod-lakehouse)
  --dry-run                   Print and validate commands without executing live cloud mutations
  --no-auto-approve           Prompt interactively on terraform apply
  -h, --help                  Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --component)
      COMPONENT="$2"
      shift 2
      ;;
    --project-id)
      PROJECT_ID="$2"
      shift 2
      ;;
    --region)
      REGION="$2"
      shift 2
      ;;
    --prefix)
      ENV_PREFIX="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN="true"
      shift
      ;;
    --no-auto-approve)
      AUTO_APPROVE=""
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

run_cmd() {
  echo "  \$ $*"
  if [[ "${DRY_RUN}" == "false" ]]; then
    eval "$@"
  fi
}

header() {
  echo ""
  echo "================================================================================"
  echo "$1"
  echo "================================================================================"
}

# ------------------------------------------------------------------------------
# Phase 0: Initialize Terraform Workspace
# ------------------------------------------------------------------------------
init_terraform() {
  header "PHASE 0: Terraform Initialization & Configuration Check"
  if [[ ! -f "${TF_DIR}/terraform.tfvars" ]]; then
    echo "-> Creating ${TF_DIR}/terraform.tfvars from terraform.tfvars.example..."
    run_cmd "cp \"${TF_DIR}/terraform.tfvars.example\" \"${TF_DIR}/terraform.tfvars\""
  fi
  run_cmd "terraform -chdir=\"${TF_DIR}\" init"
}

# ------------------------------------------------------------------------------
# Component 1: Networking (VPC, Subnets, Cloud NAT, Private DNS, PSA, Firewalls, VPC-SC)
# ------------------------------------------------------------------------------
install_component_1_networking() {
  header "COMPONENT 1: Zero-Trust Networking, Subnets, Private DNS & VPC-SC (module.network_and_psc)"
  echo "Provisioning:"
  echo "  - Custom VPC (${ENV_PREFIX}-vpc) with Global Dynamic Routing"
  echo "  - 4 Segmented Subnets: Databricks (/19 + GKE Pods/Services), Denodo MIG (/22), PSC (/24), ILB Proxy (/24)"
  echo "  - Cloud Router & Cloud NAT + /20 Private Service Access (Cloud SQL peering)"
  echo "  - Private Cloud DNS Zone (restricted.googleapis.com -> 199.36.153.4/30)"
  echo "  - 5 Priority-Ordered Firewall Rules (Priorities 100, 150, 200, 250, 65534)"
  echo "  - VPC Service Controls (VPC-SC) Enforced Perimeter"
  echo ""
  run_cmd "terraform -chdir=\"${TF_DIR}\" apply -target=module.network_and_psc ${AUTO_APPROVE}"

  if [[ -n "${PROJECT_ID}" ]]; then
    echo ""
    echo "-> Verifying Component 1 (Networking):"
    run_cmd "gcloud compute networks subnets list --project=\"${PROJECT_ID}\" --network=\"${ENV_PREFIX}-vpc\" --regions=\"${REGION}\""
    run_cmd "gcloud compute firewall-rules list --project=\"${PROJECT_ID}\" --filter=\"network:${ENV_PREFIX}-vpc\" --sort-by=priority"
    run_cmd "gcloud dns record-sets list --project=\"${PROJECT_ID}\" --zone=\"${ENV_PREFIX}-restricted-googleapis-dns\""
  fi
}

# ------------------------------------------------------------------------------
# Component 2: GCS Managed Folder & Bucket Structure (Standard GCS, No HNS)
# ------------------------------------------------------------------------------
install_component_2_gcs_managed_folders() {
  header "COMPONENT 2: GCS Managed Folder & Bucket Structure (module.gcs_medallion_lakehouse)"
  echo "Provisioning:"
  echo "  - Cloud KMS KeyRing & CMEK CryptoKey (90-day rotation: 7,776,000s)"
  echo "  - 5 Domain-Scoped Zero-Key Service Accounts (sa-sts-ingest, sa-dbx-uc, sa-cust-analytics, sa-supply-chain, sa-ent-finance)"
  echo "  - 4 Standard GCS Buckets (uniform_bucket_level_access = true, HNS DISABLED for Databricks compatibility):"
  echo "      1. ${ENV_PREFIX}-sts-landing   (Ingress landing zone)"
  echo "      2. ${ENV_PREFIX}-ent-lakehouse (Medallion Bronze/Silver/Gold lakehouse)"
  echo "      3. ${ENV_PREFIX}-denodo-cache  (Denodo 9.0 silent installer & BigQuery Avro bulk-load staging)"
  echo "      4. ${ENV_PREFIX}-worm-archive  (30-Year Retention Policy: 946,728,000s)"
  echo "  - 12 Subfolder-Scoped GCS Managed Folders (google_storage_managed_folder) + Domain IAM Bindings"
  echo ""
  run_cmd "terraform -chdir=\"${TF_DIR}\" apply -target=module.gcs_medallion_lakehouse ${AUTO_APPROVE}"

  if [[ -n "${PROJECT_ID}" ]]; then
    echo ""
    echo "-> Verifying Component 2 (GCS Buckets & Managed Folders):"
    run_cmd "gcloud storage buckets describe \"gs://${ENV_PREFIX}-ent-lakehouse\" --project=\"${PROJECT_ID}\" --format=\"yaml(name,iamConfiguration.uniformBucketLevelAccess,encryption)\""
    run_cmd "gcloud storage managed-folders list \"gs://${ENV_PREFIX}-ent-lakehouse\" --project=\"${PROJECT_ID}\""
  fi
}

# ------------------------------------------------------------------------------
# Component 3: Databricks VMs, Unity Catalog & External Hive Metastore
# ------------------------------------------------------------------------------
install_component_3_databricks_vms() {
  header "COMPONENT 3: Databricks VMs, Unity Catalog & External Hive Metastore"
  echo "Provisioning:"
  echo "  - Regional HA Cloud SQL PostgreSQL 15 External Hive Metastore (module.external_hive_metastore)"
  echo "  - Databricks on GCP Workspace, Unity Catalog SA & 9 External Locations (module.databricks_workspace)"
  echo "  - 5 Next-Gen GCE VM Compute Pools:"
  echo "      * pool-general-etl-n4       -> n4-standard-16  (2..32 nodes, Hyperdisk Balanced)"
  echo "      * pool-photon-c4            -> c4-highmem-32   (2..24 nodes, Hyperdisk Extreme)"
  echo "      * pool-memory-reconcile-m3  -> m3-megamem-64   (1..12 nodes, In-Memory Join Pool)"
  echo "      * pool-shuffle-heavy-z3     -> z3-highmem-88   (2..16 nodes, 9 TB NVMe Local SSD)"
  echo "      * pool-streaming-dlt-n4     -> n4-highmem-8    (2..20 nodes, Delta Live Tables)"
  echo "  - Photon SQL Warehouse (2X-Large, 1..8 clusters, Serverless/Pro)"
  echo ""
  run_cmd "terraform -chdir=\"${TF_DIR}\" apply -target=module.external_hive_metastore -target=module.databricks_workspace ${AUTO_APPROVE}"

  echo ""
  echo "-> Post-Provisioning SQL Scripts for Component 3:"
  echo "   1. Hive Metastore URI Rewrite (abfss:// -> gs://): ${REPO_ROOT}/sql/02_hive_metastore_uri_rewrite.sql"
  echo "   2. Unity Catalog Medallion DDL (Bronze/Silver/Gold): ${REPO_ROOT}/sql/03_databricks_unity_catalog_medallion_ddl.sql"
}

# ------------------------------------------------------------------------------
# Component 4: Denodo 9.0 on GCE Managed Instance Group (MIG) + BigQuery Cache
# ------------------------------------------------------------------------------
install_component_4_denodo_mig() {
  header "COMPONENT 4: Denodo 9.0 on GCE Managed Instance Group (MIG) + BigQuery Cache"
  echo "Provisioning:"
  echo "  - BigQuery Native Denodo Cache Dataset (denodo_vdp_cache) + 50 GB BI Engine Reservation (module.bigquery_biglake)"
  echo "  - Cloud Secret Manager CMEK Secrets (denodo.lic + VDP Admin Password)"
  echo "  - Shielded GCE Instance Template (n4-standard-8, 200 GB CMEK Hyperdisk, RHEL 9 Base OS Image)"
  echo "  - Regional Managed Instance Group (MIG) across 3 zones (${REGION}-a/b/c) with TCP :9999 Health Check"
  echo "  - Regional CPU Autoscaler (min=2, max=6 VMs, target CPU 70%)"
  echo "  - Internal Passthrough Network Load Balancer (VIP on TCP :9999, :9996, :9090, :9443, :8000)"
  echo ""
  run_cmd "terraform -chdir=\"${TF_DIR}\" apply -target=module.bigquery_biglake -target=module.denodo_vdp_platform ${AUTO_APPROVE}"

  echo ""
  echo "-> Running Denodo 9.0 Silent Installer Staging & Zero-Downtime MIG Rolling Replacement:"
  if [[ "${DRY_RUN}" == "true" ]]; then
    run_cmd "\"${REPO_ROOT}/scripts/deploy_denodo_vm_scaleset.sh\" --project-id \"${PROJECT_ID:-<YOUR_GCP_PROJECT_ID>}\" --region \"${REGION}\" --dry-run"
  elif [[ -n "${PROJECT_ID}" ]]; then
    run_cmd "\"${REPO_ROOT}/scripts/deploy_denodo_vm_scaleset.sh\" --project-id \"${PROJECT_ID}\" --region \"${REGION}\""
  else
    echo "  (Tip: Pass --project-id <YOUR_GCP_PROJECT_ID> to execute live GCS staging & MIG rolling replacement)"
  fi
}

# ------------------------------------------------------------------------------
# Dispatch Selected Component(s)
# ------------------------------------------------------------------------------
init_terraform

case "${COMPONENT}" in
  1|networking)
    install_component_1_networking
    ;;
  2|gcs-managed-folders)
    install_component_2_gcs_managed_folders
    ;;
  3|databricks-vms)
    install_component_3_databricks_vms
    ;;
  4|denodo-mig)
    install_component_4_denodo_mig
    ;;
  all)
    install_component_1_networking
    install_component_2_gcs_managed_folders
    install_component_3_databricks_vms
    install_component_4_denodo_mig
    ;;
  *)
    echo "Invalid --component value: ${COMPONENT} (expected 1, 2, 3, 4, or all)" >&2
    usage
    exit 1
    ;;
esac

echo ""
echo "================================================================================"
echo "Completed Step-by-Step Component Installation (${COMPONENT})"
echo "================================================================================"
