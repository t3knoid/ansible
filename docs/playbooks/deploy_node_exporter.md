# 📖 Playbook: prometheus/deploy_node_exporter.yml

## 🛠 Purpose
Deploy Node Exporter on node_exporter hosts Note: This playbook only installs or updates node_exporter on the selected inventory's node_exporter hosts. It does not update Prometheus scrape targets.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`node_exporter_setup`](../roles/node_exporter_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_node_exporter.yml
```