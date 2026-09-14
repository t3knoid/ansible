# 🛠️ Role: `plex_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs Plex Media Server.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `plex_setup_version` | `"{{ plex_setup_version | default('1.42.1.10060-4e8b05daf') }}"` |  |
| `plex_setup_package` | `"plexmediaserver_{{ plex_setup_version }}_amd64.deb"` |  |
| `plex_setup_download_url` | `"https://downloads.plex.tv/plex-media-server-new/{{ plex_setup_version }}/debian/{{ plex_setup_package }}"` |  |
| `plex_setup_data_dir` | `/var/lib/plexmediaserver` |  |
| `plex_setup_backup_dir` | `/nfs/backups/plex` |  |
| `plex_setup_timestamp` | `"{{ lookup('pipe', 'date +%Y%m%d_%H%M%S') }}"` |  |
| `plex_setup_backup_file` | `"{{ plex_setup_backup_dir }}/plex_backup_{{ plex_setup_timestamp }}.tar.gz"` |  |
| `plex_setup_restore_path` | `""` |  |
| `plex_setup_check_update` | `true` |  |
| `plex_setup_update_check_token` | `""` |  |
| `plex_setup_update_check_distro` | `"debian"` |  |
| `plex_setup_update_check_build` | `"linux-x86_64"` |  |
| `plex_setup_update_check_script_path` | `/usr/local/bin/check_plex_update.sh` |  |
| `plex_setup_update_metrics_path` | `"{{ node_exporter_setup_textfile_collector_dir | default('/var/lib/node_exporter/textfile') }}/plex_update.prom"` |  |
| `plex_setup_update_check_minute` | `"*/30"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Wait for Plex host to come on line
- Download Plex Media Server package
- Install Plex Media Server
- Ensure Plex Media Server is started
- Check Plex Media Server for available updates via Prometheus metrics

## 🔔 Handlers
- Restart Plex Media Server

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: plex_setup
```