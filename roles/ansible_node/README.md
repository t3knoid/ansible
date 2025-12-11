# 🛠️ Role: `ansible_node`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Configures a node to be used as an Ansible control node.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `ansible_node_custom_sudo_users` | `` |  |
| `ansible_node_remote_tmp` | `"/tmp/.ansible/$USER"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Ensure ansible group exists
- Store USER value, set to undefined if not defined
- Store SUDO_USER value
- Add current_user to ansible group, if undefined, use SUDO_USER value instead
- Add custom user list to ansible group
- Ensure sudoers.d directory exists
- Add 'ansible' group to sudoers with NOPASSWD
- Ensure remote temp directory exists

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: ansible_node
```