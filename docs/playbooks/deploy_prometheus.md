# 📖 Playbook: prometheus/deploy_prometheus.yml

## 🛠 Purpose
Deploy Prometheus monitoring system

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`users`](../roles/users/README.md)
- [`autofs`](../roles/autofs/README.md)
- [`prometheus_setup`](../roles/prometheus_setup/README.md)
- [`alertmanager_setup`](../roles/alertmanager_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_prometheus.yml
```