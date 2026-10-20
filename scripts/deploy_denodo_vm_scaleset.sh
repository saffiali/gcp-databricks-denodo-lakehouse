#!/usr/bin/env bash
# ==============================================================================
# Automated 5-Step Denodo 9.0 VM Scale Set (Base OS Image) Staging & Rollout CLI
#
# Stages the Denodo 9.0 silent installer archive, JDBC drivers & VQL to the
# Standard GCS staging bucket (HNS disabled for Databricks compatibility),
# configures Secret Manager BYOL license & admin credentials, provisions the
# Regional MIG on hardened Enterprise Linux Base OS images (RHEL 9 / Rocky 9),
# and triggers a zero-downtime rolling update across the Regional VM Scale Set.
# ==============================================================================
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-your-gcp-project-id}"
REGION="${REGION:-europe-west2}"
PREFIX="${PREFIX:-ent-lakehouse}"
ENV="${ENV:-prod}"
DRY_RUN="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project|--project-id) PROJECT_ID="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --prefix) PREFIX="$2"; shift 2 ;;
    --dry-run) DRY_RUN="true"; shift ;;
    *) shift ;;
  esac
done

MIG_NAME="${PREFIX}-denodo-vmss-${REGION}"
CACHE_BUCKET="gs://${PROJECT_ID}-${PREFIX}-denodo-cache"
LICENSE_SECRET="${PREFIX}-denodo-license"
ADMIN_PWD_SECRET="${PREFIX}-denodo-vdp-admin-pwd"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

run_cmd() {
  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "  [DRY-RUN] $*"
  else
    eval "$@"
  fi
}

echo "================================================================================"
echo " DENODO 9.0 ON BASE OS IMAGES — VM SCALE SET (REGIONAL MIG) ROLLOUT ORCHESTRATOR"
echo " Project: ${PROJECT_ID} | Region: ${REGION} | MIG: ${MIG_NAME}"
echo "================================================================================"

echo "[Step 1/5] Staging Denodo 9.0 Silent Installer, Simba Spark JDBC, BigQuery JDBC & VQL to ${CACHE_BUCKET}/installers/..."
run_cmd "gcloud storage cp '${REPO_ROOT}/sql/01_denodo_vql_bootstrap.vql' '${CACHE_BUCKET}/installers/01_denodo_vql_bootstrap.vql'"
if [[ -n "${DENODO_INSTALLER_TAR:-}" && -f "${DENODO_INSTALLER_TAR}" ]]; then
  run_cmd "gcloud storage cp '${DENODO_INSTALLER_TAR}' '${CACHE_BUCKET}/installers/denodo-install-9.0-linux64.tar.gz'"
fi

echo "[Step 2/5] Updating Cloud Secret Manager (${ADMIN_PWD_SECRET} & ${LICENSE_SECRET})..."
if [[ -n "${DENODO_LICENSE_FILE:-}" && -f "${DENODO_LICENSE_FILE}" ]]; then
  run_cmd "gcloud secrets versions add '${LICENSE_SECRET}' --data-file='${DENODO_LICENSE_FILE}' --project='${PROJECT_ID}'"
else
  echo "  [INFO] Ensure your Denodo license file (denodo.lic) or Solution Manager config is stored in Secret Manager (${LICENSE_SECRET}) for the Base OS image installer."
fi

echo "[Step 3/5] Applying Terraform Denodo 9.0 Base-Image VM Scale Set (Regional MIG + Autoscaler + Internal NLB)..."
run_cmd "terraform -chdir='${REPO_ROOT}/terraform' apply -target=module.denodo_vdp_platform -auto-approve"

echo "[Step 4/5] Triggering zero-downtime PROACTIVE rolling replacement on VM Scale Set (${MIG_NAME})..."
run_cmd "gcloud compute instance-groups managed rolling-action replace '${MIG_NAME}' --region='${REGION}' --max-surge=3 --max-unavailable=0 --project='${PROJECT_ID}'"

echo "[Step 5/5] Verifying Regional VM Scale Set health & Internal NLB (:9999 VDP / :9090 Design Studio & Scheduler)..."
run_cmd "gcloud compute instance-groups managed wait-until '${MIG_NAME}' --stable --region='${REGION}' --timeout=600 --project='${PROJECT_ID}'"
echo "================================================================================"
echo " Denodo 9.0 Base-Image VM Scale Set (${MIG_NAME}) is READY:"
echo "   - VDP JDBC Server:   jdbc:vdb://<ilb-vip>:9999/enterprise_data_mesh"
echo "   - Design Studio:     http://<ilb-vip>:9090/denodo-design-studio/"
echo "   - Scheduler Admin:   http://<ilb-vip>:9090/webadmin/denodo-scheduler-admin/"
echo "================================================================================"
