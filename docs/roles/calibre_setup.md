# 🛠️ Role: `calibre_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs and configures Calibre eBook management software. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/calibre).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `calibre_setup_config_dir` | `"/config/calibre"` |  |
| `calibre_setup_version` | `8.13.0-ls368` |  |
| `calibre_setup_docker_image_name` | `"calibre:{{ calibre_setup_version }}"` |  |
| `calibre_setup_mount_point` | `/nfs/backups` |  |
| `calibre_setup_backup_prefix` | `"calibre_"` |  |
| `calibre_setup_backup_filename` | `"{{ calibre_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `calibre_setup_backups_dir` | `"{{ calibre_setup_mount_point }}/calibre"` |  |
| `calibre_setup_backup_path` | `"{{ calibre_setup_backups_dir }}/{{ calibre_setup_backup_filename }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Stop Docker Container
- Create config folder
- Verify config folder exists
- Fail if config folder does not exists
- Create network calibre backup folder
- Copy docker-compose.yml to target machine
- Make sure docker service account has access to config dir
- Stop Docker Container
- Prune unused Docker images
- Run Docker Container

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: calibre_setup
```