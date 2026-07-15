# 🛠️ Role: `vms`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Provides tasks to manage virtual machines hosted in Proxmox VE.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `vms_proxmox_node` | `pve-0` | defaults file for vm |
| `vms_autoinstall` | `false` |  |
| `vms_additional_packages` | `[]` |  |
| `vms_name` | `"{{ name | default(inventory_hostname) }}"` |  |
| `vms_set_to_template` | `false` |  |
| `vms_clone_host` | `192.168.2.199` |  |
| `vms_ip_address_configured` | `false` |  |
| `vms_clone` | `false` | Deprecated: this variable is currently ignored by the vms role. |
| `vms_pve_tls_insecure` | `true` |  |

## 📦 Vars
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `vms_terraform_module_dir` | `"{{ global_terraform_root_dir }}/{{ inventory_hostname }}"` |  |

## 📑 Tasks
- Create new ubuntu virtual machine
- Include add_disk tasks
- Mount cd-rom installer image
- Include autoinstall tasks
- Include serial terminal tasks
- Eject installer media

## 🔔 Handlers
- Restart virtual machine
- Validate Terraform config

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: vms
```