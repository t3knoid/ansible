# 📖 Playbook: template/create_template.yml

## 🛠 Purpose
Creates a VM template using cloud-init on the specified Proxmox node.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`cloudinit`](../roles/cloudinit/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/template/create_template.yml
```