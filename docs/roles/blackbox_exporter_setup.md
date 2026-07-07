# 🛠️ Role: `blackbox_exporter_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Install and configure Prometheus Blackbox Exporter for probing web services.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (bionic, focal, jammy, noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `blackbox_exporter_setup_version` | `"0.25.0"` |  |
| `blackbox_exporter_setup_platform` | `"linux-amd64"` |  |
| `blackbox_exporter_setup_download_url` | `"https://github.com/prometheus/blackbox_exporter/releases/download/v{{ blackbox_exporter_setup_version }}/blackbox_exporter-{{ blackbox_exporter_setup_version }}.{{ blackbox_exporter_setup_platform }}.tar.gz"` |  |
| `blackbox_exporter_setup_install_dir` | `"/opt/blackbox_exporter-{{ blackbox_exporter_setup_version }}.{{ blackbox_exporter_setup_platform }}"` |  |
| `blackbox_exporter_setup_home` | `"/opt/blackbox_exporter"` |  |
| `blackbox_exporter_setup_binary` | `"/usr/local/bin/blackbox_exporter"` |  |
| `blackbox_exporter_setup_mode` | `"0755"` |  |
| `blackbox_exporter_port` | `9115` |  |
| `blackbox_exporter_setup_listen_address` | `"0.0.0.0:{{ blackbox_exporter_port }}"` |  |
| `blackbox_exporter_setup_user` | `"blackbox-exporter"` |  |
| `blackbox_exporter_setup_group` | `"blackbox-exporter"` |  |
| `blackbox_exporter_setup_service_name` | `"blackbox_exporter"` |  |
| `blackbox_exporter_setup_service_file` | `"/etc/systemd/system/blackbox_exporter.service"` |  |
| `blackbox_exporter_setup_service_mode` | `"0644"` |  |
| `blackbox_exporter_setup_config_dir` | `"/etc/blackbox_exporter"` |  |
| `blackbox_exporter_setup_config_file` | `"{{ blackbox_exporter_setup_config_dir }}/blackbox.yml"` |  |
| `blackbox_exporter_setup_log_level` | `"info"` |  |
| `blackbox_exporter_setup_modules` | `` |  |
| `http_2xx` | `` |  |
| `prober` | `http` |  |
| `timeout` | `5s` |  |
| `http` | `` |  |
| `method` | `GET` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `https_2xx` | `` |  |
| `prober` | `http` |  |
| `timeout` | `5s` |  |
| `http` | `` |  |
| `method` | `GET` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `fail_if_ssl` | `false` |  |
| `tcp_connect` | `` |  |
| `prober` | `tcp` |  |
| `timeout` | `5s` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Create Blackbox Exporter group
- Create Blackbox Exporter user
- Download and extract Blackbox Exporter
- Create symlink for Blackbox Exporter
- Set ownership for Blackbox Exporter directory
- Copy Blackbox Exporter binary to /usr/local/bin
- Create Blackbox Exporter configuration directory
- Render Blackbox Exporter configuration
- Create Blackbox Exporter systemd service file
- Enable and start Blackbox Exporter service

## 🔔 Handlers
- Reload systemd daemon
- Restart blackbox_exporter service

## 🔗 Dependencies
- `global`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: blackbox_exporter_setup
```