# 🛠️ Role: `azure_cli_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs Microsoft Azure CLI

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `azure_cli_setup_version` | `2.85.0` |  |
| `azure_cli_setup_repo_url` | `"https://packages.microsoft.com/repos/azure-cli/"` |  |
| `azure_cli_setup_key_url` | `"https://packages.microsoft.com/keys/microsoft.asc"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Ensure required packages are installed
- Add Microsoft signing key
- Ensure key file permissions
- Add Azure CLI repository
- Install Azure CLI

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: azure_cli_setup
```