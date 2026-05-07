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
| `lidarr_setup_restore_path` | `""` |  |
| `lidarr_setup_api_url` | `"http://127.0.0.1:{{ lidarr_setup_port }}"` |  |
| `lidarr_setup_api_validate_certs` | `false` |  |
| `lidarr_setup_root_folders` | `` |  |
| `- name` | `Music` |  |
| `path` | `/music` |  |
| `default_quality_profile_name` | `"Lossless"` |  |
| `default_metadata_profile_name` | `"Standard"` |  |
| `default_monitor_option` | `"all"` |  |
| `default_new_item_monitor_option` | `"all"` |  |
| `default_tags` | `[]` |  |
| `lidarr_setup_download_clients` | `` |  |
| `- name` | `sabnzbd` |  |
| `implementation` | `Sabnzbd` |  |
| `enable` | `true` |  |
| `priority` | `1` |  |
| `fields` | `` |  |
| `host` | `"{{ global_ip_addresses[groups['sabnzbd'][0]] }}"` |  |
| `port` | `8080` |  |
| `musicCategory` | `music` |  |
| `lidarr_setup_indexers` | `` |  |
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
| `lidarr_setup_root_folder_default_quality_profile_name` | `"Any"` |  |
| `lidarr_setup_root_folder_default_metadata_profile_name` | `"Standard"` |  |
| `lidarr_setup_root_folder_default_monitor_option` | `"all"` |  |
| `lidarr_setup_root_folder_default_new_item_monitor_option` | `"all"` |  |
| `lidarr_setup_configure_api` | `>-` |  |
| `lidarr_setup_authentication_method` | `"External" # Options: Basic, Forms, External` |  |
| `lidarr_setup_authentication_required` | `"DisabledForLocalAddresses" # Options: Enabled, DisabledForLocalAddresses` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Configure Lidarr Through API

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