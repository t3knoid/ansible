# Role: `autofs`

## 📖 Overview
Installs and configures autofs on Debian/Ubuntu.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (focal, jammy)

## 🧮 Defaults
_No default variables found in defaults._

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Install autofs
- Configure /etc/auto.master
- Append NFS mounts to auto.nfs

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: autofs
```