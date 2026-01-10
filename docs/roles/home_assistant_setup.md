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
| `home_assistant_setup_qcow2_image` | `"{{ home_assistant_setup_qcow2_image_xz | replace('.xz', '') }}"` |  |
| `home_assistant_setup_vz_image_path` | `"/var/lib/vz/images/{{ vms_vmid }}"` |  |
| `home_assistant_setup_vz_image_full_path` | `"{{ home_assistant_setup_vz_image_path }}/{{ home_assistant_setup_qcow2_image }}"` |  |
| `home_assistant_setup_disk_storage` | `"{{ vms_config.storage | default('local') }}"` |  |
| `home_assistant_setup_disk_volume` | `"{{ home_assistant_setup_disk_storage }}:{{ vms_vmid }}/{{ home_assistant_setup_qcow2_image }}"` |  |
| `home_assistant_setup_vz_image_format` | `"qcow2"` |  |
| `home_assistant_setup_disk_id` | `"scsi0"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Get next available vmid
- Set home_assistant_setup_vmid fact
- Check if VM exists
- Show home_assistant_setup_vm_info debug
- Set MAC address fact if VM exists
- Create empty VM shell if missing
- Set Mac address fact from created VM
- Show Home Assistant VM creation result
- Flush handlers to download and prepare Home Assistant image
- Start the Home Assistant VM
- Show confirmation message
- Initialize home_assistant_setup_vm_interfaces by querying QEMU guest agent
- Wait for VM to report an IP address on the host NIC using its MAC address
- Extract the VM's IPv4 address
- Wait for Home Assistant Web UI to become accessible
- Show Home Assistant access information

## 🔔 Handlers
- Create temporary directory for qcow2.xz extraction
- Download Home Assistant QCOW2 image
- Decompress qcow2.xz
- Import qcow2 image
- Remove temporary directory
- Extract disk volume ID from import output
- Attach unused disk using qm set
- Configure boot order to boot from disk

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: home_assistant_setup
```