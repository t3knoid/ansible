# 📖 Playbook: vms/decommission_vm.yml

## 🛠 Purpose
Preview VM decommissioning; destructive stages are not implemented. Usage: ansible-playbook playbooks/vms/decommission_vm.yml -e '{"decommission_hosts":["retired-0"]}'

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/vms/decommission_vm.yml
```