# 🛠️ Role: `azure_ps_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs Microsoft Azure PowerShell

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `azure_ps_setup_prereq_packages` | `` |  |
| `azure_ps_setup_ms_repo_keys_file` | `packages-microsoft-prod.deb` |  |
| `azure_ps_setup_ms_repo_keys_url` | `"https://packages.microsoft.com/config/ubuntu/{{ ansible_distribution_version }}/{{ azure_ps_setup_ms_repo_keys_file }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Update package list
- Install re-requisite packages
- Download Microsoft repository package
- Register Microsoft repository package
- Remove repository package file
- Update package list again
- Install PowerShell
- Check if Az module is installed
- Install Az PowerShell module if not installed

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: azure_ps_setup
```