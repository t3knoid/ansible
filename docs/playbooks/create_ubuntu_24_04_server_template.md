# 📖 Playbook: template/create_ubuntu_24_04_server_template.yml

## 🛠 Purpose
Creates an Ubuntu 24.04 Server VM template using cloud-init on the specified Proxmox node.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`cloudinit`](../roles/cloudinit/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/template/create_ubuntu_24_04_server_template.yml
```