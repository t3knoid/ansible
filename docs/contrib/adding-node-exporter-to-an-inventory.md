# 📈 Runbook: Adding Node Exporter to an Inventory

## 📖 Purpose

This runbook explains how to:

1. add hosts to node exporter monitoring in a given inventory
2. deploy node exporter to those hosts
3. refresh the Prometheus scrape configuration so Prometheus starts scraping them

In this repository, node exporter targets come from the inventory you deploy from. Prometheus does not maintain a separate manual list of node exporter targets.

---

## 🧭 How Node Exporter Targeting Works Here

Node exporter scraping is driven by the `node_exporter` group in an inventory.

There are two common patterns in this repo:

### Direct group membership

```ini
[node_exporter]
plex-0
```

### Group-of-groups membership

```ini
[node_exporter:children]
lidarr
sonarr
radarr
```

Use whichever pattern best matches the inventory you are editing. Follow the nearest existing example in that inventory.

---

## 🛠 Add Node Exporter to an Inventory

### 1. Open the target inventory

Examples:

```text
inventory/plex/inventory.ini
inventory/rproxy/inventory.ini
inventory/services/inventory.ini
```

### 2. Define the node exporter port at inventory level

Open the inventory's group vars file:

```text
inventory/<name>/group_vars/all/main.yml
```

Ensure it defines:

```yaml
node_exporter_port: 9200
```

Example:

```yaml
# inventory/minecraft/group_vars/all/main.yml
node_exporter_port: 9200
```

Set this at the inventory level so the node exporter role and the Prometheus scrape configuration use the same port for every host in that inventory.

### 3. Add the host or service group to node exporter monitoring

If the inventory uses direct host membership:

```ini
[node_exporter]
plex-0
```

If the inventory uses a children group:

```ini
[node_exporter:children]
lidarr
sonarr
radarr
```

Guidelines:

* Reuse the pattern already present in the inventory.
* Define `node_exporter_port: 9200` in `group_vars/all/main.yml` for the inventory.
* Add only hosts or groups that should expose node exporter metrics.
* Ensure the host is also present in the inventory in its appropriate service or host group.
* Do not create a second competing node exporter pattern in the same inventory unless there is a clear reason.

---

## 🚀 Deploy Node Exporter to the Target Hosts

Run the node exporter deployment playbook against the same inventory:

```bash
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_node_exporter.yml
```

Example:

```bash
ansible-playbook -i inventory/plex/inventory.ini playbooks/prometheus/deploy_node_exporter.yml
```

What this does:

* installs or updates node exporter on the inventory's `node_exporter` hosts
* configures the service on those hosts
* does not update Prometheus scrape targets by itself

---

## 🔄 Deploy the Updated Targets to Prometheus

After node exporter is present in the inventory and deployed to the hosts, refresh the Prometheus exporter scrape configuration:

```bash
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml
```

Example:

```bash
ansible-playbook -i inventory/plex/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml
```

What this does:

* reads the current inventory's `node_exporter` group
* renders the Prometheus node scrape job from that inventory membership
* updates Prometheus so the selected hosts are scraped

If your normal workflow uses an inventory shell variable such as `$INV`, keep using the repo convention you already use.

---

## ✅ Validate Before Deploying

If Ansible is installed in the repo Python environment:

```bash
source /opt/python_3.12/bin/activate
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_node_exporter.yml --syntax-check
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml --syntax-check
```

This checks both the node exporter deployment path and the Prometheus scrape refresh path.

---

## 🔍 Verify After Deployment

### In Prometheus

Run a query such as:

```promql
up{job="node"}
```

Expected behavior:

* the new host appears in the `node` job
* the `instance` label matches the inventory host name
* the value is `1` when the exporter is reachable

You can also check a standard node exporter metric:

```promql
node_time_seconds{job="node"}
```

### In Grafana

Open the node or observability dashboards and confirm the host appears in the node status panels.

---

## ⚠️ Common Mistakes

* Adding a host to the inventory but not to the `node_exporter` group
* Deploying node exporter but forgetting to refresh Prometheus exporters
* Running `deploy_prometheus_exporters.yml` against the wrong inventory
* Creating a new group style instead of following the inventory's existing pattern
* Expecting Prometheus to discover hosts that are not present in the selected inventory

---

## ✅ Summary

To add node exporter for a given inventory:

1. Define `node_exporter_port: 9200` in the inventory's `group_vars/all/main.yml`
2. Edit the inventory and add hosts or groups to `node_exporter`
3. Deploy [playbooks/prometheus/deploy_node_exporter.yml](playbooks/prometheus/deploy_node_exporter.yml)
4. Deploy [playbooks/prometheus/deploy_prometheus_exporters.yml](playbooks/prometheus/deploy_prometheus_exporters.yml)
5. Verify the new host in Prometheus and Grafana

The inventory is the source of truth for which hosts should be scraped by the Prometheus `node` job.
