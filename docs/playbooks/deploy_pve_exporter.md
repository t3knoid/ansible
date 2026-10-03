# 📖 Playbook: prometheus/deploy_pve_exporter.yml

## 🛠 Purpose
Deploy Node Exporter and the Proxmox VE Exporter on Proxmox hosts for monitoring Usage: ansible-playbook -i inventory/pve/inventory.ini playbooks/prometheus/deploy_pve_exporter.yml

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`pve_exporter_setup`](../roles/pve_exporter_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_pve_exporter.yml
```