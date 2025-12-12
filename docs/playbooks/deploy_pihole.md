# 📖 Playbook: dns/deploy_pihole.yml

## 🛠 Purpose
Deploy Pi-hole DNS server https://docs.pi-hole.net/main/basic-install/#alternative-1-clone-our-repository-and-run

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`pihole`](../roles/pihole/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/dns/deploy_pihole.yml
```