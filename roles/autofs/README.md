# 🛠️ Role: `autofs`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures autofs on Debian/Ubuntu.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (focal, jammy)

## ⚙️ Defaults
_No default variables found._

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install autofs
- Configure /etc/auto.master
- Append NFS mounts to auto.nfs

## 🔔 Handlers
- Restart autofs

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: autofs
```