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
| `rproxy_setup_check_health` | `true` |  |
| `rproxy_setup_health_check_script_path` | `/usr/local/bin/check_rproxy_health.sh` |  |
| `rproxy_setup_health_metrics_path` | `"{{ node_exporter_setup_textfile_collector_dir | default('/var/lib/node_exporter/textfile') }}/rproxy_health.prom"` |  |
| `rproxy_setup_health_check_minute` | `"*/5"` |  |
| `rproxy_setup_cloudflare_only` | `true # There is an existing bug that deletes the cloudflare-allow.conf if this is false` |  |
| `rproxy_setup_cloudflare_ipv4` | `` |  |
| `rproxy_setup_cloudflare_ipv6` | `` |  |
| `- 2400` | `cb00::/32` |  |
| `- 2606` | `4700::/32` |  |
| `- 2803` | `f800::/32` |  |
| `- 2405` | `b500::/32` |  |
| `- 2405` | `8100::/32` |  |
| `- 2a06` | `98c0::/29` |  |
| `- 2c0f` | `f248::/32` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Add upstream block to "{{ nginx_setup_conf }}"
- Set rproxy_setup_site to default_server
- Configure default_server
- Enable default_server site
- Check reverse proxy health via Prometheus metrics

## 🔔 Handlers
- Restart nginx

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: rproxy_setup
```