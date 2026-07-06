# 📖 Playbook: prometheus/deploy_nginx_prometheus_exporter.yml

## 🛠 Purpose
Deploy nginx-prometheus-exporter on nginx exporter hosts Usage: ansible-playbook -i inventory/rproxy/inventory.ini playbooks/prometheus/deploy_nginx_prometheus_exporter.yml

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`nginx_setup`](../roles/nginx_setup/README.md)
- [`nginx_prometheus_exporter_setup`](../roles/nginx_prometheus_exporter_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_nginx_prometheus_exporter.yml
```