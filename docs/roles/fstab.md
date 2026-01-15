# 🛠️ Role: `fstab`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Manage fstab entries on Debian/Ubuntu.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (focal, jammy)

## ⚙️ Defaults
_No default variables found._

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Initialize fstab mounts list
- Calculate mounts to remove
- Store currently defined mount points for future reference
- Check if filesystems are mounted
- Unmount filesystems that are no longer defined
- Remove mount entries from /etc/fstab that are no longer defined
- Remove mount directories that are no longer defined
- Ensure mount directories exist
- Add mount entries to /etc/fstab
- Ensure mount entries are presently mounted

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: fstab
```