# Role: `plex_exporter_setup`

## 📖 Overview
Provides tasks to install and configure prometheus-plex-exporter (https://github.com/jsclayton/prometheus-plex-exporter).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## 🧮 Defaults
- `plex_exporter_setup_tz`: ``
- `plex_exporter_setup_plex_server`: `http://192.168.2.220:32400`
- `plex_exporter_setup_plex_token`: `pGaJmdwsFuuHCyRkahZT`

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
_No tasks defined._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: plex_exporter_setup
```