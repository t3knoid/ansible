# 📊 Runbook: Adding NGINX Exporter to an Inventory

## 📖 Purpose

This runbook explains how to:

1. add hosts or groups to nginx exporter monitoring in a given inventory
2. deploy nginx-prometheus-exporter to those hosts
3. refresh the Prometheus scrape configuration so Prometheus starts scraping them

In this repository, nginx exporter targets come from the inventory you deploy from. Prometheus does not maintain a separate manual list of nginx exporter targets.

---

## 🧭 How NGINX Exporter Targeting Works Here

NGINX exporter scraping is driven by the `nginx_exporter` group in an inventory.

The current repo pattern uses a children group such as:

```ini
[nginx_exporter:children]
rproxy_main
rproxy_primary
rproxy_secondary
```

This is appropriate when the exporter should be installed on all hosts in one or more existing service groups.

If a nearby inventory already uses a different valid pattern, follow the local example in that inventory.

---

## 🛠 Add NGINX Exporter to an Inventory

### 1. Open the target inventory

Examples:

```text
inventory/rproxy/inventory.ini
inventory/pg/inventory.ini
```

### 2. Define the exporter port at inventory level

Open the inventory's group vars file:

```text
inventory/<name>/group_vars/all/main.yml
```

Ensure it defines:

```yaml
nginx_prometheus_exporter_port: 9113
```

Example:

```yaml
# inventory/rproxy/group_vars/all/main.yml
nginx_prometheus_exporter_port: 9113
```

Set this at the inventory level so the nginx exporter role and the Prometheus scrape configuration use the same port for every host in that inventory.

### 3. Add the host group to nginx exporter monitoring

If the inventory uses a children group:

```ini
[nginx_exporter:children]
rproxy_main
rproxy_primary
rproxy_secondary
```

If you need direct host membership instead, use the simplest valid inventory pattern for that inventory:

```ini
[nginx_exporter]
host-0
```

Guidelines:

* Reuse the pattern already present in the inventory.
* Define `nginx_prometheus_exporter_port: 9113` in `group_vars/all/main.yml` for the inventory.
* Add only hosts or groups that actually run NGINX and should expose NGINX metrics.
* Ensure the hosts are already present in the inventory in their appropriate service or host groups.
* Do not add unrelated non-NGINX hosts to `nginx_exporter`.

---

## 🚀 Deploy NGINX Exporter to the Target Hosts

Run the nginx exporter deployment playbook against the same inventory:

```bash
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_nginx_prometheus_exporter.yml
```

Example:

```bash
ansible-playbook -i inventory/rproxy/inventory.ini playbooks/prometheus/deploy_nginx_prometheus_exporter.yml
```

What this does:

* installs or updates `nginx-prometheus-exporter` on the inventory's `nginx_exporter` hosts
* configures the exporter service on those hosts
* configures the local NGINX status endpoint used by the exporter
* does not update Prometheus scrape targets by itself

---

## 🔄 Deploy the Updated Targets to Prometheus

After nginx exporter is present in the inventory and deployed to the hosts, refresh the Prometheus exporter scrape configuration:

```bash
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml
```

Example:

```bash
ansible-playbook -i inventory/rproxy/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml
```

What this does:

* reads the current inventory's `nginx_exporter` group
* renders the Prometheus NGINX exporter scrape job from that inventory membership
* updates Prometheus so the selected hosts are scraped

If your normal workflow uses an inventory shell variable such as `$INV`, keep using the repo convention you already use.

---

## ✅ Validate Before Deploying

If Ansible is installed in the repo Python environment:

```bash
source /opt/python_3.12/bin/activate
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_nginx_prometheus_exporter.yml --syntax-check
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml --syntax-check
```

This checks both the nginx exporter deployment path and the Prometheus scrape refresh path.

---

## 🔍 Verify After Deployment

### In Prometheus

Run a query such as:

```promql
up{job="nginx_exporter"}
```

Expected behavior:

* the new host appears in the `nginx_exporter` job
* the `instance` label matches the inventory host name
* the value is `1` when the exporter is reachable

You can also check a standard NGINX exporter metric:

```promql
nginx_up{job="nginx_exporter"}
```

### In Grafana

Open the NGINX or observability dashboards and confirm the host appears in the NGINX exporter panels.

---

## ⚠️ Common Mistakes

* Adding a host to the inventory but not to the `nginx_exporter` group
* Forgetting to define `nginx_prometheus_exporter_port: 9113` at inventory level
* Deploying nginx exporter but forgetting to refresh Prometheus exporters
* Running `deploy_prometheus_exporters.yml` against the wrong inventory
* Adding hosts that do not run NGINX or do not expose the expected local status endpoint

---

## ✅ Summary

To add nginx exporter for a given inventory:

1. Define `nginx_prometheus_exporter_port: 9113` in the inventory's `group_vars/all/main.yml`
2. Edit the inventory and add hosts or groups to `nginx_exporter`
3. Deploy [playbooks/prometheus/deploy_nginx_prometheus_exporter.yml](playbooks/prometheus/deploy_nginx_prometheus_exporter.yml)
4. Deploy [playbooks/prometheus/deploy_prometheus_exporters.yml](playbooks/prometheus/deploy_prometheus_exporters.yml)
5. Verify the new host in Prometheus and Grafana

The inventory is the source of truth for which hosts should be scraped by the Prometheus `nginx_exporter` job.
