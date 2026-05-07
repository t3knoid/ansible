# 🛠️ Role: `radarr_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures a Radarr Docker container. It uses an image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/radarr).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `radarr_setup_version` | `"5.27.5.10198"` |  |
| `radarr_setup_config_dir` | `"/config"` |  |
| `radarr_setup_port` | `7878` |  |
| `radarr_setup_ssl_port` | `8787` |  |
| `radarr_setup_debug_level` | `debug` |  |
| `radarr_setup_pg_port` | `5432` |  |
| `radarr_setup_pg_host` | `"{{ global_ip_addresses[groups['pgdb'][0]] }}"` |  |
| `radarr_setup_mount_point` | `/nfs/backups` | radarr_setup_db_password |
| `radarr_setup_backup_prefix` | `"radarr_"` |  |
| `radarr_setup_backup_filename` | `"{{ radarr_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `radarr_setup_backup_dir` | `"{{ radarr_setup_mount_point }}/radarr"` |  |
| `radarr_setup_backup_path` | `"{{ radarr_setup_backup_dir }}/{{ radarr_setup_backup_filename }}"` |  |
| `radarr_setup_restore_path` | `""` |  |
| `radarr_setup_api_url` | `"http://127.0.0.1:{{ radarr_setup_port }}"` |  |
| `radarr_setup_api_validate_certs` | `false` |  |
| `radarr_setup_root_folders` | `` |  |
| `- path` | `/movies` |  |
| `radarr_setup_download_clients` | `` |  |
| `- name` | `sabnzbd.refol.us` |  |
| `implementation` | `Sabnzbd` |  |
| `enable` | `true` |  |
| `priority` | `1` |  |
| `remove_completed_downloads` | `true` |  |
| `remove_failed_downloads` | `true` |  |
| `fields` | `` |  |
| `host` | `192.168.20.153` |  |
| `port` | `8080` |  |
| `useSsl` | `false` |  |
| `username` | `frank` |  |
| `movieCategory` | `movies` |  |
| `radarr_setup_indexers` | `` |  |
| `- name` | `Nzb.su` |  |
| `implementation` | `Newznab` |  |
| `enable_rss` | `true` |  |
| `enable_automatic_search` | `true` |  |
| `enable_interactive_search` | `true` |  |
| `priority` | `25` |  |
| `fields` | `` |  |
| `baseUrl` | `https://api.nzb.su` |  |
| `apiPath` | `/api` |  |
| `apiKey` | `"{{ nzbsu_api_key }}"` |  |
| `categories` | `` |  |
| `- name` | `NZBgeek` |  |
| `implementation` | `Newznab` |  |
| `enable_rss` | `true` |  |
| `enable_automatic_search` | `true` |  |
| `enable_interactive_search` | `true` |  |
| `priority` | `25` |  |
| `fields` | `` |  |
| `baseUrl` | `https://api.nzbgeek.info` |  |
| `apiPath` | `/api` |  |
| `apiKey` | `"{{ nzbgeek_api_key }}"` |  |
| `categories` | `` |  |
| `radarr_setup_configure_api` | `>-` |  |
| `radarr_setup_authentication_method` | `"External" # Options: Basic, Forms, External` |  |
| `radarr_setup_authentication_required` | `"DisabledForLocalAddresses" # Options: Enabled, DisabledForLocalAddresses` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Deploy Radarr Docker Service
- Configure Radarr Through API

## 🔔 Handlers
- Restart PostgreSQL

## 🔗 Dependencies
- `python3`
- `global`
- `autofs`
- `users`
- `docker_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: radarr_setup
```