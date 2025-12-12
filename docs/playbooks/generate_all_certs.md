# 📖 Playbook: certs/generate_all_certs.yml

## 🛠 Purpose
Generate Let’s Encrypt certbot certificates for every domain

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`certs`](../roles/certs/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/certs/generate_all_certs.yml
```