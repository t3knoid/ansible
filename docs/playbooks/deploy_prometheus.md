# 📖 Playbook: prometheus/deploy_prometheus.yml

## 🛠 Purpose
Deploy Prometheus monitoring system Usage: ansible-playbook -i inventory/prometheus/inventory.ini playbooks/prometheus/deploy_prometheus.yml Use playbooks/prometheus/deploy_prometheus_exporters.yml to refresh exporter scrape targets.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`users`](../roles/users/README.md)
- [`autofs`](../roles/autofs/README.md)
- [`prometheus_setup`](../roles/prometheus_setup/README.md)
- [`alertmanager_setup`](../roles/alertmanager_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_prometheus.yml
```