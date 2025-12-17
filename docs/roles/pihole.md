# 🛠️ Role: `pihole`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Installs and configures Pi-hole on Ubuntu systems (https://pi-hole.net/). Provides tasks to manage Pi-hole settings and configurations.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `pihole_api_host` | `"{{ global_pihole_api_host | default('192.168.2.253') }}"` | defaults file for pi-hole |
| `pihole_config_dir` | `/etc/pihole` |  |
| `pihole_config_upstreams` | `` |  |
| `pihole_config_reverse_servers` | `` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Consolidate all consolidate_cname_entries
- Create Pi-Hole config directory
- Create pihole.toml
- Download Pi-hole install script
- Run Pi-hole install script

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: pihole
```