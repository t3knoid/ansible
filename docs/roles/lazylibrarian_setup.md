# 🛠️ Role: `lazylibrarian_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures LazyLibrarian on Debian/Ubuntu systems. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/lazylibrarian).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `lazylibrarian_setup_config_dir` | `"/config/lazylibrarian"` |  |
| `lazylibrarian_setup_config_ini` | `"{{ lazylibrarian_setup_config_dir }}/config.ini"` |  |
| `lazylibrarian_setup_version` | `0c862d0f` |  |
| `lazylibrarian_setup_mount_point` | `/nfs/backups` |  |
| `lazylibrarian_setup_backup_prefix` | `"lazy_"` |  |
| `lazylibrarian_setup_backup_filename` | `"{{ lazylibrarian_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `lazylibrarian_setup_backups_dir` | `"{{ lazylibrarian_setup_mount_point }}/lazy"` |  |
| `lazylibrarian_setup_backup_path` | `"{{ lazylibrarian_setup_backups_dir }}/{{ lazylibrarian_setup_backup_filename }}"` |  |
| `lazylibrarian_setup_ebook_dir` | `"/books"` |  |
| `lazylibrarian_setup_download_dir` | `"/downloads"` |  |
| `lazylibrarian_setup_alt_download_dir` | `"/downloads"` |  |
| `lazylibrarian_setup_user_agent` | `"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Deploy Lazylibrarian Docker Service

## 🔔 Handlers
- Restart Lazy Librarian

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: lazylibrarian_setup
```