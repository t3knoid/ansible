# 📖 Playbook: tautulli/deploy_tautulli.yml

## 🛠 Purpose
Deploys Tautulli media tracking service with necessary configurations and NFS mounts.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`users`](../roles/users/README.md)
- [`docker_setup`](../roles/docker_setup/README.md)
- [`tautulli_setup`](../roles/tautulli_setup/README.md)
- [`autofs`](../roles/autofs/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/tautulli/deploy_tautulli.yml
```