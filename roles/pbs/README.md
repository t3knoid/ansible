# 🛠️ Role: `pbs`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Installs and configures Proxmox Backup Server on Ubuntu systems.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
_No default variables found._

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Configure apt sources.list
- Download the Proxmox GPG key
- Update apt cache
- Proxmox Backup Server

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
- `redis_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: pbs
```