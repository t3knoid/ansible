# 🛠️ Role: `oc_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Install and configure TP-Link Omada Controller on Ubuntu systems.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `oc_setup_java_major_version` | `"{{ java_setup_version.split('.')[0] | default(11) }}"` |  |
| `oc_setup_commons_daemon_version` | `1.4.1` |  |
| `oc_setup_commons_daemon_package` | `commons-daemon-{{ oc_setup_commons_daemon_version }}-src.tar.gz` |  |
| `oc_setup_commons_daemon_root_url` | `https://archive.apache.org/dist/commons/daemon/source/` |  |
| `oc_setup_version` | `5.15.6.7` |  |
| `oc_setup_download_url` | `"https://static.tp-link.com/upload/software/2024/202412/20241224/Omada_SDN_Controller_v{{ oc_setup_version }}_linux_x64.deb"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install dependencies for JSVC
- Extract JSVC source code
- Remove existing JSVC softlink
- Build and install JSVC
- Cleanup JSVC download
- Download Omada Controller package
- Install Omada Controller

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
- `redis_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: oc_setup
```