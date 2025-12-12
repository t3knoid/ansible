# 🛠️ Role: `grafana_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Install and configure Grafana on Debian/Ubuntu

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (focal, jammy)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `grafana_setup_version` | `"12.2.0"` |  |
| `grafana_setup_edition` | `"grafana-enterprise"` |  |
| `grafana_setup_tgz_file` | `"{{ grafana_setup_edition }}_{{ grafana_setup_version }}_17949786146_linux_amd64.tar.gz"` |  |
| `grafana_setup_dl_url` | `"https://dl.grafana.com/{{ grafana_setup_edition }}/release/{{ grafana_setup_version }}/{{ grafana_setup_tgz_file }}"` |  |
| `grafana_setup_install_dir` | `"/opt/grafana-{{ grafana_setup_version }}"` |  |
| `grafana_setup_bin_path` | `"{{ grafana_setup_install_dir }}/bin/grafana server"` |  |
| `grafana_setup_http_port` | `3000` |  |
| `grafana_setup_user` | `"grafana"` |  |
| `grafana_setup_group` | `"users"` |  |
| `grafana_setup_home_dir` | `"/data/grafana"` |  |
| `grafana_setup_logs_dir` | `"{{ grafana_setup_home_dir }}/logs"` |  |
| `grafana_setup_plugins_dir` | `"{{ grafana_setup_home_dir }}/plugins"` |  |
| `grafana_setup_bin_dir` | `"{{ grafana_setup_home_dir }}/bin/grafana"` |  |
| `grafana_setup_provisioning_dir` | `"{{ grafana_setup_home_dir }}/provisioning"` |  |
| `grafana_setup_conf_dir` | `"{{ grafana_setup_home_dir }}/conf"` |  |
| `grafana_setup_pid_dir` | `"{{ grafana_setup_home_dir }}/run"` |  |
| `grafana_setup_config_file` | `"{{ grafana_setup_conf_dir }}/defaults.ini"` |  |
| `grafana_setup_service_file` | `"/usr/lib/systemd/system/grafana-server.service"` |  |
| `grafana_setup_environment_file` | `"{{ grafana_setup_home_dir }}/defaults"` |  |
| `grafana_setup_pg_port` | `5432` |  |
| `grafana_setup_pg_host` | `"{{ global_ip_addresses[groups['pgdb'][0]] }}"` |  |
| `grafana_setup_mount_point` | `/nfs/backups` | grafana_setup_db_password |
| `grafana_setup_backup_prefix` | `"grafana_"` |  |
| `grafana_setup_backup_filename` | `"{{ grafana_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `grafana_setup_backup_path` | `"{{ grafana_setup_mount_point }}/{{ grafana_setup_backup_filename }}"` |  |
| `grafana_setup_ldap_server` | `"192.168.2.251"` | LDAP settings |
| `grafana_setup_ldap_port` | `389` |  |
| `grafana_setup_ldap_use_tls` | `false` |  |
| `grafana_setup_ldap_bind_dn` | `"CN=LDAP Bind User,OU=Service Accounts,DC=refol,DC=us"` |  |
| `grafana_setup_ldap_searchdn` | `"CN=Users,DC=refol,DC=us"` | grafana_setup_ldap_bindpassword: "See vault" |
| `grafana_setup_ldap_searchfilter` | `"(sAMAccountName=%s)"` |  |
| `grafana_setup_ldap_group_dn` | `"CN=GrafanaAdmins,CN=Users,DC=refol,DC=us"` |  |
| `grafana_setup_ldap_editor_group` | `"CN=GrafanaEditors,CN=Users,DC=refol,DC=us"` |  |
| `grafana_setup_ldap_viewer_group` | `"CN=GrafanaViewers,CN=Users,DC=refol,DC=us"` |  |
| `grafana_setup_ldap_group_searchfilter` | `"(objectClass=group)"` |  |
| `grafana_setup_ldap_group_searchdn` | `"CN=Users,DC=refol,DC=us"` |  |
| `grafana_setup_ldap_verbose_logging` | `false` | Log settings |
| `grafana_setup_log_mode` | `"console file"` |  |
| `grafana_setup_log_level` | `"info"` |  |
| `grafana_setup_log_filters` | `"ldap:info"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Update pg_hba.conf to allow password access using host ip address
- Update pg_hba.conf to allow password access using the database host ip address
- Install required packages
- Download and Extract Grafana
- Create symlink to Grafana installation
- Create Grafana data directory
- Create Grafana log directory
- Create Grafana plugins directory
- Create Grafana pid file directory
- Create Grafana provisioning directory
- Create Grafana provisioning/plugins directory
- Create Grafana configuration directory
- Copy Grafana configuration file
- Copy Grafana LDAP settings file
- Copy Grafana defaults file
- Set ownership for Grafana directory
- Create Grafana systemd service file
- Enable and start Grafana service

## 🔔 Handlers
- Restart Grafana
- Restart PostgreSQL
- Reload systemd daemon

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: grafana_setup
```