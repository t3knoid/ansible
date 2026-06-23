# 🛠️ Role: `nginx_prometheus_exporter_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Install and configure nginx-prometheus-exporter for local NGINX status scraping.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `nginx_prometheus_exporter_setup_version` | `"1.5.1"` |  |
| `nginx_prometheus_exporter_setup_download_base_url` | `"https://github.com/nginx/nginx-prometheus-exporter/releases/download/v"` |  |
| `nginx_prometheus_exporter_setup_platform` | `"linux_amd64"` |  |
| `nginx_prometheus_exporter_setup_installdir` | `/opt/nginx-prometheus-exporter_{{ nginx_prometheus_exporter_setup_version }}_{{ nginx_prometheus_exporter_setup_platform }}` |  |
| `nginx_prometheus_exporter_setup_home` | `"/opt/nginx-prometheus-exporter"` |  |
| `nginx_prometheus_exporter_setup_binary` | `"/usr/local/bin/nginx-prometheus-exporter"` |  |
| `nginx_prometheus_exporter_setup_mode` | `"0755"` |  |
| `nginx_prometheus_exporter_setup_service_name` | `"nginx-prometheus-exporter"` |  |
| `nginx_prometheus_exporter_setup_service_file` | `"/etc/systemd/system/nginx-prometheus-exporter.service"` |  |
| `nginx_prometheus_exporter_setup_service_mode` | `"0644"` |  |
| `nginx_prometheus_exporter_setup_user` | `"nginx-prometheus-exporter"` |  |
| `nginx_prometheus_exporter_setup_group` | `"nginx-prometheus-exporter"` |  |
| `nginx_prometheus_exporter_setup_listen_address` | `"0.0.0.0:{{ nginx_prometheus_exporter_port }}"` |  |
| `nginx_prometheus_exporter_setup_telemetry_path` | `"/metrics"` |  |
| `nginx_prometheus_exporter_setup_scrape_uri` | `"http://127.0.0.1:9114/stub_status"` |  |
| `nginx_prometheus_exporter_setup_nginx_status_site_name` | `"nginx-prometheus-exporter-status"` |  |
| `nginx_prometheus_exporter_setup_nginx_status_listen_address` | `"127.0.0.1:9114"` |  |
| `nginx_prometheus_exporter_setup_nginx_status_path` | `"/stub_status"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Create nginx-prometheus-exporter group
- Create nginx-prometheus-exporter user
- Create destination directory
- Download and extract nginx-prometheus-exporter
- Create symlink for nginx-prometheus-exporter
- Set ownership for nginx-prometheus-exporter directory
- Copy nginx-prometheus-exporter binary to /usr/local/bin
- Configure local nginx status site
- Enable local nginx status site
- Validate nginx configuration
- Create nginx-prometheus-exporter systemd service file
- Enable and start nginx-prometheus-exporter service

## 🔔 Handlers
- Reload systemd daemon
- Restart nginx-prometheus-exporter service

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: nginx_prometheus_exporter_setup
```