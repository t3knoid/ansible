# 🛠️ Role: `ombi_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Ombi Setup installs and configures an Ombi Docker container. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/ombi)

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `ombi_setup_version` | `4.47.1` |  |
| `ombi_setup_config_dir` | `"/config"` |  |
| `ombi_setup_port` | `3579` |  |
| `ombi_setup_pg_port` | `5432` |  |
| `ombi_setup_pg_host` | `"{{ global_ip_addresses[groups['pgdb'][0]] }}"` |  |
| `ombi_setup_mount_point` | `/nfs/backups` | ombi_setup_db_password: |
| `ombi_setup_backup_prefix` | `"ombi_"` |  |
| `ombi_setup_backup_filename` | `"{{ ombi_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `ombi_setup_backup_path` | `"{{ ombi_setup_mount_point }}/{{ ombi_setup_backup_filename }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Create config folder
- Verify config folder exists
- Fail if config folder does not exists
- Copy database.json to target machine
- Copy docker-compose.yml to target machine
- Make sure docker service account has access to config dir
- Stop Docker Container
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
    - role: ombi_setup
```