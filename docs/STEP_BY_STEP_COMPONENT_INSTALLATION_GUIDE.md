# Step-by-Step Component Installation Guide

> **Component-by-Component Deployment Blueprint** — Install and verify each infrastructure layer independently in strict dependency order:
> 1. **Component 1 — Networking** (`module.network_and_psc`)
> 2. **Component 2 — GCS Managed Folder & Bucket Structure** (`module.gcs_medallion_lakehouse`)
> 3. **Component 3 — Databricks VMs, Unity Catalog & Hive Metastore** (`module.external_hive_metastore` + `module.databricks_workspace`)
> 4. **Component 4 — Denodo 9.0 on GCE Managed Instance Group (MIG)** (`module.bigquery_biglake` + `module.denodo_vdp_platform`)

---

## Installation Dependency Flow

```mermaid
flowchart LR
    classDef c1 fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px,color:#0d47a1
    classDef c2 fill:#fef7e0,stroke:#f29900,stroke-width:2px,color:#b06000
    classDef c3 fill:#fce8e6,stroke:#c5221f,stroke-width:2px,color:#a50e0e
    classDef c4 fill:#e6f4ea,stroke:#137333,stroke-width:2px,color:#0d652d

    P0["Phase 0\nterraform init &\nterraform.tfvars"] --> C1["Component 1: Networking\nCustom VPC, 4 Subnets, NAT,\nPrivate DNS, 5 Firewalls, VPC-SC"]:::c1
    C1 --> C2["Component 2: GCS & Managed Folders\n90d KMS CMEK, 5 Zero-Key SAs,\n4 Standard Buckets (No HNS),\n12 Managed Folders"]:::c2
    C2 --> C3["Component 3: Databricks VMs\nHA Cloud SQL PG15 HMS,\nN4/C4/M3/Z3 GCE Pools,\n9 Unity Catalog Locations"]:::c3
    C3 --> C4["Component 4: Denodo 9.0 on GCE MIG\nBigQuery Cache (50 GB BI Engine),\nRHEL 9 Base OS Template,\nRegional MIG (2–6 VMs) + NLB"]:::c4
```

| Automated Step-by-Step CLI | Command |
| :--- | :--- |
| **Dry-Run All 4 Components** | `./scripts/install_components_step_by_step.sh --component all --dry-run` |
| **Install Component 1 (Networking)** | `./scripts/install_components_step_by_step.sh --component 1 --project-id "<YOUR_GCP_PROJECT_ID>"` |
| **Install Component 2 (GCS & Managed Folders)** | `./scripts/install_components_step_by_step.sh --component 2 --project-id "<YOUR_GCP_PROJECT_ID>"` |
| **Install Component 3 (Databricks VMs)** | `./scripts/install_components_step_by_step.sh --component 3 --project-id "<YOUR_GCP_PROJECT_ID>"` |
| **Install Component 4 (Denodo 9.0 on GCE MIG)** | `./scripts/install_components_step_by_step.sh --component 4 --project-id "<YOUR_GCP_PROJECT_ID>"` |

---

## Phase 0 — Prerequisites & Workspace Initialization

```bash
# 1. Authenticate with Google Cloud & set target project
gcloud auth application-default login
export PROJECT_ID="<YOUR_GCP_PROJECT_ID>"
export REGION="europe-west2"
gcloud config set project "${PROJECT_ID}"

# 2. Copy and customize terraform.tfvars
cp terraform/terraform.tfvars.example terraform/terraform.tfvars

# 3. Initialize Terraform providers (google, google-beta, databricks)
terraform -chdir=terraform init
```

---

## Component 1 — Networking (`module.network_and_psc`)

<p align="center">
  <img src="../assets/02_zero_trust_network_and_vpc_sc_topology.svg" alt="Component 1: Zero-Trust Network & VPC-SC Topology" width="100%"/>
</p>

```mermaid
flowchart TB
    classDef vpc fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px,color:#0d47a1
    classDef snet fill:#ffffff,stroke:#1a73e8,stroke-width:1.5px,color:#1f1f1f
    classDef sec fill:#fce8e6,stroke:#c5221f,stroke-width:2px,color:#a50e0e

    subgraph VPC["Custom VPC (ent-prod-lakehouse-vpc) — Global Dynamic Routing"]
        S1["snet-databricks-workers\nPrimary: 10.168.0.0/19\nPods: 10.176.0.0/16 | Svc: 10.177.0.0/20"]:::snet
        S2["snet-denodo-vdp\nPrimary: 10.169.0.0/22\nDenodo 9.0 Regional MIG + Internal NLB"]:::snet
        S3["snet-psc-endpoints\nPrimary: 10.169.4.0/24\nPSC & Databricks SCC Relay"]:::snet
        S4["snet-ilb-proxies\nPrimary: 10.169.5.0/24\nREGIONAL_MANAGED_PROXY"]:::snet
        PSA["Private Service Access (/20)\n10.169.16.0/20 -> Cloud SQL PG15"]:::snet
    end

    DNS["Private Cloud DNS Zone\nrestricted.googleapis.com -> 199.36.153.4/30"]:::vpc
    NAT["Cloud Router + Cloud NAT\nEndpoint-Independent Mapping"]:::vpc
    FW["5 Micro-Segmented Firewalls\nP100 Restricted APIs | P150 JDBC | P200 DBX | P250 IAP/HC | P65534 Deny Internet"]:::sec
    VPCSC["VPC Service Controls Perimeter\nstorage, bigquery, compute, sqladmin, cloudkms, secretmanager"]:::sec

    S1 & S2 & S3 --> DNS
    S1 & S2 --> NAT
    FW --> VPC
    VPCSC --> VPC
```

### 1.1 What Gets Installed in Component 1

| Network Resource | Terraform Resource | CIDR / Specification |
| :--- | :--- | :--- |
| **Custom VPC** | `google_compute_network.lakehouse_vpc` | `REGIONAL` dynamic routing, default routes deleted |
| **Databricks Subnet** | `google_compute_subnetwork.databricks_compute_subnet` | `10.168.0.0/19` + GKE Pods `10.176.0.0/16` + Services `10.177.0.0/20` |
| **Denodo MIG Subnet** | `google_compute_subnetwork.denodo_vdp_subnet` | `10.169.0.0/22` (`private_ip_google_access = true`, Flow Logs enabled) |
| **PSC Endpoint Subnet** | `google_compute_subnetwork.psc_endpoints_subnet` | `10.169.4.0/24` (Private Service Connect & SCC relay) |
| **ILB Proxy Subnet** | `google_compute_subnetwork.ilb_proxy_subnet` | `10.169.5.0/24` (`REGIONAL_MANAGED_PROXY`, `ACTIVE`) |
| **Cloud SQL PSA Peering** | `google_service_networking_connection.private_vpc_connection` | `10.169.16.0/20` peering to `servicenetworking.googleapis.com` |
| **Restricted APIs DNS** | `google_dns_managed_zone.restricted_googleapis_zone` | `*.googleapis.com` $\rightarrow$ `restricted.googleapis.com` (`199.36.153.4/30`) |
| **5 Zero-Trust Firewalls** | `google_compute_firewall.*` | Priorities `100` (API Egress), `150` (Denodo$\rightarrow$DBX), `200` (DBX Internal), `250` (IAP/HC$\rightarrow$Denodo `:9999/:9090/:8000`), `65534` (Deny All Egress) |
| **VPC-SC Perimeter** | `google_access_context_manager_service_perimeter` | Locks down `storage`, `bigquery`, `compute`, `sqladmin`, `cloudkms`, `secretmanager` |

### 1.2 Step-by-Step Commands (Component 1)

```bash
# Step 1.1 — Preview Component 1 (Networking) plan
terraform -chdir=terraform plan -target=module.network_and_psc

# Step 1.2 — Apply Component 1 (Networking)
terraform -chdir=terraform apply -target=module.network_and_psc

# Step 1.3 — Verify Subnets, Firewall Priorities & Restricted Google APIs DNS
gcloud compute networks subnets list \
  --project="${PROJECT_ID}" \
  --network="ent-prod-lakehouse-vpc" \
  --regions="${REGION}"

gcloud compute firewall-rules list \
  --project="${PROJECT_ID}" \
  --filter="network:ent-prod-lakehouse-vpc" \
  --sort-by=priority \
  --format="table(name,direction,priority,sourceRanges.list(),targetTags.list())"

gcloud dns record-sets list \
  --project="${PROJECT_ID}" \
  --zone="ent-prod-lakehouse-restricted-googleapis-dns"
```

---

## Component 2 — GCS Managed Folder & Bucket Structure (`module.gcs_medallion_lakehouse`)

> **Critical Databricks Compatibility Requirement**: **Hierarchical Namespace (HNS) is disabled** across all GCS buckets because Databricks on GCP and Unity Catalog do not support HNS-enabled buckets. Subfolder IAM isolation is enforced on standard flat-namespace GCS buckets (`uniform_bucket_level_access = true`) using **12 GCS Managed Folders (`google_storage_managed_folder`)**.

<p align="center">
  <img src="../assets/03_storage_accounts_and_managed_folder_governance.svg" alt="Component 2: Storage Accounts & Standard GCS Managed Folder Structure" width="100%"/>
</p>

```mermaid
flowchart TB
    classDef kms fill:#fef7e0,stroke:#f29900,stroke-width:2px,color:#b06000
    classDef bkt fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px,color:#0d47a1
    classDef mf fill:#e6f4ea,stroke:#137333,stroke-width:1.5px,color:#0d652d
    classDef sa fill:#f3e8fd,stroke:#9334e6,stroke-width:1.5px,color:#681da8

    KMS["Cloud KMS CMEK KeyRing & CryptoKey\n90-Day Automatic Rotation (7,776,000s)"]:::kms

    subgraph Buckets["4 Standard Flat-Namespace GCS Buckets (uniform_bucket_level_access = true, NO HNS)"]
        B1["1. *-sts-landing\nIngress Landing Zone"]:::bkt
        B2["2. *-ent-lakehouse\nMedallion Lakehouse Bucket"]:::bkt
        B3["3. *-denodo-cache\nDenodo 9.0 Installer & BQ Avro Staging"]:::bkt
        B4["4. *-worm-archive\n30-Year WORM Retention (946,728,000s)"]:::bkt
    end

    subgraph Folders["12 Subfolder-Scoped GCS Managed Folders (google_storage_managed_folder)"]
        MF1["bronze/{customer_analytics,supply_chain,enterprise_finance}/"]:::mf
        MF2["silver/{customer_analytics,supply_chain,enterprise_finance}/"]:::mf
        MF3["gold/{customer_analytics,supply_chain,enterprise_finance}/"]:::mf
        MF4["hive_warehouse/ | unity_catalog/ | denodo_cache/"]:::mf
    end

    SA1["sa-cust-analytics\nobjectAdmin on */customer_analytics/"]:::sa
    SA2["sa-supply-chain\nobjectAdmin on */supply_chain/"]:::sa
    SA3["sa-ent-finance\nobjectAdmin on */enterprise_finance/"]:::sa
    SA4["sa-dbx-uc\nUnity Catalog External Location SA"]:::sa

    KMS --> B1 & B2 & B3 & B4
    B2 --> MF1 & MF2 & MF3 & MF4
    SA1 --> MF1 & MF2 & MF3
    SA2 --> MF1 & MF2 & MF3
    SA3 --> MF1 & MF2 & MF3
    SA4 --> B2
```

### 2.1 Bucket & Managed Folder Matrix

| Bucket / Managed Folder Resource | Terraform Resource | Folder Path / Policy | Bound Service Account |
| :--- | :--- | :--- | :--- |
| **Cloud KMS CMEK Key** | `google_kms_crypto_key.lakehouse_cmek_key` | `rotation_period = "7776000s"` (90 days) | GCS Service Agent + 5 SAs |
| **Bucket 1 — STS Landing** | `google_storage_bucket.sts_landing_bucket` | `gs://<prefix>-sts-landing` (UBLA = `true`, No HNS) | `sa-sts-ingest` (`objectCreator`) |
| **Bucket 2 — Medallion Lakehouse** | `google_storage_bucket.medallion_lakehouse_bucket` | `gs://<prefix>-ent-lakehouse` (UBLA = `true`, No HNS, Soft Delete `14d`) | `sa-dbx-uc` (`objectViewer`) |
| **Bucket 3 — Denodo Cache** | `google_storage_bucket.denodo_cache_staging_bucket` | `gs://<prefix>-denodo-cache` (UBLA = `true`, No HNS, 7d abort cleanup) | `sa-denodo-vdp` (`objectAdmin`) |
| **Bucket 4 — 30-Yr WORM Archive** | `google_storage_bucket.worm_compliance_archive_bucket` | `gs://<prefix>-worm-archive` (`946,728,000s` = 30-Yr Retention) | `sa-dbx-uc` (`objectCreator`) |
| **9 Domain Managed Folders** | `google_storage_managed_folder.medallion_domain_folders` | `{bronze,silver,gold}/{customer_analytics,supply_chain,enterprise_finance}/` | `sa-cust-analytics`, `sa-supply-chain`, `sa-ent-finance` (`objectAdmin`) |
| **3 System Managed Folders** | `google_storage_managed_folder.system_folders` | `hive_warehouse/`, `unity_catalog/`, `denodo_cache/` | `sa-dbx-uc` (`objectAdmin`) |

### 2.2 Step-by-Step Commands (Component 2)

```bash
# Step 2.1 — Preview Component 2 (KMS CMEK, 5 Service Accounts, 4 Standard Buckets, 12 Managed Folders)
terraform -chdir=terraform plan -target=module.gcs_medallion_lakehouse

# Step 2.2 — Apply Component 2
terraform -chdir=terraform apply -target=module.gcs_medallion_lakehouse

# Step 2.3 — Verify Standard GCS Bucket Configuration (UBLA = true, HNS Disabled, CMEK Active)
gcloud storage buckets describe "gs://ent-prod-lakehouse-ent-lakehouse" \
  --project="${PROJECT_ID}" \
  --format="yaml(name,iamConfiguration.uniformBucketLevelAccess,hierarchicalNamespace,encryption)"

# Step 2.4 — List all 12 GCS Managed Folders & Verify Subfolder IAM Policy
gcloud storage managed-folders list "gs://ent-prod-lakehouse-ent-lakehouse" \
  --project="${PROJECT_ID}"

gcloud storage managed-folders get-iam-policy \
  "gs://ent-prod-lakehouse-ent-lakehouse/gold/customer_analytics/" \
  --project="${PROJECT_ID}"
```

---

## Component 3 — Databricks VMs, Unity Catalog & External Hive Metastore (`module.external_hive_metastore` + `module.databricks_workspace`)

```mermaid
flowchart LR
    classDef hms fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px,color:#0d47a1
    classDef dbx fill:#fce8e6,stroke:#c5221f,stroke-width:2px,color:#a50e0e
    classDef uc fill:#fef7e0,stroke:#f29900,stroke-width:2px,color:#b06000

    subgraph HMS["1. External Hive Metastore (module.external_hive_metastore)"]
        PG["Cloud SQL PostgreSQL 15\nREGIONAL HA + Private IP Only\ndb-custom-8-32768 + CMEK"]:::hms
        SQL2["sql/02_hive_metastore_uri_rewrite.sql\nabfss:// -> gs:// URI Migration"]:::hms
    end

    subgraph Pools["2. Databricks GCE VM Node Pools (module.databricks_workspace)"]
        P1["pool-general-etl-n4\nn4-standard-16 (2–32 VMs)"]:::dbx
        P2["pool-photon-c4\nc4-highmem-32 (2–24 VMs)"]:::dbx
        P3["pool-memory-reconcile-m3\nm3-megamem-64 (1–12 VMs)"]:::dbx
        P4["pool-shuffle-heavy-z3\nz3-highmem-88 (2–16 VMs, 9TB NVMe)"]:::dbx
        P5["pool-streaming-dlt-n4\nn4-highmem-8 (2–20 VMs)"]:::dbx
        WH["Photon SQL Warehouse\n2X-Large (1–8 Clusters)"]:::dbx
    end

    subgraph UC["3. Unity Catalog Governance"]
        EXT["9 External Locations\nMapped to GCS Managed Folders"]:::uc
        DDL["sql/03_databricks_unity_catalog_medallion_ddl.sql\nLiquid-Clustered Bronze/Silver/Gold Tables"]:::uc
    end

    PG --> SQL2 --> Pools
    Pools --> EXT --> DDL
```

### 3.1 Databricks GCE VM Pools & Metastore Specification

| Component | Machine Type / SKU | Scaling & Disk | Workload Role |
| :--- | :--- | :--- | :--- |
| **External Hive Metastore** | Cloud SQL `POSTGRES_15` (`db-custom-8-32768`) | `REGIONAL` HA, `250 GB` SSD, Private IP (`PSA /20`) | Legacy Hive metadata (`DBS`, `SDS`, `SERDE_PARAMS`) |
| `pool-general-etl-n4` | `n4-standard-16` (16 vCPU, 64 GB) | `2–32` VMs, Hyperdisk Balanced | Standard Bronze $\rightarrow$ Silver Delta ETL |
| `pool-photon-c4` | `c4-highmem-32` (32 vCPU, 248 GB) | `2–24` VMs, Hyperdisk Extreme | High-concurrency Photon Gold aggregations |
| `pool-memory-reconcile-m3` | `m3-megamem-64` (64 vCPU, 976 GB) | `1–12` VMs, Hyperdisk Balanced | Large in-memory state reconciliation joins |
| `pool-shuffle-heavy-z3` | `z3-highmem-88` (88 vCPU, 704 GB) | `2–16` VMs, `9 TB` Local NVMe SSD | Multi-terabyte shuffle & sort workloads |
| `pool-streaming-dlt-n4` | `n4-highmem-8` (8 vCPU, 64 GB) | `2–20` VMs, Hyperdisk Balanced | Continuous Delta Live Tables (DLT) streaming |
| **Photon SQL Warehouse** | `2X-Large` (`PRO` / Serverless) | `1–8` clusters, `15m` auto-stop | Serves Denodo 9.0 Simba Spark JDBC `:443` queries |

### 3.2 Step-by-Step Commands (Component 3)

```bash
# Step 3.1 — Provision Regional HA Cloud SQL PostgreSQL 15 Hive Metastore & Databricks VM Pools
terraform -chdir=terraform plan \
  -target=module.external_hive_metastore \
  -target=module.databricks_workspace

terraform -chdir=terraform apply \
  -target=module.external_hive_metastore \
  -target=module.databricks_workspace

# Step 3.2 — Verify Cloud SQL Hive Metastore HA Instance & Private IP
HMS_IP=$(terraform -chdir=terraform output -raw hive_metastore_private_ip)
echo "External Hive Metastore Private IP: ${HMS_IP}"

# Step 3.3 — (If migrating legacy Hive tables) Run transactional abfss:// -> gs:// URI rewrite
psql "host=${HMS_IP} port=5432 dbname=hive_metastore user=hive_admin sslmode=require" \
  -f sql/02_hive_metastore_uri_rewrite.sql

# Step 3.4 — Bootstrap Unity Catalog Medallion Schemas & Liquid-Clustered Delta Tables
databricks sql-cli -f sql/03_databricks_unity_catalog_medallion_ddl.sql
```

---

## Component 4 — Denodo 9.0 on GCE Managed Instance Group (MIG) (`module.bigquery_biglake` + `module.denodo_vdp_platform`)

> **Enterprise Base OS Image Architecture**: Rather than using a rigid Marketplace appliance, Component 4 provisions a **Regional GCE Managed Instance Group (`google_compute_region_instance_group_manager`)** booting **Shielded `n4-standard-8` VMs** from **Enterprise Linux Base OS Images** (`projects/rhel-cloud/global/images/family/rhel-9`), paired with **BigQuery (`denodo_vdp_cache` + `50 GB` BI Engine)** and an unattended 5-stage silent installer (`scripts/install_denodo_vmss_startup.sh`).

<p align="center">
  <img src="../assets/04_denodo_vm_scaleset_installation_pipeline.svg" alt="Component 4: Denodo 9.0 on GCE Managed Instance Group (MIG) Installation Pipeline" width="100%"/>
</p>

```mermaid
flowchart TB
    classDef tf fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px,color:#0d47a1
    classDef mig fill:#e6f4ea,stroke:#137333,stroke-width:2px,color:#0d652d
    classDef boot fill:#fef7e0,stroke:#f29900,stroke-width:2px,color:#b06000
    classDef bq fill:#f3e8fd,stroke:#9334e6,stroke-width:2px,color:#681da8

    subgraph Step4A["Step 4A: Terraform Infrastructure (module.bigquery_biglake + module.denodo_vdp_platform)"]
        BQ["BigQuery denodo_vdp_cache\n+ 50 GB BI Engine Reservation"]:::bq
        SM["Secret Manager (CMEK)\ndenodo-9-license-key & vdp-admin-password"]:::tf
        TPL["Shielded Instance Template\nn4-standard-8 | 200 GB CMEK Hyperdisk\nBase Image: rhel-9"]:::tf
        MIG["Regional MIG (europe-west2-a/b/c)\nAutoscaler: 2–6 VMs (70% CPU)\nTCP :9999 Auto-Healing (15s)"]:::mig
        NLB["Internal Passthrough NLB (10.169.0.50)\nPorts: 9999, 9996, 9090, 9443, 8000"]:::mig
    end

    subgraph Step4B["Step 4B: Unattended Silent Installer & Zero-Downtime Rollout (deploy_denodo_vm_scaleset.sh)"]
        S1["Stage 1: Boot RHEL 9 Base OS\nInstall OpenJDK 17 + Kernel TCP Tuning"]:::boot
        S2["Stage 2: Pull GCS Artifacts\ndenodo-install-9.0 + Databricks/BQ JDBC"]:::boot
        S3["Stage 3: Fetch Secret Manager\nPull denodo.lic & VDP Admin Password"]:::boot
        S4["Stage 4: Silent Install & BQ Cache\ninstaller_cli.sh install --xml\nEnableHighThroughputAPI=1"]:::boot
        S5["Stage 5: VQL Bootstrap\nImport 01_denodo_vql_bootstrap.vql\nExpose dv_enterprise_customer_360"]:::boot
    end

    BQ & SM --> TPL --> MIG --> NLB
    MIG --> S1 --> S2 --> S3 --> S4 --> S5
```

### 4.1 Denodo 9.0 GCE MIG & BigQuery Cache Resource Matrix

| Resource | Terraform Resource / Script | Configuration |
| :--- | :--- | :--- |
| **BigQuery Cache Dataset** | `google_bigquery_dataset.denodo_vdp_cache_dataset` | `denodo_vdp_cache` (CMEK encrypted, granted to `sa-denodo-vdp`) |
| **BI Engine Reservation** | `google_bigquery_bi_engine_reservation` | `50 GB` (`53,687,091,200` bytes) in-memory cache acceleration |
| **CMEK Secrets** | `google_secret_manager_secret.*` | `*-denodo-9-license-key` (`denodo.lic`) & `*-denodo-vdp-admin-password` |
| **Enterprise Base OS Template** | `google_compute_instance_template.denodo_9_vmss_template` | `n4-standard-8`, `200 GB` CMEK Hyperdisk, `rhel-9` base image, Shielded Secure Boot + vTPM |
| **Regional MIG (Scale Set)** | `google_compute_region_instance_group_manager.denodo_vdp_mig` | 3 zones (`a/b/c`), `PROACTIVE` update policy (`max_surge = 3`, `max_unavailable = 0`) |
| **TCP `:9999` Health Check** | `google_compute_region_health_check.denodo_vdp_hc` | Probes VDP port `:9999` every `15s` (`300s` initial startup grace period) |
| **Regional CPU Autoscaler** | `google_compute_region_autoscaler.denodo_vdp_autoscaler` | Scales `2` $\rightarrow$ `6` VMs at `70%` CPU utilization |
| **Internal Passthrough NLB** | `google_compute_forwarding_rule.denodo_vdp_ilb_forwarding_rule` | Static VIP (`10.169.0.50`) on ports `9999, 9996, 9090, 9443, 8000` |

### 4.2 Step-by-Step Commands (Component 4)

```bash
# Step 4.1 — Provision BigQuery Denodo Cache (50 GB BI Engine) & Denodo 9.0 GCE Regional MIG
terraform -chdir=terraform plan \
  -target=module.bigquery_biglake \
  -target=module.denodo_vdp_platform

terraform -chdir=terraform apply \
  -target=module.bigquery_biglake \
  -target=module.denodo_vdp_platform

# Step 4.2 — Stage Denodo 9.0 Silent Installer, JDBC Drivers, License Secret & Trigger MIG Rollout
./scripts/deploy_denodo_vm_scaleset.sh \
  --project-id "${PROJECT_ID}" \
  --region "${REGION}" \
  --installer-archive "/path/to/denodo-install-9.0-linux64.tar.gz" \
  --license-file "/path/to/denodo.lic"

# Step 4.3 — Verify Regional MIG Instances, Health Status & Internal NLB VIP Endpoints
gcloud compute instance-groups managed list-instances \
  "ent-prod-lakehouse-denodo-9-vmss-mig" \
  --region="${REGION}" \
  --project="${PROJECT_ID}"

terraform -chdir=terraform output denodo_vdp_jdbc_uri
terraform -chdir=terraform output denodo_design_studio_url
terraform -chdir=terraform output denodo_scheduler_admin_url
```

---

## End-to-End Verification Checklist

```bash
# Run the 20-check offline Terraform & Security validation suite
python3 tests/validate_all.py
```

| Component | Verification Check | Expected Result |
| :--- | :--- | :--- |
| **1. Networking** | `gcloud compute firewall-rules list` | 5 rules active; internet egress blocked at priority `65534`; DNS resolves `*.googleapis.com` to `199.36.153.4/30` |
| **2. GCS & Managed Folders** | `gcloud storage managed-folders list` | 4 Standard GCS buckets (`UBLA = true`, **No HNS**) + 12 Managed Folders with domain SA bindings |
| **3. Databricks VMs** | `terraform output databricks_compute_pools` | HA Cloud SQL PG15 HMS + 5 GCE VM pools (`N4`, `C4`, `M3`, `Z3`) + 9 Unity Catalog External Locations |
| **4. Denodo 9.0 on GCE MIG** | `gcloud compute instance-groups managed list-instances` | `2–6` `RUNNING` Shielded RHEL 9 VMs passing `:9999` health checks behind Internal NLB (`10.169.0.50`) |
