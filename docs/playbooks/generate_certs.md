# 📖 Playbook: certs/generate_certs.yml

## 🛠 Purpose
Generate Let’s Encrypt certbot certificates on the cert staging host

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`certs`](../roles/certs/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/certs/generate_certs.yml
```