# 🛠️ Role: `nginx_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs the nginx service.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `nginx_setup_version` | `"1.24.0-2ubuntu7.7"` |  |
| `nginx_setup_site_name` | `"{{ inventory_hostname }}"` |  |
| `nginx_setup_worker_connections` | `768` |  |
| `nginx_setup_homedir` | `/data/nginx` |  |
| `nginx_setup_access_log` | `"{{ nginx_setup_homedir }}/log/access.log"` |  |
| `nginx_setup_conf` | `/etc/nginx/nginx.conf` |  |
| `nginx_setup_certroot` | `/data/certs` |  |
| `nginx_setup_disable_default_site` | `true` |  |
| `nginx_setup_start` | `true` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Update apt cache
- Unhold package versions
- Install nginx
- Hold package versions
- Include config.yml tasks
- Enable nginx

## 🔔 Handlers
- Restart nginx

## 🔗 Dependencies
- `global`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: nginx_setup
```