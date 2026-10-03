# 📖 Playbook: prometheus/deploy_nginxlog_exporter.yml

## 🛠 Purpose
Collect per-domain HTTP traffic on the main reverse proxy.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`nginx_setup`](../roles/nginx_setup/README.md)
- [`nginxlog_exporter_setup`](../roles/nginxlog_exporter_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_nginxlog_exporter.yml
```