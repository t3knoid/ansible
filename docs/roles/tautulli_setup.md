# 🛠️ Role: `tautulli_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures an Tautulli Docker container. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/tautulli).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `tautulli_setup_version` | `2.16.0` |  |
| `tautulli_setup_config_dir` | `"/config"` |  |
| `tautulli_setup_port` | `8181` |  |
| `tautulli_setup_host` | `"http://localhost:8181"` | tautulli_apikey |
| `tautulli_setup_backups_dir` | `"/nfs/backups/tautulli"` |  |
| `tautulli_setup_backup_dir_native` | `"{{ tautulli_setup_config_dir }}/backups"` |  |
| `tautulli_setup_restore_path` | `""` |  |
| `tautulli_setup_check_update` | `true` |  |
| `tautulli_setup_update_check_script_path` | `/usr/local/bin/check_tautulli_update.sh` |  |
| `tautulli_setup_update_metrics_path` | `"{{ node_exporter_setup_textfile_collector_dir | default('/var/lib/node_exporter/textfile') }}/tautulli_update.prom"` |  |
| `tautulli_setup_update_check_minute` | `"*/30"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Deploy Tautulli Docker Service
- Check Tautulli for available updates via Prometheus metrics

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: tautulli_setup
```