# 🛠️ Role: `disks`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Prepares an attached disk by formatting and mounting to a defined mountpoint. Removes mounts from fstab that is associated with a none existing device.


## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `disks_disk_mounts` | `[]` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Run lsblk command to get disk info
- Display lsblk output
- Extract valid devices from lsblk output
- Display disks_valid_devices
- Read current fstab
- Decode fstab content
- Split fstab content into separate line items
- Initialize disks_filtered_fstab
- Filter fstab line-by-line and remove mounts that are associated with an invalid device
- Compare fstab contents
- Backup original fstab only if there is a change in fstab
- Write filtered fstab only if there is a change in fstab
- Find unformatted disks
- Display unformatted disks
- Create an ext4 primary partition
- Format the drive
- Run lsblk command to get disk info
- Display lsblk output
- Find ummounted disks
- Display ummounted disks
- Ensure mountpoint exists
- Mount disks
- Ensure mounted disk has proper ownership

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: disks
```