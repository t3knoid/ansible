# 🛡️ Deploying the Pi-hole Exporter to DNS Nodes

## 📖 Purpose

This runbook explains how to:

1. add Pi-hole DNS hosts to Pi-hole exporter monitoring
2. supply the Pi-hole password the exporter needs
3. deploy the Pi-hole exporter to the DNS hosts
4. refresh the Prometheus scrape configuration and Pi-hole alert rules
5. verify Pi-hole metrics in Prometheus and Grafana

In this repository, Pi-hole exporter targets come from the `pihole_exporter` inventory group. Prometheus does not maintain a separate manual list of Pi-hole exporter targets.

---

## 🧭 How Pi-hole Exporter Targeting Works Here

The exporter ([eko/pihole-exporter](https://github.com/eko/pihole-exporter)) runs **on each Pi-hole host**. Each exporter reads its own local Pi-hole v6 API at `http://127.0.0.1:80`, listens on port `9617`, and serves `/metrics`.

Key behavior:

* Each host reports its own counters, so `dns-0` and `dns-1` appear as separate targets.
* The exporter logs in to the Pi-hole API with a password read from `/etc/pihole_exporter/password`.
* Prometheus scrapes every host in `pihole_exporter` every 30 seconds, with a 15 second timeout.
* Every metric carries a `hostname="127.0.0.1"` label from the exporter. Use the Prometheus `instance` label to tell the servers apart.

The exporter is deployed by:

```text
playbooks/prometheus/deploy_pihole_exporter.yml
```

Prometheus scraping is driven by the `pihole_exporter` group in the DNS inventory:

```ini
[pihole_exporter]
dns-0
dns-1
```

---

## 🛠 Add a Pi-hole Host to Exporter Monitoring

### 1. Open the DNS inventory

```text
inventory/dns/inventory.ini
```

### 2. Add the host to the Pi-hole exporter group

Add the host to `pihole_exporter`:

```ini
[pihole_exporter]
dns-0
dns-1
```

Guidelines:

* Only add hosts that run Pi-hole. Pi-hole is installed on the `dns` group by `playbooks/dns/deploy_pihole.yml`.
* Ensure each host has a matching entry in `global_ip_addresses` in `roles/global/vars/main.yml`. Prometheus scrapes that address.
* The DNS hosts are on `lan20`. Prometheus already reaches them for Node Exporter, so no extra routing is needed for an existing network.

### 3. Supply the Pi-hole password

By default, the exporter uses the `pihole` role's vaulted `pihole_password`. The deployment playbook loads it from:

```text
roles/pihole/defaults/main/vault.yml
```

No change is needed when every Pi-hole host uses that password.

To use a Pi-hole **application password** instead, or a different password for one host, set this in vault for the host or group:

```yaml
pihole_exporter_setup_password: <Pi-hole password or application password>
```

Create an application password in the Pi-hole web interface under **Settings → Web interface / API**.

Do not place the password in unencrypted inventory variables or in this runbook. The deployment role stops before making changes if no password is set.

### 4. Review the exporter and scrape settings (optional)

The exporter defaults live in `roles/pihole_exporter_setup/defaults/main/main.yml`:

```yaml
pihole_exporter_setup_version: "1.3.0"
pihole_exporter_setup_port: 9617
pihole_exporter_setup_pihole_protocol: "http"
pihole_exporter_setup_pihole_hostname: "127.0.0.1"
pihole_exporter_setup_pihole_port: 80
```

The Prometheus defaults live in `roles/prometheus_setup/defaults/main/main.yml`:

```yaml
prometheus_setup_pihole_exporter_job_name: "pihole_exporter"
prometheus_setup_pihole_exporter_port: 9617
prometheus_setup_pihole_alerts_enabled: true
```

If you change `pihole_exporter_setup_port` for a host, Prometheus picks up the new port for that host from its `pihole_exporter_setup_port` host variable.

---

## 🚀 Deploy the Pi-hole Exporter

Run the Pi-hole exporter playbook against the DNS inventory:

```bash
ansible-playbook -i inventory/dns/inventory.ini playbooks/prometheus/deploy_pihole_exporter.yml
```

What this does on every `pihole_exporter` host:

* checks that a Pi-hole password is set
* creates the `pihole-exporter` system user and group
* downloads the exporter binary from the GitHub release and verifies its SHA-256 checksum
* installs it in `/opt/pihole_exporter` and links it to `/usr/local/bin/pihole_exporter`
* writes the password to `/etc/pihole_exporter/password` (`root:pihole-exporter`, mode `0640`)
* installs and starts the `pihole_exporter` systemd service
* listens on port `9617`

The playbook does not update the Prometheus configuration by itself.

---

## 🔄 Deploy the Updated Targets and Rules to Prometheus

### Scrape targets

Refresh the Prometheus exporter scrape configuration using the repository's combined default inventory:

```bash
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml
```

What this does:

* reads the `pihole_exporter` group from the combined inventory
* merges its hosts into the existing Pi-hole exporter targets
* renders the `pihole_exporter` scrape job with a 30 second interval and 15 second timeout
* points each target at `<global_ip_addresses entry>:9617`

Do not scope this run with `-i` to a single inventory folder, because other exporter groups would not be visible.

### Alert rules

The Pi-hole alert rules are part of `prometheus.rules.yml`, which is deployed by the main Prometheus playbook:

```bash
ansible-playbook -i inventory/prometheus/inventory.ini playbooks/prometheus/deploy_prometheus.yml
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml
```

Run the exporter refresh afterward so every exporter scrape job is rendered back into `prometheus.yml`. The role validates the rule file with `promtool` and reloads Prometheus.

The `pihole` rule group contains:

| Alert | Fires when | Severity |
|---|---|---|
| `PiholeExporterDown` | the exporter cannot be scraped for 5 minutes | critical |
| `PiholeMetricsAbsent` | the exporter is up but returns no Pi-hole data for 10 minutes | warning |
| `PiholeBlockingDisabled` | blocking is disabled for 15 minutes | warning |
| `PiholeGravityEmpty` | the blocklist has no domains for 15 minutes | warning |

Set `prometheus_setup_pihole_alerts_enabled: false` to leave the group out.

> **Note:** `prometheus.yml` does not currently have an `alerting:` section, so these alerts appear in Prometheus and Grafana but are not sent to Alertmanager.

---

## ✅ Validate Before Deploying

If Ansible is installed in the repository Python environment:

```bash
source /opt/python_3.12/bin/activate
ansible-inventory -i inventory/dns/inventory.ini --graph pihole_exporter
ansible-playbook -i inventory/dns/inventory.ini playbooks/prometheus/deploy_pihole_exporter.yml --syntax-check
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml --syntax-check
```

Confirm that the inventory graph lists the intended hosts under `pihole_exporter`.

---

## 🔍 Verify After Deployment

### On each Pi-hole host

Check the service:

```bash
systemctl status pihole_exporter
/usr/local/bin/pihole_exporter -version
```

Check the local exporter endpoint:

```bash
curl --fail -s http://localhost:9617/metrics | grep -E '^pihole_(status|domains_being_blocked)'
```

The response should contain `pihole_status` and `pihole_domains_being_blocked`. If it does not, check the service logs for a `401` or connection error:

```bash
journalctl -u pihole_exporter -n 50 --no-pager
```

### In Prometheus

Run:

```promql
up{job="pihole_exporter"}
```

Expected behavior:

* every host in `pihole_exporter` appears in the `pihole_exporter` job
* the `instance` label matches the inventory host name
* the value is `1` when port `9617` is reachable

Then confirm that every host returns Pi-hole data:

```promql
pihole_status
```

This should return one series per host, with the value `1` while blocking is enabled.

Check the alert rules on the **Alerts** page. The `pihole` group should be listed. If `PiholeMetricsAbsent` is firing for a host, its exporter cannot read the Pi-hole API.

### In Grafana

No Pi-hole dashboard is provisioned yet. To view the metrics, import the exporter's published dashboard (grafana.com ID `10176`) and select the Prometheus data source. Group panels by `instance`, not `hostname`.

---

## ⚠️ Common Mistakes

* Adding a host that does not run Pi-hole
* Forgetting the host's `global_ip_addresses` entry
* Running the playbook without the vault password, so `pihole_password` cannot be loaded
* Using a password that does not match the Pi-hole web password on that host
* Putting the Pi-hole password in plaintext inventory variables
* Deploying the exporter but forgetting to refresh Prometheus exporters
* Passing only the DNS inventory to `deploy_prometheus_exporters.yml`
* Running `deploy_prometheus.yml` without running `deploy_prometheus_exporters.yml` afterward
* Grouping dashboards by `hostname`, which is `127.0.0.1` on every host
* Expecting the Pi-hole alerts to send notifications while Prometheus has no `alerting:` section

---

## ✅ Summary

To deploy the Pi-hole exporter to the DNS hosts:

1. Add each Pi-hole host to `pihole_exporter` in `inventory/dns/inventory.ini`.
2. Make sure the host has a `global_ip_addresses` entry.
3. Rely on the vaulted `pihole_password`, or set `pihole_exporter_setup_password` in vault.
4. Run `playbooks/prometheus/deploy_pihole_exporter.yml` with the DNS inventory.
5. Run `playbooks/prometheus/deploy_prometheus.yml` to deploy the Pi-hole alert rules.
6. Run `playbooks/prometheus/deploy_prometheus_exporters.yml` with the combined default inventory.
7. Verify the `pihole_exporter` job in Prometheus.

The inventory is the source of truth for which Pi-hole hosts are deployed and scraped.
