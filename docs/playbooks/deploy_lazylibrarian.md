# 📖 Playbook: services/deploy_lazylibrarian.yml

## 🛠 Purpose
Installs Lazy Librarian application.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`users`](../roles/users/README.md)
- [`autofs`](../roles/autofs/README.md)
- [`docker_setup`](../roles/docker_setup/README.md)
- [`lazylibrarian_setup`](../roles/lazylibrarian_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/services/deploy_lazylibrarian.yml
```