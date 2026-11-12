# 🛠️ Role: `pihole_exporter_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Install and configure eko/pihole-exporter for Pi-hole v6 monitoring.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `pihole_exporter_setup_version` | `"1.3.0"` |  |
| `pihole_exporter_setup_platform` | `"linux-amd64"` |  |
| `pihole_exporter_setup_download_base_url` | `"https://github.com/eko/pihole-exporter/releases/download"` |  |
| `pihole_exporter_setup_download_url` | `>-` |  |
| `pihole_exporter_setup_install_dir` | `"/opt/pihole_exporter"` |  |
| `pihole_exporter_setup_versioned_binary` | `"{{ pihole_exporter_setup_install_dir }}/pihole_exporter-{{ pihole_exporter_setup_version }}"` |  |
| `pihole_exporter_setup_binary` | `"/usr/local/bin/pihole_exporter"` |  |
| `pihole_exporter_setup_user` | `"pihole-exporter"` |  |
| `pihole_exporter_setup_group` | `"pihole-exporter"` |  |
| `pihole_exporter_setup_config_dir` | `"/etc/pihole_exporter"` |  |
| `pihole_exporter_setup_password_file` | `"{{ pihole_exporter_setup_config_dir }}/password"` |  |
| `pihole_exporter_setup_service_name` | `"pihole_exporter"` |  |
| `pihole_exporter_setup_service_file` | `"/etc/systemd/system/pihole_exporter.service"` |  |
| `pihole_exporter_setup_service_mode` | `"0644"` |  |
| `pihole_exporter_setup_port` | `9617` |  |
| `pihole_exporter_setup_bind_address` | `"0.0.0.0"` |  |
| `pihole_exporter_setup_timeout` | `"5s"` |  |
| `pihole_exporter_setup_log_level` | `"info"` |  |
| `pihole_exporter_setup_pihole_protocol` | `"http"` | reads that host's local API, the same way pve_exporter reads its local Proxmox API. |
| `pihole_exporter_setup_pihole_hostname` | `"127.0.0.1"` |  |
| `pihole_exporter_setup_pihole_port` | `80` |  |
| `pihole_exporter_setup_password` | `"{{ pihole_password | default('') }}"` | which deploy_pihole_exporter.yml loads. Override via vault to use an app password. |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Require a Pi-hole password for pihole_exporter
- Create pihole_exporter group
- Create pihole_exporter user
- Create pihole_exporter install directory
- Download pihole_exporter binary
- Link pihole_exporter binary into /usr/local/bin
- Create pihole_exporter configuration directory
- Write the Pi-hole password file
- Create pihole_exporter systemd service file
- Enable and start pihole_exporter service

## 🔔 Handlers
- Reload systemd daemon
- Restart pihole_exporter service

## 🔗 Dependencies
- `global`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: pihole_exporter_setup
```