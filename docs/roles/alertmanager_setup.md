# 🛠️ Role: `alertmanager_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs AlertManager.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `alertmanager_setup_version` | `0.30.1` |  |
| `alertmanager_setup_home` | `"/opt/alertmanager"` |  |
| `alertmanager_setup_work_dir` | `"/data/alertmanager"` |  |
| `alertmanager_setup_download_base_url` | `"https://github.com/prometheus/alertmanager/releases/download/"` |  |
| `alertmanager_setup_user` | `"{{ (users_list | default([{'username': 'prometheus'}]) | first).username }}" # Same as prometheus user defined in inventory` |  |
| `alertmanager_setup_group` | `"{{ (users_list | default([{'username': 'prometheus'}]) | first).username }}"` |  |
| `alertmanager_setup_service_file` | `"/etc/systemd/system/alertmanager.service"` |  |
| `alertmanager_setup_wait_for_prometheus` | `false` |  |
| `alertmanager_setup_config_file` | `"{{ alertmanager_setup_work_dir }}/etc/alertmanager.yml"` |  |
| `alertmanager_setup_binary` | `"/usr/local/bin/alertmanager"` |  |
| `alertmanager_setup_mode` | `"0755"` |  |
| `alertmanager_setup_config_mode` | `"0644"` |  |
| `alertmanager_setup_service_mode` | `"0644"` |  |
| `alertmanager_setup_data_mode` | `"0755"` |  |
| `alertmanager_setup_listen_address` | `"0.0.0.0:9093"` |  |
| `alertmanager_setup_templates` | `` |  |
| `alertmanager_setup_route` | `` |  |
| `receiver` | `default-receiver` |  |
| `group_by` | `` |  |
| `group_wait` | `30s` |  |
| `group_interval` | `5m` |  |
| `repeat_interval` | `4h` |  |
| `routes` | `[]` |  |
| `alertmanager_setup_default_email_to` | `"{{ alertmanager_setup_smtp_from }}"` |  |
| `alertmanager_setup_receivers` | `` |  |
| `- name` | `default-receiver` |  |
| `email_configs` | `` |  |
| `- to` | `"{{ alertmanager_setup_default_email_to }}"` |  |
| `send_resolved` | `true` |  |
| `alertmanager_setup_inhibit_rules` | `` |  |
| `- source_matchers` | `` |  |
| `target_matchers` | `` |  |
| `equal` | `` |  |
| `alertmanager_setup_global` | `` |  |
| `resolve_timeout` | `5m` |  |
| `alertmanager_setup_smtp_settings_address` | `smtp-relay.gmail.com` |  |
| `alertmanager_setup_smtp_settings_port` | `587` |  |
| `alertmanager_setup_smtp_from` | `"alertmanager@refol.us"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Download and Extract AlertManager
- Create symlink for AlertManager
- Set ownership for AlertManager directory
- Copy AlertManager binary to /usr/local/bin
- Create AlertManager working directory
- Create AlertManager directories for config and templates
- Copy AlertManager configuration file
- Create AlertManager systemd service file
- Enable and start AlertManager service

## 🔔 Handlers
- Reload systemd daemon
- Validate AlertManager configuration
- Restart AlertManager service

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: alertmanager_setup
```