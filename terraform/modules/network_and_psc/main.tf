variable "project_id" { type = string }
variable "region" { type = string }
variable "environment" { type = string }
variable "resource_prefix" { type = string }
variable "vpc_subnet_cidr" { type = string }
variable "gke_pods_cidr" { type = string }
variable "gke_services_cidr" { type = string }
variable "denodo_subnet_cidr" { type = string }
variable "denodo_gke_pods_cidr" { type = string }
variable "denodo_gke_services_cidr" { type = string }
variable "denodo_gke_master_cidr" { type = string }
variable "psc_subnet_cidr" { type = string }
variable "ilb_proxy_subnet_cidr" { type = string }
variable "access_policy_id" { type = string }
variable "labels" { type = map(string) }

# -----------------------------------------------------------------------------
# 1. Customer-Managed Single-Environment VPC
# -----------------------------------------------------------------------------
resource "google_compute_network" "single_env_vpc" {
  name                    = "${var.resource_prefix}-vpc-${var.environment}"
  project                 = var.project_id
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
  description             = "Customer-managed Zero-Trust VPC segmented across Databricks on GCP, Denodo 8.0 Trial GKE Cluster, and PSC endpoints"
}

# -----------------------------------------------------------------------------
# 2. Subnet A: Databricks on GCP Compute Plane (/19 + GKE Secondary Ranges)
# -----------------------------------------------------------------------------
resource "google_compute_subnetwork" "databricks_compute_subnet" {
  name                     = "${var.resource_prefix}-snet-databricks-${var.region}"
  project                  = var.project_id
  region                   = var.region
  network                  = google_compute_network.single_env_vpc.id
  ip_cidr_range            = var.vpc_subnet_cidr
  private_ip_google_access = true
  description              = "Dedicated /19 subnet for Databricks GKE Enterprise Compute Pools (N4/C4/M3/Z3)"

  secondary_ip_range {
    range_name    = "gke-pods-range"
    ip_cidr_range = var.gke_pods_cidr
  }

  secondary_ip_range {
    range_name    = "gke-services-range"
    ip_cidr_range = var.gke_services_cidr
  }

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# -----------------------------------------------------------------------------
# 3. Subnet B: Denodo 8.0 Trial Server on GKE Tier (/22 + GKE Secondary Ranges)
# -----------------------------------------------------------------------------
resource "google_compute_subnetwork" "denodo_vdp_subnet" {
  name                     = "${var.resource_prefix}-snet-denodo-vdp-${var.region}"
  project                  = var.project_id
  region                   = var.region
  network                  = google_compute_network.single_env_vpc.id
  ip_cidr_range            = var.denodo_subnet_cidr
  private_ip_google_access = true
  description              = "Dedicated /22 subnet for Denodo 8.0 Trial Server on GKE (n4-standard-8 nodes + Internal Passthrough LoadBalancer)"

  secondary_ip_range {
    range_name    = "denodo-gke-pods-range"
    ip_cidr_range = var.denodo_gke_pods_cidr
  }

  secondary_ip_range {
    range_name    = "denodo-gke-services-range"
    ip_cidr_range = var.denodo_gke_services_cidr
  }

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# -----------------------------------------------------------------------------
# 4. Subnet C: Private Service Connect (PSC) Endpoints (/24)
# -----------------------------------------------------------------------------
resource "google_compute_subnetwork" "psc_endpoints_subnet" {
  name                     = "${var.resource_prefix}-snet-psc-${var.region}"
  project                  = var.project_id
  region                   = var.region
  network                  = google_compute_network.single_env_vpc.id
  ip_cidr_range            = var.psc_subnet_cidr
  private_ip_google_access = true
  description              = "Dedicated /24 subnet for Databricks Control Plane & SQL Warehouse Private Service Connect endpoints"
}

# -----------------------------------------------------------------------------
# 5. Subnet D: Regional Managed Proxy-Only Subnet (/24)
# -----------------------------------------------------------------------------
resource "google_compute_subnetwork" "ilb_proxy_subnet" {
  name          = "${var.resource_prefix}-snet-ilb-proxy-${var.region}"
  project       = var.project_id
  region        = var.region
  network       = google_compute_network.single_env_vpc.id
  ip_cidr_range = var.ilb_proxy_subnet_cidr
  purpose       = "REGIONAL_MANAGED_PROXY"
  role          = "ACTIVE"
  description   = "Regional Envoy proxy-only subnet for internal HTTPS load balancing"
}

resource "google_compute_address" "psc_databricks_workspace_ip" {
  name         = "${var.resource_prefix}-psc-databricks-ip"
  project      = var.project_id
  region       = var.region
  subnetwork   = google_compute_subnetwork.psc_endpoints_subnet.id
  address_type = "INTERNAL"
  description  = "Internal IP for Databricks Control Plane & Serverless SQL Warehouse Private Link"
}

resource "google_compute_global_address" "private_service_access_range" {
  name          = "${var.resource_prefix}-psa-cloudsql-range"
  project       = var.project_id
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 20
  network       = google_compute_network.single_env_vpc.id
  description   = "Private Service Access (/20) peering range for HA Cloud SQL PostgreSQL 15 Hive Metastore & Filestore Enterprise"
}

# -----------------------------------------------------------------------------
# 6. Private Cloud DNS Routing to restricted.googleapis.com (199.36.153.4/30)
# -----------------------------------------------------------------------------
resource "google_dns_managed_zone" "private_googleapis_zone" {
  name        = "${var.resource_prefix}-private-googleapis"
  project     = var.project_id
  dns_name    = "googleapis.com."
  description = "Routes all Google Cloud API calls (GCS, BigQuery, KMS, Secret Manager) over restricted.googleapis.com"
  visibility  = "private"

  private_visibility_config {
    networks {
      network_url = google_compute_network.single_env_vpc.id
    }
  }
}

resource "google_dns_record_set" "restricted_googleapis_a" {
  name         = "restricted.googleapis.com."
  project      = var.project_id
  managed_zone = google_dns_managed_zone.private_googleapis_zone.name
  type         = "A"
  ttl          = 300
  rrdatas      = ["199.36.153.4", "199.36.153.5", "199.36.153.6", "199.36.153.7"]
}

resource "google_dns_record_set" "wildcard_googleapis_cname" {
  name         = "*.googleapis.com."
  project      = var.project_id
  managed_zone = google_dns_managed_zone.private_googleapis_zone.name
  type         = "CNAME"
  ttl          = 300
  rrdatas      = ["restricted.googleapis.com."]
}

# -----------------------------------------------------------------------------
# 7. Cloud Router & Cloud NAT (Controlled Outbound Package Patching w/ Logging)
# -----------------------------------------------------------------------------
resource "google_compute_router" "nat_router" {
  name    = "${var.resource_prefix}-nat-router-${var.region}"
  project = var.project_id
  region  = var.region
  network = google_compute_network.single_env_vpc.id
}

resource "google_compute_router_nat" "egress_nat" {
  name                               = "${var.resource_prefix}-cloud-nat-${var.region}"
  project                            = var.project_id
  router                             = google_compute_router.nat_router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

# -----------------------------------------------------------------------------
# 8. Zero-Trust Micro-Segmented GCP Firewall Controls (Ingress & Egress)
# -----------------------------------------------------------------------------

# Priority 65534: Default-Deny All Internet Egress
resource "google_compute_firewall" "deny_all_internet_egress" {
  name               = "${var.resource_prefix}-fw-deny-internet-egress"
  project            = var.project_id
  network            = google_compute_network.single_env_vpc.name
  direction          = "EGRESS"
  priority           = 65534
  destination_ranges = ["0.0.0.0/0"]

  deny {
    protocol = "all"
  }

  log_config {
    metadata = "INCLUDE_ALL_METADATA"
  }
}

# Priority 100: Allow Egress to restricted.googleapis.com VIPs (199.36.153.4/30)
resource "google_compute_firewall" "allow_egress_restricted_googleapis" {
  name               = "${var.resource_prefix}-fw-allow-restricted-googleapis"
  project            = var.project_id
  network            = google_compute_network.single_env_vpc.name
  direction          = "EGRESS"
  priority           = 100
  destination_ranges = ["199.36.153.4/30"]

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }
}

# Priority 150: Allow Denodo 8.0 Trial GKE Pods & Nodes -> Databricks SQL Warehouse PSC & Worker Nodes
resource "google_compute_firewall" "allow_denodo_to_databricks_jdbc" {
  name          = "${var.resource_prefix}-fw-allow-denodo-to-databricks"
  project       = var.project_id
  network       = google_compute_network.single_env_vpc.name
  direction     = "INGRESS"
  priority      = 150
  source_ranges = [var.denodo_subnet_cidr, var.denodo_gke_pods_cidr]
  target_tags   = ["databricks-worker"]

  allow {
    protocol = "tcp"
    ports    = ["443", "8443"]
  }
}

# Priority 200: Allow Internal Databricks Compute Plane & Hive Metastore Traffic
resource "google_compute_firewall" "allow_databricks_internal_cluster" {
  name      = "${var.resource_prefix}-fw-allow-databricks-internal"
  project   = var.project_id
  network   = google_compute_network.single_env_vpc.name
  direction = "INGRESS"
  priority  = 200

  allow {
    protocol = "tcp"
    ports    = ["443", "2049", "5432", "8443"]
  }

  source_ranges = [
    var.vpc_subnet_cidr,
    var.gke_pods_cidr,
    var.psc_subnet_cidr,
  ]
  target_tags = ["databricks-worker"]
}

# Priority 250: Allow IAP Zero-Trust Admin, GKE Control Plane & GCP Health Checks -> Denodo 8.0 Trial GKE Nodes
resource "google_compute_firewall" "allow_iap_and_hc_to_denodo_vdp" {
  name      = "${var.resource_prefix}-fw-allow-iap-and-hc-to-denodo"
  project   = var.project_id
  network   = google_compute_network.single_env_vpc.name
  direction = "INGRESS"
  priority  = 250

  allow {
    protocol = "tcp"
    ports    = ["22", "8008", "9090", "9443", "9996", "9997", "9999", "10250"]
  }

  source_ranges = [
    "35.235.240.0/20",
    "130.211.0.0/22",
    "35.191.0.0/16",
    var.denodo_gke_master_cidr,
    var.vpc_subnet_cidr,
    var.denodo_subnet_cidr,
    var.denodo_gke_pods_cidr,
  ]
  target_tags = ["denodo-gke-node", "denodo-vdp-node"]
}

# -----------------------------------------------------------------------------
# 9. VPC Service Controls (VPC-SC) Data Exfiltration Perimeter (Optional Toggle)
# -----------------------------------------------------------------------------
resource "google_access_context_manager_service_perimeter" "single_env_perimeter" {
  count  = var.access_policy_id != "" ? 1 : 0
  parent = "accessPolicies/${var.access_policy_id}"
  name   = "accessPolicies/${var.access_policy_id}/servicePerimeters/${replace(var.resource_prefix, "-", "_")}_perimeter"
  title  = "${var.resource_prefix}-vpc-sc-perimeter"

  status {
    resources = ["projects/${var.project_id}"]
    restricted_services = [
      "storage.googleapis.com",
      "bigquery.googleapis.com",
      "bigquerystorage.googleapis.com",
      "sqladmin.googleapis.com",
      "secretmanager.googleapis.com",
      "cloudkms.googleapis.com",
      "container.googleapis.com",
      "file.googleapis.com",
    ]
  }
}

output "vpc_id" {
  value = google_compute_network.single_env_vpc.id
}

output "databricks_subnet_id" {
  value = google_compute_subnetwork.databricks_compute_subnet.id
}

output "denodo_subnet_id" {
  value = google_compute_subnetwork.denodo_vdp_subnet.id
}

output "psc_subnet_id" {
  value = google_compute_subnetwork.psc_endpoints_subnet.id
}

output "ilb_proxy_subnet_id" {
  value = google_compute_subnetwork.ilb_proxy_subnet.id
}
