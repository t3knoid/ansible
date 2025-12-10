# 📖 Playbook: services/deploy_radarr.yml

## 🛠 Purpose
Installs Radarr application.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`users`](../roles/users/README.md)
- [`autofs`](../roles/autofs/README.md)
- [`docker_setup`](../roles/docker_setup/README.md)
- [`radarr_setup`](../roles/radarr_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/services/deploy_radarr.yml
```