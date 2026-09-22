# 📖 Playbook: proxmox/deploy_pve_monitoring.yml

## 🛠 Purpose
Deploy Node Exporter and the Proxmox VE Exporter on Proxmox hosts for monitoring Usage: ansible-playbook -i inventory/pve/inventory.ini playbooks/proxmox/deploy_pve_monitoring.yml

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`node_exporter_setup`](../roles/node_exporter_setup/README.md)
- [`pve_exporter_setup`](../roles/pve_exporter_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/proxmox/deploy_pve_monitoring.yml
```