# 📖 Playbook: prometheus/deploy_prometheus_exporters.yml

## 🛠 Purpose
Refresh Prometheus exporter scrape targets Usage: ansible-playbook -i inventory/rproxy/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml Note: This merges exporter targets from the current inventory into the existing Prometheus config. Existing node_exporter, nginx_exporter, and blackbox targets are preserved unless replaced by the same target key.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml
```