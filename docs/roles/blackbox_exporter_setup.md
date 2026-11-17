# 🛠️ Role: `blackbox_exporter_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Install and configure Prometheus Blackbox Exporter for probing web services.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (bionic, focal, jammy, noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `blackbox_exporter_setup_version` | `"0.25.0"` |  |
| `blackbox_exporter_setup_platform` | `"linux-amd64"` |  |
| `blackbox_exporter_setup_download_url` | `"https://github.com/prometheus/blackbox_exporter/releases/download/v{{ blackbox_exporter_setup_version }}/blackbox_exporter-{{ blackbox_exporter_setup_version }}.{{ blackbox_exporter_setup_platform }}.tar.gz"` |  |
| `blackbox_exporter_setup_install_dir` | `"/opt/blackbox_exporter-{{ blackbox_exporter_setup_version }}.{{ blackbox_exporter_setup_platform }}"` |  |
| `blackbox_exporter_setup_home` | `"/opt/blackbox_exporter"` |  |
| `blackbox_exporter_setup_binary` | `"/usr/local/bin/blackbox_exporter"` |  |
| `blackbox_exporter_setup_mode` | `"0755"` |  |
| `blackbox_exporter_port` | `9115` |  |
| `blackbox_exporter_setup_listen_address` | `"0.0.0.0:{{ blackbox_exporter_port }}"` |  |
| `blackbox_exporter_setup_user` | `"blackbox-exporter"` |  |
| `blackbox_exporter_setup_group` | `"blackbox-exporter"` |  |
| `blackbox_exporter_setup_service_name` | `"blackbox_exporter"` |  |
| `blackbox_exporter_setup_service_file` | `"/etc/systemd/system/blackbox_exporter.service"` |  |
| `blackbox_exporter_setup_service_mode` | `"0644"` |  |
| `blackbox_exporter_setup_config_dir` | `"/etc/blackbox_exporter"` |  |
| `blackbox_exporter_setup_config_file` | `"{{ blackbox_exporter_setup_config_dir }}/blackbox.yml"` |  |
| `blackbox_exporter_setup_log_level` | `"info"` |  |
| `blackbox_exporter_setup_modules` | `` |  |
| `http_2xx` | `` |  |
| `prober` | `http` |  |
| `timeout` | `5s` |  |
| `http` | `` |  |
| `method` | `GET` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `https_2xx` | `` |  |
| `prober` | `http` |  |
| `timeout` | `5s` |  |
| `http` | `` |  |
| `method` | `GET` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `fail_if_ssl` | `false` |  |
| `tcp_connect` | `` |  |
| `prober` | `tcp` |  |
| `timeout` | `5s` |  |
| `icmp_ipv4` | `` | --- Service request-path probes (see service_path_services) --- |
| `prober` | `icmp` |  |
| `timeout` | `3s` |  |
| `icmp` | `` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `tcp_connect_ipv4` | `` |  |
| `prober` | `tcp` |  |
| `timeout` | `5s` |  |
| `tcp` | `` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `http_vhost_2xx` | `` | Redirects are not followed: a 301 means the vhost is missing and nginx fell back to the default server. |
| `prober` | `http` |  |
| `timeout` | `5s` |  |
| `http` | `` |  |
| `method` | `GET` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `follow_redirects` | `false` |  |
| `http_vhost_reachable` | `` | destination, which means the vhost is missing and another server block answered. |
| `prober` | `http` |  |
| `timeout` | `5s` |  |
| `http` | `` |  |
| `method` | `GET` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `follow_redirects` | `false` |  |
| `valid_status_codes` | `[200, 204, 301, 302, 303, 307, 308, 401, 403]` |  |
| `fail_if_header_matches` | `` |  |
| `- header` | `Location` |  |
| `regexp` | `"/projects/home-lab"` |  |
| `https_frontdoor_oauth2` | `` | which proves TLS + nginx vhost + oauth2-proxy are working on the front proxy. |
| `prober` | `http` |  |
| `timeout` | `5s` |  |
| `http` | `` |  |
| `method` | `GET` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `follow_redirects` | `false` |  |
| `fail_if_not_ssl` | `true` |  |
| `valid_status_codes` | `[401, 403]` |  |
| `fail_if_body_not_matches_regexp` | `` |  |
| `https_frontdoor_open` | `` |  |
| `prober` | `http` |  |
| `timeout` | `5s` |  |
| `http` | `` |  |
| `method` | `GET` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `follow_redirects` | `false` |  |
| `fail_if_not_ssl` | `true` |  |
| `valid_status_codes` | `[200, 204, 301, 302, 303, 307, 308, 401, 403, 502, 503, 504]` | 401/403 = the app's own login, 502-504 = rproxy-0 answered but the backend did not |
| `https_edge_oauth2` | `` | and come from the origin (oauth2 sign-in page), so Cloudflare error pages (52x) and WAF blocks fail. |
| `prober` | `http` |  |
| `timeout` | `10s` |  |
| `http` | `` |  |
| `method` | `GET` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `follow_redirects` | `false` |  |
| `fail_if_not_ssl` | `true` |  |
| `valid_status_codes` | `[401, 403]` |  |
| `fail_if_header_not_matches` | `` |  |
| `- header` | `Server` |  |
| `regexp` | `"cloudflare"` |  |
| `fail_if_body_not_matches_regexp` | `` |  |
| `https_edge_open` | `` |  |
| `prober` | `http` |  |
| `timeout` | `10s` |  |
| `http` | `` |  |
| `method` | `GET` |  |
| `preferred_ip_protocol` | `ip4` |  |
| `follow_redirects` | `false` |  |
| `fail_if_not_ssl` | `true` |  |
| `valid_status_codes` | `[200, 204, 301, 302, 303, 307, 308, 401, 403, 502, 503, 504]` | 401/403 = the app's own login, 502-504 = rproxy-0 answered but the backend did not |
| `fail_if_header_not_matches` | `` |  |
| `- header` | `Server` |  |
| `regexp` | `"cloudflare"` |  |
| `blackbox_exporter_setup_service_path_services` | `"{{ service_path_services | default([]) }}"` | because the Blackbox DNS prober takes the query name from the module, not from the target. |
| `blackbox_exporter_setup_service_path_front_proxy` | `"{{ groups['rproxy_main'] | default([]) | first | default('') }}"` | Answer the internal resolvers must return for each fqdn (split DNS points at the front proxy). |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Create Blackbox Exporter group
- Create Blackbox Exporter user
- Download and extract Blackbox Exporter
- Create symlink for Blackbox Exporter
- Set ownership for Blackbox Exporter directory
- Copy Blackbox Exporter binary to /usr/local/bin
- Create Blackbox Exporter configuration directory
- Render Blackbox Exporter configuration
- Create Blackbox Exporter systemd service file
- Enable and start Blackbox Exporter service

## 🔔 Handlers
- Reload systemd daemon
- Restart blackbox_exporter service

## 🔗 Dependencies
- `global`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: blackbox_exporter_setup
```