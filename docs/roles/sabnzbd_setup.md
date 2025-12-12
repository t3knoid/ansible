# 🛠️ Role: `sabnzbd_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures a Sabnzbd Docker container. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/sabnzbd).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `sabnzbd_setup_version` | `4.5.3` |  |
| `sabnzbd_setup_config_dir` | `"/config"` |  |
| `sabnzbd_setup_port` | `8080` |  |
| `sabnzbd_setup_mount_point` | `/nfs/backups` |  |
| `sabnzbd_setup_backup_prefix` | `"sabnzbd_"` |  |
| `sabnzbd_setup_backup_filename` | `"{{ sabnzbd_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `sabnzbd_setup_backups_dir` | `"{{ sabnzbd_setup_config_dir }}/sabnzbd"` |  |
| `sabnzbd_setup_backup_path` | `"{{ sabnzbd_setup_backups_dir }}/{{ sabnzbd_setup_backup_filename }}"` |  |
| `sabnzbd_setup_download_dir` | `/incomplete-downloads` | sabnzbd_setup_nzb_key: see vault |
| `sabnzbd_setup_complete_dir` | `/downloads` |  |
| `sabnzbd_setup_local_network_ranges` | `` |  |
| `sabnzbd_setup_servers` | `` |  |
| `- name` | `news.easynews.com` |  |
| `displayname` | `news.easynews.com` |  |
| `host` | `news.easynews.com` |  |
| `port` | `563` |  |
| `timeout` | `60` |  |
| `username` | `"{{ sabnzbd_setup_easynews_login }}"` |  |
| `password` | `"{{ sabnzbd_setup_easynews_password }}"` |  |
| `connections` | `60` |  |
| `ssl` | `1` |  |
| `ssl_verify` | `3` |  |
| `ssl_ciphers` | `""` |  |
| `enable` | `1` |  |
| `required` | `0` |  |
| `optional` | `0` |  |
| `retention` | `0` |  |
| `expire_date` | `""` |  |
| `quota` | `""` |  |
| `usage_at_start` | `0` |  |
| `priority` | `0` |  |
| `notes` | `""` |  |
| `- name` | `news.newsdemon.com` |  |
| `displayname` | `news.newsdemon.com` |  |
| `host` | `news.newsdemon.com` |  |
| `port` | `563` |  |
| `timeout` | `60` |  |
| `username` | `"{{ sabnzbd_setup_newsdemon_login }}"` |  |
| `password` | `"{{ sabnzbd_setup_newsdemon_password }}"` |  |
| `connections` | `50` |  |
| `ssl` | `1` |  |
| `ssl_verify` | `3` |  |
| `ssl_ciphers` | `""` |  |
| `enable` | `1` |  |
| `required` | `0` |  |
| `optional` | `0` |  |
| `retention` | `0` |  |
| `expire_date` | `""` |  |
| `quota` | `""` |  |
| `usage_at_start` | `0` |  |
| `priority` | `0` |  |
| `notes` | `""` |  |

## 📦 Vars
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `sabnzbd_setup_external_internet_access` | `` |  |
| `no access` | `0` |  |
| `add nzb files` | `1` |  |
| `api` | `2` |  |
| `full api` | `3` |  |
| `full web interface with external login` | `4` |  |
| `full web interface no internal login` | `5` |  |

## 📑 Tasks
- Stop Docker Container
- Create config folder
- Verify config folder exists
- Fail if config folder does not exists
- Create network backups folder
- Copy sabnzbd.ini to target machine
- Copy docker-compose.yml to target machine
- Make sure docker service account has access to config dir
- Prune unused Docker images
- Remove all images
- Pull latest image
- Run Docker Container

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
- `global`
- `users`
- `autofs`
- `docker_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: sabnzbd_setup
```