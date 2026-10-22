# 📖 Playbook: grafana/deploy_grafana_dashboards.yml

## 🛠 Purpose
Update provisioned dashboards on an existing Grafana installation without Azure or Entra setup. Usage: ansible-playbook -i inventory/grafana/inventory.ini playbooks/grafana/deploy_grafana_dashboards.yml

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/grafana/deploy_grafana_dashboards.yml
```