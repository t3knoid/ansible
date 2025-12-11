# 🛠️ Role: `ansible_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Provides tasks to install and configure Ansible on a control node.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `ansible_setup_ver` | `10.5.0` |  |
| `ansible_setup_callback_plugins` | `` |  |
| `ansible_setup_workdir` | `"~/ansible/dev"` |  |
| `ansible_setup_config_path` | `"{{ ansible_setup_workdir }}/ansible.cfg"` |  |
| `ansible_setup_git_repository` | `https://github.com/t3knoid/ansible.git` |  |
| `ansible_setup_remote_tmp` | `"~/.ansible/tmp/"` |  |
| `ansible_setup_python_modules` | `` |  |
| `- ansible==12.0.0 # https` | `//pypi.org/project/ansible/` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Create ansible work folder
- Install Ansible Python modules
- Checkout Ansible source code from github
- Create vault password file

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: ansible_setup
```