# 🛠️ Role: `terraform_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs Terraform

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `terraform_setup_version` | `1.13.5` |  |
| `terraform_setup_home` | `"/usr/local/bin"` |  |
| `terraform_setup_os_arch` | `"linux_amd64"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install Terraform dependencies
- Download and extract terraform archive
- Make Terraform executable

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: terraform_setup
```