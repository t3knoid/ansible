# 📖 Playbook: plex/deploy_plex.yml

## 🛠 Purpose
Install and configure Plex Media Server on plex hosts

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`ad`](../roles/ad/README.md)
- [`autofs`](../roles/autofs/README.md)
- [`python3`](../roles/python3/README.md)
- [`users`](../roles/users/README.md)
- [`ansible_node`](../roles/ansible_node/README.md)
- [`plex_setup`](../roles/plex_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/plex/deploy_plex.yml
```