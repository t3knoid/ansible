# 🛠️ Role: `plex_exporter_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Deploy Prometheus Plex Exporter as a Docker service.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `plex_exporter_setup_version` | `"main"` |  |
| `plex_exporter_setup_image` | `"ghcr.io/jsclayton/prometheus-plex-exporter:{{ plex_exporter_setup_version }}"` |  |
| `plex_exporter_setup_container_name` | `"prometheus-plex-exporter"` |  |
| `plex_exporter_setup_port` | `9000` |  |
| `plex_exporter_setup_server_url` | `""` |  |
| `plex_exporter_setup_token` | `""` |  |
| `plex_exporter_setup_config_dir` | `"/opt/plex-exporter"` |  |
| `plex_exporter_setup_backups_dir` | `"/nfs/backups/plex-exporter"` |  |
| `plex_exporter_setup_secret_dir` | `"/etc/plex-exporter"` |  |
| `plex_exporter_setup_env_file` | `"{{ plex_exporter_setup_secret_dir }}/exporter.env"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Require Plex exporter connection settings
- Create Plex exporter secret directory
- Install Plex exporter token environment file
- Deploy Plex exporter container

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: plex_exporter_setup
```