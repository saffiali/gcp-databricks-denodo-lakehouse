#!/usr/bin/env python3
"""Generates publication-grade SVG architecture diagrams with embedded official Google Cloud icons."""

import base64
import pathlib
import shutil

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


def build_svg_1_end_to_end(icons: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1560 920" width="100%" height="100%">
  <defs>
    <style>
      .title {{ font: 700 22px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 500 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #475569; }}
      .zone-hdr {{ font: 700 14px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #1e293b; letter-spacing: 0.4px; }}
      .zone-sub {{ font: 600 11px 'Roboto Mono', monospace; fill: #475569; }}
      .card-title {{ font: 700 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .card-body {{ font: 500 11px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #334155; }}
      .card-mono {{ font: 600 10.5px 'Roboto Mono', monospace; fill: #0f172a; }}
      .badge {{ font: 700 10px 'Roboto Mono', monospace; fill: #ffffff; }}
      .edge-lbl {{ font: 700 10.5px 'Roboto Mono', monospace; fill: #1e293b; }}
    </style>
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1a73e8"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ea580c"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#7c3aed"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
  </defs>

  <!-- Canvas Background -->
  <rect width="1560" height="920" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Top Header Banner -->
  <rect x="20" y="18" width="1520" height="68" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="20" y="18" width="10" height="68" rx="4" fill="#1a73e8"/>
  <text x="48" y="48" class="title">Single-Environment Enterprise Reference Architecture: Databricks on GCP + Denodo 8.0 VDP + BigQuery Cache</text>
  <text x="48" y="70" class="subtitle">Zero-Trust VPC-SC Perimeter  |  GCS Hierarchical Namespace (HNS) &amp; 30-Yr GxP WORM  |  Databricks Medallion Lakehouse  |  Denodo Semantic Layer  |  BigQuery Native Cache Engine ONLY</text>

  <!-- Outer VPC-SC Perimeter Box -->
  <rect x="20" y="102" width="1520" height="796" rx="14" fill="#f1f5f9" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="10,6"/>
  <rect x="40" y="91" width="660" height="24" rx="6" fill="#dc2626"/>
  <text x="52" y="107" class="badge">VPC SERVICE CONTROLS (VPC-SC) PERIMETER  |  ZERO PUBLIC IPs  |  restricted.googleapis.com (199.36.153.4/30)</text>

  <!-- ===================================================================== -->
  <!-- SWIMLANE 1: STORAGE ACCOUNTS, KMS CMEK & GCS HNS LAKEHOUSE (LEFT)     -->
  <!-- ===================================================================== -->
  <rect x="38" y="128" width="350" height="752" rx="12" fill="#ecfdf5" stroke="#10b981" stroke-width="2" filter="url(#shadow)"/>
  <rect x="38" y="128" width="350" height="44" rx="12" fill="#059669"/>
  <text x="54" y="148" class="badge" style="font-size:12.5px;">1. STORAGE ACCOUNTS &amp; GCS HNS TIER</text>
  <text x="54" y="164" class="badge" style="font-weight:500;fill:#d1fae5;">modules/gcs_hns_lakehouse (CMEK + HNS + WORM)</text>

  <!-- Card 1A: 7 Least-Privilege Service Accounts + KMS CMEK -->
  <rect x="54" y="186" width="318" height="122" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['identity_and_access_management']}" x="66" y="198" width="38" height="38"/>
  <image href="{icons['key_management_service']}" x="66" y="246" width="38" height="38"/>
  <text x="116" y="210" class="card-title">7 Dedicated GCP Service Accounts</text>
  <text x="116" y="226" class="card-body">Zero static keys (IAM Impersonation only)</text>
  <text x="116" y="242" class="card-mono">sa-sts | sa-uc-master | sa-denodo-vdp</text>
  <text x="116" y="257" class="card-mono">sa-clinical | sa-rwd | sa-cmc | sa-dbx</text>
  <text x="116" y="276" class="card-title">Cloud KMS CMEK (90-Day Rotation)</text>
  <text x="116" y="292" class="card-body">Encrypts GCS, Cloud SQL, BigQuery &amp; Disks</text>

  <!-- Card 1B: STS Landing Bucket -->
  <rect x="54" y="322" width="318" height="92" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="66" y="340" width="40" height="40"/>
  <text x="116" y="344" class="card-title">1. Cross-Cloud STS Landing Bucket</text>
  <text x="116" y="361" class="card-mono">gs://*-rd-lakehouse-hns-sts-landing</text>
  <text x="116" y="378" class="card-body">Event-driven Storage Transfer Service</text>
  <text x="116" y="394" class="card-body">TLS 1.3 + SHA-256 manifest verification</text>

  <!-- Card 1C: Primary Medallion HNS Lakehouse Bucket -->
  <rect x="54" y="428" width="318" height="218" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="66" y="444" width="42" height="42"/>
  <text x="116" y="450" class="card-title">2. Primary Medallion HNS Bucket</text>
  <text x="116" y="467" class="card-mono">gs://gke-demos-363017-rd-lakehouse-hns</text>
  <text x="116" y="483" class="card-body">hierarchical_namespace {{ enabled = true }}</text>
  <rect x="68" y="496" width="290" height="42" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="76" y="513" class="card-mono" style="font-size:10px;">Domain 1: bronze|silver|gold/clinical_ddf/</text>
  <text x="76" y="529" class="card-body">Managed Folder ACL -&gt; sa-clinical-ddf</text>
  <rect x="68" y="544" width="290" height="42" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="76" y="561" class="card-mono" style="font-size:10px;">Domain 2: bronze|silver|gold/real_world_data/</text>
  <text x="76" y="577" class="card-body">Managed Folder ACL -&gt; sa-rwd-cohorts</text>
  <rect x="68" y="592" width="290" height="42" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="76" y="609" class="card-mono" style="font-size:10px;">Domain 3: bronze|silver|gold/cmc_manufacturing/</text>
  <text x="76" y="625" class="card-body">Managed Folder ACL -&gt; sa-cmc-mfg</text>

  <!-- Card 1D: Denodo Delta Cache Bucket & 30-Yr GxP WORM Archive Bucket -->
  <rect x="54" y="660" width="318" height="102" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="66" y="684" width="40" height="40"/>
  <text x="116" y="682" class="card-title">3. Denodo Delta Cache HNS Bucket</text>
  <text x="116" y="698" class="card-mono">gs://*-rd-lakehouse-hns-denodo-cache</text>
  <text x="116" y="722" class="card-title">4. 30-Yr GxP WORM Archive Bucket</text>
  <text x="116" y="738" class="card-mono">gs://*-gxp-worm-archive (946,728,000s)</text>
  <text x="116" y="753" class="card-body">21 CFR Part 11 / EU Annex 11 retention</text>

  <!-- Card 1E: Optional Filestore Enterprise POSIX Scratch -->
  <rect x="54" y="774" width="318" height="90" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['filestore']}" x="66" y="796" width="40" height="40"/>
  <text x="116" y="798" class="card-title">5. Filestore Enterprise (Optional)</text>
  <text x="116" y="815" class="card-mono">NFSv4.1 /rd_posix_scratch (1 TB HA)</text>
  <text x="116" y="832" class="card-body">Strict POSIX flock/fcntl byte-range locks</text>
  <text x="116" y="848" class="card-body">for legacy SAS / C++ statistical binaries</text>

  <!-- ===================================================================== -->
  <!-- SWIMLANE 2: DATABRICKS ON GCP LAKEHOUSE ENGINE (CENTER-LEFT)          -->
  <!-- ===================================================================== -->
  <rect x="412" y="128" width="420" height="752" rx="12" fill="#fff7ed" stroke="#f97316" stroke-width="2" filter="url(#shadow)"/>
  <rect x="412" y="128" width="420" height="44" rx="12" fill="#ea580c"/>
  <text x="428" y="148" class="badge" style="font-size:12.5px;">2. DATABRICKS ON GCP LAKEHOUSE ENGINE</text>
  <text x="428" y="164" class="badge" style="font-weight:500;fill:#ffedd5;">snet-databricks-compute (10.168.0.0/19) + GKE Pods (/16)</text>

  <!-- Card 2A: Databricks Workspace & Unity Catalog Governance -->
  <rect x="428" y="186" width="388" height="140" rx="10" fill="#ffffff" stroke="#fed7aa" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['google_kubernetes_engine']}" x="442" y="204" width="40" height="40"/>
  <image href="{icons['private_service_connect']}" x="442" y="262" width="40" height="40"/>
  <text x="494" y="208" class="card-title">Databricks on GCP Workspace (GKE Enterprise)</text>
  <text x="494" y="225" class="card-mono">Workspace ID: 8259555750233451 (PSC Enabled)</text>
  <text x="494" y="242" class="card-body">Unity Catalog Storage Credential (sa-dbx-uc)</text>
  <text x="494" y="259" class="card-body">9 External Locations mapped to HNS Subfolders</text>
  <text x="494" y="278" class="card-title">Schemas &amp; 11 Delta Lake Medallion Tables</text>
  <text x="494" y="295" class="card-mono" style="font-size:10px;">workspace.rd_lakehouse_medallion | cmc_manufacturing</text>
  <text x="494" y="311" class="card-mono" style="font-size:10px;">workspace.clinical_development | real_world_evidence</text>

  <!-- Card 2B: Next-Gen GCE Compute Pools -->
  <rect x="428" y="340" width="388" height="206" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['compute_engine']}" x="442" y="356" width="40" height="40"/>
  <text x="494" y="364" class="card-title">Next-Gen GCE Compute Pools (Photon + Delta)</text>
  <text x="494" y="381" class="card-body">Replaces legacy Standard_D96ds_v5 nodes</text>
  <rect x="442" y="396" width="360" height="32" rx="6" fill="#fff7ed" stroke="#fdba74"/>
  <text x="452" y="416" class="card-mono">Pool 1 (Clinical DDF): n4-standard-16 (16 vCPU, 64 GB)</text>
  <rect x="442" y="434" width="360" height="32" rx="6" fill="#fff7ed" stroke="#fdba74"/>
  <text x="452" y="454" class="card-mono">Pool 2 (RWD Cohorts):  c4-highmem-32  (32 vCPU, 248 GB)</text>
  <rect x="442" y="472" width="360" height="32" rx="6" fill="#fff7ed" stroke="#fdba74"/>
  <text x="452" y="492" class="card-mono">Pool 3 (Genomics/PK):  m3-megamem-64  (64 vCPU, 976 GB)</text>
  <rect x="442" y="510" width="360" height="28" rx="6" fill="#fff7ed" stroke="#fdba74"/>
  <text x="452" y="528" class="card-mono">Pool 4 (NVMe Cache):   z3-highmem-88  (Titanium SSD)</text>

  <!-- Card 2C: Serverless / Pro SQL Warehouse -->
  <rect x="428" y="560" width="388" height="134" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['compute_engine']}" x="442" y="578" width="40" height="40"/>
  <text x="494" y="584" class="card-title">Databricks Serverless / Pro SQL Warehouse</text>
  <text x="494" y="601" class="card-mono" style="font-size:10px;">Warehouse ID: 0154a901254a4f17 (Photon Vectorized)</text>
  <text x="494" y="618" class="card-body">Liquid Clustering: CLUSTER BY (studyid, molecule_id)</text>
  <text x="494" y="635" class="card-body">Predictive I/O + Deletion Vectors enabled</text>
  <rect x="442" y="646" width="360" height="36" rx="6" fill="#ffedd5" stroke="#fb923c"/>
  <text x="452" y="663" class="card-mono">Simba Spark JDBC Endpoint (:443 over PSC)</text>
  <text x="452" y="677" class="card-mono">/sql/1.0/warehouses/0154a901254a4f17</text>

  <!-- Card 2D: External Hive Metastore (HA Cloud SQL PostgreSQL 15) -->
  <rect x="428" y="708" width="388" height="156" rx="10" fill="#ffffff" stroke="#fed7aa" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_sql']}" x="442" y="718" width="34" height="34"/>
  <image href="{icons['secret_manager']}" x="442" y="756" width="34" height="34"/>
  <text x="488" y="730" class="card-title">External Hive Metastore (Legacy 2.3.9 Parity)</text>
  <text x="488" y="747" class="card-mono">Regional HA Cloud SQL PostgreSQL 15 (:5432)</text>
  <text x="488" y="764" class="card-body">Private Service Access (/20 VPC Peering + SSL)</text>
  <text x="488" y="781" class="card-body">Credentials injected via Cloud Secret Manager</text>
  <rect x="442" y="796" width="360" height="54" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="452" y="814" class="card-mono" style="font-size:10px;">SQL URI Rewrite (sql/02_hive_metastore_uri_rewrite.sql):</text>
  <text x="452" y="830" class="card-mono" style="font-size:10px;">UPDATE "SDS" SET "LOCATION" =</text>
  <text x="452" y="844" class="card-mono" style="font-size:10px;">  REGEXP_REPLACE(LOCATION, '^abfss://...', 'gs://...')</text>

  <!-- ===================================================================== -->
  <!-- SWIMLANE 3: DENODO 8.0 VDP SEMANTIC VIRTUALIZATION LAYER (CENTER-RT)  -->
  <!-- ===================================================================== -->
  <rect x="856" y="128" width="330" height="752" rx="12" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="2" filter="url(#shadow)"/>
  <rect x="856" y="128" width="330" height="44" rx="12" fill="#7c3aed"/>
  <text x="872" y="148" class="badge" style="font-size:12.5px;">3. DENODO 8.0 VDP SEMANTIC LAYER</text>
  <text x="872" y="164" class="badge" style="font-weight:500;fill:#ede9fe;">snet-denodo-vdp (10.169.0.0/22) Shielded MIG</text>

  <!-- Card 3A: Internal Passthrough NLB -->
  <rect x="872" y="186" width="298" height="114" rx="10" fill="#ffffff" stroke="#ddd6fe" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_load_balancing']}" x="884" y="206" width="42" height="42"/>
  <text x="936" y="208" class="card-title">Internal Passthrough NLB</text>
  <text x="936" y="225" class="card-mono">denodo-vdp-internal:9999</text>
  <text x="936" y="242" class="card-body">:9999 (JDBC) | :9996 (ODBC)</text>
  <text x="936" y="258" class="card-body">:9443 (Design Studio &amp; Data Catalog)</text>
  <text x="936" y="274" class="card-body">TCP Health Check (15s interval)</text>
  <text x="936" y="290" class="card-mono">IAP Tunnel: 35.235.240.0/20</text>

  <!-- Card 3B: Denodo 8.0 VDP Regional Multi-Zone MIG -->
  <rect x="872" y="316" width="298" height="178" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['compute_engine']}" x="884" y="334" width="42" height="42"/>
  <text x="936" y="340" class="card-title">Denodo 8.0 VDP Cluster (MIG)</text>
  <text x="936" y="357" class="card-mono">2x n4-standard-8 (Zone A &amp; B)</text>
  <text x="936" y="374" class="card-body">Shielded VM (vTPM + Secure Boot)</text>
  <text x="936" y="390" class="card-body">200 GB Hyperdisk Balanced (CMEK)</text>
  <rect x="884" y="404" width="274" height="78" rx="6" fill="#f5f3ff" stroke="#c4b5fd"/>
  <text x="894" y="422" class="card-title">Federated Derived Views (VQL)</text>
  <text x="894" y="439" class="card-mono">1. dv_rd_molecule_360 (4-Way Join)</text>
  <text x="894" y="455" class="card-mono">2. dv_cmc_clinical_lot_trace</text>
  <text x="894" y="471" class="card-body">Cost-Based Optimizer + Pushdown</text>

  <!-- Card 3C: Dynamic GxP Blinding & Cross-Border Governance -->
  <rect x="872" y="510" width="298" height="184" rx="10" fill="#ffffff" stroke="#ddd6fe" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_armor']}" x="884" y="528" width="40" height="40"/>
  <text x="934" y="534" class="card-title">Dynamic Policy Enforcement</text>
  <text x="934" y="551" class="card-body">Evaluated at query runtime in Denodo</text>
  <rect x="884" y="564" width="274" height="54" rx="6" fill="#fef2f2" stroke="#fecaca"/>
  <text x="894" y="581" class="card-title" style="fill:#991b1b;">Policy 1: GxP Study-Arm Blinding</text>
  <text x="894" y="597" class="card-mono" style="fill:#7f1d1d;">ROLE != DSMB -&gt; '***BLINDED-GXP***'</text>
  <text x="894" y="611" class="card-body" style="fill:#991b1b;">Masks active vs. placebo dosing arms</text>
  <rect x="884" y="626" width="274" height="54" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
  <text x="894" y="643" class="card-title" style="fill:#1e40af;">Policy 2: Cross-Border Row Filter</text>
  <text x="894" y="659" class="card-mono" style="fill:#1e3a8a;">WHERE region_code &lt;&gt; 'CN'</text>
  <text x="894" y="673" class="card-body" style="fill:#1e40af;">Enforces PIPL / GDPR residency boundaries</text>

  <!-- Card 3D: Enterprise BI, AI & Regulatory Consumers -->
  <rect x="872" y="710" width="298" height="154" rx="10" fill="#ffffff" stroke="#ddd6fe" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['virtual_private_cloud']}" x="884" y="728" width="40" height="40"/>
  <text x="934" y="734" class="card-title">Downstream R&amp;D Consumers</text>
  <text x="934" y="751" class="card-body">Zero SQL/application code changes</text>
  <text x="888" y="776" class="card-mono">• Translational Medicine Dashboards</text>
  <text x="888" y="794" class="card-mono">• Unblinded DSMB Safety Boards</text>
  <text x="888" y="812" class="card-mono">• CMC Quality &amp; Batch Release</text>
  <text x="888" y="830" class="card-mono">• AI / GenAI Clinical Assistants</text>
  <text x="888" y="848" class="card-mono">• Regulatory Submission Portals</text>

  <!-- ===================================================================== -->
  <!-- SWIMLANE 4: BIGQUERY NATIVE DENODO CACHE LAYER ONLY (RIGHT)           -->
  <!-- ===================================================================== -->
  <rect x="1210" y="128" width="312" height="752" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <rect x="1210" y="128" width="312" height="44" rx="12" fill="#1d4ed8"/>
  <text x="1226" y="148" class="badge" style="font-size:12.5px;">4. BIGQUERY DENODO CACHE ONLY</text>
  <text x="1226" y="164" class="badge" style="font-weight:500;fill:#dbeafe;">Strictly Scoped to Denodo View Caching</text>

  <!-- Card 4A: Architectural Separation Mandate -->
  <rect x="1226" y="186" width="280" height="106" rx="10" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="1238" y="208" class="card-title" style="fill:#1e3a8a;">Architectural Mandate</text>
  <text x="1238" y="226" class="card-body" style="fill:#1e3a8a;">BigQuery does NOT replace Databricks.</text>
  <text x="1238" y="242" class="card-body" style="fill:#1e3a8a;">It is used strictly &amp; exclusively as</text>
  <text x="1238" y="258" class="card-body" style="fill:#1e3a8a;">the Denodo 8.0 VDP Native Cache</text>
  <text x="1238" y="274" class="card-body" style="fill:#1e3a8a;">Engine (replacing legacy Snowflake).</text>

  <!-- Card 4B: BigQuery Dataset denodo_vdp_cache + BI Engine -->
  <rect x="1226" y="308" width="280" height="224" rx="10" fill="#ffffff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['bigquery']}" x="1238" y="324" width="44" height="44"/>
  <text x="1292" y="334" class="card-title">BigQuery Native Cache</text>
  <text x="1292" y="351" class="card-mono">Dataset: denodo_vdp_cache</text>
  <text x="1292" y="368" class="card-body">Region: EU (CMEK Encrypted)</text>
  <rect x="1238" y="382" width="256" height="48" rx="6" fill="#eff6ff" stroke="#93c5fd"/>
  <text x="1248" y="400" class="card-title">50 GB BI Engine Reservation</text>
  <text x="1248" y="418" class="card-body">Sub-second vectorized memory cache</text>
  <rect x="1238" y="438" width="256" height="82" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="1248" y="456" class="card-title">Clustered Cache Tables:</text>
  <text x="1248" y="474" class="card-mono">• cache_dv_rd_molecule_360</text>
  <text x="1248" y="490" class="card-body">  CLUSTER BY (studyid, molecule_id)</text>
  <text x="1248" y="508" class="card-mono">• cache_dv_cmc_clinical_lot_trace</text>

  <!-- Card 4C: High-Throughput gRPC StorageReadAPI -->
  <rect x="1226" y="548" width="280" height="128" rx="10" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['private_service_connect']}" x="1238" y="566" width="40" height="40"/>
  <text x="1288" y="572" class="card-title">Simba BigQuery JDBC + gRPC</text>
  <text x="1288" y="589" class="card-mono">EnableHighThroughputAPI=1</text>
  <text x="1238" y="614" class="card-body">Streams Arrow/Avro blocks via</text>
  <text x="1238" y="630" class="card-mono">bigquerystorage.googleapis.com</text>
  <text x="1238" y="646" class="card-body">using roles/bigquery.readSessionUser</text>
  <text x="1238" y="662" class="card-body">over restricted.googleapis.com</text>

  <!-- Card 4D: Live Caching Spike Benchmark Results -->
  <rect x="1226" y="692" width="280" height="172" rx="10" fill="#ffffff" stroke="#10b981" stroke-width="2" filter="url(#shadow)"/>
  <rect x="1226" y="692" width="280" height="30" rx="8" fill="#059669"/>
  <text x="1240" y="711" class="badge">LIVE DENODO CACHING BENCHMARK</text>
  <text x="1238" y="742" class="card-mono" style="fill:#059669;font-size:11.5px;">1. BIGQUERY_NATIVE_CACHE:</text>
  <text x="1238" y="758" class="card-title" style="fill:#047857;">   1,077.2 ms  (6.31x Speedup)</text>
  <text x="1238" y="784" class="card-mono" style="fill:#0284c7;font-size:11.5px;">2. DELTA_GCS_CACHE (Parquet):</text>
  <text x="1238" y="800" class="card-title" style="fill:#0369a1;">   1,584.1 ms  (4.29x Speedup)</text>
  <text x="1238" y="826" class="card-mono" style="fill:#dc2626;font-size:11.5px;">3. DIRECT_UNCACHED_FEDERATION:</text>
  <text x="1238" y="842" class="card-title" style="fill:#b91c1c;">   6,801.3 ms  (1.00x Baseline)</text>

  <!-- ===================================================================== -->
  <!-- DIRECTIONAL DATA-FLOW ARROWS BETWEEN SWIMLANES                        -->
  <!-- ===================================================================== -->
  <!-- Arrow 1: Primary HNS Bucket <-> Databricks Compute Pools -->
  <path d="M 372 480 L 424 480" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)" marker-start="url(#arrow-green)"/>
  <!-- Arrow 2: Primary HNS Bucket <-> Databricks SQL Warehouse -->
  <path d="M 372 605 L 424 605" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)" marker-start="url(#arrow-green)"/>
  <!-- Arrow 3: Denodo VDP MIG -> Databricks SQL Warehouse (Simba Spark JDBC :443) -->
  <path d="M 872 435 L 844 435 L 844 625 L 820 625" fill="none" stroke="#ea580c" stroke-width="3" marker-end="url(#arrow-orange)"/>
  <rect x="752" y="534" width="104" height="22" rx="4" fill="#ea580c"/>
  <text x="760" y="549" class="badge">JDBC Pushdown</text>

  <!-- Arrow 4: Denodo VDP MIG <-> BigQuery Native Cache (gRPC StorageReadAPI) -->
  <path d="M 1170 405 L 1222 405" stroke="#1a73e8" stroke-width="3.5" marker-end="url(#arrow-blue)" marker-start="url(#arrow-blue)"/>
  <rect x="1152" y="366" width="88" height="22" rx="4" fill="#1a73e8"/>
  <text x="1160" y="381" class="badge">Cache R/W</text>

  <!-- Arrow 5: Consumers -> Internal NLB -> Denodo VDP MIG -->
  <path d="M 1020 710 L 1020 696" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arrow-purple)"/>
  <path d="M 1020 300 L 1020 314" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arrow-purple)"/>
</svg>
"""


def build_svg_2_network_and_vpc_sc(icons: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1560 860" width="100%" height="100%">
  <defs>
    <style>
      .title {{ font: 700 22px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 500 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #475569; }}
      .card-title {{ font: 700 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .card-body {{ font: 500 11px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #334155; }}
      .card-mono {{ font: 600 10.5px 'Roboto Mono', monospace; fill: #0f172a; }}
      .badge {{ font: 700 10px 'Roboto Mono', monospace; fill: #ffffff; }}
    </style>
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1a73e8"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
  </defs>

  <rect width="1560" height="860" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Header -->
  <rect x="20" y="18" width="1520" height="68" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="20" y="18" width="10" height="68" rx="4" fill="#dc2626"/>
  <text x="48" y="48" class="title">Zero-Trust Network Controls, Multi-Subnet Segmentation &amp; VPC-SC Perimeter (modules/network_and_psc)</text>
  <text x="48" y="70" class="subtitle">4 Segmented Subnets (/19 Databricks, /22 Denodo VDP, /24 PSC, /24 ILB Proxy)  |  Private Cloud DNS (199.36.153.4/30)  |  Micro-Segmented Firewalls</text>

  <!-- VPC Box -->
  <rect x="20" y="102" width="1020" height="736" rx="14" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <rect x="20" y="102" width="1020" height="42" rx="12" fill="#1d4ed8"/>
  <image href="{icons['virtual_private_cloud']}" x="34" y="107" width="32" height="32"/>
  <text x="76" y="128" class="badge" style="font-size:13px;">CUSTOMER-MANAGED VPC: rd-lakehouse-vpc-mvp (REGIONAL ROUTING, AUTO_CREATE_SUBNETWORKS = FALSE)</text>

  <!-- Subnet A: Databricks Compute Plane (/19) -->
  <rect x="42" y="162" width="470" height="260" rx="10" fill="#ffffff" stroke="#f97316" stroke-width="2" filter="url(#shadow)"/>
  <rect x="42" y="162" width="470" height="32" rx="8" fill="#ea580c"/>
  <text x="56" y="183" class="badge">SUBNET A: snet-databricks-europe-west2 (10.168.0.0/19)</text>
  <image href="{icons['google_kubernetes_engine']}" x="58" y="208" width="42" height="42"/>
  <text x="112" y="220" class="card-title">Databricks Compute Plane (8,192 Node IPs)</text>
  <text x="112" y="237" class="card-mono">Primary CIDR:   10.168.0.0/19 (Private Google Access)</text>
  <text x="112" y="254" class="card-mono">GKE Pods Range: 10.176.0.0/16 (65,536 Pod IPs)</text>
  <text x="112" y="271" class="card-mono">GKE Svc Range:  10.177.0.0/20 (4,096 ClusterIPs)</text>
  <rect x="58" y="286" width="438" height="120" rx="6" fill="#fff7ed" stroke="#fdba74"/>
  <text x="70" y="306" class="card-title">Network Tag: [databricks-worker] &amp; VPC Flow Logs (5s)</text>
  <text x="70" y="324" class="card-mono">• Hosts N4, C4, M3, and Z3 Databricks Worker Pools</text>
  <text x="70" y="342" class="card-mono">• Outbound TCP :5432 -&gt; HA Cloud SQL Hive Metastore</text>
  <text x="70" y="360" class="card-mono">• Outbound TCP :443  -&gt; restricted.googleapis.com (GCS HNS)</text>
  <text x="70" y="378" class="card-mono">• Inbound TCP :443/:8443 from snet-denodo-vdp &amp; PSC only</text>

  <!-- Subnet B: Denodo 8.0 VDP Cluster (/22) -->
  <rect x="536" y="162" width="482" height="260" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2" filter="url(#shadow)"/>
  <rect x="536" y="162" width="482" height="32" rx="8" fill="#7c3aed"/>
  <text x="550" y="183" class="badge">SUBNET B: snet-denodo-vdp-europe-west2 (10.169.0.0/22)</text>
  <image href="{icons['compute_engine']}" x="552" y="208" width="42" height="42"/>
  <image href="{icons['cloud_load_balancing']}" x="552" y="260" width="42" height="42"/>
  <text x="606" y="220" class="card-title">Denodo 8.0 VDP Virtualization Tier (1,024 IPs)</text>
  <text x="606" y="237" class="card-mono">Primary CIDR: 10.169.0.0/22 (Private Google Access)</text>
  <text x="606" y="254" class="card-body">Shielded VM Regional MIG (n4-standard-8, Zones a/b)</text>
  <text x="606" y="274" class="card-title">Internal Passthrough NLB VIP (:9999/:9996/:9443)</text>
  <rect x="552" y="294" width="450" height="112" rx="6" fill="#f5f3ff" stroke="#c4b5fd"/>
  <text x="564" y="314" class="card-title">Network Tag: [denodo-vdp-node] &amp; Zero Public IPs</text>
  <text x="564" y="332" class="card-mono">• Inbound :9999/:9996/:9443 from IAP (35.235.240.0/20) &amp; VPC</text>
  <text x="564" y="350" class="card-mono">• Outbound :443 -&gt; Databricks SQL Warehouse PSC Endpoint</text>
  <text x="564" y="368" class="card-mono">• Outbound :443 -&gt; BigQuery StorageReadAPI (199.36.153.4/30)</text>
  <text x="564" y="386" class="card-mono">• Health Checks from 130.211.0.0/22 &amp; 35.191.0.0/16</text>

  <!-- Subnet C: Private Service Connect (/24) -->
  <rect x="42" y="442" width="470" height="176" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2" filter="url(#shadow)"/>
  <rect x="42" y="442" width="470" height="32" rx="8" fill="#0284c7"/>
  <text x="56" y="463" class="badge">SUBNET C: snet-psc-europe-west2 (10.169.4.0/24)</text>
  <image href="{icons['private_service_connect']}" x="58" y="488" width="42" height="42"/>
  <text x="112" y="500" class="card-title">Private Service Connect (PSC) Endpoint Subnet</text>
  <text x="112" y="518" class="card-mono">Internal IP: rd-lakehouse-psc-databricks-ip</text>
  <text x="112" y="536" class="card-body">Terminates Databricks Control Plane Web UI, REST API,</text>
  <text x="112" y="552" class="card-body">Secure Cluster Connectivity (SCC) relay, and Serverless</text>
  <text x="112" y="568" class="card-body">SQL Warehouse JDBC traffic strictly inside the VPC.</text>
  <text x="112" y="588" class="card-mono">SUBNET D: snet-ilb-proxy (10.169.5.0/24) REGIONAL_PROXY</text>

  <!-- Subnet E / PSA Peering: Cloud SQL & Filestore + Cloud DNS -->
  <rect x="536" y="442" width="482" height="176" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <rect x="536" y="442" width="482" height="32" rx="8" fill="#059669"/>
  <text x="550" y="463" class="badge">PRIVATE SERVICE ACCESS (/20) &amp; PRIVATE CLOUD DNS</text>
  <image href="{icons['cloud_sql']}" x="552" y="486" width="40" height="40"/>
  <image href="{icons['cloud_dns']}" x="552" y="542" width="40" height="40"/>
  <text x="606" y="498" class="card-title">PSA Peering: HA Cloud SQL Hive Metastore (:5432)</text>
  <text x="606" y="515" class="card-mono">db-custom-4-16384 (REGIONAL HA + SSL Required)</text>
  <text x="606" y="532" class="card-body">+ Optional Filestore Enterprise NFSv4.1 (:2049)</text>
  <text x="606" y="556" class="card-title">Private Cloud DNS Zone (googleapis.com.)</text>
  <text x="606" y="573" class="card-mono">*.googleapis.com CNAME -&gt; restricted.googleapis.com</text>
  <text x="606" y="590" class="card-mono">A Records: 199.36.153.4, .5, .6, .7 (VIP Range /30)</text>

  <!-- Firewall Policy Table inside VPC -->
  <rect x="42" y="636" width="976" height="184" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="42" y="636" width="976" height="30" rx="8" fill="#1e293b"/>
  <text x="58" y="656" class="badge">ZERO-TRUST GCP FIREWALL POLICY MATRIX (PRIORITY-ORDERED INGRESS &amp; EGRESS CONTROLS)</text>
  <text x="58" y="686" class="card-mono" style="fill:#047857;">[Prio 100 | EGRESS | ALLOW] -&gt; 199.36.153.4/30 (TCP :443)  | Allows GCS HNS, BigQuery StorageReadAPI, Cloud KMS, Secret Manager</text>
  <text x="58" y="708" class="card-mono" style="fill:#0284c7;">[Prio 150 | INGRESS| ALLOW] 10.169.0.0/22 -&gt; [databricks-worker] (:443, :8443) | Allows Denodo VDP Simba Spark JDBC pushdown</text>
  <text x="58" y="730" class="card-mono" style="fill:#0284c7;">[Prio 200 | INGRESS| ALLOW] 10.168.0.0/19, 10.176.0.0/16 -&gt; [databricks-worker] (:443, :2049, :5432, :8443) | Spark Shuffle &amp; HMS</text>
  <text x="58" y="752" class="card-mono" style="fill:#7c3aed;">[Prio 250 | INGRESS| ALLOW] 35.235.240.0/20 (IAP) &amp; GCP HC -&gt; [denodo-vdp-node] (:22, :9090, :9443, :9996, :9999) | Zero-Trust Admin</text>
  <text x="58" y="776" class="card-mono" style="fill:#dc2626;">[Prio 65534| EGRESS | DENY ] -&gt; 0.0.0.0/0 (ALL PROTOCOLS) + INCLUDE_ALL_METADATA Logging | Blocks all unauthorized internet egress</text>
  <text x="58" y="800" class="card-body">Cloud NAT (rd-lakehouse-cloud-nat) is attached with ERRORS_ONLY logging strictly for allowlisted OS/driver package repositories.</text>

  <!-- Right Column: VPC-SC Protected Google APIs & Blocked Public Internet -->
  <rect x="1064" y="102" width="476" height="486" rx="14" fill="#ecfdf5" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <rect x="1064" y="102" width="476" height="42" rx="12" fill="#059669"/>
  <text x="1082" y="128" class="badge" style="font-size:13px;">RESTRICTED GOOGLE APIs VIP (199.36.153.4/30)</text>

  <rect x="1084" y="162" width="436" height="92" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5"/>
  <image href="{icons['cloud_storage']}" x="1098" y="186" width="42" height="42"/>
  <text x="1154" y="188" class="card-title">storage.googleapis.com (VPC-SC Protected)</text>
  <text x="1154" y="206" class="card-body">• STS Landing, Primary HNS Lakehouse, Denodo Cache</text>
  <text x="1154" y="224" class="card-body">• 30-Yr GxP WORM Archive Bucket</text>
  <text x="1154" y="240" class="card-mono">Zero public internet exposure; perimeter locked</text>

  <rect x="1084" y="268" width="436" height="92" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5"/>
  <image href="{icons['bigquery']}" x="1098" y="292" width="42" height="42"/>
  <text x="1154" y="294" class="card-title">bigquery.googleapis.com &amp; bigquerystorage</text>
  <text x="1154" y="312" class="card-body">• Denodo VDP Native Cache (denodo_vdp_cache ONLY)</text>
  <text x="1154" y="330" class="card-body">• 50 GB BI Engine + High-Throughput gRPC Read API</text>
  <text x="1154" y="346" class="card-mono">Accessible solely by sa-denodo-vdp inside perimeter</text>

  <rect x="1084" y="374" width="436" height="92" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5"/>
  <image href="{icons['key_management_service']}" x="1098" y="398" width="42" height="42"/>
  <text x="1154" y="400" class="card-title">cloudkms &amp; secretmanager.googleapis.com</text>
  <text x="1154" y="418" class="card-body">• 90-Day rotating CMEK key ring (europe-west2)</text>
  <text x="1154" y="436" class="card-body">• External Hive Metastore credentials &amp; JDBC tokens</text>
  <text x="1154" y="452" class="card-mono">Hardware-backed KMS protection across all tiers</text>

  <rect x="1084" y="480" width="436" height="90" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5"/>
  <image href="{icons['identity_and_access_management']}" x="1098" y="502" width="42" height="42"/>
  <text x="1154" y="506" class="card-title">container &amp; sqladmin.googleapis.com</text>
  <text x="1154" y="524" class="card-body">• Databricks GKE Enterprise node pool management</text>
  <text x="1154" y="542" class="card-body">• Regional HA Cloud SQL PostgreSQL 15 control plane</text>

  <!-- Blocked Public Internet Box -->
  <rect x="1064" y="608" width="476" height="230" rx="14" fill="#fef2f2" stroke="#dc2626" stroke-width="2" filter="url(#shadow)"/>
  <rect x="1064" y="608" width="476" height="42" rx="12" fill="#dc2626"/>
  <image href="{icons['cloud_armor']}" x="1078" y="613" width="32" height="32"/>
  <text x="1118" y="634" class="badge" style="font-size:13px;">PUBLIC INTERNET (0.0.0.0/0) — EGRESS BLOCKED</text>
  <text x="1086" y="676" class="card-title" style="fill:#991b1b;">4-Layer Exfiltration Defense:</text>
  <text x="1086" y="700" class="card-body" style="fill:#7f1d1d;">1. Zero Public IPs on Databricks workers &amp; Denodo VMs</text>
  <text x="1086" y="722" class="card-body" style="fill:#7f1d1d;">2. Firewall Rule Priority 65534 denies all 0.0.0.0/0 egress</text>
  <text x="1086" y="744" class="card-body" style="fill:#7f1d1d;">3. Private DNS forces *.googleapis.com -&gt; 199.36.153.4/30</text>
  <text x="1086" y="766" class="card-body" style="fill:#7f1d1d;">4. VPC-SC Perimeter blocks unauthorized project copies</text>
  <text x="1086" y="794" class="card-mono" style="fill:#991b1b;">Audit Trail: INCLUDE_ALL_METADATA -&gt; Cloud Logging</text>

  <!-- Arrows -->
  <path d="M 1018 525 L 1062 320" stroke="#059669" stroke-width="3.5" marker-end="url(#arrow-green)"/>
  <path d="M 1018 770 L 1062 720" stroke="#dc2626" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-red)"/>
</svg>
"""


def build_svg_3_storage_and_folder_governance(icons: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1560 820" width="100%" height="100%">
  <defs>
    <style>
      .title {{ font: 700 22px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 500 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #475569; }}
      .card-title {{ font: 700 13px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #0f172a; }}
      .card-body {{ font: 500 11px 'Google Sans', 'Inter', 'Segoe UI', Arial, sans-serif; fill: #334155; }}
      .card-mono {{ font: 600 10.5px 'Roboto Mono', monospace; fill: #0f172a; }}
      .badge {{ font: 700 10px 'Roboto Mono', monospace; fill: #ffffff; }}
    </style>
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1a73e8"/>
    </marker>
  </defs>

  <rect width="1560" height="820" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Header -->
  <rect x="20" y="18" width="1520" height="68" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="20" y="18" width="10" height="68" rx="4" fill="#059669"/>
  <text x="48" y="48" class="title">Storage Accounts (Zero-Key GCP Service Accounts) &amp; GCS HNS Managed Folder Hierarchy</text>
  <text x="48" y="70" class="subtitle">Replaces Legacy Shared Storage Account Keys &amp; ADLS Gen2 POSIX ACLs with Subfolder-Scoped google_storage_managed_folder_iam_member Bindings</text>

  <!-- Left Column: 7 Least-Privilege Service Accounts -->
  <rect x="24" y="104" width="440" height="692" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="104" width="440" height="40" rx="10" fill="#1d4ed8"/>
  <text x="42" y="129" class="badge" style="font-size:12.5px;">7 DEDICATED GCP SERVICE ACCOUNTS (ZERO KEYS)</text>

  <!-- SA Cards -->
  <rect x="42" y="158" width="404" height="72" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>
  <image href="{icons['identity_and_access_management']}" x="54" y="174" width="36" height="36"/>
  <text x="102" y="178" class="card-title">1. rd-lakehouse-sa-sts-ingest</text>
  <text x="102" y="195" class="card-mono">Role: roles/storage.objectCreator (STS Landing Only)</text>
  <text x="102" y="212" class="card-body">Cross-cloud ingestion identity; cannot read Gold tables</text>

  <rect x="42" y="242" width="404" height="72" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>
  <image href="{icons['identity_and_access_management']}" x="54" y="258" width="36" height="36"/>
  <text x="102" y="262" class="card-title">2. rd-lakehouse-sa-uc-master &amp; dbx-uc</text>
  <text x="102" y="279" class="card-mono">Role: Unity Catalog Storage Credential Master</text>
  <text x="102" y="296" class="card-body">Vends short-lived downscoped OAuth tokens to clusters</text>

  <rect x="42" y="326" width="404" height="82" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
  <image href="{icons['identity_and_access_management']}" x="54" y="346" width="36" height="36"/>
  <text x="102" y="348" class="card-title">3. rd-lakehouse-sa-clinical-ddf (Mesh Node 1)</text>
  <text x="102" y="365" class="card-mono">Role: roles/storage.objectAdmin (Managed Folder)</text>
  <text x="102" y="382" class="card-body">Scoped STRICTLY to bronze|silver|gold/clinical_ddf/</text>
  <text x="102" y="397" class="card-body">Zero access to RWD or CMC Manufacturing folders</text>

  <rect x="42" y="420" width="404" height="82" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
  <image href="{icons['identity_and_access_management']}" x="54" y="440" width="36" height="36"/>
  <text x="102" y="442" class="card-title">4. rd-lakehouse-sa-rwd-cohorts (Mesh Node 2)</text>
  <text x="102" y="459" class="card-mono">Role: roles/storage.objectAdmin (Managed Folder)</text>
  <text x="102" y="476" class="card-body">Scoped STRICTLY to bronze|silver|gold/real_world_data/</text>
  <text x="102" y="491" class="card-body">Zero access to Clinical DDF or CMC folders</text>

  <rect x="42" y="514" width="404" height="82" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
  <image href="{icons['identity_and_access_management']}" x="54" y="534" width="36" height="36"/>
  <text x="102" y="536" class="card-title">5. rd-lakehouse-sa-cmc-mfg (Mesh Node 3)</text>
  <text x="102" y="553" class="card-mono">Role: roles/storage.objectAdmin (Managed Folder)</text>
  <text x="102" y="570" class="card-body">Scoped STRICTLY to bronze|silver|gold/cmc_manufacturing/</text>
  <text x="102" y="585" class="card-body">Zero access to unblinded Clinical DDF folders</text>

  <rect x="42" y="608" width="404" height="172" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="2"/>
  <image href="{icons['identity_and_access_management']}" x="54" y="626" width="36" height="36"/>
  <text x="100" y="630" class="card-title">6. rd-lakehouse-denodo-vdp-mvp (Denodo VDP)</text>
  <text x="100" y="647" class="card-mono" style="font-size:10px;">• roles/bigquery.jobUser (Project)</text>
  <text x="100" y="663" class="card-mono" style="font-size:10px;">• roles/bigquery.readSessionUser (StorageReadAPI)</text>
  <text x="100" y="679" class="card-mono" style="font-size:10px;">• roles/bigquery.dataEditor (denodo_vdp_cache)</text>
  <text x="100" y="695" class="card-mono" style="font-size:10px;">• roles/storage.objectAdmin (Denodo Cache Bucket)</text>
  <rect x="54" y="708" width="380" height="58" rx="6" fill="#f5f3ff" stroke="#ddd6fe"/>
  <text x="64" y="726" class="card-title">Why This Matters for GxP &amp; Least Privilege:</text>
  <text x="64" y="742" class="card-body">Denodo VDP cannot bypass Databricks Unity Catalog to read raw</text>
  <text x="64" y="756" class="card-body">Bronze/Silver GCS files; it queries Databricks via JDBC only.</text>

  <!-- Right Area: GCS HNS Managed Folder Tree & 4 Purpose-Built Buckets -->
  <rect x="494" y="104" width="1042" height="692" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <rect x="494" y="104" width="1042" height="40" rx="10" fill="#059669"/>
  <text x="514" y="129" class="badge" style="font-size:12.5px;">PRIMARY GCS HNS BUCKET: gs://gke-demos-363017-rd-lakehouse-hns (hierarchical_namespace = true)</text>

  <!-- 3 Data Mesh Columns inside Primary HNS Bucket -->
  <!-- Column 1: Clinical Development (DDF) -->
  <rect x="514" y="160" width="320" height="360" rx="10" fill="#ffffff" stroke="#10b981" stroke-width="2" filter="url(#shadow)"/>
  <rect x="514" y="160" width="320" height="32" rx="8" fill="#047857"/>
  <text x="528" y="181" class="badge">MESH NODE 1: CLINICAL DEVELOPMENT</text>
  <image href="{icons['cloud_storage']}" x="528" y="204" width="36" height="36"/>
  <text x="574" y="218" class="card-title">google_storage_managed_folder</text>
  <text x="574" y="234" class="card-mono">IAM: sa-clinical-ddf (objectAdmin)</text>

  <rect x="528" y="252" width="292" height="76" rx="6" fill="#fef3c7" stroke="#f59e0b"/>
  <text x="540" y="272" class="card-mono">bronze/clinical_ddf/</text>
  <text x="540" y="289" class="card-body">• cdisc_sdtm_raw/ (SDTM DM, EX, AE, LB)</text>
  <text x="540" y="305" class="card-body">• genomics_ngs_fastq/ (ctDNA &amp; RNASeq)</text>
  <text x="540" y="320" class="card-body">• ivrs_randomization_feeds/</text>

  <rect x="528" y="338" width="292" height="76" rx="6" fill="#f1f5f9" stroke="#64748b"/>
  <text x="540" y="358" class="card-mono">silver/clinical_ddf/</text>
  <text x="540" y="375" class="card-body">• silver_cdisc_dm_subjects (Delta)</text>
  <text x="540" y="391" class="card-body">• silver_biomarker_pkpd (Delta)</text>
  <text x="540" y="406" class="card-body">• Liquid Clustered by (studyid, molecule_id)</text>

  <rect x="528" y="424" width="292" height="80" rx="6" fill="#fef9c3" stroke="#eab308"/>
  <text x="540" y="444" class="card-mono">gold/clinical_ddf/</text>
  <text x="540" y="461" class="card-body">• gold_clinical_efficacy_summary (ADaM)</text>
  <text x="540" y="477" class="card-body">• gold_biomarker_response_matrix</text>
  <text x="540" y="493" class="card-mono">Exposed via Unity Catalog + Denodo VDP</text>

  <!-- Column 2: Real-World Evidence (RWD) -->
  <rect x="854" y="160" width="320" height="360" rx="10" fill="#ffffff" stroke="#10b981" stroke-width="2" filter="url(#shadow)"/>
  <rect x="854" y="160" width="320" height="32" rx="8" fill="#047857"/>
  <text x="868" y="181" class="badge">MESH NODE 2: REAL-WORLD EVIDENCE</text>
  <image href="{icons['cloud_storage']}" x="868" y="204" width="36" height="36"/>
  <text x="914" y="218" class="card-title">google_storage_managed_folder</text>
  <text x="914" y="234" class="card-mono">IAM: sa-rwd-cohorts (objectAdmin)</text>

  <rect x="868" y="252" width="292" height="76" rx="6" fill="#fef3c7" stroke="#f59e0b"/>
  <text x="880" y="272" class="card-mono">bronze/real_world_data/</text>
  <text x="880" y="289" class="card-body">• ehr_claims_ingest/ (FHIR R4 / OMOP)</text>
  <text x="880" y="305" class="card-body">• oncology_disease_registries/</text>
  <text x="880" y="320" class="card-body">• tokenized_patient_linkage/</text>

  <rect x="868" y="338" width="292" height="76" rx="6" fill="#f1f5f9" stroke="#64748b"/>
  <text x="880" y="358" class="card-mono">silver/real_world_data/</text>
  <text x="880" y="375" class="card-body">• silver_rwd_ehs_cohorts (OMOP CDM v5.4)</text>
  <text x="880" y="391" class="card-body">• silver_rwd_synthetic_control (Delta)</text>
  <text x="880" y="406" class="card-body">• Propensity-score matched cohorts</text>

  <rect x="868" y="424" width="292" height="80" rx="6" fill="#fef9c3" stroke="#eab308"/>
  <text x="880" y="444" class="card-mono">gold/real_world_data/</text>
  <text x="880" y="461" class="card-body">• gold_rwd_external_control_arms</text>
  <text x="880" y="477" class="card-body">• gold_so_care_hazard_ratios</text>
  <text x="880" y="493" class="card-mono">Joined in Denodo dv_rd_molecule_360</text>

  <!-- Column 3: CMC Biologics & Manufacturing -->
  <rect x="1194" y="160" width="322" height="360" rx="10" fill="#ffffff" stroke="#10b981" stroke-width="2" filter="url(#shadow)"/>
  <rect x="1194" y="160" width="322" height="32" rx="8" fill="#047857"/>
  <text x="1208" y="181" class="badge">MESH NODE 3: CMC MANUFACTURING</text>
  <image href="{icons['cloud_storage']}" x="1208" y="204" width="36" height="36"/>
  <text x="1254" y="218" class="card-title">google_storage_managed_folder</text>
  <text x="1254" y="234" class="card-mono">IAM: sa-cmc-mfg (objectAdmin)</text>

  <rect x="1208" y="252" width="294" height="76" rx="6" fill="#fef3c7" stroke="#f59e0b"/>
  <text x="1220" y="272" class="card-mono">bronze/cmc_manufacturing/</text>
  <text x="1220" y="289" class="card-body">• erp_batch_genealogy/ (WERKS/MATNR/CHARG)</text>
  <text x="1220" y="305" class="card-body">• lims_analytical_results/ (SEC-HPLC, pH)</text>
  <text x="1220" y="320" class="card-body">• bioreactor_historian_telemetry/</text>

  <rect x="1208" y="338" width="294" height="76" rx="6" fill="#f1f5f9" stroke="#64748b"/>
  <text x="1220" y="358" class="card-mono">silver/cmc_manufacturing/</text>
  <text x="1220" y="375" class="card-body">• silver_cmc_batch_genealogy (Delta)</text>
  <text x="1220" y="391" class="card-body">• silver_cmc_stability_ich_q1a (Delta)</text>
  <text x="1220" y="406" class="card-body">• Links Drug Substance -&gt; Clinical Lot ID</text>

  <rect x="1208" y="424" width="294" height="80" rx="6" fill="#fef9c3" stroke="#eab308"/>
  <text x="1220" y="444" class="card-mono">gold/cmc_manufacturing/</text>
  <text x="1220" y="461" class="card-body">• gold_cmc_lot_release_certificates</text>
  <text x="1220" y="477" class="card-body">• gold_cmc_shelf_life_regression</text>
  <text x="1220" y="493" class="card-mono">Joined in dv_cmc_clinical_lot_trace</text>

  <!-- Bottom Row: System Managed Folders & Companion Buckets -->
  <rect x="514" y="538" width="490" height="238" rx="10" fill="#ffffff" stroke="#059669" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="532" y="564" class="card-title">Shared Platform Managed Folders (Inside Primary HNS Bucket)</text>
  <text x="532" y="588" class="card-mono">• hive_warehouse/    -&gt; External Hive Metastore (Cloud SQL HA) root URI</text>
  <text x="532" y="610" class="card-mono">• unity_catalog/     -&gt; Unity Catalog managed tables &amp; lineage metadata</text>
  <text x="532" y="632" class="card-mono">• denodo_cache/      -&gt; Denodo 8.0 MPP Parquet/Delta spill directory</text>
  <rect x="532" y="650" width="454" height="110" rx="8" fill="#f0fdf4" stroke="#86efac"/>
  <text x="546" y="672" class="card-title">Why GCS Hierarchical Namespace (HNS) Is Mandatory:</text>
  <text x="546" y="692" class="card-body">1. Atomic O(1) RenameFolder: Eliminates slow O(N) object copy+delete</text>
  <text x="546" y="708" class="card-body">   during Spark task/job commits and Delta Lake _delta_log checkpoints.</text>
  <text x="546" y="726" class="card-body">2. 5x–8x Higher Per-Prefix QPS: Eliminates HTTP 429 throttling on deep</text>
  <text x="546" y="742" class="card-body">   partition trees (studyid=.../molecule_id=.../).</text>

  <rect x="1024" y="538" width="492" height="238" rx="10" fill="#ffffff" stroke="#dc2626" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="1040" y="556" width="42" height="42"/>
  <image href="{icons['key_management_service']}" x="1040" y="612" width="42" height="42"/>
  <text x="1096" y="566" class="card-title">Companion Regulatory &amp; Caching Buckets</text>
  <text x="1096" y="588" class="card-mono">1. gs://*-sts-landing (Cross-Cloud STS Ingest)</text>
  <text x="1096" y="608" class="card-mono">2. gs://*-denodo-cache (Dedicated HNS Cache Bucket)</text>
  <text x="1096" y="628" class="card-mono">3. gs://*-gxp-worm-archive (30-Yr GxP WORM Lock)</text>
  <rect x="1040" y="650" width="460" height="110" rx="8" fill="#fef2f2" stroke="#fecaca"/>
  <text x="1054" y="672" class="card-title" style="fill:#991b1b;">30-Year GxP WORM Regulatory Lock (21 CFR Part 11 / Annex 11):</text>
  <text x="1054" y="692" class="card-mono" style="fill:#7f1d1d;">retention_policy {{ retention_period = 946728000 # 30 Years }}</text>
  <text x="1054" y="712" class="card-body" style="fill:#7f1d1d;">Guarantees immutable, tamper-proof preservation of locked clinical</text>
  <text x="1054" y="728" class="card-body" style="fill:#7f1d1d;">trial datasets (CDISC SDTM/ADaM) and CMC batch release certificates</text>
  <text x="1054" y="744" class="card-body" style="fill:#7f1d1d;">with Object Versioning + Cloud KMS CMEK encryption.</text>

  <!-- Clean orthogonal connector from Service Accounts to Primary HNS Bucket -->
  <path d="M 446 365 L 490 365" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"/>
  <path d="M 446 460 L 490 460" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"/>
  <path d="M 446 555 L 490 555" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"/>
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

    svg1.write_text(build_svg_1_end_to_end(icons), encoding="utf-8")
    svg2.write_text(build_svg_2_network_and_vpc_sc(icons), encoding="utf-8")
    svg3.write_text(build_svg_3_storage_and_folder_governance(icons), encoding="utf-8")

    # Also copy the two generated raster images for reference
    shutil.copyfile(
        "/usr/local/google/home/saffi/.gemini/jetski/brain/9fe31b76-de83-4647-a7f0-e19255f0a5e8/gcp_databricks_denodo_architecture_1791284857318.jpg",
        ASSETS_DIR / "gcp_databricks_denodo_overview.jpg",
    )
    shutil.copyfile(
        "/usr/local/google/home/saffi/.gemini/jetski/brain/9fe31b76-de83-4647-a7f0-e19255f0a5e8/gcp_network_storage_governance_1791284948287.jpg",
        ASSETS_DIR / "gcp_network_storage_governance.jpg",
    )
    print("Generated 3 SVG blueprints and copied 2 JPG diagrams into", ASSETS_DIR)


if __name__ == "__main__":
    main()
