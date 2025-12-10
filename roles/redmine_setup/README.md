# 🛠️ Role: `redmine_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Redmine Setup installs and configures an [Redmine](https://www.redmine.org/). The installation instructions are taken directly from [Redmine's installation guide](https://www.redmine.org/projects/redmine/wiki/RedmineInstall) and adapting [redmineadvisor.com's instructions](https://www.redmineadvisor.com/articles/6_0/install/ubuntu24/) on installing Redmine in Ubuntu 24.


## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `redmine_setup_port` | `80` |  |
| `redmine_setup_pg_port` | `5432` |  |
| `redmine_setup_pg_host` | `"{{ global_ip_addresses[groups['pgdb'][0]] }}"` |  |
| `redmine_setup_version` | `6.0.5` |  |
| `redmine_setup_archive` | `"redmine-{{ redmine_setup_version }}.tar.gz"` |  |
| `redmine_setup_installdir_root` | `"/data/redmine"` |  |
| `redmine_setup_installdir` | `"{{ redmine_setup_installdir_root }}/{{ redmine_setup_archive | regex_replace('\\.tar\\.gz$', '') }}"` |  |
| `redmine_setup_download_url` | `"https://www.redmine.org/releases/{{ redmine_setup_archive }}"` |  |
| `redmine_setup_www_rootdir` | `/var/lib/redmine` |  |
| `redmine_setup_www_publicdir` | `"{{ redmine_setup_www_rootdir }}/public"` |  |
| `redmine_setup_apache_default_conf` | `/etc/apache2/sites-enabled/000-default.conf` |  |
| `redmine_setup_smtp_settings_address` | `localhost` |  |
| `redmine_setup_smtp_settings_port` | `25` |  |
| `redmine_setup_mount_point` | `/nfs/backups` | redmine_setup_db_password |
| `redmine_setup_backup_prefix` | `"redmine_"` |  |
| `redmine_setup_backup_filename` | `"{{ redmine_setup_backup_prefix }}{{ ansible_date_time.date }}.sqlc"` |  |
| `redmine_setup_backup_path` | `"{{ redmine_setup_mount_point }}/{{ redmine_setup_backup_filename }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install development tools and header files
- Install PostgreSQL header files
- Install git
- Install Apache and header files
- Ensure extraction folder exists
- Download and extract Redmine source code
- Chown Redmine extracted source code with www-data
- Create softlink of extracted source code to root directory
- Copy database.yml to target machine
- Copy configuration.yml to target machine
- Install Gem packages
- Create a Secret Token for Session Tampering Prevention
- Create Database Tables
- Install Passenger
- Install Passenger Module for Apache
- Confirming Configuration Details for Apache
- Show Configuration Details for Apache
- Set redmine_setup_passenger_snippet
- Copy redmine.conf to /etc/apache2/conf-available/
- Update Apache default site DocumentRoot with Redmine public directory
- Enable the Redmine configuration in Apache
- Test Apache configuration
- Reload Apache service

## 🔔 Handlers
- Restart PostgreSQL

## 🔗 Dependencies
- `global`
- `users`
- `postgresql_setup`
- `ruby_setup`
- `postgresql_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: redmine_setup
```