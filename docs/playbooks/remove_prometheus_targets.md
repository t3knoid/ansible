# 📖 Playbook: prometheus/remove_prometheus_targets.yml

## 🛠 Purpose
Remove explicitly selected Prometheus static targets with validation and backup. Usage: ansible-playbook playbooks/prometheus/remove_prometheus_targets.yml -e '{"prometheus_setup_remove_instances":["retired-0"]}'

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/remove_prometheus_targets.yml
```