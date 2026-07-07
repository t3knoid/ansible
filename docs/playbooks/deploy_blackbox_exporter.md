# 📖 Playbook: prometheus/deploy_blackbox_exporter.yml

## 🛠 Purpose
Deploy Prometheus Blackbox Exporter on a selected host group for remote service probing

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`blackbox_exporter_setup`](../roles/blackbox_exporter_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_blackbox_exporter.yml
```