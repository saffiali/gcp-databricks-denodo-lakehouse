#!/usr/bin/env python3
"""Generates 4 publication-grade HORIZONTAL-LAYERED SVG & PNG architecture diagrams with embedded official Google Cloud icons."""

import base64
import pathlib
import shutil
import subprocess

CANDIDATE_ICON_DIRS = [
    pathlib.Path(
        "/google/src/cloud/saffi/deploy_domino_gcp_terraform/google3/"
        "googledata/html/external_content/gstatic/cgc/shared/product-icons"
    ),
    pathlib.Path(
        "/google/src/files/head/depot/google3/"
        "googledata/html/external_content/gstatic/cgc/shared/product-icons"
    ),
]
REPO_ROOT = pathlib.Path(
    "/usr/local/google/home/saffi/teamwork_projects/databricks_denodo_gcp_single_env"
)
ASSETS_DIR = REPO_ROOT / "assets"


def load_icon_data_uri(name: str) -> str:
    for icon_dir in CANDIDATE_ICON_DIRS:
        path = icon_dir / name / f"{name}.png"
        if path.is_file():
            b64 = base64.b64encode(path.read_bytes()).decode("ascii")
            return f"data:image/png;base64,{b64}"
    raise FileNotFoundError(f"Icon not found: {name}")


def build_svg_1_end_to_end_horizontal(icons: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 980" width="100%" height="100%">
  <defs>
    <style>
      .title {{ font: 700 22px 'Google Sans', 'Inter', Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 500 13px 'Google Sans', 'Inter', Arial, sans-serif; fill: #475569; }}
      .node-title {{ font: 700 15px 'Google Sans', 'Inter', Arial, sans-serif; fill: #0f172a; }}
      .node-sub {{ font: 500 12px 'Google Sans', 'Inter', Arial, sans-serif; fill: #475569; }}
      .badge {{ font: 700 11px 'Google Sans', 'Roboto Mono', monospace; fill: #ffffff; }}
    </style>
    <filter id="shadow" x="-2%" y="-4%" width="104%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.07"/>
    </filter>
    <marker id="arrow-purple" markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#7c3aed"/>
    </marker>
    <marker id="arrow-blue" markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1d4ed8"/>
    </marker>
    <marker id="arrow-orange" markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ea580c"/>
    </marker>
    <marker id="arrow-green" markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
  </defs>

  <rect width="1600" height="980" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Header -->
  <rect x="24" y="18" width="1552" height="66" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="24" y="18" width="10" height="66" rx="4" fill="#1a73e8"/>
  <text x="50" y="46" class="title">Enterprise Lakehouse &amp; Virtualization Reference Architecture (Horizontal Layered View)</text>
  <text x="50" y="68" class="subtitle">Layer 1: Denodo 9.0 Base-Image VM Scale Set  |  Layer 2: BigQuery Native Denodo Cache  |  Layer 3: Databricks on GCP Lakehouse  |  Layer 4: Standard GCS (No HNS)</text>

  <!-- Outer VPC-SC Perimeter -->
  <rect x="24" y="102" width="1552" height="856" rx="14" fill="#f1f5f9" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="10,6"/>
  <rect x="44" y="91" width="690" height="22" rx="6" fill="#dc2626"/>
  <text x="56" y="106" class="badge">VPC SERVICE CONTROLS (VPC-SC) PERIMETER  |  ZERO PUBLIC IPs  |  restricted.googleapis.com (199.36.153.4/30)</text>

  <!-- LAYER 1: DENODO 9.0 ON BASE OS IMAGES -->
  <rect x="44" y="126" width="1512" height="178" rx="12" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="2" filter="url(#shadow)"/>
  <rect x="44" y="126" width="1512" height="34" rx="10" fill="#7c3aed"/>
  <text x="64" y="148" class="badge">LAYER 1 — SEMANTIC VIRTUALIZATION TIER: Denodo 9.0 VM Scale Set on Enterprise Base OS Images</text>

  <rect x="70" y="176" width="460" height="110" rx="10" fill="#ffffff" stroke="#ddd6fe" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_load_balancing']}" x="90" y="206" width="48" height="48"/>
  <text x="156" y="224" class="node-title">Internal Passthrough NLB (:9999 / :9090)</text>
  <text x="156" y="248" class="node-sub">Routes BI, AI &amp; JDBC traffic to Denodo VDP &amp; Design Studio</text>

  <rect x="570" y="176" width="460" height="110" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['compute_engine']}" x="590" y="206" width="48" height="48"/>
  <text x="656" y="224" class="node-title">Denodo 9.0 Base-Image VM Scale Set (MIG)</text>
  <text x="656" y="248" class="node-sub">2–6 Shielded RHEL 9 Base VMs via Silent Installer</text>

  <rect x="1070" y="176" width="460" height="110" rx="10" fill="#ffffff" stroke="#ddd6fe" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_armor']}" x="1090" y="206" width="48" height="48"/>
  <text x="1156" y="224" class="node-title">Dynamic Policy &amp; Row/Column Masking</text>
  <text x="1156" y="248" class="node-sub">Enforces role-based PII masking &amp; regional residency rules</text>

  <path d="M 530 231 L 568 231" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arrow-purple)"/>
  <path d="M 1030 231 L 1068 231" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arrow-purple)"/>

  <!-- LAYER 2: BIGQUERY NATIVE DENODO CACHE -->
  <rect x="44" y="330" width="1512" height="178" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <rect x="44" y="330" width="1512" height="34" rx="10" fill="#1d4ed8"/>
  <text x="64" y="352" class="badge">LAYER 2 — DENODO NATIVE CACHE TIER ONLY: Google BigQuery + 50 GB BI Engine</text>

  <rect x="70" y="380" width="460" height="110" rx="10" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['bigquery']}" x="90" y="410" width="48" height="48"/>
  <text x="156" y="428" class="node-title">BigQuery Dataset (denodo_vdp_cache)</text>
  <text x="156" y="452" class="node-sub">Dedicated strictly to Denodo materialized view caching</text>

  <rect x="570" y="380" width="460" height="110" rx="10" fill="#ffffff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['bigquery']}" x="590" y="410" width="48" height="48"/>
  <text x="656" y="428" class="node-title">50 GB BI Engine In-Memory Acceleration</text>
  <text x="656" y="452" class="node-sub">Sub-second cache lookups on clustered derived views</text>

  <rect x="1070" y="380" width="460" height="110" rx="10" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['private_service_connect']}" x="1090" y="410" width="48" height="48"/>
  <text x="1156" y="428" class="node-title">High-Throughput gRPC StorageReadAPI</text>
  <text x="1156" y="452" class="node-sub">Streams Arrow blocks privately over restricted.googleapis.com</text>

  <path d="M 800 304 L 800 328" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arrow-blue)"/>

  <!-- LAYER 3: DATABRICKS ON GCP LAKEHOUSE -->
  <rect x="44" y="534" width="1512" height="178" rx="12" fill="#fff7ed" stroke="#f97316" stroke-width="2" filter="url(#shadow)"/>
  <rect x="44" y="534" width="1512" height="34" rx="10" fill="#ea580c"/>
  <text x="64" y="556" class="badge">LAYER 3 — PRIMARY LAKEHOUSE COMPUTE &amp; METASTORE TIER: Databricks on GCP + HA Cloud SQL</text>

  <rect x="70" y="584" width="460" height="110" rx="10" fill="#ffffff" stroke="#fed7aa" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['google_kubernetes_engine']}" x="90" y="614" width="48" height="48"/>
  <text x="156" y="632" class="node-title">Databricks on GCP &amp; Unity Catalog</text>
  <text x="156" y="656" class="node-sub">Hosts Bronze, Silver &amp; Gold Delta Lake Medallion tables</text>

  <rect x="570" y="584" width="460" height="110" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['compute_engine']}" x="590" y="614" width="48" height="48"/>
  <text x="656" y="632" class="node-title">Photon SQL Warehouse &amp; N4/C4/M3/Z3 Pools</text>
  <text x="656" y="656" class="node-sub">Executes Spark ETL &amp; Simba JDBC pushdown over PSC</text>

  <rect x="1070" y="584" width="460" height="110" rx="10" fill="#ffffff" stroke="#fed7aa" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_sql']}" x="1090" y="614" width="48" height="48"/>
  <text x="1156" y="632" class="node-title">HA Cloud SQL PG 15 Hive Metastore</text>
  <text x="1156" y="656" class="node-sub">Regional HA external metastore with gs:// URI rewrite</text>

  <path d="M 800 508 L 800 532" stroke="#ea580c" stroke-width="2.5" marker-end="url(#arrow-orange)"/>

  <!-- LAYER 4: STANDARD GCS STORAGE & KMS CMEK (NO HNS) -->
  <rect x="44" y="738" width="1512" height="196" rx="12" fill="#ecfdf5" stroke="#10b981" stroke-width="2" filter="url(#shadow)"/>
  <rect x="44" y="738" width="1512" height="34" rx="10" fill="#059669"/>
  <text x="64" y="760" class="badge">LAYER 4 — STORAGE &amp; ENCRYPTION TIER: Standard GCS Buckets (UBLA = true, HNS Disabled for Databricks) + KMS CMEK</text>

  <rect x="70" y="792" width="460" height="118" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['key_management_service']}" x="90" y="826" width="48" height="48"/>
  <text x="156" y="842" class="node-title">Zero-Key Service Accounts &amp; KMS CMEK</text>
  <text x="156" y="866" class="node-sub">90-day automatic key rotation &amp; domain-scoped IAM</text>

  <rect x="570" y="792" width="460" height="118" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="590" y="826" width="48" height="48"/>
  <text x="656" y="842" class="node-title">Standard GCS Medallion Bucket (No HNS)</text>
  <text x="656" y="866" class="node-sub">Flat namespace + 12 Managed Folders for Databricks UC</text>

  <rect x="1070" y="792" width="460" height="118" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="1090" y="826" width="48" height="48"/>
  <text x="1156" y="842" class="node-title">STS Landing, Denodo Stage &amp; WORM Archive</text>
  <text x="1156" y="866" class="node-sub">Isolated buckets for ingestion, installer staging &amp; 30-yr lock</text>

  <path d="M 800 712 L 800 736" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"/>
</svg>
"""


def build_svg_2_network_and_vpc_sc_horizontal(icons: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 960" width="100%" height="100%">
  <defs>
    <style>
      .title {{ font: 700 22px 'Google Sans', 'Inter', Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 500 13px 'Google Sans', 'Inter', Arial, sans-serif; fill: #475569; }}
      .node-title {{ font: 700 15px 'Google Sans', 'Inter', Arial, sans-serif; fill: #0f172a; }}
      .node-sub {{ font: 500 12px 'Google Sans', 'Inter', Arial, sans-serif; fill: #475569; }}
      .badge {{ font: 700 11px 'Google Sans', 'Roboto Mono', monospace; fill: #ffffff; }}
    </style>
    <filter id="shadow" x="-2%" y="-4%" width="104%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.07"/>
    </filter>
    <marker id="arrow-blue" markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1d4ed8"/>
    </marker>
    <marker id="arrow-green" markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
  </defs>

  <rect width="1600" height="960" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Header -->
  <rect x="24" y="18" width="1552" height="66" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="24" y="18" width="10" height="66" rx="4" fill="#dc2626"/>
  <text x="50" y="46" class="title">Zero-Trust Network Segmentation &amp; VPC-SC Perimeter (Horizontal Layered View)</text>
  <text x="50" y="68" class="subtitle">Layer 1: Zero-Trust Ingress Boundary  |  Layer 2: Segmented VPC Subnets  |  Layer 3: Firewall Policy Matrix  |  Layer 4: Restricted Google APIs VIP</text>

  <!-- LAYER 1: INGRESS BOUNDARY -->
  <rect x="24" y="102" width="1552" height="186" rx="12" fill="#f1f5f9" stroke="#64748b" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="102" width="1552" height="34" rx="10" fill="#334155"/>
  <text x="46" y="124" class="badge">LAYER 1 — ZERO-TRUST INGRESS ACCESS &amp; INTERNET EGRESS BOUNDARY</text>

  <rect x="56" y="152" width="468" height="114" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['identity_and_access_management']}" x="76" y="184" width="48" height="48"/>
  <text x="142" y="202" class="node-title">Identity-Aware Proxy (IAP) Tunnel</text>
  <text x="142" y="226" class="node-sub">35.235.240.0/20 zero-trust admin access without public IPs</text>

  <rect x="566" y="152" width="468" height="114" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_nat']}" x="586" y="184" width="48" height="48"/>
  <text x="652" y="202" class="node-title">GCP Health Probers &amp; Cloud NAT</text>
  <text x="652" y="226" class="node-sub">Probes TCP :9999 on Denodo MIG &amp; logs outbound NAT</text>

  <rect x="1076" y="152" width="468" height="114" rx="10" fill="#fef2f2" stroke="#dc2626" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_armor']}" x="1096" y="184" width="48" height="48"/>
  <text x="1162" y="202" class="node-title">Public Internet (0.0.0.0/0) Blocked</text>
  <text x="1162" y="226" class="node-sub">Priority 65534 deny-all egress &amp; VPC-SC exfiltration lock</text>

  <!-- LAYER 2: CUSTOMER-MANAGED VPC SUBNETS -->
  <rect x="24" y="314" width="1552" height="186" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="314" width="1552" height="34" rx="10" fill="#1d4ed8"/>
  <text x="46" y="336" class="badge">LAYER 2 — CUSTOMER-MANAGED VPC SUBNET SEGMENTATION</text>

  <rect x="56" y="364" width="468" height="114" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['google_kubernetes_engine']}" x="76" y="396" width="48" height="48"/>
  <text x="142" y="414" class="node-title">Databricks Compute Subnet (10.168.0.0/19)</text>
  <text x="142" y="438" class="node-sub">Private GKE Enterprise worker nodes &amp; secondary pod ranges</text>

  <rect x="566" y="364" width="468" height="114" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['compute_engine']}" x="586" y="396" width="48" height="48"/>
  <text x="652" y="414" class="node-title">Denodo 9.0 VM Scale Set Subnet (10.169.0.0/22)</text>
  <text x="652" y="438" class="node-sub">Regional MIG on Base OS images + Internal Passthrough NLB</text>

  <rect x="1076" y="364" width="468" height="114" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['private_service_connect']}" x="1096" y="396" width="48" height="48"/>
  <text x="1162" y="414" class="node-title">PSC Endpoints &amp; Private Cloud DNS</text>
  <text x="1162" y="438" class="node-sub">10.169.4.0/24 Private Link + googleapis.com private zone</text>

  <path d="M 800 288 L 800 312" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arrow-blue)"/>

  <!-- LAYER 3: FIREWALL POLICY LAYER -->
  <rect x="24" y="526" width="1552" height="186" rx="12" fill="#ffffff" stroke="#1e293b" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="526" width="1552" height="34" rx="10" fill="#1e293b"/>
  <text x="46" y="548" class="badge">LAYER 3 — MICRO-SEGMENTED GCP FIREWALL RULES</text>

  <rect x="56" y="576" width="468" height="114" rx="10" fill="#f0fdf4" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['virtual_private_cloud']}" x="76" y="608" width="48" height="48"/>
  <text x="142" y="626" class="node-title">Priority 100 &amp; 150: API &amp; JDBC Pushdown</text>
  <text x="142" y="650" class="node-sub">Allows TCP :443 to restricted VIP &amp; Denodo -&gt; Databricks</text>

  <rect x="566" y="576" width="468" height="114" rx="10" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_load_balancing']}" x="586" y="608" width="48" height="48"/>
  <text x="652" y="626" class="node-title">Priority 200 &amp; 250: Cluster &amp; Denodo Ports</text>
  <text x="652" y="650" class="node-sub">Allows Spark shuffle (:5432) &amp; Denodo (:9999, :9090, :8000)</text>

  <rect x="1076" y="576" width="468" height="114" rx="10" fill="#fef2f2" stroke="#dc2626" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_armor']}" x="1096" y="608" width="48" height="48"/>
  <text x="1162" y="626" class="node-title">Priority 65534: Default-Deny All Egress</text>
  <text x="1162" y="650" class="node-sub">Blocks unauthorized 0.0.0.0/0 egress with full flow logging</text>

  <path d="M 800 500 L 800 524" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arrow-blue)"/>

  <!-- LAYER 4: RESTRICTED GOOGLE APIs & VPC-SC -->
  <rect x="24" y="738" width="1552" height="196" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="738" width="1552" height="34" rx="10" fill="#059669"/>
  <text x="46" y="760" class="badge">LAYER 4 — RESTRICTED GOOGLE APIs VIP (199.36.153.4/30) &amp; VPC-SC PROTECTED SERVICES</text>

  <rect x="56" y="792" width="468" height="118" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="76" y="826" width="48" height="48"/>
  <text x="142" y="842" class="node-title">Standard Cloud Storage (No HNS)</text>
  <text x="142" y="866" class="node-sub">storage.googleapis.com locked inside VPC-SC perimeter</text>

  <rect x="566" y="792" width="468" height="118" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['bigquery']}" x="586" y="826" width="48" height="48"/>
  <text x="652" y="842" class="node-title">BigQuery &amp; BigQuery Storage Read API</text>
  <text x="652" y="866" class="node-sub">Serves Denodo 9.0 VDP Native Cache over private gRPC</text>

  <rect x="1076" y="792" width="468" height="118" rx="10" fill="#ffffff" stroke="#a7f3d0" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['key_management_service']}" x="1096" y="826" width="48" height="48"/>
  <text x="1162" y="842" class="node-title">Cloud KMS, Secret Manager &amp; Cloud SQL</text>
  <text x="1162" y="866" class="node-sub">90-day CMEK keys, Denodo license vault &amp; HA Hive Metastore</text>

  <path d="M 800 712 L 800 736" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"/>
</svg>
"""


def build_svg_3_storage_and_folder_governance_horizontal(icons: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 880" width="100%" height="100%">
  <defs>
    <style>
      .title {{ font: 700 22px 'Google Sans', 'Inter', Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 500 13px 'Google Sans', 'Inter', Arial, sans-serif; fill: #475569; }}
      .node-title {{ font: 700 15px 'Google Sans', 'Inter', Arial, sans-serif; fill: #0f172a; }}
      .node-sub {{ font: 500 12px 'Google Sans', 'Inter', Arial, sans-serif; fill: #475569; }}
      .badge {{ font: 700 11px 'Google Sans', 'Roboto Mono', monospace; fill: #ffffff; }}
    </style>
    <filter id="shadow" x="-2%" y="-4%" width="104%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.07"/>
    </filter>
    <marker id="arrow-green" markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
  </defs>

  <rect width="1600" height="880" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Header -->
  <rect x="24" y="18" width="1552" height="66" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="24" y="18" width="10" height="66" rx="4" fill="#059669"/>
  <text x="50" y="46" class="title">Storage Accounts &amp; Standard GCS Managed Folder Governance (Horizontal Layered View)</text>
  <text x="50" y="68" class="subtitle">Layer 1: Zero-Key Service Accounts &amp; KMS CMEK  |  Layer 2: Standard GCS Medallion Bucket (No HNS)  |  Layer 3: Companion &amp; WORM Buckets</text>

  <!-- LAYER 1: ZERO-KEY SERVICE ACCOUNTS -->
  <rect x="24" y="104" width="1552" height="220" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="104" width="1552" height="34" rx="10" fill="#1d4ed8"/>
  <text x="46" y="126" class="badge">LAYER 1 — IDENTITY &amp; ENCRYPTION TIER: Dedicated Zero-Key GCP Service Accounts + Cloud KMS CMEK (90-Day Rotation)</text>

  <rect x="56" y="158" width="468" height="142" rx="10" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['identity_and_access_management']}" x="76" y="204" width="48" height="48"/>
  <text x="142" y="220" class="node-title">Unity Catalog &amp; STS Ingestion SAs</text>
  <text x="142" y="244" class="node-sub">sa-uc-master &amp; sa-sts-ingest (zero static keys)</text>

  <rect x="566" y="158" width="468" height="142" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['identity_and_access_management']}" x="586" y="204" width="48" height="48"/>
  <text x="652" y="220" class="node-title">3 Domain-Scoped Data Mesh SAs</text>
  <text x="652" y="244" class="node-sub">sa-cust-analytics, sa-supply-chain &amp; sa-ent-finance</text>

  <rect x="1076" y="158" width="468" height="142" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['key_management_service']}" x="1096" y="204" width="48" height="48"/>
  <text x="1162" y="220" class="node-title">Denodo 9.0 VDP SA &amp; 90-Day KMS CMEK</text>
  <text x="1162" y="244" class="node-sub">sa-denodo-vdp scoped strictly to Cache bucket &amp; BigQuery</text>

  <!-- LAYER 2: STANDARD GCS MEDALLION LAKEHOUSE (NO HNS) -->
  <rect x="24" y="352" width="1552" height="236" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="352" width="1552" height="34" rx="10" fill="#059669"/>
  <text x="46" y="374" class="badge">LAYER 2 — STANDARD GCS MEDALLION BUCKET (uniform_bucket_level_access = true | HNS Disabled for Databricks Compatibility)</text>

  <rect x="56" y="408" width="468" height="154" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="76" y="460" width="48" height="48"/>
  <text x="142" y="474" class="node-title">Domain 1: Customer Analytics Folders</text>
  <text x="142" y="498" class="node-sub">bronze/, silver/, gold/customer_analytics/ Managed Folders</text>

  <rect x="566" y="408" width="468" height="154" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="586" y="460" width="48" height="48"/>
  <text x="652" y="474" class="node-title">Domain 2: Supply Chain Folders</text>
  <text x="652" y="498" class="node-sub">bronze/, silver/, gold/supply_chain/ Managed Folders</text>

  <rect x="1076" y="408" width="468" height="154" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="1096" y="460" width="48" height="48"/>
  <text x="1162" y="474" class="node-title">Domain 3: Enterprise Finance Folders</text>
  <text x="1162" y="498" class="node-sub">bronze/, silver/, gold/enterprise_finance/ Managed Folders</text>

  <path d="M 800 324 L 800 350" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"/>

  <!-- LAYER 3: COMPANION & WORM BUCKETS -->
  <rect x="24" y="616" width="1552" height="236" rx="12" fill="#fef2f2" stroke="#dc2626" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="616" width="1552" height="34" rx="10" fill="#dc2626"/>
  <text x="46" y="638" class="badge">LAYER 3 — COMPANION INGESTION, DENODO STAGING &amp; 30-YEAR WORM ARCHIVE TIER (STANDARD GCS, NO HNS)</text>

  <rect x="56" y="672" width="468" height="154" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="76" y="724" width="48" height="48"/>
  <text x="142" y="738" class="node-title">Cross-Cloud STS Landing Bucket</text>
  <text x="142" y="762" class="node-sub">gs://*-ent-lakehouse-sts-landing (write-only ingestion)</text>

  <rect x="566" y="672" width="468" height="154" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="586" y="724" width="48" height="48"/>
  <text x="652" y="738" class="node-title">Denodo Cache &amp; Installer Staging Bucket</text>
  <text x="652" y="762" class="node-sub">gs://*-ent-lakehouse-denodo-cache (standard flat namespace)</text>

  <rect x="1076" y="672" width="468" height="154" rx="10" fill="#ffffff" stroke="#dc2626" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="1096" y="724" width="48" height="48"/>
  <text x="1162" y="738" class="node-title">30-Year WORM Compliance Archive</text>
  <text x="1162" y="762" class="node-sub">gs://*-ent-lakehouse-worm-archive (retention = 946728000s)</text>

  <path d="M 800 588 L 800 614" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"/>
</svg>
"""


def build_svg_4_denodo_vm_scaleset_pipeline_horizontal(icons: dict[str, str]) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 880" width="100%" height="100%">
  <defs>
    <style>
      .title {{ font: 700 22px 'Google Sans', 'Inter', Arial, sans-serif; fill: #0f172a; }}
      .subtitle {{ font: 500 13px 'Google Sans', 'Inter', Arial, sans-serif; fill: #475569; }}
      .node-title {{ font: 700 15px 'Google Sans', 'Inter', Arial, sans-serif; fill: #0f172a; }}
      .node-sub {{ font: 500 12px 'Google Sans', 'Inter', Arial, sans-serif; fill: #475569; }}
      .badge {{ font: 700 11px 'Google Sans', 'Roboto Mono', monospace; fill: #ffffff; }}
    </style>
    <filter id="shadow" x="-2%" y="-4%" width="104%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.07"/>
    </filter>
    <marker id="arrow-blue" markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1d4ed8"/>
    </marker>
    <marker id="arrow-green" markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
  </defs>

  <rect width="1600" height="880" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Header -->
  <rect x="24" y="18" width="1552" height="66" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="24" y="18" width="10" height="66" rx="4" fill="#7c3aed"/>
  <text x="50" y="46" class="title">Denodo 9.0 on Enterprise Base OS Images — VM Scale Set Pipeline (Horizontal Layered View)</text>
  <text x="50" y="68" class="subtitle">Layer 1: Base OS Image, Silent Installer &amp; Secret Manager  |  Layer 2: Regional VM Scale Set &amp; Internal NLB  |  Layer 3: Unattended Bootstrap</text>

  <!-- LAYER 1: STAGING & SECRET MANAGER -->
  <rect x="24" y="104" width="1552" height="220" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="104" width="1552" height="34" rx="10" fill="#1d4ed8"/>
  <text x="46" y="126" class="badge">LAYER 1 — ENTERPRISE BASE OS IMAGE, SILENT INSTALLER STAGING &amp; SECRET MANAGER</text>

  <rect x="56" y="158" width="468" height="142" rx="10" fill="#ffffff" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_storage']}" x="76" y="204" width="48" height="48"/>
  <text x="142" y="220" class="node-title">Denodo 9.0 Silent Installer &amp; JDBC Staging</text>
  <text x="142" y="244" class="node-sub">denodo-install-9.0-linux64.tar.gz + Spark/BQ JDBC in GCS</text>

  <rect x="566" y="158" width="468" height="142" rx="10" fill="#ffffff" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['secret_manager']}" x="586" y="204" width="48" height="48"/>
  <text x="652" y="220" class="node-title">Cloud Secret Manager (CMEK)</text>
  <text x="652" y="244" class="node-sub">Injects denodo.lic &amp; VDP admin password at boot</text>

  <rect x="1076" y="158" width="468" height="142" rx="10" fill="#ffffff" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['identity_and_access_management']}" x="1096" y="204" width="48" height="48"/>
  <text x="1162" y="220" class="node-title">Zero-Key VM Service Account</text>
  <text x="1162" y="244" class="node-sub">Attached to MIG VMs for GCS, Secret Manager &amp; BQ Cache</text>

  <!-- LAYER 2: REGIONAL VM SCALE SET & INTERNAL NLB -->
  <rect x="24" y="352" width="1552" height="236" rx="12" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="352" width="1552" height="34" rx="10" fill="#7c3aed"/>
  <text x="46" y="374" class="badge">LAYER 2 — DENODO 9.0 BASE-IMAGE VM SCALE SET (REGIONAL MIG), AUTOSCALER &amp; INTERNAL NLB</text>

  <rect x="56" y="408" width="468" height="154" rx="10" fill="#ffffff" stroke="#c4b5fd" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['compute_engine']}" x="76" y="460" width="48" height="48"/>
  <text x="142" y="474" class="node-title">Shielded Base-OS Instance Template</text>
  <text x="142" y="498" class="node-sub">RHEL 9 Base OS image + n4-standard-8 + 200 GB CMEK disk</text>

  <rect x="566" y="408" width="468" height="154" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['compute_engine']}" x="586" y="460" width="48" height="48"/>
  <text x="652" y="474" class="node-title">Regional Managed Instance Group (2–6 VMs)</text>
  <text x="652" y="498" class="node-sub">Multi-zone HA, 70% CPU autoscaler &amp; TCP :9999 auto-healing</text>

  <rect x="1076" y="408" width="468" height="154" rx="10" fill="#ffffff" stroke="#c4b5fd" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['cloud_load_balancing']}" x="1096" y="460" width="48" height="48"/>
  <text x="1162" y="474" class="node-title">Internal Passthrough NLB (:9999 / :9090)</text>
  <text x="1162" y="498" class="node-sub">Exposes VDP JDBC (:9999), Design Studio (:9090) &amp; Scheduler</text>

  <path d="M 800 324 L 800 350" stroke="#1d4ed8" stroke-width="3" marker-end="url(#arrow-blue)"/>

  <!-- LAYER 3: UNATTENDED BOOTSTRAP PIPELINE -->
  <rect x="24" y="616" width="1552" height="236" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <rect x="24" y="616" width="1552" height="34" rx="10" fill="#059669"/>
  <text x="46" y="638" class="badge">LAYER 3 — UNATTENDED BASE-OS SILENT INSTALLATION &amp; VQL BOOTSTRAP (scripts/install_denodo_vmss_startup.sh)</text>

  <rect x="56" y="672" width="468" height="154" rx="10" fill="#ffffff" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['compute_engine']}" x="76" y="724" width="48" height="48"/>
  <text x="142" y="738" class="node-title">1. Base OS Prep &amp; Artifact Download</text>
  <text x="142" y="762" class="node-sub">Installs OpenJDK 17 &amp; pulls Denodo tar.gz + JDBC from GCS</text>

  <rect x="566" y="672" width="468" height="154" rx="10" fill="#ffffff" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
  <image href="{icons['secret_manager']}" x="586" y="724" width="48" height="48"/>
  <text x="652" y="738" class="node-title">2. Silent Install &amp; BigQuery Cache</text>
  <text x="652" y="762" class="node-sub">Runs installer_cli.sh --xml &amp; sets EnableHighThroughputAPI=1</text>

  <rect x="1076" y="672" width="468" height="154" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#shadow)"/>
  <image href="{icons['bigquery']}" x="1096" y="724" width="48" height="48"/>
  <text x="1162" y="738" class="node-title">3. Service Startup &amp; VQL Catalog Import</text>
  <text x="1162" y="762" class="node-sub">Starts VDP (:9999) &amp; imports 01_denodo_vql_bootstrap.vql</text>

  <path d="M 800 588 L 800 614" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"/>
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
    svg3 = ASSETS_DIR / "03_storage_accounts_and_managed_folder_governance.svg"
    svg4 = ASSETS_DIR / "04_denodo_vm_scaleset_installation_pipeline.svg"

    svg1.write_text(build_svg_1_end_to_end_horizontal(icons), encoding="utf-8")
    svg2.write_text(build_svg_2_network_and_vpc_sc_horizontal(icons), encoding="utf-8")
    svg3.write_text(build_svg_3_storage_and_folder_governance_horizontal(icons), encoding="utf-8")
    svg4.write_text(build_svg_4_denodo_vm_scaleset_pipeline_horizontal(icons), encoding="utf-8")
    print("Generated 4 HORIZONTAL-LAYERED SVG blueprints in", ASSETS_DIR)

    chrome_bin = shutil.which("google-chrome") or "/usr/bin/google-chrome"
    if pathlib.Path(chrome_bin).exists():
        specs = [
            (svg1, "1600,980"),
            (svg2, "1600,960"),
            (svg3, "1600,880"),
            (svg4, "1600,880"),
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
        print("Rendered 4 HORIZONTAL-LAYERED PNG blueprints in", ASSETS_DIR)


if __name__ == "__main__":
    main()
