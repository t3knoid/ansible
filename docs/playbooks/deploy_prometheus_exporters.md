# 📖 Playbook: prometheus/deploy_prometheus_exporters.yml

## 🛠 Purpose
Refresh Prometheus exporter scrape targets Usage: ansible-playbook -i inventory/rproxy/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml Note: This merges exporter targets from the current inventory into the existing Prometheus config. Existing node_exporter and nginx_exporter targets are preserved unless replaced by the same host.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml
```