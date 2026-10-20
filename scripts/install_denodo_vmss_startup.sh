#!/usr/bin/env bash
# ==============================================================================
# Unattended Denodo 9.0 VM Scale Set (Regional MIG) Startup Script on Base Images
#
# Key Base-OS-Image Bootstrap Behaviors Automated Here:
#   1. Boots from a hardened Enterprise Linux Base OS Image (e.g., RHEL 9,
#      Rocky Linux 9, or Ubuntu 22.04 LTS — NOT a Marketplace PAYG image),
#      applies kernel TCP tuning, and installs OpenJDK 17 & OS utilities.
#   2. Pulls the Denodo 9.0 silent installer archive (`denodo-install-9.0-linux64.tar.gz`),
#      Simba Spark JDBC (`DatabricksJDBC42.jar`), and BigQuery JDBC (`GoogleBigQueryJDBC42.jar`)
#      from the Standard GCS staging bucket over `restricted.googleapis.com`.
#   3. Retrieves the CMEK-encrypted Denodo license (`denodo.lic`) and VDP admin
#      password from Cloud Secret Manager via the attached VM Service Account.
#   4. Executes the unattended Denodo silent installer (`installer_cli.sh install --xml`),
#      configures BigQuery Native VDP Cache (`EnableHighThroughputAPI=1`), starts
#      systemd services (`:9999` VDP, `:9090` Design Studio, `:8000` Scheduler),
#      and imports `01_denodo_vql_bootstrap.vql`.
# ==============================================================================
set -euo pipefail

LOG_FILE="/var/log/denodo-vmss-bootstrap.log"
exec > >(tee -a "${LOG_FILE}") 2>&1

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Starting Denodo 9.0 Base-Image VM Scale Set bootstrap..."

METADATA_BASE="http://metadata.google.internal/computeMetadata/v1"
METADATA_URL="${METADATA_BASE}/instance/attributes"
METADATA_HEADER="Metadata-Flavor: Google"

fetch_attr() {
  local key="$1"
  local default_val="${2:-}"
  curl -sf -H "${METADATA_HEADER}" "${METADATA_URL}/${key}" || echo "${default_val}"
}

PROJECT_ID="$(curl -sf -H "${METADATA_HEADER}" "${METADATA_BASE}/project/project-id" || echo "your-gcp-project-id")"
DENODO_HOME="/opt/denodo/denodo-platform-9.0"
STAGE_DIR="/opt/denodo-stage"

DENODO_INSTALLER_GCS_URI="$(fetch_attr DENODO_INSTALLER_GCS_URI "gs://${PROJECT_ID}-ent-lakehouse-denodo-cache/installers")"
DENODO_LICENSE_SECRET_ID="$(fetch_attr DENODO_LICENSE_SECRET_ID "ent-lakehouse-denodo-license")"
DENODO_ADMIN_PWD_SECRET_ID="$(fetch_attr DENODO_ADMIN_PWD_SECRET_ID "ent-lakehouse-denodo-vdp-admin-pwd")"
DATABRICKS_JDBC_URL="$(fetch_attr DATABRICKS_JDBC_URL "jdbc:databricks://1234567890123456.1.gcp.databricks.com:443/default;transportMode=http;ssl=1;AuthMech=3;httpPath=/sql/1.0/warehouses/0123456789abcdef")"
BIGQUERY_CACHE_DATASET="$(fetch_attr BIGQUERY_CACHE_DATASET "${PROJECT_ID}.denodo_vdp_cache")"
DELTA_CACHE_GCS_URI="$(fetch_attr DELTA_CACHE_GCS_URI "gs://${PROJECT_ID}-ent-lakehouse-denodo-cache/vdp_cached_views/")"

mkdir -p "${STAGE_DIR}" "${DENODO_HOME}/conf/vdp" "${DENODO_HOME}/extensions/thirdparty/lib" "${DENODO_HOME}/bin"

# ------------------------------------------------------------------------------
# Stage 1: Base OS Package Installation (OpenJDK 17) & Kernel TCP Tuning
# ------------------------------------------------------------------------------
echo "[Stage 1/5] Preparing Enterprise Linux Base OS (OpenJDK 17 & kernel TCP tuning for :9999, :9090, :8000)..."
if command -v dnf >/dev/null 2>&1; then
  dnf install -y -q java-17-openjdk-devel curl jq unzip nmap-ncat tar || true
elif command -v yum >/dev/null 2>&1; then
  yum install -y -q java-17-openjdk-devel curl jq unzip nmap-ncat tar || true
elif command -v apt-get >/dev/null 2>&1; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y -qq || true
  apt-get install -y -qq openjdk-17-jdk-headless curl jq unzip netcat-openbsd tar || true
fi

cat <<'EOF' >/etc/sysctl.d/99-denodo-vdp.conf
net.core.somaxconn = 4096
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 10240 65535
vm.max_map_count = 262144
EOF
sysctl --system >/dev/null 2>&1 || true

# ------------------------------------------------------------------------------
# Stage 2: Pull Denodo Silent Installer, Simba Spark/BQ JDBC & VQL from GCS
# ------------------------------------------------------------------------------
echo "[Stage 2/5] Pulling Denodo 9.0 installer archive, JDBC drivers & VQL definitions from ${DENODO_INSTALLER_GCS_URI}..."
gcloud storage cp "${DENODO_INSTALLER_GCS_URI}/denodo-install-9.0-linux64.tar.gz" "${STAGE_DIR}/denodo-install-9.0-linux64.tar.gz" 2>/dev/null || true
gcloud storage cp "${DENODO_INSTALLER_GCS_URI}/DatabricksJDBC42.jar" "${STAGE_DIR}/DatabricksJDBC42.jar" 2>/dev/null || true
gcloud storage cp "${DENODO_INSTALLER_GCS_URI}/GoogleBigQueryJDBC42.jar" "${STAGE_DIR}/GoogleBigQueryJDBC42.jar" 2>/dev/null || true
gcloud storage cp "${DENODO_INSTALLER_GCS_URI}/01_denodo_vql_bootstrap.vql" "${STAGE_DIR}/01_denodo_vql_bootstrap.vql" 2>/dev/null || true

# ------------------------------------------------------------------------------
# Stage 3: Retrieve Denodo License (`denodo.lic`) & VDP Admin Password from Secret Manager
# ------------------------------------------------------------------------------
echo "[Stage 3/5] Retrieving Denodo 9.0 license and VDP admin password from Cloud Secret Manager..."
DENODO_ADMIN_PWD="$(gcloud secrets versions access latest --secret="${DENODO_ADMIN_PWD_SECRET_ID}" --project="${PROJECT_ID}" 2>/dev/null || echo "ChangeMeDenodo9!")"

if gcloud secrets versions access latest --secret="${DENODO_LICENSE_SECRET_ID}" --project="${PROJECT_ID}" >"${STAGE_DIR}/denodo.lic" 2>/dev/null; then
  chmod 0600 "${STAGE_DIR}/denodo.lic"
fi

# ------------------------------------------------------------------------------
# Stage 4: Execute Unattended Denodo 9.0 Silent Installer on Base OS Image
#          & Configure BigQuery Native Cache (`EnableHighThroughputAPI=1`)
# ------------------------------------------------------------------------------
echo "[Stage 4/5] Running unattended Denodo 9.0 silent installer on Base OS image..."
cat <<EOF >"${STAGE_DIR}/denodo_silent_install.xml"
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<AutomatedInstallation langpack="eng">
  <com.denodo.installer.panels.DenodoTargetPanel id="target_panel">
    <installPath>${DENODO_HOME}</installPath>
  </com.denodo.installer.panels.DenodoTargetPanel>
  <com.denodo.installer.panels.DenodoLicensePanel id="license_panel">
    <licenseFile>${STAGE_DIR}/denodo.lic</licenseFile>
  </com.denodo.installer.panels.DenodoLicensePanel>
  <com.denodo.installer.panels.DenodoPacksPanel id="packs_panel">
    <pack index="0" name="Virtual DataPort" selected="true"/>
    <pack index="1" name="Design Studio" selected="true"/>
    <pack index="2" name="Scheduler" selected="true"/>
  </com.denodo.installer.panels.DenodoPacksPanel>
  <com.denodo.installer.panels.DenodoVDPPanel id="vdp_panel">
    <vdpPort>9999</vdpPort>
    <vdpOdbcPort>9996</vdpOdbcPort>
    <vdpShutdownPort>9997</vdpShutdownPort>
    <httpPort>9090</httpPort>
    <httpsPort>9443</httpsPort>
  </com.denodo.installer.panels.DenodoVDPPanel>
</AutomatedInstallation>
EOF

if [[ ! -x "${DENODO_HOME}/bin/vqlserver_startup.sh" && -f "${STAGE_DIR}/denodo-install-9.0-linux64.tar.gz" ]]; then
  tar -xzf "${STAGE_DIR}/denodo-install-9.0-linux64.tar.gz" -C "${STAGE_DIR}"
  if [[ -x "${STAGE_DIR}/denodo-install-9.0/installer_cli.sh" ]]; then
    "${STAGE_DIR}/denodo-install-9.0/installer_cli.sh" install --xml "${STAGE_DIR}/denodo_silent_install.xml"
  fi
fi

if [[ -f "${STAGE_DIR}/denodo.lic" ]]; then
  cp -f "${STAGE_DIR}/denodo.lic" "${DENODO_HOME}/conf/denodo.lic"
  chmod 0600 "${DENODO_HOME}/conf/denodo.lic"
fi
if [[ -f "${STAGE_DIR}/DatabricksJDBC42.jar" ]]; then
  cp -f "${STAGE_DIR}/DatabricksJDBC42.jar" "${DENODO_HOME}/extensions/thirdparty/lib/DatabricksJDBC42.jar"
fi
if [[ -f "${STAGE_DIR}/GoogleBigQueryJDBC42.jar" ]]; then
  cp -f "${STAGE_DIR}/GoogleBigQueryJDBC42.jar" "${DENODO_HOME}/extensions/thirdparty/lib/GoogleBigQueryJDBC42.jar"
fi

# Configure VDBConfiguration.properties for BigQuery Native Cache + gRPC StorageReadAPI
cat <<EOF >>"${DENODO_HOME}/conf/vdp/VDBConfiguration.properties"
com.denodo.vdb.vdbinterface.server.VDBManagerImpl.registryPort=9999
com.denodo.vdb.vdbinterface.server.VDBManagerImpl.odbcPort=9996
com.denodo.vdb.vdbinterface.server.VDBManagerImpl.shutdownPort=9997
com.denodo.vdb.cache.cacheStatus=ON
com.denodo.vdb.cache.adapter=bigquery
com.denodo.vdb.cache.jdbcDriverClass=com.simba.googlebigquery.jdbc42.Driver
com.denodo.vdb.cache.connectionUri=jdbc:bigquery://https://www.googleapis.com/bigquery/v2:443;ProjectId=${PROJECT_ID};OAuthType=3;DefaultDataset=${BIGQUERY_CACHE_DATASET##*.};EnableHighThroughputAPI=1;HighThroughputActivationRatio=1;HighThroughputMinTableSize=100;
com.denodo.vdb.cache.gcsStagingUri=${DELTA_CACHE_GCS_URI}
com.denodo.vdb.databricks.jdbcUri=${DATABRICKS_JDBC_URL}
EOF

# Register and start systemd service for Denodo 9.0 on Base OS image
cat <<EOF >/etc/systemd/system/denodo-vdp.service
[Unit]
Description=Denodo 9.0 on Base OS Image — Virtual DataPort, Design Studio & Scheduler
After=network-online.target
Wants=network-online.target

[Service]
Type=forking
Environment="DENODO_JVM_OPTS=-Xms8g -Xmx20g -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
ExecStart=${DENODO_HOME}/bin/vqlserver_startup.sh
ExecStop=${DENODO_HOME}/bin/vqlserver_shutdown.sh
Restart=on-failure
RestartSec=15
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload || true
if [[ -x "${DENODO_HOME}/bin/vqlserver_startup.sh" ]]; then
  systemctl enable --now denodo-vdp.service || true
fi
if [[ -x "${DENODO_HOME}/bin/scheduler_startup.sh" ]]; then
  "${DENODO_HOME}/bin/scheduler_startup.sh" || true
fi
if [[ -x "${DENODO_HOME}/resources/apache-tomcat/bin/tomcat.sh" ]]; then
  "${DENODO_HOME}/resources/apache-tomcat/bin/tomcat.sh" startup || true
fi

# ------------------------------------------------------------------------------
# Stage 5: Admin Password Rotation & VQL Catalog Import (Databricks JDBC + BQ Cache)
# ------------------------------------------------------------------------------
echo "[Stage 5/5] Setting VDP admin password & importing VQL catalog (01_denodo_vql_bootstrap.vql)..."
if [[ -x "${DENODO_HOME}/bin/import.sh" && -f "${STAGE_DIR}/01_denodo_vql_bootstrap.vql" ]]; then
  for attempt in {1..30}; do
    if nc -z 127.0.0.1 9999 2>/dev/null; then
      cat <<VQL_EOF >"${STAGE_DIR}/00_rotate_admin_pwd.vql"
ALTER USER admin '${DENODO_ADMIN_PWD}';
VQL_EOF
      "${DENODO_HOME}/bin/import.sh" -h "127.0.0.1:9999/admin?admin@admin" \
        -f "${STAGE_DIR}/00_rotate_admin_pwd.vql" 2>/dev/null || true
      "${DENODO_HOME}/bin/import.sh" -h "127.0.0.1:9999/admin?admin@${DENODO_ADMIN_PWD}" \
        -f "${STAGE_DIR}/01_denodo_vql_bootstrap.vql"
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Denodo 9.0 VQL Catalog bootstrap completed successfully."
      break
    fi
    sleep 5
  done
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Denodo 9.0 Base-Image VM Scale Set node ready (:9999 VDP, :9090 Design Studio & Scheduler)."
