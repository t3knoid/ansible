cloudinit
======

The cloudinit role creates a cloudinit virtual machine template.

Requirements
------------

None

Role variables
--------------

- cloudinit_download_dest: cloud-init disk image download destination
- cloudinit_vmid: 9500
- cloudinit_memory_mb: 2048
- cloudinit_storage: local
- cloudinit_network_device: "virtio,bridge=vmbr0"
- cloudinit_scsi_controller_model: virtio-scsi-pci
- cloudinit_cpu_type: host

Dependencies
------------

None

Example Playbook
----------------

The following playbook creates a virtual machine cloud-init template.

      - name: Create a Template
        hosts: template
        gather_facts: false
        roles:
          - global
          - cloudinit
        become: true


