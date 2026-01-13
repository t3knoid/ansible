# 🛠️ Role: `lidarr_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures Lidarr on Debian/Ubuntu systems. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/lidarr).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `lidarr_setup_version` | `2.13.3.4711` |  |
| `lidarr_setup_config_dir` | `"/config"` |  |
| `lidarr_setup_port` | `8686` |  |
| `lidarr_setup_ssl_port` | `6868` |  |
| `lidarr_setup_debug_level` | `debug` |  |
| `lidarr_setup_pg_port` | `5432` |  |
| `lidarr_setup_pg_host` | `"{{ global_ip_addresses[groups['pgdb'][0]] }}"` |  |
| `lidarr_setup_mount_point` | `/nfs/backups` | lidarr_setup_db_password |
| `lidarr_setup_backup_prefix` | `"lidarr_"` |  |
| `lidarr_setup_backup_filename` | `"{{ lidarr_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `lidarr_setup_backups_dir` | `"{{ lidarr_setup_mount_point }}/lidarr"` |  |
| `lidarr_setup_backup_path` | `"{{ lidarr_setup_backups_dir }}/{{ lidarr_setup_backup_filename }}"` |  |
| `lidarr_setup_authentication_method` | `"External"  # Options: Basic, Forms, External` |  |
| `lidarr_setup_authentication_required` | `"DisabledForLocalAddresses"  # Options: Enabled, DisabledForLocalAddresses` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Stop Docker Container
- Create config folder
- Verify config folder exists
- Fail if config folder does not exists
- Create network lidarr backup folder
- Copy config.yml to target machine
- Copy docker-compose.yml to target machine
- Make sure docker service account has access to config dir
- Prune unused Docker images
- Remove all images
- Pull latest image
- Run Docker Container

## 🔔 Handlers
- Restart PostgreSQL

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: lidarr_setup
```