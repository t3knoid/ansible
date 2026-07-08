# 🐘 Runbook: Adding PostgreSQL Exporter to an Inventory

## 📖 Purpose

This runbook explains how to:

1. add hosts to PostgreSQL exporter monitoring in a given inventory
2. deploy `postgres_exporter` to those hosts
3. refresh the Prometheus scrape configuration so Prometheus starts scraping them

In this repository, PostgreSQL exporter targets come from the inventory you deploy from. Prometheus does not maintain a separate manual list of PostgreSQL exporter targets.

---

## 🧭 How PostgreSQL Exporter Targeting Works Here

PostgreSQL exporter scraping is driven by the `postgres_exporter` group in an inventory.

The current repo pattern uses direct host membership such as:

```ini
[postgres_exporter]
pg-0
pg-1
pg-2
```

Use the nearest existing example in the inventory you are editing.

---

## 🛠 Add PostgreSQL Exporter to an Inventory

### 1. Open the target inventory

Example:

```text
inventory/pg/inventory.ini
```

### 2. Define the exporter settings at inventory level

Open the inventory's group vars file:

```text
inventory/<name>/group_vars/all/main.yml
```

Ensure it defines:

```yaml
postgres_exporter_port: 9187
postgres_exporter_setup_db_username: "postgres_exporter"
postgres_exporter_setup_db_name: "postgres"
postgres_exporter_setup_db_host: "127.0.0.1"
postgres_exporter_setup_db_port: 5432
postgres_exporter_setup_sslmode: "disable"
```

Example:

```yaml
# inventory/pg/group_vars/all/main.yml
postgres_exporter_port: 9187
postgres_exporter_setup_db_username: "postgres_exporter"
postgres_exporter_setup_db_name: "postgres"
postgres_exporter_setup_db_host: "127.0.0.1"
postgres_exporter_setup_db_port: 5432
postgres_exporter_setup_sslmode: "disable"
```

Set these at the inventory level so the exporter role and the Prometheus scrape configuration use the same connection and port settings for every PostgreSQL host in that inventory.

### 3. Define the secret values in vault

Set the PostgreSQL exporter credentials in the inventory vault file:

```text
inventory/<name>/group_vars/all/vault.yml
```

Define:

```yaml
postgres_exporter_setup_db_password: "REDACTED"
```

Notes:

* The role manages the `postgres_exporter` database user locally on the PostgreSQL host.
* The exporter user is granted `pg_monitor` so it can read monitoring data without using the default `postgres` account.
* The role performs the database-user creation over the local PostgreSQL Unix socket as the `postgres` OS user.

### 4. Add hosts to the PostgreSQL exporter group

Add the PostgreSQL hosts to the inventory's `postgres_exporter` group:

```ini
[postgres_exporter]
pg-0
pg-1
pg-2
pg-3
pg-4
```

Guidelines:

* Reuse the existing inventory pattern.
* Define `postgres_exporter_port: 9187` in `group_vars/all/main.yml` for the inventory.
* Add only hosts that actually run PostgreSQL and should expose PostgreSQL metrics.
* Ensure the hosts are already present in the inventory in their appropriate service or host groups.

---

## 🚀 Deploy PostgreSQL Exporter to the Target Hosts

Run the PostgreSQL exporter deployment playbook against the same inventory:

```bash
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_postgres_exporter.yml
```

Example:

```bash
ansible-playbook -i inventory/pg/inventory.ini playbooks/prometheus/deploy_postgres_exporter.yml
```

What this does:

* installs or updates `postgres_exporter` on the inventory's `postgres_exporter` hosts
* creates or updates the dedicated PostgreSQL monitoring user
* grants the monitoring user `pg_monitor`
* configures the exporter service on those hosts
* does not update Prometheus scrape targets by itself

---

## 🔄 Deploy the Updated Targets to Prometheus

After PostgreSQL exporter is present in the inventory and deployed to the hosts, refresh the Prometheus exporter scrape configuration:

```bash
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml
```

Example:

```bash
ansible-playbook -i inventory/pg/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml
```

What this does:

* reads the current inventory's `postgres_exporter` group
* renders the Prometheus PostgreSQL exporter scrape job from that inventory membership
* updates Prometheus so the selected hosts are scraped

If your normal workflow uses an inventory shell variable such as `$INV`, keep using the repo convention you already use.

---

## ✅ Validate Before Deploying

If Ansible is installed in the repo Python environment:

```bash
source /opt/python_3.12/bin/activate
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_postgres_exporter.yml --syntax-check
ansible-playbook -i inventory/<name>/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml --syntax-check
```

This checks both the PostgreSQL exporter deployment path and the Prometheus scrape refresh path.

---

## 🔍 Verify After Deployment

### In Prometheus

Run queries such as:

```promql
up{job="postgres_exporter"}
```

```promql
pg_up{job="postgres_exporter"}
```

Expected behavior:

* the new host appears in the `postgres_exporter` job
* the `instance` label matches the inventory host name
* `pg_up` is `1` when the exporter can reach PostgreSQL successfully

You can also check standard PostgreSQL exporter metrics such as:

```promql
pg_stat_database_numbackends{job="postgres_exporter"}
```

```promql
pg_postmaster_start_time_seconds{job="postgres_exporter"}
```

### In Grafana

Open the PostgreSQL or observability dashboards and confirm the host appears in the PostgreSQL panels.

---

## ⚠️ Common Mistakes

* Adding a host to the inventory but not to the `postgres_exporter` group
* Forgetting to define `postgres_exporter_port: 9187` at inventory level
* Forgetting to set `postgres_exporter_setup_db_password` in the inventory vault
* Deploying PostgreSQL exporter but forgetting to refresh Prometheus exporters
* Running `deploy_prometheus_exporters.yml` against the wrong inventory
* Using the default `postgres` database account instead of the dedicated exporter user

---

## ✅ Summary

To add PostgreSQL exporter for a given inventory:

1. Define `postgres_exporter_port: 9187` and the PostgreSQL exporter connection settings in the inventory's `group_vars/all/main.yml`
2. Define `postgres_exporter_setup_db_password` in the inventory vault
3. Edit the inventory and add hosts to `postgres_exporter`
4. Deploy [playbooks/prometheus/deploy_postgres_exporter.yml](playbooks/prometheus/deploy_postgres_exporter.yml)
5. Deploy [playbooks/prometheus/deploy_prometheus_exporters.yml](playbooks/prometheus/deploy_prometheus_exporters.yml)
6. Verify the new host in Prometheus and Grafana

The inventory is the source of truth for which hosts should be scraped by the Prometheus `postgres_exporter` job.
