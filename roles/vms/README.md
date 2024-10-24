vms
=========

This role is used to manage virtual machine operations hosted in a Proxmox VE environment. Virtual management tasks include the following:

- Creating a virtual machine from scratch
- Deleting a virtual machine
- Cloning a virtual machine

Requirements
------------

The following Proxmox specific modules are used 
 
- [community.general.proxmox_kvm](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_kvm_module.html)
- [community.general.proxmox_nic](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_nic_module.html)
- [community.general.proxmox_disk](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_disk_module.html)
- [community.general.proxmox_vm_info](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_vm_info_module.html)
- [community.general.proxmox_template](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_template_module.html)

The following Python modules are required:
- proxmoxer
- requests

```bash
python -m pip install proxmoxer
python -m pip install requests
```

Role Variables
--------------

Ensure that global variables are loaded prior to using this role. This can be done from the playbook that calls this role as shown in the following example.

```yaml
- name: Create a VM
  hosts: vms
  gather_facts: false
  roles:
    - global
```

There are two variables that must be set, vms_config and vms_os . The vms_disk2 variable is optional.

- **vms_config** is a nested variable that provides values to configure the virtual machine hardware. Use the [proxmox_kvm_module](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_kvm_module.html#parameters) parameter values as reference for some of settings in this variable. Note that **vms_config.vms_disk2** is optional and only necessary if a second disk is required.
- **vms_os** determines which operating system iso image will be mounted and installed after the virtual machine is created.

```yaml
vms_config:
  agent: "1"
  cores: "4"
  cpu: host
  memory: 2048
  ostype: l26
  scsihw: virtio-scsi-single
  sockets: 1
  storage: linstor_storage
  vms_disk_os: 
    backup: true
    size: 20
    storage: linstor_storage
  vms_disk2:
    backup: true
    size: 20
    storage: linstor_storage

os: ubuntu_24_server
```

Use Cases
----------------

### Create a new VM

The following playbook calls the vm role and load tasks from the create.yml file.

```bash
- name: Create a VM
  hosts: vms
  gather_facts: false
  roles:
    - global

  tasks:
    - name: Create vm
      ansible.builtin.import_role:
        name: vms
        tasks_from: create
```

References
-----------
- [Introduction to autoinstall](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html)
- [Proxmox API - network-get-interfaces](https://pve.proxmox.com/pve-docs/api-viewer/index.html#/nodes/{node}/qemu/{vmid}/agent/network-get-interfaces)
- [Proxmox API - Execute QEMU commands](https://pve.proxmox.com/pve-docs/api-viewer/index.html#/nodes/{node}/qemu/{vmid}/monitor)