# 🛠️ Role: `rproxy_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
rproxy_setup configures reverse proxy with failover support using nginx. This role requires at least three hosts to be defined. One host is configure as the main frontend proxy, the other two acts as the primary and secondary proxy.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `rproxy_setup_backend_servers` | `|` |  |
| `server {{ hostvars[groups['rproxy_primary'][0]]['ansible_default_ipv4']['address'] }}` | `80 max_fails=3 fail_timeout=5s;` |  |
| `server {{ hostvars[groups['rproxy_secondary'][0]]['ansible_default_ipv4']['address'] }}` | `80 backup;` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Add upstream block to "{{ nginx_setup_conf }}"
- Set rproxy_setup_site to default_server
- Configure default_server
- Enable default_server site

## 🔔 Handlers
- Restart nginx

## 🔗 Dependencies
- `global`
- `nginx_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: rproxy_setup
```