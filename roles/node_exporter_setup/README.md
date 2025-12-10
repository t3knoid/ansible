# 🛠️ Role: `node_exporter_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs Prometheus Node Exporter

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `node_exporter_setup_version` | `1.9.1` |  |
| `node_exporter_setup_home` | `"/opt/node_exporter"` |  |
| `node_exporter_setup_mode` | `'0755'` |  |
| `node_exporter_setup_user` | `"prometheus"` |  |
| `node_exporter_setup_group` | `"prometheus"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Download and Extract Node xporter
- Create symlink for Node Exporter
- Set ownership for Node Exporter directory
- Copy Node Exporter binary to /usr/local/bin

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
- `global`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: node_exporter_setup
```