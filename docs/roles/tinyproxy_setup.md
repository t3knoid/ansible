# 🛠️ Role: `tinyproxy_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs Tinyproxy and configures it as a lightweight HTTP/HTTPS proxy server

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (jammy, noble)
- Supported on: `Debian` (bullseye, bookworm)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `tinyproxy_setup_enabled` | `true` |  |
| `tinyproxy_setup_listen_address` | `"0.0.0.0"` | Basic proxy settings |
| `tinyproxy_setup_port` | `8888` |  |
| `tinyproxy_setup_allowed_clients` | `` |  |
| `tinyproxy_setup_enable_authentication` | `false` |  |
| `tinyproxy_setup_auth_username` | `"proxyuser"` | Authentication credentials (if authentication is enabled) |
| `tinyproxy_setup_auth_password` | `"{{ lookup('env', 'TINYPROXY_SETUP_AUTH_PASSWORD') | default('', true) }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install Tinyproxy
- Validate Tinyproxy authentication settings
- Deploy Tinyproxy configuration
- Enable and start Tinyproxy

## 🔔 Handlers
- Restart tinyproxy

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: tinyproxy_setup
```