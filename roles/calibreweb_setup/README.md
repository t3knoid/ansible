# 🛠️ Role: `calibreweb_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs and configures Calibre-Web, a web-based eBook management application. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/calibre-web).


## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `calibreweb_setup_config_dir` | `"/config/calibreweb"` |  |
| `calibreweb_setup_version` | `0.6.25` |  |
| `calibreweb_setup_docker_image_name` | `"calibre-web:{{ calibreweb_setup_version }}"` |  |
| `calibreweb_setup_mount_point` | `/nfs/backups` |  |
| `calibreweb_setup_backup_prefix` | `"calibreweb_"` |  |
| `calibreweb_setup_backup_filename` | `"{{ calibreweb_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `calibreweb_setup_backups_dir` | `"{{ calibreweb_setup_mount_point }}/calibre"` |  |
| `calibreweb_setup_backup_path` | `"{{ calibreweb_setup_backups_dir }}/{{ calibreweb_setup_backup_filename }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Stop Docker Container
- Create config folder
- Verify config folder exists
- Fail if config folder does not exists
- Create network calibreweb backup folder
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
    - role: calibreweb_setup
```