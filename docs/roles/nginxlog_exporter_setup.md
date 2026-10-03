# 🛠️ Role: `nginxlog_exporter_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Export per-domain reverse proxy request metrics from privacy-preserving nginx access logs.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `nginxlog_exporter_setup_version` | `"1.11.0"` |  |
| `nginxlog_exporter_setup_platform` | `linux_amd64` |  |
| `nginxlog_exporter_setup_download_base_url` | `https://github.com/martin-helmich/prometheus-nginxlog-exporter/releases/download` |  |
| `nginxlog_exporter_setup_archive` | `"prometheus-nginxlog-exporter_{{ nginxlog_exporter_setup_version }}_{{ nginxlog_exporter_setup_platform }}.tar.gz"` |  |
| `nginxlog_exporter_setup_port` | `4040` |  |
| `nginxlog_exporter_setup_listen_address` | `"{{ global_ip_addresses[inventory_hostname] }}"` |  |
| `nginxlog_exporter_setup_install_dir` | `"/opt/prometheus-nginxlog-exporter_{{ nginxlog_exporter_setup_version }}"` |  |
| `nginxlog_exporter_setup_binary` | `"{{ nginxlog_exporter_setup_install_dir }}/prometheus-nginxlog-exporter"` |  |
| `nginxlog_exporter_setup_user` | `nginxlog-exporter` |  |
| `nginxlog_exporter_setup_config_file` | `/etc/prometheus-nginxlog-exporter.hcl` |  |
| `nginxlog_exporter_setup_log_file` | `"{{ nginx_setup_homedir }}/log/traffic.log"` |  |
| `nginxlog_exporter_setup_nginx_config` | `/etc/nginx/conf.d/nginxlog-exporter.conf` |  |
| `nginxlog_exporter_setup_log_format` | `'$server_name "$request" $status $body_bytes_sent $request_time'` |  |
| `nginxlog_exporter_setup_histogram_buckets` | `` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Create nginxlog exporter user
- Create nginxlog exporter install directory
- Download and extract nginxlog exporter
- Ensure traffic log exists with collector read access
- Configure nginxlog exporter
- Configure privacy-preserving nginx traffic logging
- Validate nginx traffic logging configuration
- Configure traffic log rotation
- Configure nginxlog exporter service
- Enable and start nginxlog exporter

## 🔔 Handlers
- Restart nginxlog exporter
- Reload nginx for traffic logging

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: nginxlog_exporter_setup
```