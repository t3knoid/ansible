# 🛠️ Role: `vault_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs and configures Hashicorp Vault

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `vault_setup_version` | `1.21.0-1` |  |
| `vault_setup_config_dir` | `/etc/vault.d` |  |
| `vault_setup_ca_key` | `ca.key` |  |
| `vault_setup_ca_crt` | `ca.crt` |  |
| `vault_setup_client_cacert_vault_dir` | `/usr/local/share/ca-certificates/vault` |  |
| `vault_setup_vault_server` | `"{{ groups['vault_servers'][0] }}"` |  |
| `vault_setup_hashicorp_gpg_key_path` | `/usr/share/keyrings/hashicorp-archive-keyring.gpg` |  |
| `vault_setup_vault_service_file` | `/etc/systemd/system/vault.service` |  |
| `vault_setup_user` | `vault` |  |
| `vault_setup_group` | `vault` |  |
| `vault_setup_listener_address` | `"0.0.0.0:8200"` |  |
| `vault_setup_alias` | `"{{ pihole_cname_entries[0].domain if pihole_cname_entries is defined else '' }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install Vault dependencies
- Add HashiCorp GPG key
- Add HashiCorp repository
- Update apt cache
- Install HashiCorp Vault
- Execute the following block of tasks in vault servers

## 🔔 Handlers
- Restart vault

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: vault_setup
```