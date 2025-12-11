# 🛠️ Role: `graphite_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures Graphite on Debian/Ubuntu systems.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `graphite_setup_whisper_version` | `master` | defaults file for graphite_setup |
| `graphite_setup_carbon_version` | `master` |  |
| `graphite_setup_graphite_web_version` | `master` |  |
| `graphite_setup_gunicorn_host` | `127.0.0.1` |  |
| `graphite_setup_gunicorn_port` | `8080` |  |
| `graphite_setup_time_zone` | `"America/New_York"` |  |
| `graphite_setup_venv` | `"/opt/graphite"` |  |
| `graphite_setup_home` | `"{{ graphite_setup_venv }}"` |  |
| `graphite_setup_pg_database` | `graphite` |  |
| `graphite_setup_pg_user` | `graphite` |  |
| `graphite_setup_web_access_log` | `"/var/log/nginx/graphite.access.log"` | graphite_setup_pg_password is in vault.yml |
| `graphite_setup_web_error_log` | `"/var/log/nginx/graphite.error.log"` |  |
| `graphite_setup_carbon_configs` | `` |  |
| `graphite_setup_ldap_server` | `"192.168.2.251"` |  |
| `graphite_setup_ldap_port` | `389` |  |
| `graphite_setup_ldap_use_tls` | `"False"` |  |
| `graphite_setup_ldap_uri` | `ldap://192.168.2.251` |  |
| `graphite_setup_ldap_search_base` | `"CN=Users,DC=refol,DC=us"` |  |
| `graphite_setup_ldap_base_user` | `"CN=LDAP Bind User,OU=Service Accounts,DC=refol,DC=us"` |  |
| `graphite_setup_ldap_user_query` | `"(sAMAccountName=%s)"` | graphite_setup_ldap_base_pass: See vault |
| `graphite_setup_ldap_user_dn_template` | `"CN=%(username)s,CN=Users,DC=refol,DC=us"` |  |
| `nginx_setup_worker_connections` | `20000` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Update apt cache
- Install required dev headers for Graphite-web and Carbon
- Set PYTHONPATH environment variable
- Import venv.yml from python3 role
- Install Whisper module
- Install Carbon module
- Install Graphite-web module
- Check if webapp is in its original location
- Copy webapp to /opt/graphite/webapp
- Delete original webapp folder
- Create log folder
- Include webapp.yml
- Include whisper.yml
- Initalize configuration files
- Start and enable graphite-web service
- Include stop_carbon_cache.yml
- Include start_carbon_cache.yml

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: graphite_setup
```