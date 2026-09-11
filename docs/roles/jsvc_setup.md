# 🛠️ Role: `jsvc_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Builds and installs Apache Commons Daemon JSVC from source.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (noble)
- Supported on: `Debian` (bookworm)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `jsvc_setup_commons_daemon_version` | `1.4.1` |  |
| `jsvc_setup_commons_daemon_package` | `"commons-daemon-{{ jsvc_setup_commons_daemon_version }}-src.tar.gz"` |  |
| `jsvc_setup_commons_daemon_root_url` | `"https://archive.apache.org/dist/commons/daemon/source"` |  |
| `jsvc_setup_extract_dir` | `/opt` |  |
| `jsvc_setup_java_home` | `"/usr/lib/jvm/java-{{ java_setup_major_version | default('17') }}-amazon-corretto"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install build dependencies for JSVC
- Check if JSVC is already built
- Extract JSVC source code
- Build JSVC
- Remove existing JSVC symlink
- Create JSVC symlink

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
- `java_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: jsvc_setup
```