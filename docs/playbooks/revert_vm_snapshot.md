# 📖 Playbook: vms/revert_vm_snapshot.yml

## 🛠 Purpose
Reverts virtual machines to a specified snapshot and starts them. Usage: ansible-playbook -k -i inventory/<name>/inventory.ini playbooks/vms/revert_vm_snapshot.yml -k (SSH password) is required because the reverted guest may not accept the controller's SSH key.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/vms/revert_vm_snapshot.yml
```