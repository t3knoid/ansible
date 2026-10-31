# Creating TrueNAS VMs with Ansible: Contributor Guide

VMs on TrueNAS hosts are declared as data in the `truenas_vms` variable and reconciled by the `truenas_api` module in `mode: vm`. The workflow uses the same plan/apply pattern as TrueNAS Apps:

1. Validate every declaration (`vms_validate.yml`) before touching the host.
2. Run the read-only preflight and confirm the host supports virtualization.
3. For each VM, plan (the default) or apply changes through the local middleware API.
4. Print a redacted report: actions, device changes, runtime state and any approvals still required.

Nothing changes on the host until you run with `truenas_vms_mode=apply`.

## 2. File map

| Path | Purpose |
| --- | --- |
| `playbooks/truenas/deploy_truenas_vms.yml` | Playbook. Imports the role's `vms.yml` (tag `truenas_vms`). |
| `roles/truenas/tasks/vms.yml` | Entry point: validate, preflight, virtualization check, per-VM reconcile, report. |
| `roles/truenas/tasks/vms_validate.yml` | Validates declarations before any host contact. |
| `roles/truenas/defaults/main.yml` | Defaults: `truenas_vms`, `truenas_vms_mode`, job/health/poll timeouts. |
| `library/truenas_api.py` | The module. `mode: vm` does the reconcile work. |
| `inventory/truenas/host_vars/truenas-01/default.yml` | VM declarations for `truenas-01`. |
| `inventory/truenas/host_vars/truenas-01/vault.yml` | Vaulted secrets, including the VM display password. |

The authoritative list of module options, defaults and choices is the `DOCUMENTATION` block in the module (`ansible-doc -M library truenas_api`). If this guide and the module disagree, the module wins and this guide should be fixed.

## 3. Prerequisites

Before declaring a VM, make sure that:

- **Virtualization is enabled** in the host BIOS/UEFI (VT-x or AMD-V). The playbook stops with a clear message if the host does not report support.
- **The parent dataset of each zvol exists**, for example `Data/vms`. The module creates the zvol, not its parent.
- **The network bridge or interface exists** on TrueNAS (for example `br20`). A NIC's `attach` names an existing one.
- **There is enough free memory.** VMs are started without memory overcommit, so TrueNAS refuses to start a VM that does not fit.
- **Install media is available** if you are installing an OS, for example an ISO under `/mnt/<pool>/isos/`.
- **The display password is in the vault** (at least 8 characters).

## 4. Declaring a VM

VMs are declared per host in `inventory/truenas/host_vars/<host>/default.yml`:

```yaml
truenas_vms:
  - name: ansible
    description: Ansible controller
    runtime: running              # running | stopped
    cpu:
      vcpus: 2
      cores: 1
      threads: 2
      mode: HOST-PASSTHROUGH
    memory_mib: 4096
    bootloader: UEFI              # UEFI | UEFI_CSM
    time: LOCAL
    enable_secure_boot: false
    shutdown_timeout: 90
    autostart: true
    disks:
      - zvol: Data/vms/ansible-naa1gkr
        size_gib: 40
        type: AHCI
        order: 1001
    nics:
      - attach: br20
        type: E1000
        trust_guest_rx_filters: false
        order: 1003
    display:
      bind: 0.0.0.0
      type: VNC
      password: "{{ vault_truenas_vms_display_password }}"
      port: 5900
      resolution: 1920x1080
      web_port: 5902
      wait: false
      web: false
      order: 1002
    allow_restart: false          # permit stop/start for CPU or memory changes
    allow_delete: false           # required for state: absent
    allow_disk_delete: false      # required to destroy zvols on delete
```

### Top-level keys

| Key | Required | Default | Notes |
| --- | --- | --- | --- |
| `name` | yes |  | Unique per host. Letters, digits and underscores, starting with a letter, at most 40 characters. The name is the VM's identity. |
| `description` | no | empty | Free text. |
| `state` | no | `present` | `present` or `absent`. |
| `runtime` | no | `running` | `running` or `stopped`. |
| `cpu` | no | 1 / 1 / 1 | `vcpus`, `cores`, `threads`, and `mode` (CPU model mode, for example `HOST-PASSTHROUGH`). |
| `memory_mib` | yes, when present |  | At least 256. |
| `bootloader` | no | `UEFI` | `UEFI` or `UEFI_CSM`. |
| `time` | no |  | Guest clock basis, `LOCAL` or `UTC`. |
| `enable_secure_boot` | no | `false` | Secure boot for UEFI guests. |
| `shutdown_timeout` | no |  | Seconds TrueNAS waits for a graceful guest shutdown before forcing. |
| `autostart` | no | `false` | Start the VM when TrueNAS boots. |
| `disks` | yes, when present |  | List of zvol-backed disks. |
| `nics` | yes, when present |  | List of network interfaces. |
| `cdrom` | no |  | Install ISO path. An empty string removes the CD-ROM device. |
| `display` | no |  | Console device. |
| `allow_restart` | no | `false` | Approves stopping and restarting a running VM. |
| `allow_delete` | no | `false` | Required for `state: absent`. |
| `allow_disk_delete` | no | `false` | Also destroys the zvols when deleting. |

### Device keys

| Device | Keys |
| --- | --- |
| `disks[]` | `zvol` (required, `pool/path`), `size_gib` (required), `type` (`VIRTIO` or `AHCI`), `sparse` (default `true`), `order` |
| `nics[]` | `attach` (required), `type` (`VIRTIO` or `E1000`), `mac`, `trust_guest_rx_filters`, `order` |
| `display` | `type` (`VNC` or `SPICE`), `bind`, `password`, `port`, `web_port`, `resolution`, `web`, `wait`, `order` |

`order` controls device ordering (lower values first). Pick `AHCI` and `E1000` for guests without VirtIO drivers, and `VIRTIO` otherwise.

### Secrets

The display password lives in `inventory/truenas/host_vars/truenas-01/vault.yml` as `vault_truenas_vms_display_password` and is referenced from `default.yml`. Edit it with `ansible-vault edit`. Note that `bind: 0.0.0.0` exposes the console on every interface. Prefer the management IP where you can.

## 5. Walkthrough: create a new VM

### Step 1: Prepare storage and network

Confirm the parent dataset (for example `Data/vms`) and the bridge (for example `br20`) exist on the TrueNAS host. If you will install from media, copy the ISO to a dataset and note its `/mnt/...` path.

### Step 2: Add the declaration

Add a new entry to `truenas_vms` in `default.yml`, using the example above as a template. For an OS install, add `cdrom: /mnt/<pool>/isos/<image>.iso`. Leave all `allow_*` flags `false`.

### Step 3: Add the display password to the vault

```bash
ansible-vault edit inventory/truenas/host_vars/truenas-01/vault.yml
```

### Step 4: Plan

Plan is the default mode, so this changes nothing on the host:

```bash
ansible-playbook playbooks/truenas/deploy_truenas_vms.yml -i inventory/truenas --limit truenas-01
```

Omit `-i` if `ansible.cfg` already sets the inventory. For a brand-new VM the report looks like this (illustrative):

```text
name: ansible
actions: [create_zvol:Data/vms/ansible-naa1gkr, create, create_device:DISK, create_device:NIC, create_device:DISPLAY, start]
planned: true
runtime_state: ABSENT
approval_required: []
```

Review the actions before continuing. If `approval_required` is not empty, see section 7.

### Step 5: Apply

```bash
ansible-playbook playbooks/truenas/deploy_truenas_vms.yml -i inventory/truenas --limit truenas-01 -e truenas_vms_mode=apply
```

The module creates the zvol, creates the VM and its devices, starts it if `runtime: running`, and waits until TrueNAS reports the desired state.

### Step 6: Verify

Check the VM under Virtual Machines in the TrueNAS UI and connect to the console. Then run the playbook again in plan mode. A second run should report no actions.

### Step 7: Remove the install media

After the OS is installed, set `cdrom: ""` and apply to remove the CD-ROM device. On a running VM this counts as a restart-requiring change (see section 7), so either stop the guest first or set `allow_restart: true` for that run.

## 6. Reading the report

| Field | Meaning |
| --- | --- |
| `name` | The VM. |
| `actions` | Steps planned (plan mode) or performed (apply mode), in execution order. Empty means the VM is in sync. |
| `device_changes` | Device-level detail of planned or performed changes, when any. |
| `planned` | `true` when nothing was changed because of plan mode or check mode. |
| `runtime_state` | Observed state in plan mode, or the state reached in apply mode. `ABSENT` means no such VM. |
| `approval_required` | Approval flags blocking the change, for example `[allow_restart]`. |

Action names: `create_zvol:<path>`, `grow_zvol:<path>`, `stop`, `create`, `update`, `create_device:<TYPE>`, `update_device:<TYPE>`, `delete_device:<TYPE>`, `start`, `delete`, `delete_zvols`.

`runtime_state` reflects the hypervisor state (`RUNNING` or `STOPPED`), not guest health. A guest stuck in an installer or a hung kernel still reports `RUNNING`.

## 7. Safety rules

| Situation | Behavior |
| --- | --- |
| Changing CPU, memory, bootloader or any device on a **running** VM | Requires `allow_restart: true`. Without it the plan shows `approval_required: [allow_restart]` and apply fails before changing anything. With it, the module stops the VM, applies the change and starts it again. |
| Declaring `runtime: stopped` for a running VM | Not gated. Stopping is the declared intent. |
| `state: absent` | Requires `allow_delete: true`. A running VM is stopped first. Zvols are destroyed only if `allow_disk_delete: true`. |
| Shrinking a disk | Refused with an error, even in plan mode. |
| Growing a disk | Done online by growing the zvol. Resize the filesystem inside the guest yourself. |
| Devices on the VM that are not declared | Never removed. The only deletion is `cdrom: ""`. |
| Display password | Cannot be read back from TrueNAS. It is sent on create and whenever another display attribute changes. To rotate it, change another display attribute in the same run. |

Keep every `allow_*` flag `false` in inventory. For a maintenance window, set the flag, apply, and set it back to `false` in the same change request.

## 8. Common tasks

**Change memory or CPU.** Edit the values, plan, and expect `approval_required: [allow_restart]` if the VM is running. Set `allow_restart: true`, apply, then set it back to `false`.

**Grow a disk.** Increase `size_gib`, plan (expect `grow_zvol`), apply, then resize the filesystem in the guest.

**Stop or start a VM.** Set `runtime: stopped` or `runtime: running` and apply.

**Delete a VM.** Set `state: absent` and `allow_delete: true`, adding `allow_disk_delete: true` if the zvols should be destroyed too. Plan, review, then apply. Back up anything you need first.

Removing an entry from `truenas_vms` does **not** delete the VM. The module only manages VMs that are declared.

## 9. Validation

`vms_validate.yml` runs before any host contact and checks that:

- the mode is `plan` or `apply` and the timeouts are positive;
- `truenas_vms` is a list of mappings with unique, valid names;
- only known keys are used, with valid values for state, runtime and bootloader;
- present VMs have memory, at least one disk with a valid zvol path and size, and at least one NIC;
- display passwords are at least 8 characters;
- no zvol is shared between VMs.

If you add a new key, it must be added to the allowed-keys list in this file as well as to the module.

## 10. Troubleshooting

| Symptom | Likely cause and fix |
| --- | --- |
| Host does not report virtualization support | Enable VT-x or AMD-V in the BIOS/UEFI. |
| Parent dataset for zvol does not exist | Create the parent (for example `Data/vms`) first. |
| Refusing to shrink zvol | `size_gib` is below the current size. Restore the old value. |
| Restarting a running VM requires `allow_restart: true` | Approve it for the maintenance window (section 7). |
| VM deletion requires `allow_delete: true` | Set the flag deliberately after taking backups. |
| VM did not reach RUNNING | Check the VM in the UI. Look for insufficient free memory or a boot problem, or raise `truenas_vms_health_timeout`. |
| Job timed out | The job may still be running. Inspect TrueNAS before retrying. |
| Display needs a password of at least 8 characters | Check the vault variable is defined and long enough. |
| Unknown or unsupported key | A typo, or a new key missing from the allowed list or the module argument spec. |
| Output shows `censored` | Tasks use `no_log`. Rerun with `-e truenas_no_log=false` on a trusted terminal only. Never use `-vvv` for this, as module parameters include the display password. |
| Device errors after a TrueNAS upgrade | The device payload shape may have changed. Check `vm_device_shape()` in the module against the API docs. |

## 11. Contributing changes

When adding or changing a VM option:

1. Add it to the `vm` suboptions in the module's `main()` argument spec.
2. Document it in the module's `DOCUMENTATION` block, and confirm the YAML still parses with `ansible-doc -M library truenas_api`.
3. Implement it in `run_vm`. If changing it requires a restart, add it to the restart-sensitive keys.
4. Allow it in `vms_validate.yml` and add any validation it needs.
5. Update the commented example in `defaults/main.yml` and this guide.
6. Check field names and payloads against the API docs on the host at `https://<truenas-host>/api/docs/`, because they vary between TrueNAS releases.

Test on a throwaway VM:

1. Plan, then apply with `runtime: stopped`.
2. Run plan again. It must report no actions.
3. Change the new option. The plan must show exactly that change.
4. Apply, then plan again to confirm there is no drift.
5. Run once with `--check --diff` to confirm check mode makes no changes.

Guidelines:

- Keep `no_log: "{{ truenas_no_log }}"` on every task that handles VM definitions.
- Plan mode and check mode must be free of side effects.
- Never delete devices or data the declaration does not explicitly ask to remove.
- New destructive behavior needs its own `allow_*` approval flag.

## 12. Known limitations

- The VM name is its identity. Renaming creates a new VM and leaves the old one.
- Changing a disk's `zvol` attaches a new disk and leaves the old one. Disks are matched by zvol path, and other devices by position within their type.
- Extra devices are never removed, and disks never shrink.
- The display password cannot be compared, so password-only changes are not detected.
- Health checks are hypervisor-level only. Use a separate guest-level check (for example SSH reachability) if you need one.
