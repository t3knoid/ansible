# 🛠️ Role: `code_server`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs and configures code server.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `code_server_version` | `4.140.3` |  |
| `code_server_port` | `8080` |  |
| `code_server_proxy_port` | `8000` |  |
| `code_server_bind_address` | `127.0.0.1` |  |
| `code_server_auth_mode` | `"password"` |  |
| `code_server_service_name` | `"code-server@{{ code_server_user }}"` |  |
| `code_server_download_file` | `"{{ code_server_version }}_amd64.deb"` |  |
| `code_server_download_url` | `"https://github.com/coder/code-server/releases/download/v{{ code_server_version }}/code-server_{{ code_server_download_file }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Gather service facts
- Check installed code-server version
- Stop the code-server package
- Remove current version of code-server
- Download code-server package
- Install code-server package
- Create code-server config folder
- Create code-server config.yaml
- Disable code-server service
- Cleanup downloaded file
- Create or update Nginx site configuration
- Enable Nginx site configuration

## 🔔 Handlers
- Restart nginx
- Restart code server

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: code_server
```