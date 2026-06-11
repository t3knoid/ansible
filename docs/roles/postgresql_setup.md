# 🛠️ Role: `postgresql_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs PostgreSQL.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `postgresql_setup_version` | `17` | defaults file for postgresql_setup |
| `postgresql_setup_data_dir` | `/data/pgdata` |  |
| `postgresql_setup_dbhost` | `"{{ groups['pgdb'][0] }}"` |  |
| `postgresql_setup_packages_to_install` | `` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install curl and ca-certificates
- Create directory /usr/share/postgresql-common/pgdg
- Download PostgreSQL GPG key
- Add PostgreSQL repository
- Install Postgresql packages
- Stop PostgreSQL service
- Delete default PostgreSQL data directory
- Create Postresql data directory
- Initialize the new data directory
- Show postgresql_setup_initdb_out
- Update data_directory in postgresql.conf
- Restart PostgreSQL service
- Update pg_hba.conf to use md5 authentication
- Update pg_hba.conf to allow password access using localhost
- Modify listen_addresses in postgresql.conf
- Ensure PostgreSQL service is running

## 🔔 Handlers
- Start PostgreSQL

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: postgresql_setup
```