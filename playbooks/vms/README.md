# 📚 Playbooks in `vms`

| Playbook | Purpose |
|----------|---------|
| [`add_disk.yml`](add_disk.md) | Adds additional disks to virtual machines. |
| [`add_users.yml`](add_users.md) | Adds users to virtual machines and bare metal servers. |
| [`convert_to_template.yml`](convert_to_template.md) | Converts virtual machines to templates. |
| [`create_cloud_init_iso.yml`](create_cloud_init_iso.md) | Creates a cloud-init ISO for virtual machines to enable autoinstallation. |
| [`create_vm.yml`](create_vm.md) | Creates virtual machines and manages their DNS entries. |
| [`create_vm_snapshot.yml`](create_vm_snapshot.md) | Creates snapshots of virtual machines. |
| [`deploy_autofs.yml`](deploy_autofs.md) | Deploys and configures autofs on designated servers. |
| [`deploy_sshpass.yml`](deploy_sshpass.md) | Deploys sshpass utility on virtual machines. |
| [`force_reboot_vm.yml`](force_reboot_vm.md) | Forces a reboot of virtual machines by stopping and starting them. |
| [`install_vm_packages.yml`](install_vm_packages.md) | Installs required packages on virtual machines. |
| [`list_vm_snapshot.yml`](list_vm_snapshot.md) | Lists snapshots of virtual machines. |
| [`migrate_vm.yml`](migrate_vm.md) | Migrates virtual machines to different hosts or storage. |
| [`prep_disk.yml`](prep_disk.md) | Prepares and formats local disks on virtual machines and bare metal servers. |
| [`provision_vm.yml`](provision_vm.md) | Provisions virtual machines using either Terraform or Ansible, managing DNS entries accordingly. |
| [`reboot_vm.yml`](reboot_vm.md) | Reboots virtual machines gracefully. |
| [`remove_vm.yml`](remove_vm.md) | Removes virtual machines using either Terraform or Ansible, with confirmation and DNS cleanup. |
| [`remove_vm_snapshot.yml`](remove_vm_snapshot.md) | Removes snapshots from virtual machines. |
| [`revert_vm_snapshot.yml`](revert_vm_snapshot.md) | Reverts virtual machines to a specified snapshot and starts them. |
| [`set_dns_servers.yml`](set_dns_servers.md) | Sets DNS servers on virtual machines and bare metal servers. |
| [`show_vm_id.yml`](show_vm_id.md) | Displays the VMID of virtual machines. |
| [`show_vm_node.yml`](show_vm_node.md) | Displays the Proxmox node hosting the specified virtual machines. |
| [`shutdown_vm.yml`](shutdown_vm.md) | Shuts down virtual machines gracefully. |
| [`start_vm.yml`](start_vm.md) | Starts a virtual machine. |
| [`stop_vm.yml`](stop_vm.md) | Stops a virtual machine. |
| [`update_known_hosts.yml`](update_known_hosts.md) | Updates the known_hosts file with the SSH fingerprints of all virtual machines. |
| [`upgrade_vm_os.yml`](upgrade_vm_os.md) | Upgrades the operating system of virtual machines. |