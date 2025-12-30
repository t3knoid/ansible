# 📖 Playbook: dns/deploy_unbound.yml

## 🛠 Purpose
Deploy Unbound DNS resolver Based on Pi-hole documentation: https://docs.pi-hole.net/guides/dns/unbound/

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`unbound`](../roles/unbound/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/dns/deploy_unbound.yml
```