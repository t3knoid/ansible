# 🛠️ Role: `oauth2_proxy_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Install and configure OAuth2 Proxy.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `oauth2_proxy_setup_version` | `"7.13.1"` |  |
| `oauth2_proxy_setup_download_tgz_file` | `"oauth2-proxy-v{{ oauth2_proxy_setup_version }}.linux-amd64.tar.gz"` |  |
| `oauth2_proxy_setup_download_url` | `>` |  |
| `https` | `//github.com/oauth2-proxy/oauth2-proxy/releases/download/v{{ oauth2_proxy_setup_version }}/{{ oauth2_proxy_setup_download_tgz_file }}` |  |
| `oauth2_proxy_setup_bin` | `/usr/local/bin/oauth2-proxy` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install prerequisites
- Download OAuth2 Proxy release archive and and extract binary
- Ensure oauth2-proxy binary is executable
- Create oauth2-proxy configuration directory
- Set Redis connection string
- Replace rproxy_setup_sites with updated list containing secrets
- Find all oauth2-proxy services
- Remove oauth2 directives from nginx configuration
- Clean up oauth2-proxy services
- Insert OAuth2 Proxy directives into nginx configuration
- Deploy oauth2-proxy configurations
- Create systemd services for oauth2-proxy
- Reload systemd daemon
- Enable and ensure all oauth2-proxy services started

## 🔔 Handlers
- Reload systemd daemon
- Reload nginx

## 🔗 Dependencies
- `redis_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: oauth2_proxy_setup
```