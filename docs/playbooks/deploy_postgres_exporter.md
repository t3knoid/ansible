# 📖 Playbook: prometheus/deploy_postgres_exporter.yml

## 🛠 Purpose
Deploy postgres_exporter on a selected host group for PostgreSQL monitoring

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`postgres_exporter_setup`](../roles/postgres_exporter_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_postgres_exporter.yml
```