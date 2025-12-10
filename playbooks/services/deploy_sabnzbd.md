# 📖 Playbook: services/deploy_sabnzbd.yml

## 🛠 Purpose
Installs Sabnzbd application.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`users`](../roles/users/README.md)
- [`autofs`](../roles/autofs/README.md)
- [`docker_setup`](../roles/docker_setup/README.md)
- [`sabnzbd_setup`](../roles/sabnzbd_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/services/deploy_sabnzbd.yml
```