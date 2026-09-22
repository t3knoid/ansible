# 📖 Playbook: prometheus/deploy_prometheus_exporters.yml

## 🛠 Purpose
Refresh Prometheus exporter scrape targets Usage: ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml Note: This refreshes exporter targets from the current inventory into the Prometheus config. Requires the full combined inventory (ansible.cfg's default inventory=inventory/) so every service's exporter group (node_exporter, postgres_exporter, pve_exporter, etc.) is visible. Do not scope this run with -i to a single inventory subfolder.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml
```