# 📖 Playbook: prometheus/deploy_pihole_exporter.yml

## 🛠 Purpose
Deploy the Pi-hole exporter on Pi-hole DNS hosts for Prometheus monitoring Usage: ansible-playbook -i inventory/dns/inventory.ini playbooks/prometheus/deploy_pihole_exporter.yml Then refresh Prometheus targets: ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`pihole_exporter_setup`](../roles/pihole_exporter_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/prometheus/deploy_pihole_exporter.yml
```