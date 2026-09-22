# 🛠️ Role: `pve_exporter_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian](https://img.shields.io/badge/platforms-Debian-orange.svg)

## 📖 Overview
Install and configure prometheus-pve-exporter for Proxmox VE monitoring.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (bookworm)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `pve_exporter_setup_version` | `"3.10.0"` |  |
| `pve_exporter_setup_venv` | `"/opt/pve_exporter"` |  |
| `pve_exporter_setup_user` | `"pve-exporter"` |  |
| `pve_exporter_setup_group` | `"pve-exporter"` |  |
| `pve_exporter_setup_config_dir` | `"/etc/pve_exporter"` |  |
| `pve_exporter_setup_config_file` | `"{{ pve_exporter_setup_config_dir }}/pve.yml"` |  |
| `pve_exporter_setup_service_name` | `"pve_exporter"` |  |
| `pve_exporter_setup_service_file` | `"/etc/systemd/system/pve_exporter.service"` |  |
| `pve_exporter_setup_service_mode` | `"0644"` |  |
| `pve_exporter_setup_port` | `9221` |  |
| `pve_exporter_setup_listen_address` | `"0.0.0.0:{{ pve_exporter_setup_port }}"` |  |
| `pve_exporter_setup_cluster_name` | `"local"` | so the same cluster-wide API token works everywhere. |
| `pve_exporter_setup_api_user` | `"prometheus@pve"` |  |
| `pve_exporter_setup_api_token_name` | `"monitoring"` |  |
| `pve_exporter_setup_api_verify_ssl` | `false` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Require pve_exporter API token value
- Create pve_exporter group
- Create pve_exporter user
- Import venv.yml from python3 role
- Install prometheus-pve-exporter in its virtual environment
- Set ownership for pve_exporter virtual environment
- Create pve_exporter configuration directory
- Render pve_exporter configuration file
- Create pve_exporter systemd service file
- Enable and start pve_exporter service

## 🔔 Handlers
- Reload systemd daemon
- Restart pve_exporter service

## 🔗 Dependencies
- `global`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: pve_exporter_setup
```