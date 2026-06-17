# 🛠️ Role: `ipsec_vpn_server_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs and configures the hwdsl2 IPsec VPN server Docker container, including vpn.env and docker-compose configuration.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (jammy, noble)
- Supported on: `Debian` (bullseye, bookworm)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `ipsec_vpn_server_setup_enabled` | `true` |  |
| `ipsec_vpn_server_setup_service_name` | `"vpn"` |  |
| `ipsec_vpn_server_setup_image` | `"hwdsl2/ipsec-vpn-server:debian"` |  |
| `ipsec_vpn_server_setup_container_name` | `"ipsec-vpn-server"` |  |
| `ipsec_vpn_server_setup_hostname` | `"ipsec-vpn-server"` |  |
| `ipsec_vpn_server_setup_config_dir` | `"/opt/ipsec-vpn-server"` |  |
| `ipsec_vpn_server_setup_etc_dir` | `"{{ ipsec_vpn_server_setup_config_dir }}/etc"` |  |
| `ipsec_vpn_server_setup_backups_dir` | `"{{ ipsec_vpn_server_setup_config_dir }}/backups"` |  |
| `ipsec_vpn_server_setup_env_file` | `"{{ ipsec_vpn_server_setup_config_dir }}/vpn.env"` |  |
| `ipsec_vpn_server_setup_restart_policy` | `"always"` |  |
| `ipsec_vpn_server_setup_privileged` | `true` |  |
| `ipsec_vpn_server_setup_ports` | `` |  |
| `- "500` | `500/udp"` |  |
| `- "4500` | `4500/udp"` |  |
| `ipsec_vpn_server_setup_volumes` | `` |  |
| `- "{{ ipsec_vpn_server_setup_etc_dir }}` | `/etc/ipsec.d"` |  |
| `- "/lib/modules` | `/lib/modules:ro"` |  |
| `ipsec_vpn_server_setup_vpn_ipsec_psk` | `""` |  |
| `ipsec_vpn_server_setup_vpn_user` | `""` |  |
| `ipsec_vpn_server_setup_vpn_password` | `""` |  |
| `ipsec_vpn_server_setup_additional_users` | `[]` |  |
| `ipsec_vpn_server_setup_additional_passwords` | `[]` |  |
| `ipsec_vpn_server_setup_public_ip` | `""` |  |
| `ipsec_vpn_server_setup_dns_name` | `""` |  |
| `ipsec_vpn_server_setup_client_name` | `"vpnclient"` |  |
| `ipsec_vpn_server_setup_dns_servers` | `` |  |
| `ipsec_vpn_server_setup_protect_config` | `false` |  |
| `ipsec_vpn_server_setup_public_ipv6` | `""` |  |
| `ipsec_vpn_server_setup_ipv6_subnet` | `""` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Validate IPsec VPN Docker settings
- Create IPsec VPN local config directories
- Deploy IPsec VPN server Docker service

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: ipsec_vpn_server_setup
```