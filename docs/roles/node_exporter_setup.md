# 🛠️ Role: `node_exporter_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs Prometheus Node Exporter

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `node_exporter_setup_version` | `1.9.1` |  |
| `node_exporter_setup_home` | `"/opt/node_exporter"` |  |
| `node_exporter_setup_mode` | `"0755"` |  |
| `node_exporter_setup_user` | `"prometheus"` |  |
| `node_exporter_setup_group` | `"prometheus"` |  |
| `node_exporter_port` | `9100` |  |
| `node_exporter_setup_listen_address` | `"0.0.0.0:{{ node_exporter_port }}"` |  |
| `node_exporter_setup_textfile_collector_dir` | `"/var/lib/node_exporter/textfile"` |  |
| `node_exporter_setup_linux_updates_script_path` | `"/usr/local/bin/check_updates.sh"` |  |
| `node_exporter_setup_linux_updates_metrics_path` | `"{{ node_exporter_setup_textfile_collector_dir }}/linux_updates.prom"` |  |
| `node_exporter_setup_linux_updates_cron_minute` | `"*/30"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Create Node Exporter system group
- Create Node Exporter system user
- Download and Extract Node Exporter
- Create symlink for Node Exporter
- Set ownership for Node Exporter directory
- Copy Node Exporter binary to /usr/local/bin
- Create Node Exporter textfile collector directory
- Install Linux updates metrics script for Ubuntu
- Seed Linux updates metrics file for Ubuntu
- Schedule Linux updates metrics cron job for Ubuntu
- Create Node Exporter systemd service
- Enable Node Exporter service
- Start Node Exporter service

## 🔔 Handlers
- reload systemd and restart node_exporter

## 🔗 Dependencies
- `global`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: node_exporter_setup
```