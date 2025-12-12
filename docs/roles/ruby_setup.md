# 🛠️ Role: `ruby_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
The ruby_setup role builds and install Ruby from it's [https://www.ruby-lang.org/en/downloads/](source code).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `ruby_setup_version` | `3.3.7` |  |
| `ruby_setup_major_minor_version` | `"{{ ruby_setup_version | regex_replace('\\.\\d+$', '') }}"` |  |
| `ruby_setup_archive` | `"ruby-{{ ruby_setup_version }}.tar.gz"` |  |
| `ruby_setup_archive_extractdir_root` | `/tmp` |  |
| `ruby_setup_archive_extractdir` | `"{{ ruby_setup_archive_extractdir_root }}/{{ ruby_setup_archive | regex_replace('\\.tar\\.gz$', '') }}"` |  |
| `ruby_setup_download_url` | `"https://cache.ruby-lang.org/pub/ruby/{{ ruby_setup_major_minor_version }}/{{ ruby_setup_archive }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install development tools and header files
- Ensure extraction folder exists
- Download and extract Ruby source code
- Build Ruby
- Configure openssl support

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: ruby_setup
```