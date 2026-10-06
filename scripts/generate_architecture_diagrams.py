#!/usr/bin/env python3
"""Generates publication-grade HORIZONTAL-LAYERED SVG architecture diagrams with embedded official Google Cloud icons."""

import base64
import pathlib

ICON_DIR = pathlib.Path(
    "/google/src/cloud/saffi/databricks_denodo_gcp_demo/google3/"
    "googledata/html/external_content/gstatic/cgc/shared/product-icons"
)
REPO_ROOT = pathlib.Path(
    "/usr/local/google/home/saffi/teamwork_projects/databricks_denodo_gcp_single_env"
)
ASSETS_DIR = REPO_ROOT / "assets"


def load_icon_data_uri(name: str) -> str:
    path = ICON_DIR / name / f"{name}.png"
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:image/png;base64,{b64}"


def build_svg_1_end_to_end_horizontal(icons: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1040" width="100%" height="100%">
  <defs>
    <style>
      .title {{ font: 700 22px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 500 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #475569; }}
      .card-title {{ font: 700 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .card-body {{ font: 500 11px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #334155; }}
      .card-mono {{ font: 600 10.2px 'Roboto Mono', monospace; fill: #0f172a; }}
      .badge {{ font: 700 10.5px 'Roboto Mono', monospace; fill: #ffffff; }}
    </style>
    <filter id="shadow" x="-2%" y="-4%" width="104%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.07"/>
    </filter>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#7c3aed"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1d4ed8"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ea580c"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
  </defs>

  <!-- Canvas Background -->
  <rect width="1600" height="1040" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Top Header Banner -->
  <rect x="20" y="16" width="1560" height="64" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="20" y="16" width="10" height="64" rx="4" fill="#1a73e8"/>
  <text x="46" y="44" class="title">Single-Environment Enterprise Reference Architecture (Horizontal Layered View)</text>
  <text x="46" y="65" class="subtitle">Layer 1: Denodo 8.0 VDP Semantic Virtualization  |  Layer 2: BigQuery Native Denodo Cache ONLY  |  Layer 3: Databricks on GCP Lakehouse  |  Layer 4: GCS HNS &amp; 30-Yr GxP WORM</text>

  <!-- Outer VPC-SC Perimeter Box -->
  <rect x="20" y="96" width="1560" height="926" rx="14" fill="#f1f5f9" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="10,6"/>
  <rect x="40" y="85" width="710" height="22" rx="6" fill="#dc2626"/>
  <text x="52" y="100" class="badge">VPC SERVICE CONTROLS (VPC-SC) PERIMETER  |  ZERO PUBLIC IPs  |  restricted.googleapis.com (199.36.153.4/30)</text>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 1 (TOP): DENODO 8.0 TRIAL SERVER ON GKE TIER         -->
  <!-- ===================================================================== -->
  <rect x="36" y="118" width="1528" height="202" rx="12" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="2" filter="url(#shadow)"/>
  <rect x="36" y="118" width="1528" height="34" rx="10" fill="#7c3aed"/>
  <text x="54" y="140" class="badge" style="font-size:12px;">LAYER 1 — SEMANTIC VIRTUALIZATION &amp; DYNAMIC GOVERNANCE TIER: Denodo 8.0 Trial Server on GKE (modules/denodo_vdp_platform | k8s/01..05)</text>

  <!-- Card 1A: Downstream R&D Consumers -->
  <rect x="52" y="164" width="340" height="142" rx="10" fill="#ffffff" stroke="#ddd6fe" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['virtual_private_cloud']}" x="64" y="178" width="36" height="36"/>
  <text x="110" y="188" class="card-title">1A. Enterprise R&amp;D Consumers</text>
  <text x="110" y="204" class="card-body">Zero SQL or application code changes</text>
  <text x="68" y="228" class="card-mono">• Translational Medicine BI Dashboards</text>
  <text x="68" y="246" class="card-mono">• Unblinded DSMB Safety Review Boards</text>
  <text x="68" y="264" class="card-mono">• CMC Batch Release &amp; Stability QA</text>
  <text x="68" y="282" class="card-mono">• GenAI Clinical &amp; Regulatory Assistants</text>

  <!-- Card 1B: GKE Internal Passthrough NLB & Artifact Registry -->
  <rect x="410" y="164" width="346" height="142" rx="10" fill="#ffffff" stroke="#ddd6fe" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_load_balancing']}" x="422" y="178" width="38" height="38"/>
  <text x="470" y="188" class="card-title">1B. GKE Internal NLB &amp; Artifact Reg</text>
  <text x="470" y="204" class="card-mono">Service: denodo-vdp-internal-lb</text>
  <text x="426" y="226" class="card-body">• TCP :9999 (JDBC)  |  TCP :9996 (ODBC)</text>
  <text x="426" y="244" class="card-body">• HTTP :9090 / :9443 (Design Studio &amp; Catalog)</text>
  <text x="426" y="262" class="card-mono">• GAR Mirror: *-denodo-trial:8.0-trial</text>
  <text x="426" y="280" class="card-mono">• 30-Day Trial Lic: Secret Manager (CMEK)</text>

  <!-- Card 1C: Denodo 8.0 Trial Server on GKE (StatefulSet) -->
  <rect x="774" y="164" width="376" height="142" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['google_kubernetes_engine']}" x="786" y="178" width="38" height="38"/>
  <text x="834" y="188" class="card-title">1C. Denodo 8.0 Trial Server on GKE</text>
  <text x="834" y="204" class="card-mono">StatefulSet: denodo-vdp-trial (n4-standard-8)</text>
  <text x="790" y="224" class="card-body">• GKE Workload Identity (denodo-vdp-ksa) + 100Gi PVC</text>
  <rect x="790" y="234" width="344" height="62" rx="6" fill="#f5f3ff" stroke="#c4b5fd"/>
  <text x="800" y="250" class="card-title">InitContainers &amp; VQL Bootstrap Job (k8s/05):</text>
  <text x="800" y="266" class="card-mono">• Stages DatabricksJDBC42 &amp; GoogleBigQueryJDBC42</text>
  <text x="800" y="281" class="card-mono">• Imports dv_rd_molecule_360 &amp; dv_cmc_lot_trace</text>

  <!-- Card 1D: Dynamic GxP Blinding & Cross-Border Policy Engine -->
  <rect x="1192" y="164" width="356" height="142" rx="10" fill="#ffffff" stroke="#ddd6fe" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_armor']}" x="1204" y="178" width="36" height="36"/>
  <text x="1250" y="188" class="card-title">1D. Runtime Governance &amp; Masking</text>
  <text x="1250" y="204" class="card-body">Evaluated dynamically per user session</text>
  <rect x="1204" y="216" width="332" height="38" rx="6" fill="#fef2f2" stroke="#fecaca"/>
  <text x="1212" y="232" class="card-title" style="fill:#991b1b; font-size:11.8px;">Policy 1 (GxP Blinding): ROLE != DSMB_STATISTICIAN</text>
  <text x="1212" y="247" class="card-mono" style="fill:#7f1d1d;">-&gt; Masks treatment arm as '***BLINDED-GXP***'</text>
  <rect x="1204" y="260" width="332" height="38" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
  <text x="1212" y="276" class="card-title" style="fill:#1e40af; font-size:11.8px;">Policy 2 (Cross-Border Filter): GLOBAL_EX_CN</text>
  <text x="1212" y="291" class="card-mono" style="fill:#1e3a8a;">-&gt; Appends row filter WHERE region_code &lt;&gt; 'CN'</text>

  <!-- Layer 1 Horizontal Arrows -->
  <path d="M 392 235 L 408 235" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arrow-purple)"/>
  <path d="M 756 235 L 772 235" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arrow-purple)"/>
  <path d="M 1150 220 L 1190 220" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arrow-purple)"/>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 2: BIGQUERY NATIVE DENODO CACHE LAYER ONLY           -->
  <!-- ===================================================================== -->
  <rect x="36" y="342" width="1528" height="196" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <rect x="36" y="342" width="1528" height="34" rx="10" fill="#1d4ed8"/>
  <text x="54" y="364" class="badge" style="font-size:12px;">LAYER 2 — DENODO NATIVE CACHING LAYER ONLY: Google BigQuery + 50 GB BI Engine (modules/bigquery_biglake | Strictly Scoped to Denodo Cache)</text>

  <!-- Card 2A: Architectural Separation Mandate -->
  <rect x="52" y="388" width="340" height="136" rx="10" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['bigquery']}" x="64" y="402" width="38" height="38"/>
  <text x="112" y="410" class="card-title" style="fill:#1e3a8a;">2A. Architectural Separation Mandate</text>
  <text x="112" y="427" class="card-body" style="fill:#1e3a8a;">BigQuery does NOT replace Databricks.</text>
  <text x="66" y="450" class="card-body" style="fill:#1e3a8a;">• Provisioned strictly &amp; exclusively as the</text>
  <text x="66" y="467" class="card-body" style="fill:#1e3a8a;">  Denodo 8.0 VDP Native Cache Engine</text>
  <text x="66" y="484" class="card-body" style="fill:#1e3a8a;">  (replacing legacy Snowflake cache).</text>
  <text x="66" y="504" class="card-mono" style="fill:#1e3a8a;">• IAM: sa-denodo-vdp dataEditor ONLY</text>

  <!-- Card 2B: BigQuery Dataset denodo_vdp_cache + BI Engine -->
  <rect x="410" y="388" width="386" height="136" rx="10" fill="#ffffff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['bigquery']}" x="422" y="402" width="40" height="40"/>
  <text x="472" y="410" class="card-title">2B. BigQuery Dataset: denodo_vdp_cache (EU)</text>
  <text x="472" y="427" class="card-mono">+ 50 GB BI Engine In-Memory Acceleration</text>
  <rect x="424" y="438" width="358" height="74" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="434" y="456" class="card-title">Clustered Denodo Materialized Cache Tables:</text>
  <text x="434" y="474" class="card-mono" style="font-size:9.5px;">1. cache_dv_rd_molecule_360 (studyid, molecule_id)</text>
  <text x="434" y="492" class="card-mono" style="font-size:9.5px;">2. cache_dv_cmc_clinical_lot_trace (studyid, lot_id)</text>
  <text x="434" y="507" class="card-body">Encrypted at rest with Cloud KMS CMEK (90-day rotation)</text>

  <!-- Card 2C: Simba BigQuery JDBC + gRPC StorageReadAPI -->
  <rect x="814" y="388" width="352" height="136" rx="10" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['private_service_connect']}" x="826" y="402" width="38" height="38"/>
  <text x="874" y="410" class="card-title">2C. High-Throughput gRPC Read API</text>
  <text x="874" y="427" class="card-mono">EnableHighThroughputAPI=1</text>
  <text x="828" y="450" class="card-body">• Streams compressed Arrow/Avro blocks via</text>
  <text x="828" y="467" class="card-mono">  bigquerystorage.googleapis.com (:443)</text>
  <text x="828" y="485" class="card-body">• Granted roles/bigquery.readSessionUser</text>
  <text x="828" y="503" class="card-body">• Zero public internet traversal (VIP 199.36.153.4/30)</text>

  <!-- Card 2D: Live 3-Way Denodo Caching Benchmark -->
  <rect x="1192" y="388" width="356" height="136" rx="10" fill="#ffffff" stroke="#10b981" stroke-width="2" filter="url(#shadow)"/>
  <rect x="1192" y="388" width="356" height="26" rx="6" fill="#059669"/>
  <text x="1206" y="405" class="badge">2D. LIVE 3-WAY DENODO CACHING SPIKE BENCHMARK</text>
  <text x="1206" y="434" class="card-mono" style="fill:#047857;">1. BIGQUERY_NATIVE_CACHE:  1,077.2 ms (6.31x Speedup)</text>
  <text x="1206" y="456" class="card-mono" style="fill:#0369a1;">2. DELTA_GCS_CACHE (HNS):  1,584.1 ms (4.29x Speedup)</text>
  <text x="1206" y="478" class="card-mono" style="fill:#b91c1c;">3. DIRECT_UNCACHED_JDBC:   6,801.3 ms (1.00x Baseline)</text>
  <text x="1206" y="502" class="card-body">Verified on 4-table federated join (dv_rd_molecule_360)</text>

  <!-- Vertical Connectors between Layer 1 (Denodo VDP) and Layer 2 (BigQuery Cache) -->
  <path d="M 900 306 L 900 340" stroke="#1d4ed8" stroke-width="3" marker-end="url(#arrow-blue)" marker-start="url(#arrow-blue)"/>
  <rect x="642" y="315" width="246" height="20" rx="4" fill="#1d4ed8"/>
  <text x="650" y="329" class="badge">1. Cache Hit / Refresh (gRPC 1,077 ms)</text>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 3: DATABRICKS ON GCP LAKEHOUSE ENGINE & METASTORE    -->
  <!-- ===================================================================== -->
  <rect x="36" y="560" width="1528" height="210" rx="12" fill="#fff7ed" stroke="#f97316" stroke-width="2" filter="url(#shadow)"/>
  <rect x="36" y="560" width="1528" height="34" rx="10" fill="#ea580c"/>
  <text x="54" y="582" class="badge" style="font-size:12px;">LAYER 3 — PRIMARY LAKEHOUSE COMPUTE &amp; METASTORE TIER: Databricks on GCP + HA Cloud SQL Hive Metastore (snet-databricks 10.168.0.0/19)</text>

  <!-- Clean Channel Connector from Layer 1 (Denodo VDP) down through x=1179 gap to Layer 3 -->
  <path d="M 1150 275 L 1179 275 L 1179 558" fill="none" stroke="#ea580c" stroke-width="3" stroke-dasharray="6,3" marker-end="url(#arrow-orange)"/>
  <rect x="880" y="535" width="290" height="20" rx="4" fill="#ea580c"/>
  <text x="888" y="549" class="badge">2. Cache Miss / Pushdown (Simba Spark JDBC :443)</text>

  <!-- Card 3A: Databricks Workspace & Unity Catalog -->
  <rect x="52" y="606" width="356" height="150" rx="10" fill="#ffffff" stroke="#fed7aa" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['google_kubernetes_engine']}" x="64" y="620" width="38" height="38"/>
  <text x="112" y="628" class="card-title">3A. Databricks on GCP &amp; Unity Catalog</text>
  <text x="112" y="645" class="card-mono">Workspace ID: 8259555750233451 (PSC)</text>
  <text x="66" y="668" class="card-body">• Unity Catalog Credential: sa-dbx-uc-mvp</text>
  <text x="66" y="686" class="card-body">• 9 External Locations -&gt; HNS Managed Folders</text>
  <text x="66" y="704" class="card-mono">• Schemas: rd_lakehouse_medallion | cmc</text>
  <text x="66" y="722" class="card-mono">  clinical_development | real_world_evidence</text>
  <text x="66" y="740" class="card-body">• 11 Liquid-Clustered Delta Lake Tables</text>

  <!-- Card 3B: Next-Gen GCE Compute Pools -->
  <rect x="424" y="606" width="380" height="150" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['compute_engine']}" x="436" y="620" width="38" height="38"/>
  <text x="484" y="628" class="card-title">3B. Next-Gen GCE Compute Pools</text>
  <text x="484" y="645" class="card-body">Replaces legacy Standard_D96ds_v5 clusters</text>
  <text x="438" y="668" class="card-mono">• Clinical DDF ETL:  n4-standard-16 (16 vCPU, 64 GB)</text>
  <text x="438" y="686" class="card-mono">• RWD Cohort Joins:  c4-highmem-32  (32 vCPU, 248 GB)</text>
  <text x="438" y="704" class="card-mono">• Genomics / PK-PD:  m3-megamem-64  (64 vCPU, 976 GB)</text>
  <text x="438" y="722" class="card-mono">• Delta Cache Pool:  z3-highmem-88  (Titanium NVMe)</text>
  <text x="438" y="740" class="card-mono">• CMC Batch Pool:    n4-highmem-8   (8 vCPU, 64 GB)</text>

  <!-- Card 3C: Serverless / Pro SQL Warehouse -->
  <rect x="820" y="606" width="356" height="150" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['private_service_connect']}" x="832" y="620" width="38" height="38"/>
  <text x="880" y="628" class="card-title">3C. Serverless / Pro SQL Warehouse</text>
  <text x="880" y="645" class="card-mono">Warehouse ID: 0154a901254a4f17</text>
  <text x="834" y="668" class="card-body">• Photon Vectorized SQL Engine + Predictive I/O</text>
  <text x="834" y="686" class="card-body">• Liquid Clustering: CLUSTER BY (studyid, molecule_id)</text>
  <rect x="834" y="698" width="328" height="46" rx="6" fill="#ffedd5" stroke="#fb923c"/>
  <text x="844" y="716" class="card-mono">Simba Spark JDBC Target (:443 over PSC):</text>
  <text x="844" y="734" class="card-mono">/sql/1.0/warehouses/0154a901254a4f17</text>

  <!-- Card 3D: External Hive Metastore (HA Cloud SQL PostgreSQL 15) -->
  <rect x="1192" y="606" width="356" height="150" rx="10" fill="#ffffff" stroke="#fed7aa" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_sql']}" x="1204" y="620" width="36" height="36"/>
  <image href="{icons['secret_manager']}" x="1246" y="620" width="36" height="36"/>
  <text x="1290" y="628" class="card-title">3D. External Hive Metastore</text>
  <text x="1290" y="645" class="card-mono">HA Cloud SQL PG 15 (:5432)</text>
  <text x="1206" y="668" class="card-body">• REGIONAL HA + Private Service Access (/20) + SSL</text>
  <text x="1206" y="686" class="card-body">• Credentials injected via Cloud Secret Manager</text>
  <rect x="1206" y="698" width="328" height="46" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="1216" y="716" class="card-mono">URI Rewrite: UPDATE "SDS" SET "LOCATION" =</text>
  <text x="1216" y="734" class="card-mono">REGEXP_REPLACE(LOCATION, '^abfss://...', 'gs://...')</text>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 4 (BOTTOM): STORAGE ACCOUNTS, GCS HNS & 30-YR WORM   -->
  <!-- ===================================================================== -->
  <rect x="36" y="792" width="1528" height="214" rx="12" fill="#ecfdf5" stroke="#10b981" stroke-width="2" filter="url(#shadow)"/>
  <rect x="36" y="792" width="1528" height="34" rx="10" fill="#059669"/>
  <text x="54" y="814" class="badge" style="font-size:12px;">LAYER 4 — STORAGE ACCOUNTS (ZERO-KEY SAs), KMS CMEK, GCS HNS MEDALLION FOLDERS &amp; 30-YR GxP WORM (modules/gcs_hns_lakehouse)</text>

  <!-- Vertical Connectors between Layer 3 (Databricks) and Layer 4 (GCS HNS Storage) -->
  <path d="M 610 756 L 610 790" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)" marker-start="url(#arrow-green)"/>
  <path d="M 998 756 L 998 790" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)" marker-start="url(#arrow-green)"/>

  <!-- Card 4A: 7 Dedicated Service Accounts & KMS CMEK -->
  <rect x="52" y="838" width="340" height="154" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['identity_and_access_management']}" x="64" y="850" width="36" height="36"/>
  <image href="{icons['key_management_service']}" x="106" y="850" width="36" height="36"/>
  <text x="150" y="860" class="card-title">4A. 7 Zero-Key Service Accounts</text>
  <text x="150" y="876" class="card-body">&amp; Cloud KMS CMEK (90d Rotation)</text>
  <text x="66" y="898" class="card-mono">• sa-sts-ingest     (STS Landing Creator)</text>
  <text x="66" y="915" class="card-mono">• sa-uc-master      (Unity Catalog Master)</text>
  <text x="66" y="932" class="card-mono">• sa-clinical-ddf   (Clinical Folder Admin)</text>
  <text x="66" y="949" class="card-mono">• sa-rwd-cohorts    (RWD Folder Admin)</text>
  <text x="66" y="966" class="card-mono">• sa-cmc-mfg        (CMC Folder Admin)</text>
  <text x="66" y="983" class="card-mono">• sa-denodo-vdp-mvp (BQ &amp; GCS Cache Admin)</text>

  <!-- Card 4B: Primary GCS HNS Medallion Lakehouse Bucket & 12 Managed Folders -->
  <rect x="408" y="838" width="510" height="154" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="420" y="850" width="38" height="38"/>
  <text x="468" y="860" class="card-title">4B. Primary HNS Bucket: gs://*-rd-lakehouse-hns</text>
  <text x="468" y="876" class="card-mono" style="font-size:9.8px;">hierarchical_namespace = true (Atomic O(1) Rename + High QPS)</text>
  <rect x="420" y="888" width="156" height="92" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="428" y="906" class="card-title">1. Clinical DDF</text>
  <text x="428" y="923" class="card-mono" style="font-size:9.2px;">bronze/clinical_ddf/</text>
  <text x="428" y="939" class="card-mono" style="font-size:9.2px;">silver/clinical_ddf/</text>
  <text x="428" y="955" class="card-mono" style="font-size:9.2px;">gold/clinical_ddf/</text>
  <text x="428" y="971" class="card-body">ACL: sa-clinical-ddf</text>

  <rect x="585" y="888" width="156" height="92" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="593" y="906" class="card-title">2. Real-World Data</text>
  <text x="593" y="923" class="card-mono" style="font-size:9.2px;">bronze/real_world_data/</text>
  <text x="593" y="939" class="card-mono" style="font-size:9.2px;">silver/real_world_data/</text>
  <text x="593" y="955" class="card-mono" style="font-size:9.2px;">gold/real_world_data/</text>
  <text x="593" y="971" class="card-body">ACL: sa-rwd-cohorts</text>

  <rect x="750" y="888" width="156" height="92" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="758" y="906" class="card-title">3. CMC Biologics</text>
  <text x="758" y="923" class="card-mono" style="font-size:8.8px;">bronze/cmc_manufacturing/</text>
  <text x="758" y="939" class="card-mono" style="font-size:8.8px;">silver/cmc_manufacturing/</text>
  <text x="758" y="955" class="card-mono" style="font-size:8.8px;">gold/cmc_manufacturing/</text>
  <text x="758" y="971" class="card-body">ACL: sa-cmc-mfg</text>

  <!-- Card 4C: Companion STS Landing & Denodo Delta Cache Buckets -->
  <rect x="934" y="838" width="296" height="154" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="946" y="850" width="36" height="36"/>
  <text x="990" y="860" class="card-title">4C. STS &amp; Denodo Cache Buckets</text>
  <text x="990" y="876" class="card-body">Dedicated isolation per workload</text>
  <text x="946" y="900" class="card-mono">1. gs://*-sts-landing</text>
  <text x="946" y="916" class="card-body">   Cross-Cloud STS ingest + SHA-256</text>
  <text x="946" y="938" class="card-mono">2. gs://*-denodo-cache (HNS)</text>
  <text x="946" y="954" class="card-body">   Denodo MPP Parquet/Delta cache</text>
  <text x="946" y="974" class="card-mono">3. Filestore NFSv4.1 (Optional POSIX)</text>

  <!-- Card 4D: 30-Year GxP WORM Regulatory Archive Bucket -->
  <rect x="1246" y="838" width="302" height="154" rx="10" fill="#ffffff" stroke="#dc2626" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="1258" y="850" width="36" height="36"/>
  <text x="1302" y="860" class="card-title" style="fill:#991b1b;">4D. 30-Yr GxP WORM Archive</text>
  <text x="1302" y="876" class="card-mono" style="fill:#7f1d1d;">gs://*-gxp-worm-archive</text>
  <text x="1258" y="900" class="card-mono" style="fill:#7f1d1d;">• retention_period = 946728000s (30 Yrs)</text>
  <text x="1258" y="918" class="card-body" style="fill:#7f1d1d;">• 21 CFR Part 11 &amp; EU Annex 11 compliant</text>
  <text x="1258" y="936" class="card-body" style="fill:#7f1d1d;">• Object Versioning + ARCHIVE class</text>
  <text x="1258" y="954" class="card-body" style="fill:#7f1d1d;">• Immutable clinical trial lock &amp; CMC</text>
  <text x="1258" y="970" class="card-body" style="fill:#7f1d1d;">  batch release certificate storage</text>
</svg>
"""


def build_svg_2_network_and_vpc_sc_horizontal(icons: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 980" width="100%" height="100%">
  <defs>
    <style>
      .title {{ font: 700 22px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 500 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #475569; }}
      .card-title {{ font: 700 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .card-body {{ font: 500 11px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #334155; }}
      .card-mono {{ font: 600 10.2px 'Roboto Mono', monospace; fill: #0f172a; }}
      .badge {{ font: 700 10.5px 'Roboto Mono', monospace; fill: #ffffff; }}
    </style>
    <filter id="shadow" x="-2%" y="-4%" width="104%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.07"/>
    </filter>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1d4ed8"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
    </marker>
  </defs>

  <rect width="1600" height="980" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Header -->
  <rect x="20" y="16" width="1560" height="64" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="20" y="16" width="10" height="64" rx="4" fill="#dc2626"/>
  <text x="46" y="44" class="title">Zero-Trust Network Controls, Multi-Subnet Segmentation &amp; VPC-SC Perimeter (Horizontal Layered View)</text>
  <text x="46" y="65" class="subtitle">Layer 1: Zero-Trust Ingress &amp; Blocked Internet  |  Layer 2: 4 Segmented VPC Subnets  |  Layer 3: Micro-Segmented Firewall Matrix  |  Layer 4: Restricted Google APIs VIP</text>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 1: INGRESS ACCESS & BLOCKED PUBLIC INTERNET BOUNDARY -->
  <!-- ===================================================================== -->
  <rect x="20" y="94" width="1560" height="156" rx="12" fill="#f1f5f9" stroke="#64748b" stroke-width="2" filter="url(#shadow)"/>
  <rect x="20" y="94" width="1560" height="32" rx="10" fill="#334155"/>
  <text x="40" y="115" class="badge" style="font-size:12px;">LAYER 1 — ZERO-TRUST INGRESS ACCESS &amp; PUBLIC INTERNET EGRESS BOUNDARY</text>

  <rect x="38" y="136" width="480" height="102" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <image href="{icons['identity_and_access_management']}" x="52" y="152" width="38" height="38"/>
  <text x="102" y="160" class="card-title">1A. Identity-Aware Proxy (IAP) Zero-Trust Tunnel</text>
  <text x="102" y="178" class="card-mono">Source CIDR: 35.235.240.0/20 (TCP :22, :9090, :9443, :9999)</text>
  <text x="102" y="196" class="card-body">• Authenticates administrators &amp; data stewards via Google Identity</text>
  <text x="102" y="214" class="card-body">• Zero bastion public IPs required anywhere in the VPC</text>

  <rect x="536" y="136" width="480" height="102" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <image href="{icons['cloud_load_balancing']}" x="550" y="152" width="38" height="38"/>
  <text x="600" y="160" class="card-title">1B. GCP Health Probers &amp; Controlled Cloud NAT</text>
  <text x="600" y="178" class="card-mono">Health Check CIDRs: 130.211.0.0/22 &amp; 35.191.0.0/16</text>
  <text x="600" y="196" class="card-body">• Probes Denodo VDP Internal Passthrough NLB on TCP :9999</text>
  <text x="600" y="214" class="card-body">• Cloud NAT (ERRORS_ONLY logging) for allowlisted OS patching</text>

  <rect x="1034" y="136" width="528" height="102" rx="10" fill="#fef2f2" stroke="#dc2626" stroke-width="2"/>
  <image href="{icons['cloud_armor']}" x="1048" y="152" width="38" height="38"/>
  <text x="1098" y="160" class="card-title" style="fill:#991b1b;">1C. Public Internet (0.0.0.0/0) — EGRESS BLOCKED</text>
  <text x="1098" y="178" class="card-mono" style="fill:#7f1d1d;">Firewall Priority 65534: DENY ALL + INCLUDE_ALL_METADATA</text>
  <text x="1098" y="196" class="card-body" style="fill:#7f1d1d;">• Zero public IPs on Databricks workers or Denodo VDP VMs</text>
  <text x="1098" y="214" class="card-body" style="fill:#7f1d1d;">• VPC-SC blocks unauthorized cross-project copies/exports</text>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 2: CUSTOMER-MANAGED VPC & 4 SEGMENTED SUBNETS        -->
  <!-- ===================================================================== -->
  <rect x="20" y="270" width="1560" height="248" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <rect x="20" y="270" width="1560" height="34" rx="10" fill="#1d4ed8"/>
  <text x="40" y="292" class="badge" style="font-size:12px;">LAYER 2 — CUSTOMER-MANAGED VPC: rd-lakehouse-vpc-mvp (4 Dedicated Subnets + Private Service Access + Private Cloud DNS)</text>

  <!-- Subnet A: Databricks Compute -->
  <rect x="38" y="316" width="372" height="188" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2" filter="url(#shadow)"/>
  <rect x="38" y="316" width="372" height="28" rx="8" fill="#ea580c"/>
  <text x="50" y="335" class="badge">SUBNET A: snet-databricks (10.168.0.0/19)</text>
  <image href="{icons['google_kubernetes_engine']}" x="50" y="356" width="36" height="36"/>
  <text x="96" y="368" class="card-title">Databricks Compute Plane (8,192 IPs)</text>
  <text x="96" y="384" class="card-mono">GKE Pods: 10.176.0.0/16 (65,536 IPs)</text>
  <text x="96" y="400" class="card-mono">GKE Svc:  10.177.0.0/20 (4,096 IPs)</text>
  <text x="50" y="424" class="card-mono">• Tag: [databricks-worker] | Flow Logs: 5s</text>
  <text x="50" y="442" class="card-body">• Hosts N4, C4, M3, Z3 GCE worker pools</text>
  <text x="50" y="460" class="card-body">• Outbound :5432 -&gt; Cloud SQL Hive Metastore</text>
  <text x="50" y="478" class="card-body">• Outbound :443  -&gt; restricted.googleapis.com</text>

  <!-- Subnet B: Denodo Trial Server on GKE -->
  <rect x="424" y="316" width="372" height="188" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2" filter="url(#shadow)"/>
  <rect x="424" y="316" width="372" height="28" rx="8" fill="#7c3aed"/>
  <text x="436" y="335" class="badge">SUBNET B: snet-denodo-vdp (10.169.0.0/22)</text>
  <image href="{icons['google_kubernetes_engine']}" x="436" y="356" width="36" height="36"/>
  <text x="482" y="368" class="card-title">Denodo 8.0 Trial GKE Cluster (1,024 IPs)</text>
  <text x="482" y="384" class="card-mono">GKE Pods: 10.178.0.0/18 (16,384 IPs)</text>
  <text x="482" y="400" class="card-mono">GKE Svc:  10.179.0.0/20 (4,096 IPs)</text>
  <text x="436" y="424" class="card-mono">• Tag: [denodo-gke-node] | Workload Identity</text>
  <text x="436" y="442" class="card-body">• Outbound :443 -&gt; Databricks PSC Endpoint</text>
  <text x="436" y="460" class="card-body">• Outbound :443 -&gt; BigQuery StorageReadAPI</text>
  <text x="436" y="478" class="card-body">• GKE Internal NLB (:9999 JDBC / :9090 UI)</text>

  <!-- Subnet C & D: PSC & ILB Proxy -->
  <rect x="810" y="316" width="372" height="188" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2" filter="url(#shadow)"/>
  <rect x="810" y="316" width="372" height="28" rx="8" fill="#0284c7"/>
  <text x="822" y="335" class="badge">SUBNET C &amp; D: PSC (/24) &amp; ILB PROXY (/24)</text>
  <image href="{icons['private_service_connect']}" x="822" y="356" width="36" height="36"/>
  <text x="868" y="368" class="card-title">Private Service Connect &amp; Envoy</text>
  <text x="868" y="384" class="card-mono">Subnet C: snet-psc (10.169.4.0/24)</text>
  <text x="868" y="400" class="card-mono">Subnet D: snet-ilb-proxy (10.169.5.0/24)</text>
  <text x="822" y="424" class="card-mono">• IP: rd-lakehouse-psc-databricks-ip</text>
  <text x="822" y="442" class="card-body">• Terminates Databricks Control Plane Web UI,</text>
  <text x="822" y="460" class="card-body">  SCC relay &amp; SQL Warehouse Private Link</text>
  <text x="822" y="478" class="card-body">• REGIONAL_MANAGED_PROXY for L7 HTTPS ILB</text>

  <!-- PSA Peering & Private Cloud DNS -->
  <rect x="1196" y="316" width="366" height="188" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <rect x="1196" y="316" width="366" height="28" rx="8" fill="#059669"/>
  <text x="1208" y="335" class="badge">PSA PEERING (/20) &amp; PRIVATE CLOUD DNS</text>
  <image href="{icons['cloud_dns']}" x="1208" y="356" width="36" height="36"/>
  <image href="{icons['cloud_sql']}" x="1250" y="356" width="36" height="36"/>
  <text x="1296" y="368" class="card-title">Cloud DNS &amp; PSA Peering</text>
  <text x="1296" y="384" class="card-mono">Zone: googleapis.com. (Private)</text>
  <text x="1208" y="408" class="card-mono">• *.googleapis.com -&gt; restricted.googleapis.com</text>
  <text x="1208" y="426" class="card-mono">• A Records: 199.36.153.4, .5, .6, .7 (/30)</text>
  <text x="1208" y="446" class="card-body">• PSA /20 Peering: HA Cloud SQL PG 15 (:5432)</text>
  <text x="1208" y="464" class="card-body">• Optional Filestore Enterprise NFSv4.1 (:2049)</text>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 3: MICRO-SEGMENTED ZERO-TRUST FIREWALL MATRIX        -->
  <!-- ===================================================================== -->
  <rect x="20" y="538" width="1560" height="196" rx="12" fill="#ffffff" stroke="#1e293b" stroke-width="2" filter="url(#shadow)"/>
  <rect x="20" y="538" width="1560" height="34" rx="10" fill="#1e293b"/>
  <text x="40" y="560" class="badge" style="font-size:12px;">LAYER 3 — ZERO-TRUST GCP FIREWALL POLICY LAYER (5 PRIORITY-ORDERED INGRESS &amp; EGRESS RULES)</text>

  <rect x="38" y="584" width="292" height="136" rx="8" fill="#f0fdf4" stroke="#10b981" stroke-width="1.5"/>
  <text x="50" y="604" class="card-title" style="fill:#047857;">Rule 1: Priority 100 (EGRESS)</text>
  <text x="50" y="622" class="card-mono" style="fill:#065f46;">ALLOW tcp:443</text>
  <text x="50" y="640" class="card-mono">Dest: 199.36.153.4/30</text>
  <text x="50" y="662" class="card-body">Allows private egress to</text>
  <text x="50" y="678" class="card-body">restricted.googleapis.com</text>
  <text x="50" y="694" class="card-body">(GCS, BQ, GAR, KMS, Secret Mgr)</text>

  <rect x="344" y="584" width="292" height="136" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="356" y="604" class="card-title" style="fill:#1d4ed8;">Rule 2: Priority 150 (INGRESS)</text>
  <text x="356" y="622" class="card-mono" style="fill:#1e40af;">ALLOW tcp:443, 8443</text>
  <text x="356" y="640" class="card-mono">Src: 10.169/22, 10.178/18 (GKE)</text>
  <text x="356" y="662" class="card-body">Target: [databricks-worker]</text>
  <text x="356" y="678" class="card-body">Permits Denodo Trial GKE pods</text>
  <text x="356" y="694" class="card-body">Simba Spark JDBC pushdown</text>

  <rect x="650" y="584" width="296" height="136" rx="8" fill="#fff7ed" stroke="#f97316" stroke-width="1.5"/>
  <text x="662" y="604" class="card-title" style="fill:#c2410c;">Rule 3: Priority 200 (INGRESS)</text>
  <text x="662" y="622" class="card-mono" style="fill:#9a3412;">ALLOW tcp:443,2049,5432,8443</text>
  <text x="662" y="640" class="card-mono">Src: 10.168.0.0/19, 10.176/16</text>
  <text x="662" y="662" class="card-body">Target: [databricks-worker]</text>
  <text x="662" y="678" class="card-body">Intra-cluster Spark shuffle,</text>
  <text x="662" y="694" class="card-body">Cloud SQL HMS &amp; Filestore</text>

  <rect x="960" y="584" width="296" height="136" rx="8" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5"/>
  <text x="972" y="604" class="card-title" style="fill:#6d28d9;">Rule 4: Priority 250 (INGRESS)</text>
  <text x="972" y="622" class="card-mono" style="fill:#5b21b6;">ALLOW tcp:22,9090,9443,9996,9999</text>
  <text x="972" y="640" class="card-mono">Src: 35.235.240.0/20 (IAP) &amp; HC</text>
  <text x="972" y="662" class="card-body">Target: [denodo-gke-node]</text>
  <text x="972" y="678" class="card-body">Zero-Trust IAP admin, GKE NLB</text>
  <text x="972" y="694" class="card-body">health checks &amp; JDBC/Design Studio</text>

  <rect x="1270" y="584" width="292" height="136" rx="8" fill="#fef2f2" stroke="#dc2626" stroke-width="2"/>
  <text x="1282" y="604" class="card-title" style="fill:#b91c1c;">Rule 5: Priority 65534 (EGRESS)</text>
  <text x="1282" y="622" class="card-mono" style="fill:#991b1b;">DENY ALL PROTOCOLS</text>
  <text x="1282" y="640" class="card-mono">Dest: 0.0.0.0/0 (Internet)</text>
  <text x="1282" y="662" class="card-body" style="fill:#7f1d1d;">Blocks all unauthorized internet</text>
  <text x="1282" y="678" class="card-body" style="fill:#7f1d1d;">egress with full packet metadata</text>
  <text x="1282" y="694" class="card-mono" style="fill:#991b1b;">Log: INCLUDE_ALL_METADATA</text>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 4 (BOTTOM): RESTRICTED GOOGLE APIs VIP & VPC-SC      -->
  <!-- ===================================================================== -->
  <rect x="20" y="754" width="1560" height="206" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <rect x="20" y="754" width="1560" height="34" rx="10" fill="#059669"/>
  <text x="40" y="776" class="badge" style="font-size:12px;">LAYER 4 — RESTRICTED GOOGLE APIs VIP (199.36.153.4/30) &amp; VPC SERVICE CONTROLS (VPC-SC) PROTECTED SERVICES</text>

  <rect x="38" y="800" width="372" height="144" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5"/>
  <image href="{icons['cloud_storage']}" x="52" y="814" width="40" height="40"/>
  <text x="104" y="824" class="card-title">storage.googleapis.com</text>
  <text x="104" y="841" class="card-mono">VPC-SC Perimeter Locked</text>
  <text x="52" y="866" class="card-body">• STS Landing Bucket (gs://*-sts-landing)</text>
  <text x="52" y="884" class="card-body">• Primary Medallion HNS Lakehouse Bucket</text>
  <text x="52" y="902" class="card-body">• Denodo Delta Cache HNS Bucket</text>
  <text x="52" y="920" class="card-body">• 30-Yr GxP WORM Archive Bucket</text>

  <rect x="424" y="800" width="372" height="144" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5"/>
  <image href="{icons['bigquery']}" x="438" y="814" width="40" height="40"/>
  <text x="490" y="824" class="card-title">bigquery &amp; bigquerystorage APIs</text>
  <text x="490" y="841" class="card-mono">Denodo 8.0 Native Cache ONLY</text>
  <text x="438" y="866" class="card-body">• Dataset: denodo_vdp_cache (EU)</text>
  <text x="438" y="884" class="card-body">• 50 GB BI Engine In-Memory Acceleration</text>
  <text x="438" y="902" class="card-body">• High-Throughput gRPC StorageReadAPI</text>
  <text x="438" y="920" class="card-body">• Accessible solely by sa-denodo-vdp</text>

  <rect x="810" y="800" width="372" height="144" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5"/>
  <image href="{icons['key_management_service']}" x="824" y="814" width="40" height="40"/>
  <image href="{icons['secret_manager']}" x="870" y="814" width="40" height="40"/>
  <text x="920" y="824" class="card-title">cloudkms &amp; secretmanager</text>
  <text x="920" y="841" class="card-mono">90-Day CMEK &amp; Vault Secrets</text>
  <text x="824" y="866" class="card-body">• Encrypts all 4 GCS Buckets &amp; HNS folders</text>
  <text x="824" y="884" class="card-body">• Encrypts HA Cloud SQL Hive Metastore</text>
  <text x="824" y="902" class="card-body">• Encrypts BigQuery Cache &amp; Hyperdisks</text>
  <text x="824" y="920" class="card-body">• Stores Hive Metastore &amp; JDBC passwords</text>

  <rect x="1196" y="800" width="366" height="144" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5"/>
  <image href="{icons['google_kubernetes_engine']}" x="1210" y="814" width="40" height="40"/>
  <image href="{icons['cloud_sql']}" x="1256" y="814" width="40" height="40"/>
  <text x="1306" y="824" class="card-title">container, sqladmin &amp; file APIs</text>
  <text x="1306" y="841" class="card-mono">Control Plane &amp; Managed Storage</text>
  <text x="1210" y="866" class="card-body">• Databricks GKE Enterprise node management</text>
  <text x="1210" y="884" class="card-body">• Regional HA Cloud SQL PG 15 control plane</text>
  <text x="1210" y="902" class="card-body">• Filestore Enterprise NFSv4.1 control plane</text>
  <text x="1210" y="920" class="card-body">• All protected inside VPC-SC service perimeter</text>

  <!-- Vertical Flow Arrows Between Horizontal Layers -->
  <path d="M 278 238 L 278 268" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <path d="M 776 238 L 776 268" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <path d="M 184 518 L 184 536" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"/>
  <path d="M 490 518 L 490 536" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <path d="M 184 720 L 184 752" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"/>
  <path d="M 1562 652 L 1572 652 L 1572 187 L 1564 187" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#arrow-red)"/>
</svg>
"""


def build_svg_3_storage_and_folder_governance_horizontal(icons: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 960" width="100%" height="100%">
  <defs>
    <style>
      .title {{ font: 700 22px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 500 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #475569; }}
      .card-title {{ font: 700 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .card-body {{ font: 500 11px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #334155; }}
      .card-mono {{ font: 600 10.2px 'Roboto Mono', monospace; fill: #0f172a; }}
      .badge {{ font: 700 10.5px 'Roboto Mono', monospace; fill: #ffffff; }}
    </style>
    <filter id="shadow" x="-2%" y="-4%" width="104%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.07"/>
    </filter>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1d4ed8"/>
    </marker>
  </defs>

  <rect width="1600" height="960" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Header -->
  <rect x="20" y="16" width="1560" height="64" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="20" y="16" width="10" height="64" rx="4" fill="#059669"/>
  <text x="46" y="44" class="title">Storage Accounts (Zero-Key Service Accounts) &amp; GCS HNS Managed Folder Hierarchy (Horizontal Layered View)</text>
  <text x="46" y="65" class="subtitle">Layer 1: 7 Dedicated Zero-Key GCP Service Accounts  |  Layer 2: Primary GCS HNS Bucket &amp; 12 Subfolder ACLs  |  Layer 3: Companion &amp; 30-Yr GxP WORM Buckets</text>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 1 (TOP): 7 DEDICATED ZERO-KEY SERVICE ACCOUNTS       -->
  <!-- ===================================================================== -->
  <rect x="20" y="94" width="1560" height="176" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <rect x="20" y="94" width="1560" height="34" rx="10" fill="#1d4ed8"/>
  <text x="40" y="116" class="badge" style="font-size:12px;">LAYER 1 — IDENTITY &amp; ENCRYPTION TIER: 7 Dedicated GCP Service Accounts (Zero Static Keys) + Cloud KMS CMEK (90-Day Rotation)</text>

  <!-- 6 Horizontal Cards for the 7 Service Accounts -->
  <rect x="36" y="140" width="242" height="116" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>
  <image href="{icons['identity_and_access_management']}" x="46" y="148" width="30" height="30"/>
  <text x="84" y="162" class="card-title">1. sa-sts-ingest</text>
  <text x="84" y="177" class="card-mono" style="font-size:9.5px;">roles/storage.objectCreator</text>
  <text x="46" y="198" class="card-body">Scoped strictly to STS</text>
  <text x="46" y="214" class="card-body">Landing bucket; zero read</text>
  <text x="46" y="230" class="card-body">access to Silver/Gold.</text>

  <rect x="290" y="140" width="246" height="116" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>
  <image href="{icons['identity_and_access_management']}" x="300" y="148" width="30" height="30"/>
  <text x="338" y="162" class="card-title">2 &amp; 3. sa-uc-master &amp; dbx</text>
  <text x="338" y="177" class="card-mono" style="font-size:9.5px;">Unity Catalog Master SAs</text>
  <text x="300" y="198" class="card-body">Vends short-lived OAuth</text>
  <text x="300" y="214" class="card-body">tokens for 9 Unity Catalog</text>
  <text x="300" y="230" class="card-body">External Locations.</text>

  <rect x="548" y="140" width="246" height="116" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
  <image href="{icons['identity_and_access_management']}" x="558" y="148" width="30" height="30"/>
  <text x="596" y="162" class="card-title">4. sa-clinical-ddf</text>
  <text x="596" y="177" class="card-mono" style="font-size:9.5px;">Managed Folder objectAdmin</text>
  <text x="558" y="198" class="card-mono" style="font-size:9.5px;">*/clinical_ddf/ ONLY</text>
  <text x="558" y="216" class="card-body">Isolates Clinical DDF,</text>
  <text x="558" y="232" class="card-body">CDISC &amp; PK/PD Biomarkers.</text>

  <rect x="806" y="140" width="246" height="116" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
  <image href="{icons['identity_and_access_management']}" x="816" y="148" width="30" height="30"/>
  <text x="854" y="162" class="card-title">5. sa-rwd-cohorts</text>
  <text x="854" y="177" class="card-mono" style="font-size:9.5px;">Managed Folder objectAdmin</text>
  <text x="816" y="198" class="card-mono" style="font-size:9.5px;">*/real_world_data/ ONLY</text>
  <text x="816" y="216" class="card-body">Isolates Real-World Data</text>
  <text x="816" y="232" class="card-body">&amp; Synthetic Control Arms.</text>

  <rect x="1064" y="140" width="246" height="116" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
  <image href="{icons['identity_and_access_management']}" x="1074" y="148" width="30" height="30"/>
  <text x="1112" y="162" class="card-title">6. sa-cmc-mfg</text>
  <text x="1112" y="177" class="card-mono" style="font-size:9.5px;">Managed Folder objectAdmin</text>
  <text x="1074" y="198" class="card-mono" style="font-size:9.5px;">*/cmc_manufacturing/ ONLY</text>
  <text x="1074" y="216" class="card-body">Isolates CMC Batch</text>
  <text x="1074" y="232" class="card-body">Genealogy &amp; Stability QC.</text>

  <rect x="1322" y="140" width="242" height="116" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="2"/>
  <image href="{icons['identity_and_access_management']}" x="1332" y="148" width="30" height="30"/>
  <text x="1370" y="162" class="card-title">7. sa-denodo-vdp-mvp</text>
  <text x="1370" y="177" class="card-mono" style="font-size:9.5px;">BQ &amp; GCS Cache Admin ONLY</text>
  <text x="1332" y="198" class="card-body">Scoped to denodo_vdp_cache</text>
  <text x="1332" y="214" class="card-body">&amp; Denodo Cache Bucket; no</text>
  <text x="1332" y="230" class="card-body">raw GCS Lakehouse read.</text>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 2 (MIDDLE): PRIMARY GCS HNS MEDALLION LAKEHOUSE      -->
  <!-- ===================================================================== -->
  <rect x="20" y="292" width="1560" height="422" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <rect x="20" y="292" width="1560" height="34" rx="10" fill="#059669"/>
  <text x="40" y="314" class="badge" style="font-size:12px;">LAYER 2 — PRIMARY GCS HNS MEDALLION LAKEHOUSE: gs://gke-demos-363017-rd-lakehouse-hns (hierarchical_namespace = true | 12 Managed Folders)</text>

  <!-- Vertical IAM Binding Arrows from Layer 1 SAs into Layer 2 Domain Folders -->
  <path d="M 671 256 L 671 290" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"/>
  <path d="M 929 256 L 929 290" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"/>
  <path d="M 1187 256 L 1187 290" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"/>

  <!-- Horizontal Band 2.1: BRONZE MEDALLION LAYER -->
  <rect x="38" y="338" width="1180" height="112" rx="10" fill="#ffffff" stroke="#f59e0b" stroke-width="2"/>
  <rect x="38" y="338" width="170" height="112" rx="8" fill="#fef3c7" stroke="#f59e0b"/>
  <image href="{icons['cloud_storage']}" x="52" y="354" width="36" height="36"/>
  <text x="52" y="408" class="card-title" style="fill:#92400e;">BRONZE TIER</text>
  <text x="52" y="424" class="card-mono" style="fill:#78350f;">Raw Landing</text>
  <text x="52" y="439" class="card-body" style="fill:#92400e;">Managed Folders</text>

  <rect x="222" y="348" width="318" height="92" rx="6" fill="#fffbeb" stroke="#fcd34d"/>
  <text x="234" y="368" class="card-mono">bronze/clinical_ddf/  [sa-clinical-ddf]</text>
  <text x="234" y="388" class="card-body">• cdisc_sdtm_raw/ (SDTM DM, EX, AE, LB)</text>
  <text x="234" y="406" class="card-body">• genomics_ngs_fastq/ (ctDNA &amp; RNASeq)</text>
  <text x="234" y="424" class="card-body">• ivrs_randomization_feeds/</text>

  <rect x="554" y="348" width="318" height="92" rx="6" fill="#fffbeb" stroke="#fcd34d"/>
  <text x="566" y="368" class="card-mono">bronze/real_world_data/  [sa-rwd-cohorts]</text>
  <text x="566" y="388" class="card-body">• ehr_claims_ingest/ (FHIR R4 / OMOP)</text>
  <text x="566" y="406" class="card-body">• oncology_disease_registries/</text>
  <text x="566" y="424" class="card-body">• tokenized_patient_linkage/</text>

  <rect x="886" y="348" width="318" height="92" rx="6" fill="#fffbeb" stroke="#fcd34d"/>
  <text x="898" y="368" class="card-mono">bronze/cmc_manufacturing/  [sa-cmc-mfg]</text>
  <text x="898" y="388" class="card-body">• erp_batch_genealogy/ (WERKS/MATNR/CHARG)</text>
  <text x="898" y="406" class="card-body">• lims_analytical_results/ (SEC-HPLC, pH)</text>
  <text x="898" y="424" class="card-body">• bioreactor_historian_telemetry/</text>

  <!-- Horizontal Band 2.2: SILVER MEDALLION LAYER -->
  <rect x="38" y="462" width="1180" height="112" rx="10" fill="#ffffff" stroke="#64748b" stroke-width="2"/>
  <rect x="38" y="462" width="170" height="112" rx="8" fill="#f1f5f9" stroke="#64748b"/>
  <image href="{icons['cloud_storage']}" x="52" y="478" width="36" height="36"/>
  <text x="52" y="532" class="card-title" style="fill:#1e293b;">SILVER TIER</text>
  <text x="52" y="548" class="card-mono" style="fill:#334155;">Harmonized Delta</text>
  <text x="52" y="563" class="card-body" style="fill:#334155;">Liquid Clustered</text>

  <rect x="222" y="472" width="318" height="92" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="234" y="492" class="card-mono">silver/clinical_ddf/  [sa-clinical-ddf]</text>
  <text x="234" y="512" class="card-body">• silver_cdisc_dm_subjects (Delta Lake)</text>
  <text x="234" y="530" class="card-body">• silver_biomarker_pkpd (Delta Lake)</text>
  <text x="234" y="548" class="card-mono">CLUSTER BY (studyid, molecule_id)</text>

  <rect x="554" y="472" width="318" height="92" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="566" y="492" class="card-mono">silver/real_world_data/  [sa-rwd-cohorts]</text>
  <text x="566" y="512" class="card-body">• silver_rwd_ehs_cohorts (OMOP CDM v5.4)</text>
  <text x="566" y="530" class="card-body">• silver_rwd_synthetic_control (Delta Lake)</text>
  <text x="566" y="548" class="card-mono">Propensity-score matched cohorts</text>

  <rect x="886" y="472" width="318" height="92" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="898" y="492" class="card-mono">silver/cmc_manufacturing/  [sa-cmc-mfg]</text>
  <text x="898" y="512" class="card-body">• silver_cmc_batch_genealogy (Delta Lake)</text>
  <text x="898" y="530" class="card-body">• silver_cmc_stability_ich_q1a (Delta Lake)</text>
  <text x="898" y="548" class="card-mono">Links Drug Substance -&gt; Clinical Lot ID</text>

  <!-- Horizontal Band 2.3: GOLD MEDALLION LAYER -->
  <rect x="38" y="586" width="1180" height="112" rx="10" fill="#ffffff" stroke="#eab308" stroke-width="2"/>
  <rect x="38" y="586" width="170" height="112" rx="8" fill="#fef9c3" stroke="#eab308"/>
  <image href="{icons['cloud_storage']}" x="52" y="602" width="36" height="36"/>
  <text x="52" y="656" class="card-title" style="fill:#854d0e;">GOLD TIER</text>
  <text x="52" y="672" class="card-mono" style="fill:#713f12;">Curated Products</text>
  <text x="52" y="687" class="card-body" style="fill:#854d0e;">Unity + Denodo</text>

  <rect x="222" y="596" width="318" height="92" rx="6" fill="#fefce8" stroke="#fde047"/>
  <text x="234" y="616" class="card-mono">gold/clinical_ddf/  [sa-clinical-ddf]</text>
  <text x="234" y="636" class="card-body">• gold_clinical_efficacy_summary (ADaM)</text>
  <text x="234" y="654" class="card-body">• gold_biomarker_response_matrix</text>
  <text x="234" y="672" class="card-mono">Exposed via Unity Catalog + Denodo VDP</text>

  <rect x="554" y="596" width="318" height="92" rx="6" fill="#fefce8" stroke="#fde047"/>
  <text x="566" y="616" class="card-mono">gold/real_world_data/  [sa-rwd-cohorts]</text>
  <text x="566" y="636" class="card-body">• gold_rwd_external_control_arms</text>
  <text x="566" y="654" class="card-body">• gold_so_care_hazard_ratios</text>
  <text x="566" y="672" class="card-mono">Joined in Denodo dv_rd_molecule_360</text>

  <rect x="886" y="596" width="318" height="92" rx="6" fill="#fefce8" stroke="#fde047"/>
  <text x="898" y="616" class="card-mono">gold/cmc_manufacturing/  [sa-cmc-mfg]</text>
  <text x="898" y="636" class="card-body">• gold_cmc_lot_release_certificates</text>
  <text x="898" y="654" class="card-body">• gold_cmc_shelf_life_regression</text>
  <text x="898" y="672" class="card-mono">Joined in dv_cmc_clinical_lot_trace</text>

  <!-- Right Panel in Layer 2: Shared System Managed Folders & HNS Benefits -->
  <rect x="1232" y="338" width="330" height="360" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2"/>
  <text x="1248" y="364" class="card-title">Shared Platform Managed Folders</text>
  <rect x="1248" y="378" width="298" height="40" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="1258" y="396" class="card-mono">10. hive_warehouse/</text>
  <text x="1258" y="411" class="card-body">External Hive Metastore (Cloud SQL) root</text>
  <rect x="1248" y="426" width="298" height="40" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="1258" y="444" class="card-mono">11. unity_catalog/</text>
  <text x="1258" y="459" class="card-body">Unity Catalog managed tables &amp; lineage</text>
  <rect x="1248" y="474" width="298" height="40" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="1258" y="492" class="card-mono">12. denodo_cache/</text>
  <text x="1258" y="507" class="card-body">Denodo 8.0 MPP Parquet/Delta spill</text>
  <rect x="1248" y="526" width="298" height="156" rx="8" fill="#ecfdf5" stroke="#10b981"/>
  <text x="1260" y="548" class="card-title">Why GCS HNS Is Mandatory:</text>
  <text x="1260" y="568" class="card-body">1. Atomic O(1) RenameFolder:</text>
  <text x="1260" y="584" class="card-body">   Eliminates slow O(N) copy+delete</text>
  <text x="1260" y="600" class="card-body">   during Spark job commits and Delta</text>
  <text x="1260" y="616" class="card-body">   Lake _delta_log compactions.</text>
  <text x="1260" y="638" class="card-body">2. 5x-8x Higher Per-Prefix QPS:</text>
  <text x="1260" y="654" class="card-body">   Eliminates HTTP 429 throttling on</text>
  <text x="1260" y="670" class="card-body">   deep partition trees.</text>

  <!-- ===================================================================== -->
  <!-- HORIZONTAL LAYER 3 (BOTTOM): COMPANION & 30-YR GxP WORM BUCKETS       -->
  <!-- ===================================================================== -->
  <rect x="20" y="734" width="1560" height="206" rx="12" fill="#fef2f2" stroke="#dc2626" stroke-width="2" filter="url(#shadow)"/>
  <rect x="20" y="734" width="1560" height="34" rx="10" fill="#dc2626"/>
  <text x="40" y="756" class="badge" style="font-size:12px;">LAYER 3 — COMPANION INGESTION, CACHING, POSIX SCRATCH &amp; 30-YEAR GxP WORM REGULATORY ARCHIVE TIER</text>

  <rect x="38" y="780" width="366" height="144" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <image href="{icons['cloud_storage']}" x="52" y="794" width="38" height="38"/>
  <text x="102" y="804" class="card-title">1. Cross-Cloud STS Landing Bucket</text>
  <text x="102" y="821" class="card-mono">gs://*-rd-lakehouse-hns-sts-landing</text>
  <text x="52" y="846" class="card-body">• Event-driven Storage Transfer Service (STS)</text>
  <text x="52" y="864" class="card-body">• TLS 1.3 transport + SHA-256 manifest checks</text>
  <text x="52" y="882" class="card-body">• Write-only for sa-sts-ingest (objectCreator)</text>
  <text x="52" y="900" class="card-body">• Encrypted with Cloud KMS CMEK (90d rotation)</text>

  <rect x="420" y="780" width="366" height="144" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <image href="{icons['cloud_storage']}" x="434" y="794" width="38" height="38"/>
  <text x="484" y="804" class="card-title">2. Denodo Delta Cache HNS Bucket</text>
  <text x="484" y="821" class="card-mono">gs://*-rd-lakehouse-hns-denodo-cache</text>
  <text x="434" y="846" class="card-body">• hierarchical_namespace {{ enabled = true }}</text>
  <text x="434" y="864" class="card-body">• Dedicated secondary Parquet/Delta cache</text>
  <text x="434" y="882" class="card-body">  for Denodo 8.0 VDP (1,584 ms / 4.29x speedup)</text>
  <text x="434" y="900" class="card-mono">• IAM: sa-denodo-vdp-mvp (objectAdmin ONLY)</text>

  <rect x="802" y="780" width="420" height="144" rx="10" fill="#ffffff" stroke="#dc2626" stroke-width="2"/>
  <image href="{icons['cloud_storage']}" x="816" y="794" width="38" height="38"/>
  <image href="{icons['key_management_service']}" x="860" y="794" width="38" height="38"/>
  <text x="908" y="804" class="card-title" style="fill:#991b1b;">3. 30-Yr GxP WORM Regulatory Archive</text>
  <text x="908" y="821" class="card-mono" style="fill:#7f1d1d;">gs://*-gxp-worm-archive (ARCHIVE Class)</text>
  <text x="816" y="846" class="card-mono" style="fill:#7f1d1d;">• retention_policy {{ retention_period = 946728000 }}</text>
  <text x="816" y="864" class="card-body" style="fill:#7f1d1d;">• Enforces 30-Year immutable WORM lock (21 CFR Part 11</text>
  <text x="816" y="882" class="card-body" style="fill:#7f1d1d;">  &amp; EU Annex 11) with Object Versioning + CMEK</text>
  <text x="816" y="900" class="card-body" style="fill:#7f1d1d;">• Stores locked CDISC submission &amp; CMC release records</text>

  <rect x="1238" y="780" width="324" height="144" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <image href="{icons['filestore']}" x="1252" y="794" width="38" height="38"/>
  <text x="1302" y="804" class="card-title">4. Filestore Enterprise (Optional)</text>
  <text x="1302" y="821" class="card-mono">NFSv4.1 /rd_posix_scratch (1 TB)</text>
  <text x="1252" y="846" class="card-body">• Regional High-Availability tier</text>
  <text x="1252" y="864" class="card-body">• Provides strict POSIX flock/fcntl</text>
  <text x="1252" y="882" class="card-body">  byte-range locking for legacy SAS</text>
  <text x="1252" y="900" class="card-body">  and C++ statistical binaries</text>
</svg>
"""


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    icon_names = [
        "bigquery",
        "cloud_storage",
        "compute_engine",
        "virtual_private_cloud",
        "identity_and_access_management",
        "private_service_connect",
        "cloud_nat",
        "cloud_sql",
        "key_management_service",
        "secret_manager",
        "cloud_load_balancing",
        "filestore",
        "google_kubernetes_engine",
        "cloud_dns",
        "cloud_armor",
    ]
    icons = {name: load_icon_data_uri(name) for name in icon_names}

    svg1 = ASSETS_DIR / "01_end_to_end_lakehouse_and_denodo_architecture.svg"
    svg2 = ASSETS_DIR / "02_zero_trust_network_and_vpc_sc_topology.svg"
    svg3 = ASSETS_DIR / "03_storage_accounts_and_hns_folder_governance.svg"

    svg1.write_text(build_svg_1_end_to_end_horizontal(icons), encoding="utf-8")
    svg2.write_text(build_svg_2_network_and_vpc_sc_horizontal(icons), encoding="utf-8")
    svg3.write_text(build_svg_3_storage_and_folder_governance_horizontal(icons), encoding="utf-8")
    print("Generated 3 HORIZONTAL-LAYERED SVG blueprints in", ASSETS_DIR)

    import subprocess
    import shutil

    chrome_bin = shutil.which("google-chrome") or "/usr/bin/google-chrome"
    if pathlib.Path(chrome_bin).exists():
        specs = [
            (svg1, "1600,1040"),
            (svg2, "1600,980"),
            (svg3, "1600,960"),
        ]
        for svg_path, win_size in specs:
            png_path = svg_path.with_suffix(".png")
            subprocess.run(
                [
                    chrome_bin,
                    "--headless",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--hide-scrollbars",
                    f"--window-size={win_size}",
                    f"--screenshot={png_path}",
                    f"file://{svg_path}",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        print("Rendered 3 HORIZONTAL-LAYERED PNG blueprints in", ASSETS_DIR)


if __name__ == "__main__":
    main()
