# 🛠️ Role: `java_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures Java on Debian/Ubuntu systems.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `java_setup_version` | `17.0.14.7.1` |  |
| `java_setup_major_version` | `"{{ java_setup_version.split('.')[0] }}"` |  |
| `java_setup_package` | `"java-{{ java_setup_major_version }}-amazon-corretto-jdk_{{ java_setup_version | regex_replace('\\.(?=[^.]*$)', '-') }}_amd64.deb"` |  |
| `java_setup_url` | `"https://corretto.aws/downloads/resources/{{ java_setup_version }}/{{ java_setup_package }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Remove default-jdk package
- Remove other Java versions
- Check if Java package already exists
- Download Java
- Install Java
- Remove Java Download
- Set Java alternatives
- Set javac alternatives
- Ensure Java home is set

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: java_setup
```