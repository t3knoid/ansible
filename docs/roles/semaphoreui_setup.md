# 🛠️ Role: `semaphoreui_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures [Semaphore UI](https://docs.semaphoreui.com/).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `semaphoreui_setup_version` | `2.16.19` |  |
| `semaphoreui_setup_installer` | `"semaphore_{{ semaphoreui_setup_version }}_linux_amd64.deb"` |  |
| `semaphoreui_setup_loglevel` | `INFO` |  |
| `semaphoreui_setup_python_packages` | `` |  |
| `semaphoreui_setup_homedir` | `/ansible/semaphore` |  |
| `semaphoreui_setup_tmpdir` | `"{{ semaphoreui_setup_homedir }}/tmp"` |  |
| `semaphoreui_setup_etcdir` | `"{{ semaphoreui_setup_homedir }}/etc"` |  |
| `semaphoreui_setup_pg_host` | `"{{ global_ip_addresses[groups['pgdb'][0]] }}"` |  |
| `semaphoreui_setup_pgclient_host` | `"{{ global_ip_addresses[groups['pgclient'][0]] }}"` |  |
| `semaphoreui_setup_port` | `3000` |  |
| `semaphoreui_setup_use_remote_runner` | `false` |  |
| `semaphoreui_setup_ldap_bind_dn` | `"CN=LDAP Bind User,OU=Service Accounts,DC=refol,DC=us"` | LDAP |
| `semaphoreui_setup_ldap_bindpassword` | `""` |  |
| `semaphoreui_setup_ldap_server` | `"ad0.refol.us:389"` |  |
| `semaphoreui_setup_ldap_searchdn` | `"CN=Users,DC=refol,DC=us"` |  |
| `semaphoreui_setup_ldap_searchfilter` | `"(sAMAccountName=%s)"` |  |
| `semaphoreui_setup_ldap_mappings` | `` |  |
| `dn` | `""` |  |
| `mail` | `"userPrincipalName"` |  |
| `uid` | `"sAMAccountName"` |  |
| `cn` | `"cn"` |  |
| `semaphoreui_setup_mount_point` | `/nfs/backups` | semaphoreui_setup_db_password: in vault |
| `semaphoreui_setup_backup_prefix` | `"semaphoreui_"` |  |
| `semaphoreui_setup_backup_filename` | `"{{ semaphoreui_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `semaphoreui_setup_backup_path` | `"{{ semaphoreui_setup_mount_point }}/{{ semaphoreui_setup_backup_filename }}"` |  |
| `semaphoreui_setup_api_base` | `"http://localhost:{{ semaphoreui_setup_port }}/api"` | API |
| `semaphoreui_setup_inventories` | `[]` |  |
| `semaphoreui_setup_projects` | `` |  |
| `- name` | `"Home Lab"` |  |
| `alert_enabled` | `false` |  |
| `alert` | `false` |  |
| `alert_chat` | `""` |  |
| `max_parallel_tasks` | `0` |  |
| `repositories` | `` |  |
| `- name` | `"Ansible"` |  |
| `git_url` | `"https://github.com/t3knoid/ansible.git"` |  |
| `git_branch` | `"main"` |  |
| `keystores` | `` |  |
| `- name` | `"Semaphore user credentials"` |  |
| `type` | `"login_password"` |  |
| `login_password` | `` |  |
| `login` | `"{{ semaphoreui_setup_semaphore_login }}"` |  |
| `password` | `"{{ semaphoreui_setup_semaphore_password }}"` |  |
| `- name` | `"Ansible user credentials"` |  |
| `type` | `"login_password"` |  |
| `login_password` | `` |  |
| `login` | `"{{ semaphoreui_setup_ansible_login }}"` |  |
| `password` | `"{{ semaphoreui_setup_ansible_password }}"` |  |
| `- name` | `"Ansible vault password"` |  |
| `type` | `"login_password"` |  |
| `login_password` | `` |  |
| `login` | `""` |  |
| `password` | `"{{ semaphoreui_setup_ansible_vault_password }}"` |  |
| `- name` | `"None"` | private_key: |
| `type` | `"none"` |  |
| `empty` | `true` |  |
| `views` | `` |  |
| `- title` | `"Certs"` |  |
| `templates` | `` |  |
| `- name` | `"Request Certificates for all hosts"` |  |
| `playbook` | `"playbooks/certs/generate_certs.yml"` |  |
| `app` | `"ansible"` |  |
| `arguments` | `"[\"-k\"]"` |  |
| `inventory` | `"rproxy"` |  |
| `credentials` | `` |  |
| `repository` | `"Ansible"` |  |
| `view` | `"Certs"` |  |
| `environment` | `"Empty"` |  |
| `- name` | `"Stage Certificates for all hosts"` |  |
| `playbook` | `"playbooks/certs/stage_certs.yml"` |  |
| `app` | `"ansible"` |  |
| `arguments` | `"[\"-k\"]"` |  |
| `inventory` | `"rproxy"` |  |
| `credentials` | `` |  |
| `repository` | `"Ansible"` |  |
| `view` | `"Certs"` |  |
| `environment` | `"Empty"` |  |
| `semaphoreui_setup_email_alert` | `false` | Email alert |
| `semaphoreui_setup_email_port` | `"587"` |  |
| `semaphoreui_setup_oidc_color` | `"blue"` | See vault for login |
| `semaphoreui_setup_oidc_display_name` | `"Sign in with Azure (EntraID)"` |  |
| `semaphoreui_setup_oidc_redirect_url` | `"https://semaphore.refol.us/api/auth/oidc/azure/redirect"` |  |
| `semaphoreui_setup_timezone` | `"America/New_York"` | timezone |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Include install.yml tasks
- Include configure.yml tasks
- Include runner.yml tasks

## 🔔 Handlers
- Restart PostgreSQL
- Restart Semaphore
- Restart Semaphore Runner

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: semaphoreui_setup
```