# 🛠️ Role: `ecube_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs ECUBE from GitHub Releases using the upstream Linux installer.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (noble)
- Supported on: `Debian` (bookworm)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `ecube_setup_version` | `"0.2.0"` |  |
| `ecube_setup_release_tag` | `"v{{ ecube_setup_version }}"` |  |
| `ecube_setup_install_dir` | `"/opt/ecube"` |  |
| `ecube_setup_release_base_url` | `"https://github.com/t3knoid/ecube/releases/download/{{ ecube_setup_release_tag }}"` |  |
| `ecube_setup_package_archive` | `"ecube-package-{{ ecube_setup_release_tag }}.tar.gz"` |  |
| `ecube_setup_package_checksum` | `"ecube-package-{{ ecube_setup_release_tag }}.sha256"` |  |
| `ecube_setup_package_url` | `"{{ ecube_setup_release_base_url }}/{{ ecube_setup_package_archive }}"` |  |
| `ecube_setup_checksum_url` | `"{{ ecube_setup_release_base_url }}/{{ ecube_setup_package_checksum }}"` |  |
| `ecube_setup_download_dir` | `"/tmp/ecube-{{ ecube_setup_release_tag }}"` |  |
| `ecube_setup_archive_path` | `"{{ ecube_setup_download_dir }}/{{ ecube_setup_package_archive }}"` |  |
| `ecube_setup_checksum_path` | `"{{ ecube_setup_download_dir }}/{{ ecube_setup_package_checksum }}"` |  |
| `ecube_setup_extract_dir` | `"{{ ecube_setup_download_dir }}/extracted"` |  |
| `ecube_setup_package_dir` | `"{{ ecube_setup_extract_dir }}/ecube-package-{{ ecube_setup_release_tag }}"` |  |
| `ecube_setup_install_script_path` | `"{{ ecube_setup_package_dir }}/install.sh"` |  |
| `ecube_setup_prerequisite_packages` | `` |  |
| `ecube_setup_linux_modules_extra_package` | `"linux-modules-extra-{{ ansible_kernel }}"` |  |
| `ecube_setup_cleanup_downloads` | `true` |  |
| `ecube_setup_no_tls` | `false` |  |
| `ecube_setup_demo` | `false` |  |
| `ecube_setup_run_setup_wizard` | `true` |  |
| `ecube_setup_http_port` | `"{{ 80 if ecube_setup_no_tls else 8443 }}"` |  |
| `ecube_setup_base_url` | `"{{ 'http' if ecube_setup_no_tls else 'https' }}://127.0.0.1:{{ ecube_setup_http_port }}"` |  |
| `ecube_setup_pg_port` | `5432` |  |
| `ecube_setup_pg_host` | `"{{ global_ip_address }}"` |  |
| `ecube_setup_mount_point` | `/nfs/backups` |  |
| `ecube_setup_backup_prefix` | `"ecube_"` |  |
| `ecube_setup_backup_filename` | `"{{ ecube_setup_backup_prefix }}{{ ansible_date_time.iso8601_basic_short }}.sqlc"` |  |
| `ecube_setup_backup_dir` | `"{{ ecube_setup_mount_point }}/ecube"` |  |
| `ecube_setup_backup_path` | `"{{ ecube_setup_backup_dir }}/{{ ecube_setup_backup_filename }}"` |  |
| `ecube_setup_trust_proxy_headers` | `false` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Update pg_hba.conf to allow password access using host ip address
- Update pg_hba.conf to allow password access using the database host ip address
- Install documented ECUBE host prerequisites
- Check for Ubuntu kernel exFAT support package
- Install Ubuntu kernel exFAT support package when available
- Create ECUBE download directory
- Download ECUBE package checksum
- Read ECUBE package checksum
- Set ECUBE package checksum fact
- Download ECUBE package archive
- Create ECUBE extraction directory
- Extract ECUBE package archive
- Remove conflicting deadsnakes apt source files
- Run ECUBE installer
- Remove ECUBE downloaded package
- Load setup.yml

## 🔔 Handlers
- Restart ECUBE
- Restart PostgreSQL
- Reload systemd daemon

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: ecube_setup
```