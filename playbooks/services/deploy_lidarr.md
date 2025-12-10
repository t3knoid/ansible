# 📖 Playbook: services/deploy_lidarr.yml

## 🛠 Purpose
Installs Lidarr application.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`users`](../roles/users/README.md)
- [`autofs`](../roles/autofs/README.md)
- [`docker_setup`](../roles/docker_setup/README.md)
- [`lidarr_setup`](../roles/lidarr_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/services/deploy_lidarr.yml
```