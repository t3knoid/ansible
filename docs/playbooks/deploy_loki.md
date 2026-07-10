# 📖 Playbook: loki/deploy_loki.yml

## 🛠 Purpose
Deploy Grafana Loki on loki hosts Usage: ansible-playbook -i inventory/<inventory>/inventory.ini playbooks/loki/deploy_loki.yml

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`loki_setup`](../roles/loki_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/loki/deploy_loki.yml
```