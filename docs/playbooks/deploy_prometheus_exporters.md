# 📖 Playbook: prometheus/deploy_prometheus_exporters.yml

## 🛠 Purpose
Refresh Prometheus exporter scrape targets Usage: ansible-playbook -i inventory/rproxy/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml Note: This refreshes exporter targets from the current inventory into the Prometheus config. Node exporter membership comes from the inventory's node_exporter group.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml
```