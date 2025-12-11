# 🛠️ Role: `ad`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs the required packages in order for a node to join an active directory domain. Use the user ansible (e.g. -u ansible) when using this role

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `ad_additional_packages` | `[]` | defaults file for ad |

## 📦 Vars
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `ad_required_packages` | `` |  |

## 📑 Tasks
- Install required packages
- Update /etc/resolv.conf with domain name
- Update /etc/resolv.conf with DNS servers
- Discover domain
- Show ad_realm_discover_output
- Find configured value
- Display "configured" value
- Display "configured" value
- Join machine to domain
- Show ad_realm_join_output
- Set use_fully_qualified_names in /etc/sssd/sssd.conf to False
- Set fallback_homedir in /etc/sssd/sssd.conf not to use domain
- Restart SSSD service
- Enable mkhomedir
- Show ad_mkhomedir_result
- Reboot machine and send a message
- Wait for machine to become reachable

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: ad
```