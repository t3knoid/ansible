# 🛠️ Role: `home_assistant_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs Home Assistant using its QCOW2 image on a Proxmox VE host.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `home_assistant_setup_version` | `"16.3"` |  |
| `home_assistant_setup_qcow2_image_xz` | `"haos_ova-{{ home_assistant_setup_version }}.qcow2.xz"` |  |
| `home_assistant_setup_qcow2_image_url_base` | `"https://github.com/home-assistant/operating-system/releases/download/{{ home_assistant_setup_version }}"` |  |
| `home_assistant_setup_qcow2_image_url` | `"{{ home_assistant_setup_qcow2_image_url_base }}/{{ home_assistant_setup_qcow2_image_xz }}"` |  |
| `home_assistant_setup_qcow2_image` | `"{{ home_assistant_setup_qcow2_image_xz | replace('.xz','') }}"` |  |
| `home_assistant_setup_vz_image_path` | `"/var/lib/vz/images/{{ vms_vmid }}"` |  |
| `home_assistant_setup_vz_image_full_path` | `"{{ home_assistant_setup_vz_image_path }}/{{ home_assistant_setup_qcow2_image }}"` |  |
| `home_assistant_setup_disk_volume` | `"local:{{ vms_vmid }}/{{ home_assistant_setup_qcow2_image }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Create empty VM shell
- Flush handlers to download and prepare Home Assistant image
- Check if scsi1 already attached
- Execute `qm disk rescan` on Proxmox node
- Attach unused disk using qm set
- Configure boot order to boot from disk
- Start the Home Assistant VM
- Show final message
- Wait for Home Assistant to start

## 🔔 Handlers
- Check if Home Assistant image already exists
- Create VM image path directory
- Create temporary directory for qcow2.xz extraction
- Download Home Assistant QCOW2 image
- Decompress qcow2.xz
- Move qcow2 to Proxmox VM images directory
- Remove temporary directory

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: home_assistant_setup
```