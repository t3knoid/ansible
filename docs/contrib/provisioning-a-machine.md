# Provisioning a Machine with `playbooks/provision_vm.yml`

This runbook explains how to provision a new virtual machine with `playbooks/provision_vm.yml` and what minimum inventory data must exist for the workflow to succeed.

The provisioning workflow creates a new virtual machine, installs Python so Ansible can manage it, joins the VM to Active Directory, applies the baseline configuration for Ansible nodes, provisions users, and prepares any additional disks for use. The result is a fully initialized, domain-joined, Ansible-ready VM with the expected hardware, networking, users, and storage.

For baremetal hosts, this playbook does not create the machine. It only runs the post-creation stages such as Python bootstrap, domain join, node preparation, user management, and disk preparation.

## 1. Login to an Ansible Control Node

Start on a control node with Ansible installed and activate the expected Python environment.

```shell
cd ~/ansible
source /opt/python_3.12/bin/activate
INV=inventory/test/inventory.ini
```

Important:

- Run this workflow from an Ansible control node.
- Make sure the control node can reach both Proxmox and the target network.

## 2. Pull the Latest Code

Update the local repository before making or deploying changes.

```shell
git pull origin main
```

Important:

- Pull first so inventory and role changes are based on the latest repository state.

## 3. Define the Host and Related Properties

Provisioning a new VM requires updates in three places.

### A. Define the host in the inventory

Edit the target inventory file, for example:

```text
inventory/test/inventory.ini
```

At minimum, define the host in these groups:

- `vms`
- `python`

Recommended:

- `linux`

Example:

```ini
[vms]
test-01 vms_proxmox_node=pve-1 vms_clone=false

[linux]
test-01

[python]
test-01
```

Pay special attention to these `[vms]` host variables:

- `vms_proxmox_node`: controls which Proxmox node will host the VM and where the provisioning tasks will target VM operations such as creation, cloud-init updates, start, stop, and reboot.
- `vms_clone`: controls whether the VM should be provisioned through the clone-based path instead of the normal non-clone creation path.

Why these groups matter:

- `vms` makes the VM creation stage run.
- `python` makes the Python bootstrap stage run.
- `linux` is not required by `playbooks/provision_vm.yml` itself, but it matches the normal inventory pattern used in this repository.

### B. Define the host IP address in global vars

Edit:

```text
roles/global/vars/main.yml
```

Add the host to `global_ip_addresses`:

```yaml
global_ip_addresses:
  test-01: 192.168.2.210
```

This is a critical prerequisite.

The provisioning workflow derives `global_ip_address` from that mapping, and the VM provisioning role uses it for cloud-init networking, DNS updates, and related host setup. If the hostname is missing from `global_ip_addresses`, the machine will not be provisioned correctly.

### C. Define VM hardware and OS configuration

Create or edit a host-specific vars file, for example:

```text
inventory/test/host_vars/test-01.yml
```

The minimum required variables for a VM are:

- `vms_config`
- `vms_os`
- `python3_version`

Example:

```yaml
vms_config:
  agent: "1"
  cores: "2"
  cpu: host
  memory: 1024
  ostype: l26
  scsihw: virtio-scsi-single
  sockets: 1
  storage: local
  disk_os:
    disk: virtio0
    backup: true
    size: 20
    storage: local
    format: qcow2
  nic0:
    model: virtio
    bridge: vmbr0
    tag: 20
  boot_order: "order=virtio0"
  disk2:
    disk: virtio1
    storage: local-lvm
    size: 20

vms_os: ubuntu_24_server
vms_autoinstall: true
vms_enable_serial_terminal: false
vms_additional_packages: []
python3_version: 3.12
```

If you prefer to share values across all hosts in an inventory, you can place them in `group_vars/all/main.yml` instead of `host_vars/<host>.yml`. The key requirement is that the host resolves these variables at runtime.

### D. `vms_config` parameter reference

| Parameter                      | Description                                                                               |
| ------------------------------ | ----------------------------------------------------------------------------------------- |
| `agent`                      | Enables the QEMU guest agent.                                                             |
| `cores`                      | Number of CPU cores.                                                                      |
| `sockets`                    | Number of CPU sockets.                                                                    |
| `cpu`                        | CPU type passed to Proxmox, such as`host`.                                              |
| `memory`                     | RAM in MB.                                                                                |
| `ostype`                     | Proxmox OS type identifier. This should match the operating system selected by`vms_os`. |
| `scsihw`                     | SCSI controller type.                                                                     |
| `storage`                    | Default Proxmox storage pool used by the VM definition.                                   |
| `disk_os.disk`               | Device name for the OS disk, such as`virtio0`.                                          |
| `disk_os.size`               | OS disk size in GB.                                                                       |
| `disk_os.storage`            | Physical Proxmox storage target for the OS disk.                                          |
| `disk_os.backup`             | Whether the OS disk is included in backups.                                               |
| `disk_os.format`             | Disk format such as`qcow2` or `raw`.                                                  |
| `nic0.model`                 | NIC model, usually`virtio`.                                                             |
| `nic0.bridge`                | Proxmox bridge, such as`vmbr0`.                                                         |
| `network.nic0.tag`           | VLAN tag for the primary interface. This determines network placement.                    |
| `boot_order`                 | Boot device order.                                                                        |
| `disk2.*`                    | Optional second disk configuration.                                                       |
| `vms_os`                     | OS template or installer identifier.                                                      |
| `vms_autoinstall`            | Enables unattended installation.                                                          |
| `vms_enable_serial_terminal` | Enables serial console configuration.                                                     |
| `vms_additional_packages`    | Extra packages installed during autoinstall.                                              |
| `python3_version`            | Python version used by the bootstrap stage.                                               |

Pay special attention to these settings:

- `vms_config.ostype` controls the Proxmox OS type and should align with `vms_os` so the VM definition matches the operating system being installed.
- `vms_config.disk_os.storage` controls the physical storage location of the boot disk.
- `vms_config.network.nic0.tag` controls the VLAN placement of the VM's primary network interface.

## 4. Commit Configuration Changes

After editing the inventory and global vars, commit the changes.

```shell
git add inventory/test/
git add roles/global/vars/main.yml
git commit -m "Provision new VM test-01 with defined hardware and IP"
git push origin main
```

Important:

- Replace `test-01` with the real VM name.
- Commit inventory and IP mapping changes together so the repository history reflects the full provisioning request.

## 5. Deploy Using the Provisioning Playbook

Run the provisioning workflow:

```shell
ansible-playbook -i $INV playbooks/provision_vm.yml -k
```

Notes:

- Use `-k` if SSH password prompting is required.
- Use `--limit <hostname>` if you only want to act on a single host in a larger inventory.

Example:

```shell
ansible-playbook -i inventory/loki/inventory.ini playbooks/provision_vm.yml --limit loki-0 -k
```

## 6. Verify Deployment

After the playbook completes:

1. Log into Proxmox.
2. Confirm the VM exists.
3. Confirm the VM is powered on.
4. Confirm the CPU, memory, disks, and NIC configuration match the requested values.
5. Confirm the assigned IP matches the entry in `global_ip_addresses`.
6. If autoinstall is enabled, confirm the operating system installation completes successfully.
7. Confirm the machine is joined to the domain and is reachable for follow-up Ansible runs.

## What `playbooks/provision_vm.yml` Calls

The top-level playbook is an orchestration wrapper around six imported playbooks.

### 1. `playbooks/vms/provision_vm.yml`

This stage creates the virtual machine.

What it does:

- targets the `vms` group
- applies the `global` role
- refreshes local DNS entries through Pi-hole tasks
- provisions through either Terraform-backed or Ansible-native VM tasks depending on `vms_use_terraform`

### 2. `playbooks/python/bootstrap_python3.yml`

This stage installs Python so Ansible can manage the host with normal modules.

What it does:

- targets the `python` group
- runs the `python3` role bootstrap tasks

### 3. `playbooks/ad/join_domain.yml`

This stage joins the host to Active Directory.

What it does:

- targets `vms`, `baremetal`, and `wsl`
- applies the `global` role
- imports the `ad` role

### 4. `playbooks/ansible/prep_ansible_node.yml`

This stage applies the repository baseline for managed nodes.

What it does:

- targets `vms`, `baremetal`, and `wsl`
- applies the `global` role
- applies the `ansible_node` role

### 5. `playbooks/vms/add_users.yml`

This stage provisions the standard users.

What it does:

- targets `vms` and `baremetal`
- applies the `global` role
- applies the `users` role

### 6. `playbooks/vms/prep_disk.yml`

This stage prepares additional local disks.

What it does:

- targets `vms` and `baremetal`
- applies the `disks` role
- formats and mounts extra disks declared through inventory variables such as `disk2` and `disks_disk_mounts`

## Minimum Requirements Summary

For a new VM, the minimum repository changes are:

1. Add the host to `inventory/<name>/inventory.ini` under `vms` and `python`.
2. Add the host IP to `roles/global/vars/main.yml` under `global_ip_addresses`.
3. Define `vms_config`, `vms_os`, and `python3_version` for the host.

For baremetal preparation with the same playbook, the machine must already exist and the minimum inventory contract is:

1. Add the host to `inventory/<name>/inventory.ini` under `baremetal` and `python`.
2. Add the host IP to `roles/global/vars/main.yml` under `global_ip_addresses`.
3. Define `python3_version` and any role-specific variables needed by `ad`, `ansible_node`, `users`, or `disks`.

## Notes

- Always double-check the hostname, IP address, storage target, VLAN tag, and requested hardware before deploying.
- Use the same workflow for both new VM provisioning and later hardware updates.
- Pulling first, committing the inventory change, and then deploying keeps the repository state consistent.
- The control node must have network access to the Proxmox cluster and to the target environment.
