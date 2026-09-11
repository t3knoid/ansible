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
| `oc_setup_version` | `6.3.0.45` | https://support.omadanetworks.com/en/download/software/omada-controller/ |
| `oc_setup_download_url` | `"https://static.tp-link.com/upload/software/2026/202609/20260904/Omada_Network_Application_v{{ oc_setup_version }}_linux_x64_20260903171910.deb"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Check if Omada Software Controller is already installed
- Get installed Omada Software Controller version
- Determine installed Omada Software Controller version
- Install Omada Software Controller (deb package)

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: oc_setup
```