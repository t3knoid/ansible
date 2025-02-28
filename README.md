# Ansible

## Inventories

The following is a list of inventories.


| Inventory | Description |
|-----------|-------------|
|inventory/ansible/inventory.ini | Ansible Control Nodes |


## Playbooks

| Playbook | Description |
|-----------|-------------|
| playbooks/vms/create_cloud_init_iso.yml | Creates cloud_init.iso for use in Ubuntu autoinstall |
| playbooks/vms/create_vm.yml | Creates a virtual machine | 
| playbooks/vms/remove_vm.yml | Removes a VM |
| playbooks/vms/provision_vm.yml | Provisions a VM by cloning from a template |

## Roles

| Role | Description | Status |
|------|-------------|--------|
| vms  | Contains related tasks to manage virtual machines | Active |


