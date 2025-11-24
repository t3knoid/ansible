# Role: `cloudinit`

## 📖 Overview
Provides tasks to create a virtual machine with cloud-init support.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## 🧮 Defaults
- `cloudinit_download_dest`: `"/tmp/{{ global_os[cloudinit_template_os].cloudinit_img }}"`
- `cloudinit_memory_mb`: `2048`
- `cloudinit_storage`: `local`
- `cloudinit_network_device`: `"virtio,bridge=vmbr0"`
- `cloudinit_scsi_controller_model`: `virtio-scsi-pci`
- `cloudinit_cpu_type`: `host`
- `cloudinit_agent_enabled`: `true`

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
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

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: cloudinit
```