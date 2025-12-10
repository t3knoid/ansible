# Role: `azure_cli_setup`

## 📖 Overview
Install Microsoft Azure CLI

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## 🧮 Defaults
- `azure_cli_setup_version`: `2.81.0`
- `azure_cli_setup_repo_url`: `"https://packages.microsoft.com/repos/azure-cli/"`
- `azure_cli_setup_key_url`: `"https://packages.microsoft.com/keys/microsoft.asc"`

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Ensure required packages are installed
- Add Microsoft signing key
- Ensure key file permissions
- Add Azure CLI repository
- Install Azure CLI

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: azure_cli_setup
```