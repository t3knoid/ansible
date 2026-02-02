# 🛠️ Role: `cloudinit`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Provides tasks to create a virtual machine with cloud-init support.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `cloudinit_template_os` | `"ubuntu_24_server"` |  |
| `cloudinit_template` | `"{{ template[cloudinit_template_os] }}"` |  |
| `cloudinit_template_name` | `"{{ cloudinit_template.name }}"` |  |
| `cloudinit_vmid` | `"{{ cloudinit_template.vmid }}"` |  |
| `cloudinit_memory_mb` | `"{{ cloudinit_template.memory_mb }}"` |  |
| `cloudinit_storage` | `"{{ cloudinit_template.storage }}"` |  |
| `cloudinit_network_device` | `"{{ cloudinit_template.network_device }}"` |  |
| `cloudinit_scsi_controller_model` | `"{{ cloudinit_template.scsi_controller_model }}"` |  |
| `cloudinit_cpu_type` | `"{{ cloudinit_template.cpu_type }}"` |  |
| `cloudinit_agent_enabled` | `"{{ cloudinit_template.agent_enabled | default(true, true) }}"` |  |
| `cloudinit_proxmox_node` | `"{{ cloudinit_template.proxmox_node }}"` |  |
| `cloudinit_download_dest` | `"/tmp/{{ global_os[cloudinit_template_os].cloudinit_img }}"` |  |
| `cloudinit_ostype` | `"{{ cloudinit_template.ostype | default('l26', true) }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Ensure required packages are installed
- Download Ubuntu cloud image
- Load JSON .vmlist file content from proxmox node
- Check if virtual machine exists
- Remove existing virtual machine
- Ensure VM is created
- Set virtio disk for VM
- Add Cloud-Init CD-ROM drive
- Set to boot from virtio0
- Configure serial console as a display
- Configure virtual machine into a template
- Cleanup Cloud-Init image

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: cloudinit
```