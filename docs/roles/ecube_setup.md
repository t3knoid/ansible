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
| `ecube_setup_no_tls` | `false` |  |
| `ecube_setup_demo` | `false` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install ECUBE installer prerequisites
- Create ECUBE download directory
- Download ECUBE package checksum
- Read ECUBE package checksum
- Set ECUBE package checksum fact
- Download ECUBE package archive
- Create ECUBE extraction directory
- Extract ECUBE package archive
- Run ECUBE installer
- Remove ECUBE downloaded package

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
- `postgresql_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: ecube_setup
```