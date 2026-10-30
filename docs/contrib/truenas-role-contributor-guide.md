# 📘 TrueNAS Role Contributor Guide

The `truenas` role configures an already-installed TrueNAS 25.10+ system through its local middleware API. It manages updates, local groups and users, the administrator account, network settings and Active Directory, datasets, shares, and services. Virtual machines use a separate, opt-in workflow and playbook. The role does not install TrueNAS or provision its initial boot disk.

## 📋 Requirements and Bootstrap

- Ansible 2.14 or newer on the control node.
- TrueNAS 25.10 or newer. The role checks the version before making changes.
- SSH access to the NAS using the inventory connection user. In this repository inventory, [`inventory/truenas/inventory.ini`](../../inventory/truenas/inventory.ini) sets `ansible_user=ansible` for `truenas-01`.
- The initial local administrator must already have been configured in the TrueNAS web UI. The role fails with a setup hint if it has not.

Before the first run, enable SSH in the TrueNAS UI for the inventory connection user, confirm that user can become root, and install its Ansible public key if you want passwordless runs. The role executes its custom `truenas_api` module on the NAS; it uses the built-in `truenas_api_client` when available and otherwise calls `midclt`. It does not install packages on TrueNAS or use web UI credentials.

If the inventory connection user does not have key-based SSH configured yet, run the playbook with `-k` to prompt for that user's SSH password. In this repository inventory, that means entering the password for `ansible_user=ansible`. Keep `--ask-vault-pass` separate; it prompts for the Ansible vault secret, not the SSH password.

## 📝 Repository Workflow

The repository deployment inventory is [`inventory/truenas/inventory.ini`](../../inventory/truenas/inventory.ini), and the main configuration playbook is [`playbooks/truenas/configure_truenas.yml`](../../playbooks/truenas/configure_truenas.yml). VM management is invoked separately with [`playbooks/truenas/deploy_truenas_vms.yml`](../../playbooks/truenas/deploy_truenas_vms.yml). Host variables belong under `inventory/truenas/host_vars/truenas-01/`; files elsewhere beside the inventory are not automatically loaded by Ansible.

Contributors should add or edit the host variable files directly. Define only the sections you want the role to manage, keep secrets in an encrypted vault file, and keep environment-specific values out of role defaults.

```bash
$EDITOR inventory/truenas/host_vars/truenas-01/default.yml inventory/truenas/host_vars/truenas-01/vault.yml
ansible-vault encrypt inventory/truenas/host_vars/truenas-01/vault.yml

ansible-inventory -i inventory/truenas/inventory.ini --host truenas-01 --yaml
ansible-playbook -i inventory/truenas/inventory.ini playbooks/truenas/configure_truenas.yml --syntax-check
ansible-playbook -i inventory/truenas/inventory.ini playbooks/truenas/configure_truenas.yml --check --diff -k --ask-vault-pass
ansible-playbook -i inventory/truenas/inventory.ini playbooks/truenas/configure_truenas.yml -k --ask-vault-pass
```

If the `ansible` account already has a working SSH key on the NAS, you can omit `-k`. When contributing new behavior, validate it against the repository inventory unless the change is intentionally generic and inventory-agnostic. Keep role defaults focused on interface documentation and safe defaults, and put site-specific configuration in inventory host vars.

## 🔢 Execution Order

The role always begins with preflight checks, then runs enabled configuration stages in this order:

1. **Preflight:** wait for middleware readiness, check the minimum version, and verify the initial administrator exists.
2. **Update:** optionally download and install a TrueNAS update into a new boot environment, with an optional reboot.
3. **Groups:** ensure configured local groups.
4. **Administrator:** manage the fixed local account `truenas_admin` and add it to `truenas_admin_groups`.
5. **Users:** ensure local users and resolve configured group names to IDs.
6. **Network and Active Directory:** apply network configuration first, then configure/join AD if requested.
7. **Datasets:** create or update configured datasets.
8. **Shares and resources:** manage SMB/NFS shares, additional middleware resources, then raw post-configuration API calls.
9. **Services:** configure service autostart and start or stop each configured service.

The order allows groups and users to exist before shares are exposed and datasets to exist before shares are configured. Services are started last.

VM management is not part of `configure_truenas.yml` or the normal role task sequence. The isolated VM playbook imports `roles/truenas/tasks/vms.yml`, validates all declarations before connecting to middleware, checks virtualization support, and then plans or applies each VM. Configure `truenas_vms` in the inventory host vars and run that playbook explicitly.

## 🔗 How Inputs Map To The API

Most role variables map directly to TrueNAS middleware methods.

| Role input                       | TrueNAS API surface                                                  |
| -------------------------------- | -------------------------------------------------------------------- |
| `truenas_groups`                 | `group.create` / `group.update` / `group.delete`                     |
| `truenas_admin`, `truenas_users` | `user.create` / `user.update` / `user.delete`                        |
| `truenas_network_configuration`  | `network.configuration.update`                                       |
| `truenas_ad`                     | `directoryservices.update`                                           |
| `truenas_datasets`               | `pool.dataset.create` / `pool.dataset.update`                        |
| `truenas_smb_shares`             | `sharing.smb.create` / `sharing.smb.update` / `sharing.smb.delete`   |
| `truenas_nfs_shares`             | `sharing.nfs.create` / `sharing.nfs.update` / `sharing.nfs.delete`   |
| `truenas_resources`              | `<namespace>.query/create/update/delete`                             |
| `truenas_post_calls`             | Raw `midclt` / middleware method calls                               |
| `truenas_services`               | `service.update`, `service.started`, `service.start`, `service.stop` |
| `truenas_vms`                    | `vm.query/create/update/delete`, `vm.device.*`, runtime methods, and `pool.dataset.*` for disk zvols |

The role is intentionally thin. If a field is accepted by the underlying API method and the role passes that object through unchanged, configure it exactly as the TrueNAS API expects.

## ⚙️ Configuration Reference

All role inputs are declared in [`defaults/main.yml`](defaults/main.yml); unset lists and maps default to empty, so their stages are skipped. Treat that file as the canonical variable contract when adding or reviewing new settings.

| Variable                                          | Purpose and behavior                                                                                                                                                                                                       |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `truenas_become`                                  | Become root for local middleware access; defaults to `true`.                                                                                                                                                               |
| `truenas_no_log`                                  | Hide task arguments/results that may include secrets; defaults to `true`. Disable only for temporary debugging.                                                                                                            |
| `truenas_min_version`                             | Minimum accepted major/minor version; defaults to `25.10`.                                                                                                                                                                 |
| `truenas_update_enabled`, `truenas_update_reboot` | Opt into updates and optionally reboot into the new boot environment. Both default to `false`. `truenas_update_train` and `truenas_update_version` optionally pin a train or version.                                      |
| `truenas_groups`                                  | `group.create` configuration. Each item supports `state: absent`; `gid` is create-only.                                                                                                                                    |
| `truenas_admin`                                   | Optional subset of `user.create` fields for `truenas_admin`. Only listed settings are compared and updated. Its password is used only when creating the account.                                                           |
| `truenas_admin_groups`                            | Local groups granting administrator privilege; defaults to `[builtin_administrators]`. The role warns if a configured group does not appear in `privilege.query`.                                                          |
| `truenas_users`                                   | Local user definitions. `groups` contains group names and is treated as the complete membership list. Users support `state: absent`; `delete_group` controls whether their primary group is also deleted (default `true`). |
| `truenas_network_configuration`                   | Partial `network.configuration` settings, commonly the DNS server required to resolve the AD domain.                                                                                                                       |
| `truenas_ad`                                      | Active Directory settings passed to `directoryservices.update`. Credentials are sent only when the managed AD configuration changes.                                                                                       |
| `truenas_datasets`                                | `pool.dataset` definitions. Datasets are never deleted by this role. Creation-only properties are listed in `truenas_dataset_create_only_keys`.                                                                            |
| `truenas_smb_shares`, `truenas_nfs_shares`        | SMB and NFS share definitions. These support `state: absent`; each uses its name or path as its lookup key.                                                                                                                |
| `truenas_resources`                               | Ordered definitions for other middleware resources, such as iSCSI or NVMe-oF. Supports `state`, name-to-ID resolution, create-only fields, and comparison/sensitive-field options.                                         |
| `truenas_post_calls`                              | Raw middleware calls executed after shares/resources. These are not idempotent; use sparingly for operations such as permissions.                                                                                          |
| `truenas_services`                                | Service names with optional `enable` and `state` (`started` by default).                                                                                                                                                   |
| `truenas_vms`                                      | VM definitions for the isolated VM playbook. `truenas_vms_mode` defaults to `plan`; set it to `apply` to permit changes. Job, health, and polling timeouts default to 900, 180, and 5 seconds.                               |

For users and groups, `state: absent` deletes the matching object. The role does not provide a deletion option for the administrator or datasets. A user's `password` is sent on creation, and is also resent on update when the `smb` flag changes because TrueNAS requires a password reset when SMB authentication is enabled for an existing account. For general password rotation on an existing account, use a deliberate `user.set_password` call or another explicit workflow.

## 🧩 Common Configuration Patterns

### 👤 Administrator and local users

- `truenas_admin` and `truenas_users` accept `user.create` fields directly.
- If `group_create: false`, set `group` to the primary group name. Supplementary `groups` do not replace the primary group field.
- `groups` is treated as the complete supplementary membership list. Avoid builtin groups such as `users`; TrueNAS rejects direct membership changes for some builtin groups.
- Valid `shell` values come from `user.shell_choices`. Common values are `/usr/bin/zsh` for a login shell and `/usr/sbin/nologin` for SMB-only or service accounts.
- `ssh_password_enabled: true` requires a real login shell and a valid `home` path.
- `home_create: true` creates the home directory only when the user is created. It does not repair an existing account during update.
- `password_disabled: true` cannot be combined with `smb: true`. SMB users must have a password.
- `random_password` is create-only. Use it only when you do not need to resend a known password later.

Minimal shape:

```yaml
truenas_users:
  - username: mediauser
    full_name: Media User
    password: "{{ vault_mediauser_password }}"
    smb: true
    group_create: false
    group: media
    groups: [media]
    shell: /usr/sbin/nologin
    ssh_password_enabled: false

  - username: ansible
    full_name: Ansible
    password: "{{ vault_ansible_password }}"
    smb: false
    group_create: false
    group: ansible
    groups: [ansible]
    shell: /usr/bin/zsh
    home: /mnt/Data/users/ansible
    home_create: true
    ssh_password_enabled: true
```

### 💾 Datasets

- `truenas_datasets` manages datasets only. It does not create SMB or NFS shares by itself.
- `share_type` is a dataset property accepted by `pool.dataset.create`; supported values used by this role include `GENERIC`, `SMB`, `MULTIPROTOCOL`, and `APPS`.
- Use `MULTIPROTOCOL` when the same dataset path will be exported over both SMB and NFS.
- Dataset create-only keys are listed in `truenas_dataset_create_only_keys`; changing them later usually requires a manual migration rather than an in-place update.

Minimal shape:

```yaml
truenas_datasets:
  - name: Data/shared
    share_type: MULTIPROTOCOL
    compression: LZ4
```

### 🖥️ Virtual machines

VMs are managed only by `playbooks/truenas/deploy_truenas_vms.yml`, not by the standard configuration playbook. Put declarations in the TrueNAS host vars and start with the default plan mode:

```yaml
truenas_vms:
  - name: debian12
    description: Build runner
    runtime: running
    cpu: {vcpus: 2, cores: 2, threads: 1}
    memory_mib: 4096
    bootloader: UEFI
    autostart: true
    disks:
      - zvol: tank/vms/debian12
        size_gib: 40
        type: VIRTIO
        disk_sectorsize: 512
    nics:
      - {attach: br0, type: VIRTIO}
    cdrom: /mnt/tank/isos/debian-12.iso
    display:
      type: SPICE
      port: 5901
      password: "{{ vault_debian12_display_password }}"
```

Validate and review the plan before applying. The default `truenas_vms_mode: plan` never mutates middleware, and Ansible check mode also prevents changes when mode is `apply`.

```bash
ansible-playbook -i inventory/truenas/inventory.ini playbooks/truenas/deploy_truenas_vms.yml --check --diff -k --ask-vault-pass
ansible-playbook -i inventory/truenas/inventory.ini playbooks/truenas/deploy_truenas_vms.yml -e truenas_vms_mode=apply -k --ask-vault-pass
```

Use `--tags truenas_vms` to select this isolated workflow. `truenas_vms` must be a list with unique names beginning with a letter, containing only letters, digits, or underscores, and no longer than 40 characters. Present VMs require at least 256 MiB of memory, one or more disks and NICs, and unique zvol paths across all declared VMs. The parent dataset for each new zvol must already exist. Disk zvols are created when missing and grown when the requested size increases; shrinking is refused.

The module reconciles CPU, memory, bootloader, autostart, and declared devices. Optional disk `disk_sectorsize` accepts `512` or `4096` and sets both the middleware `logical_sectorsize` and `physical_sectorsize` to match the TrueNAS UI. When omitted, the sector size is not managed and TrueNAS uses its default for a new disk. It does not remove extra devices automatically; set `cdrom: ""` to explicitly remove CD-ROM devices. A display can optionally set an integer `port`; if omitted, TrueNAS chooses the port. A display password must be at least eight characters and should come from Ansible Vault.

Review approval controls carefully:

- Changing restart-sensitive hardware or devices on a running VM requires `allow_restart: true`. This permits the workflow to stop and restart the VM; changing the desired runtime to `stopped` also stops it.
- `state: absent` requires `allow_delete: true` and a reviewed backup/data-retention plan. Set `allow_disk_delete: true` only when the VM's zvols should also be destroyed; otherwise the disks are retained.
- `runtime` defaults to `running`; use `stopped` to leave a present VM powered off.

### 📁 SMB shares

- `truenas_smb_shares` entries are passed to `sharing.smb`.
- `purpose` must be a valid TrueNAS enum such as `DEFAULT_SHARE` or `MULTIPROTOCOL_SHARE`.
- If you set `options.purpose`, it must match the top-level `purpose`.
- Use `MULTIPROTOCOL_SHARE` when the path is also exported over NFS.

Minimal shape:

```yaml
truenas_smb_shares:
  - name: shared
    path: /mnt/Data/shared
    purpose: MULTIPROTOCOL_SHARE
    comment: Shared data
    options:
      purpose: MULTIPROTOCOL_SHARE
```

### 🌐 NFS shares

- `truenas_nfs_shares` entries are passed to `sharing.nfs`.
- `maproot_*` and `mapall_*` are mutually exclusive in the TrueNAS API. Set one family or the other, not both.
- `path` is the lookup key, so changing it is effectively a delete/create operation.

Minimal shape:

```yaml
truenas_nfs_shares:
  - path: /mnt/Data/shared
    networks: ["192.168.1.0/24"]
    maproot_user: root
```

### ➕ Additional resources

Use `truenas_resources` when there is no SMB/NFS shortcut. This is the preferred place for iSCSI, NVMe-oF, WebDAV, S3, and other middleware-managed objects that are not covered by dedicated role inputs.

- `namespace` identifies the middleware namespace.
- `lookup` must uniquely identify the object through `<namespace>.query`.
- `config` is the desired object body.
- Optional per-entry controls are `state`, `create_only_keys`, `skip_compare_keys`, `sensitive_keys`, `send_sensitive_on_update`, `name_to_id`, and `delete_args`.

Minimal shape:

```yaml
truenas_resources:
  - namespace: iscsi.extent
    lookup: { name: vm-lun0 }
    config: { name: vm-lun0, type: DISK, disk: zvol/tank/vm-lun0 }
  - namespace: iscsi.targetextent
    lookup: { target: vm, extent: vm-lun0 }
    config: { target: vm, extent: vm-lun0, lunid: 0 }
    name_to_id: { target: "iscsi.target:name", extent: "iscsi.extent:name" }
```

### 🔧 Raw post-configuration calls

`truenas_post_calls` is an escape hatch for raw middleware operations that should run after datasets, shares, and `truenas_resources` are already in place.

- Each item maps to `truenas_api` with `mode: call`.
- `method` is required.
- `args` is a positional argument list.
- `job: true` waits for a middleware job.
- `read_only: true` makes the call safe in check mode.
- `ignore_error_patterns` can downgrade known non-fatal call errors to unchanged.
- Calls are not idempotent unless the underlying middleware method is read-only.

Minimal shape:

```yaml
truenas_post_calls:
  - method: filesystem.setperm
    job: true
    args:
      - { path: /mnt/Data/shared, mode: "770", uid: 0, gid: 3000 }
```

## 🏷️ Tags and Targeted Runs

The role exposes these tags for selecting a stage:

| Stage                | Tag                |
| -------------------- | ------------------ |
| Update               | `truenas_update`   |
| Groups               | `truenas_groups`   |
| Administrator        | `truenas_admin`    |
| Users                | `truenas_users`    |
| Network and AD       | `truenas_ad`       |
| Datasets             | `truenas_datasets` |
| Shares and resources | `truenas_shares`   |
| Services             | `truenas_services` |
| Virtual machines     | `truenas_vms`      |

Use `--tags truenas_shares` to select share/resource work. The groups task also carries `truenas_users`, so a user-targeted run ensures declared groups first. Preflight is tagged `always` and continues to run for tagged invocations.
VMs are run through the separate playbook; use `--tags truenas_vms` there.

## 🛡️ Idempotency and Safety

The custom module queries each object and compares only the keys provided in its desired `config`. Unspecified fields are left alone. It creates, updates, or deletes an object only when necessary; check mode reports the planned changes without applying them. Sensitive values are omitted from comparison and diffs.

- Always run with `--check --diff` first, then inspect the proposed changes before applying them.
- Updates install into a new boot environment. With `truenas_update_reboot: false`, the NAS is not rebooted by the role.
- `truenas_no_log: true` is important because user, AD, and other API task arguments can contain passwords.
- A listed `groups` value replaces the user's complete group membership, not just an additive subset.
- AD requires DNS that resolves the domain and a clock within five minutes of the domain controller. The AD `hostname` is the computer-account name and must be no longer than 15 characters.
- Review service changes carefully, especially SSH autostart/state or `ssh_password_enabled`, to avoid losing access.
- `truenas_post_calls` are raw calls. In check mode, a non-read-only call is reported as a pending change but is not executed.
- VM plans are read-only by default. `truenas_vms_mode: apply` permits middleware changes, but Ansible check mode still suppresses them. Inspect planned actions and approvals before applying.
- VM deletion and restarting a running VM for a hardware/device change are gated by `allow_delete` and `allow_restart`. Zvol deletion is separately opt-in with `allow_disk_delete`; zvols are never shrunk.

## 🔌 The `truenas_api` Module

The role's custom [truenas_api.py](library/truenas_api.py) module is the implementation layer behind every stage.

- `mode: resource` manages objects found through `<namespace>.query` and then created, updated, or deleted.
- `mode: config` manages singleton configuration namespaces with `<namespace>.config` and `<namespace>.update`.
- `mode: call` performs an arbitrary middleware method call.
- `mode: vm` plans or reconciles a VM, its devices, and requested disk zvols through `vm.*`, `vm.device.*`, and `pool.dataset.*` middleware calls. VM device argument shape is selected based on the TrueNAS version; verify accepted fields against `/api/docs/` on the target release.
- `create_only_keys` are sent on create but are not compared or resent on update.
- `skip_compare_keys` suppresses drift detection for fields the API returns in a shape that cannot be compared directly.
- `sensitive_keys` are omitted from diffs and can be resent on update through `send_sensitive_on_update` or `send_sensitive_when`.
- `name_to_id` translates human-readable names in `lookup` or `config` into the integer ids the middleware expects.
- `no_create: true` turns a missing resource into a failure instead of silently creating it.
- `query_options` passes the optional second argument to `<namespace>.query`.
- `delete_args` appends extra arguments to `<namespace>.delete`.
- `transport: auto` prefers `truenas_api_client` on the NAS and falls back to `midclt`.

Use the module directly only when extending the role or prototyping a new resource pattern. Prefer the higher-level role inputs whenever one already exists.

## 📌 Contributor Notes

- Keep the role interface narrow. Add a dedicated top-level variable only when a middleware surface needs custom orchestration, validation, or ordering beyond a generic `truenas_resources` entry.
- Prefer expressing new TrueNAS objects through `truenas_resources` before introducing new tasks. Promote a pattern into its own task file only after the generic form becomes noisy or needs special update semantics.
- When adding a new field to a managed object, check whether TrueNAS treats it as create-only, sensitive, name-to-id, or mutually exclusive with another field. Those rules belong in the task or module arguments, not only in prose.
- Keep update semantics aligned with the middleware API. If an update requires companion fields such as SMB `purpose` or mutually exclusive NFS mapping keys, document that behavior and encode it in [`library/truenas_api.py`](library/truenas_api.py) or the calling task.
- Validate role changes with the repository inventory and a focused tag whenever possible, then rerun a syntax check for the full playbook.

Consult the [TrueNAS 25.10 API](https://api.truenas.com/v25.10/) for accepted fields. The API can also be inspected on the NAS with `midclt call <namespace>.query`.

## ✅ Verification Status

The module's comparison behavior and role Jinja expressions have been exercised offline against a mock middleware, including check mode, drift, name-to-ID resolution, and sensitive values. The relevant API method names and argument shapes were checked against TrueNAS 25.10 documentation. The role has not been verified against a live TrueNAS 25.10.7 host; begin with check-mode runs and verify version-specific fields, shell choices, and the administrator privilege group against the target system.
