# 🛠️ Role: `prometheus_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures a Prometheus monitoring system on Debian/Ubuntu.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `prometheus_setup_version` | `3.6.0` |  |
| `prometheus_setup_home` | `"/opt/prometheus"` |  |
| `prometheus_setup_data_dir` | `"/data/prometheus"` |  |
| `prometheus_setup_user` | `"{{ users_list[0].username }}"` |  |
| `prometheus_setup_group` | `"{{ users_list[0].username }}"` |  |
| `prometheus_setup_service_file` | `"/etc/systemd/system/prometheus.service"` |  |
| `prometheus_setup_binary` | `"/usr/local/bin/prometheus"` |  |
| `prometheus_setup_mode` | `"0755"` |  |
| `prometheus_setup_config_mode` | `"0644"` |  |
| `prometheus_setup_service_mode` | `"0644"` |  |
| `prometheus_setup_data_mode` | `"0755"` |  |
| `prometheus_setup_listen_address` | `"0.0.0.0:9090"` |  |
| `prometheus_setup_config_file` | `"{{ prometheus_setup_data_dir }}/etc/prometheus.yml"` |  |
| `prometheus_setup_rules_file` | `"{{ prometheus_setup_data_dir }}/etc/prometheus.rules.yml"` |  |
| `prometheus_setup_tsdb_dir` | `"{{ prometheus_setup_data_dir }}/data"` |  |
| `prometheus_setup_snapshots_dir` | `"{{ prometheus_setup_tsdb_dir }}/snapshots"` |  |
| `prometheus_setup_console_templates` | `"{{ prometheus_setup_data_dir }}/consoles"` |  |
| `prometheus_setup_console_libraries` | `"{{ prometheus_setup_data_dir }}/console_libraries"` |  |
| `prometheus_setup_extra_args` | `"--web.enable-lifecycle --web.enable-admin-api"` |  |
| `prometheus_setup_skip_head` | `false` |  |
| `prometheus_setup_backup_retention_count` | `3` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Download and Extract Prometheus
- Create symlink for Prometheus
- Set ownership for Prometheus directory
- Copy Prometheus binary to /usr/local/bin
- Create Prometheus data directory
- Create Prometheus TSDB directory
- Create Prometheus etc directory
- Create Prometheus consoles directory
- Create Prometheus console_libraries directory
- Copy Prometheus configuration file
- Copy Prometheus rule file
- Create a Prometheus backup directory on /nfs/backups/
- Bind mount NAS share to Prometheus data directory
- Create Prometheus systemd service file
- Enable and start Prometheus service

## 🔔 Handlers
- Reload systemd daemon
- Restart Prometheus service
- Reload Prometheus configuration
- Validate Prometheus rules with promtool

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: prometheus_setup
```