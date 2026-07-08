# 🛠️ Role: `postgres_exporter_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Install and configure postgres_exporter for PostgreSQL monitoring.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (bionic, focal, jammy, noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `postgres_exporter_setup_version` | `"0.17.1"` |  |
| `postgres_exporter_setup_platform` | `"linux-amd64"` |  |
| `postgres_exporter_setup_download_url` | `"https://github.com/prometheus-community/postgres_exporter/releases/download/v{{ postgres_exporter_setup_version }}/postgres_exporter-{{ postgres_exporter_setup_version }}.{{ postgres_exporter_setup_platform }}.tar.gz"` |  |
| `postgres_exporter_setup_install_dir` | `"/opt/postgres_exporter-{{ postgres_exporter_setup_version }}.{{ postgres_exporter_setup_platform }}"` |  |
| `postgres_exporter_setup_home` | `"/opt/postgres_exporter"` |  |
| `postgres_exporter_setup_binary` | `"/usr/local/bin/postgres_exporter"` |  |
| `postgres_exporter_setup_mode` | `"0755"` |  |
| `postgres_exporter_port` | `9187` |  |
| `postgres_exporter_setup_listen_address` | `"0.0.0.0:{{ postgres_exporter_port }}"` |  |
| `postgres_exporter_setup_telemetry_path` | `"/metrics"` |  |
| `postgres_exporter_setup_user` | `"postgres-exporter"` |  |
| `postgres_exporter_setup_group` | `"postgres-exporter"` |  |
| `postgres_exporter_setup_service_name` | `"postgres_exporter"` |  |
| `postgres_exporter_setup_service_file` | `"/etc/systemd/system/postgres_exporter.service"` |  |
| `postgres_exporter_setup_service_mode` | `"0644"` |  |
| `postgres_exporter_setup_config_dir` | `"/etc/postgres_exporter"` |  |
| `postgres_exporter_setup_env_file` | `"{{ postgres_exporter_setup_config_dir }}/postgres_exporter.env"` |  |
| `postgres_exporter_setup_data_source_name` | `""` |  |
| `postgres_exporter_setup_manage_db_user` | `true` |  |
| `postgres_exporter_setup_admin_username` | `"postgres"` |  |
| `postgres_exporter_setup_admin_password` | `""` |  |
| `postgres_exporter_setup_admin_database` | `"postgres"` |  |
| `postgres_exporter_setup_login_unix_socket` | `"/var/run/postgresql"` |  |
| `postgres_exporter_setup_db_username` | `"postgres_exporter"` |  |
| `postgres_exporter_setup_db_password` | `""` |  |
| `postgres_exporter_setup_db_name` | `"postgres"` |  |
| `postgres_exporter_setup_db_host` | `"127.0.0.1"` |  |
| `postgres_exporter_setup_db_port` | `5432` |  |
| `postgres_exporter_setup_sslmode` | `"disable"` |  |
| `postgres_exporter_setup_db_role_flags` | `"LOGIN"` |  |
| `postgres_exporter_setup_db_grant_monitor_role` | `true` |  |
| `postgres_exporter_setup_extra_args` | `[]` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Require postgres_exporter database password or explicit data source name
- Build effective postgres_exporter data source name
- Create postgres_exporter group
- Create postgres_exporter user
- Ensure postgres_exporter database role exists
- Grant pg_monitor role to postgres_exporter database role
- Download and extract postgres_exporter
- Create symlink for postgres_exporter
- Set ownership for postgres_exporter directory
- Copy postgres_exporter binary to /usr/local/bin
- Create postgres_exporter configuration directory
- Render postgres_exporter environment file
- Create postgres_exporter systemd service file
- Enable and start postgres_exporter service

## 🔔 Handlers
- Reload systemd daemon
- Restart postgres_exporter service

## 🔗 Dependencies
- `global`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: postgres_exporter_setup
```