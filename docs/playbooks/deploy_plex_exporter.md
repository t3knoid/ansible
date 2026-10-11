# 📖 Playbook: plex/deploy_plex_exporter.yml

## 🛠 Purpose
Deploy Prometheus Plex Exporter on plex-0.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`users`](../roles/users/README.md)
- [`autofs`](../roles/autofs/README.md)
- [`docker_setup`](../roles/docker_setup/README.md)
- [`plex_exporter_setup`](../roles/plex_exporter_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/plex/deploy_plex_exporter.yml
```