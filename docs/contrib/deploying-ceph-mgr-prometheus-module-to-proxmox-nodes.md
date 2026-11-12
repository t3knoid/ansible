# 🐙 Deploying the Ceph Mgr Prometheus Module to Proxmox Nodes

## 📖 Purpose

This runbook explains how to:

1. add Proxmox Ceph nodes to Ceph monitoring
2. enable and configure the `ceph-mgr` Prometheus module
3. refresh the Prometheus scrape configuration and Ceph alert rules
4. verify Ceph metrics in Prometheus and Grafana

In this repository, Ceph scrape targets come from the `ceph_nodes` inventory group. Prometheus does not maintain a separate manual list of Ceph targets.

---

## 🧭 How Ceph Monitoring Works Here

Ceph metrics come from the **Prometheus module built into `ceph-mgr`**. There is no separate exporter to install. Once the module is enabled, every manager daemon listens on port `9283` and serves `/metrics`.

Key behavior:

* Only the **active** manager returns Ceph metrics. Standby managers answer the scrape but return no Ceph samples.
* Prometheus therefore scrapes **every** node in `ceph_nodes`. Whichever node holds the active manager supplies the data, and scraping keeps working after a manager failover.
* The `ceph` scrape job uses `honor_labels: true` so labels set by `ceph-mgr` are kept rather than overwritten.
* The module is cluster-wide. It is enabled once, not per node.

The module is configured by:

```text
playbooks/proxmox/deploy_pve_monitoring.yml
```

Prometheus scraping is driven by the `ceph_nodes` group in the PVE inventory:

```ini
[ceph_nodes]
pve-0
pve-1
pve-2
```

---

## 🛠 Add a Proxmox Node to Ceph Monitoring

### 1. Open the PVE inventory

```text
inventory/pve/inventory.ini
```

### 2. Add the node to the Ceph node group

Add the host to `ceph_nodes`:

```ini
[ceph_nodes]
pve-0
pve-1
pve-2
```

Guidelines:

* Only add hosts that are members of the Proxmox Ceph cluster.
* Keep the host in `pvenodes` as well, so `deploy_pve_monitoring.yml` targets it.
* Ensure each host has a matching entry in `global_ip_addresses` in `roles/global/vars/main.yml`. Prometheus scrapes that address, not the Ceph cluster network address.

### 3. Make sure the node runs a Ceph manager

Prometheus only receives data from nodes that run a `ceph-mgr` daemon. Check from any Ceph node:

```bash
ceph mgr stat
ceph mgr services
```

If the new node has no manager and should have one, create it in the Proxmox UI under **Ceph → Monitor → Manager**, or on the node:

```bash
pveceph mgr create
```

### 4. Open the port if the Proxmox firewall is enabled

Allow TCP `9283` from the Prometheus host (`prometheus-0`) to every node in `ceph_nodes`.

### 5. Review the scrape settings (optional)

The defaults live in `roles/prometheus_setup/defaults/main/main.yml`:

```yaml
prometheus_setup_ceph_job_name: "ceph"
prometheus_setup_ceph_port: 9283
prometheus_setup_ceph_alerts_enabled: true
```

No credentials are needed. The module serves metrics without authentication, so restrict access to port `9283` at the network or firewall level.

---

## 🚀 Enable the Ceph Mgr Prometheus Module

Run the Proxmox monitoring playbook against the PVE inventory:

```bash
ansible-playbook -i inventory/pve/inventory.ini playbooks/proxmox/deploy_pve_monitoring.yml
```

What this does for Ceph, once, on the first host in `ceph_nodes`:

* runs `ceph mgr module enable prometheus`
* sets `mgr/prometheus/exclude_perf_counters` to `false`, only if it is not already `false`

Since Ceph Reef, per-daemon performance counters (per-OSD latency, operations, and similar) are excluded from the manager module by default. They are expected to come from cephadm's `ceph-exporter` daemon, which Proxmox does not deploy. Turning the exclusion off makes the manager module export them instead.

The same playbook also deploys node exporter and PVE exporter to every `pvenodes` host. It does not update the Prometheus configuration.

---

## 🔄 Deploy the Updated Targets and Rules to Prometheus

### Scrape targets

Refresh the Prometheus exporter scrape configuration using the repository's combined default inventory:

```bash
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml
```

What this does:

* reads the `ceph_nodes` group from the combined inventory
* merges its hosts into the existing Ceph targets
* renders the `ceph` scrape job with a 30 second interval and `honor_labels: true`
* points each target at `<global_ip_addresses entry>:9283`

Do not scope this run with `-i` to a single inventory folder, because other exporter groups would not be visible.

### Alert rules

The Ceph alert rules are part of `prometheus.rules.yml`, which is deployed by the main Prometheus playbook:

```bash
ansible-playbook -i inventory/prometheus/inventory.ini playbooks/prometheus/deploy_prometheus.yml
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml
```

Run the exporter refresh afterward so every exporter scrape job is rendered back into `prometheus.yml`. The role validates the rule file with `promtool` and reloads Prometheus.

The `ceph` rule group contains:

| Alert | Fires when | Severity |
|---|---|---|
| `CephMetricsAbsent` | no `ceph_health_status` for 5 minutes (no active manager is being scraped) | critical |
| `CephHealthWarning` | cluster in `HEALTH_WARN` for 15 minutes | warning |
| `CephHealthError` | cluster in `HEALTH_ERR` for 5 minutes | critical |
| `CephMonQuorumLost` | a monitor out of quorum for 5 minutes | warning |
| `CephOSDDown` | an OSD down for 5 minutes | critical |
| `CephOSDOut` | an OSD marked out for 15 minutes | warning |
| `CephOSDNearFull` | an OSD over 80% used for 15 minutes | warning |
| `CephClusterNearFull` | raw cluster capacity over 80% used for 15 minutes | warning |
| `CephClusterCriticallyFull` | raw cluster capacity over 90% used for 5 minutes | critical |
| `CephPGsNotActive` | any placement group not active for 15 minutes | critical |

Set `prometheus_setup_ceph_alerts_enabled: false` to leave the group out.

> **Note:** `prometheus.yml` does not currently have an `alerting:` section, so these alerts appear in Prometheus and Grafana but are not sent to Alertmanager.

---

## ✅ Validate Before Deploying

If Ansible is installed in the repository Python environment:

```bash
source /opt/python_3.12/bin/activate
ansible-inventory -i inventory/pve/inventory.ini --graph ceph_nodes
ansible-playbook -i inventory/pve/inventory.ini playbooks/proxmox/deploy_pve_monitoring.yml --syntax-check
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml --syntax-check
```

Confirm that the inventory graph lists the intended nodes under `ceph_nodes`.

---

## 🔍 Verify After Deployment

### On a Proxmox Ceph node

Check that the module is enabled and where it is served:

```bash
ceph mgr module ls | grep prometheus
ceph mgr services
```

`ceph mgr services` should list `"prometheus": "http://<active-node>:9283/"`.

Check the perf counter setting:

```bash
ceph config get mgr mgr/prometheus/exclude_perf_counters
```

The result should be `false`.

Check the endpoint on the **active** manager node:

```bash
curl --fail -s http://localhost:9283/metrics | grep '^ceph_health_status'
```

The response should contain `ceph_health_status`. The same command on a standby node returns no Ceph metrics, which is expected.

### In Prometheus

Run:

```promql
up{job="ceph"}
```

Expected behavior:

* every node in `ceph_nodes` appears in the `ceph` job
* the `instance` label matches the inventory host name
* the value is `1` when port `9283` is reachable

Then confirm that exactly one node supplies Ceph data:

```promql
count by (instance) (ceph_health_status{job="ceph"})
```

This should return one series, for the node with the active manager.

Check the alert rules on the **Alerts** page. The `ceph` group should be listed. If `CephMetricsAbsent` is firing, no active manager is being scraped.

### In Grafana

Open the **Proxmox VE Status** dashboard and confirm that the Ceph panels report current data:

* Ceph Health
* Ceph OSDs Up / Total
* Ceph Capacity Used
* Ceph Monitors In Quorum
* Ceph Pool Usage

---

## ⚠️ Common Mistakes

* Adding a host to `ceph_nodes` but not to `pvenodes`, so the monitoring playbook does not target it
* Adding a host that is not part of the Ceph cluster
* Forgetting the host's `global_ip_addresses` entry
* Scraping only one node, so metrics stop after a manager failover
* Expecting Ceph metrics from a standby manager
* Enabling the module but forgetting to refresh Prometheus exporters
* Passing only the PVE inventory to `deploy_prometheus_exporters.yml`
* Running `deploy_prometheus.yml` without running `deploy_prometheus_exporters.yml` afterward
* Leaving TCP `9283` blocked by the Proxmox firewall
* Expecting the Ceph alerts to send notifications while Prometheus has no `alerting:` section

---

## ✅ Summary

To monitor Ceph on the Proxmox nodes:

1. Add each Ceph node to `ceph_nodes` (and `pvenodes`) in `inventory/pve/inventory.ini`.
2. Make sure the nodes run a `ceph-mgr` daemon and allow TCP `9283` from Prometheus.
3. Run `playbooks/proxmox/deploy_pve_monitoring.yml` with the PVE inventory to enable the module.
4. Run `playbooks/prometheus/deploy_prometheus.yml` to deploy the Ceph alert rules.
5. Run `playbooks/prometheus/deploy_prometheus_exporters.yml` with the combined default inventory.
6. Verify the `ceph` job in Prometheus and the Ceph panels in the Proxmox VE Status dashboard.

The inventory is the source of truth for which Ceph nodes are scraped.
