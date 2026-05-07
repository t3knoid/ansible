# 🛠️ Role: `sonarr_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures a Sonarr Docker container. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/sonarr).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `sonarr_setup_version` | `4.0.15.2941` |  |
| `sonarr_setup_config_dir` | `"/config"` |  |
| `sonarr_setup_port` | `8989` |  |
| `sonarr_setup_ssl_port` | `9898` |  |
| `sonarr_setup_debug_level` | `debug` |  |
| `sonarr_setup_pg_port` | `5432` |  |
| `sonarr_setup_pg_host` | `"{{ global_ip_addresses[groups['pgdb'][0]] }}"` |  |
| `sonarr_setup_mount_point` | `/nfs/backups` | sonarr_setup_db_password |
| `sonarr_setup_backup_prefix` | `"sonarr_"` |  |
| `sonarr_setup_backup_filename` | `"{{ sonarr_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `sonarr_setup_backups_dir` | `"{{ sonarr_setup_mount_point }}/sonarr"` |  |
| `sonarr_setup_backup_path` | `"{{ sonarr_setup_backups_dir }}/{{ sonarr_setup_backup_filename }}"` |  |
| `sonarr_setup_api_url` | `"http://127.0.0.1:{{ sonarr_setup_port }}"` |  |
| `sonarr_setup_api_validate_certs` | `false` |  |
| `sonarr_setup_root_folders` | `` |  |
| `- path` | `/tv` |  |
| `sonarr_setup_download_clients` | `` |  |
| `- name` | `sabnzbd` |  |
| `implementation` | `Sabnzbd` |  |
| `enable` | `true` |  |
| `priority` | `1` |  |
| `fields` | `` |  |
| `host` | `"{{ global_ip_addresses[groups['sabnzbd'][0]] }}"` |  |
| `port` | `8080` |  |
| `tvCategory` | `tv` |  |
| `sonarr_setup_indexers` | `` |  |
| `- name` | `nzbgeek` |  |
| `implementation` | `Newznab` |  |
| `enable_rss` | `true` |  |
| `enable_automatic_search` | `true` |  |
| `enable_interactive_search` | `true` |  |
| `priority` | `1` |  |
| `download_client_name` | `sabnzbd` |  |
| `fields` | `` |  |
| `baseUrl` | `https://api.nzbgeek.info` |  |
| `apiKey` | `"{{ nzbgeek_api_key }}"` |  |
| `categories` | `` |  |
| `- name` | `nzb.su` |  |
| `implementation` | `Newznab` |  |
| `enable_rss` | `true` |  |
| `enable_automatic_search` | `true` |  |
| `enable_interactive_search` | `true` |  |
| `priority` | `1` |  |
| `download_client_name` | `sabnzbd` |  |
| `fields` | `` |  |
| `baseUrl` | `https://api.nzb.su` |  |
| `apiKey` | `"{{ nzbsu_api_key }}"` |  |
| `categories` | `` |  |
| `sonarr_setup_configure_api` | `>-` |  |
| `sonarr_setup_authentication_method` | `"External" # Options: Basic, Forms, External` |  |
| `sonarr_setup_authentication_required` | `"DisabledForLocalAddresses" # Options: Enabled, DisabledForLocalAddresses` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Deploy Sonarr Docker Service
- Configure Sonarr Through API

## 🔔 Handlers
- Restart PostgreSQL

## 🔗 Dependencies
- `global`
- `users`
- `autofs`
- `docker_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: sonarr_setup
```