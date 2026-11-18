# truenas_api — Idempotently manage TrueNAS objects through the local middleware API

## Synopsis

Runs on the TrueNAS host and talks to the middleware over its local socket.

Uses `truenas_api_client` when it can be imported, otherwise falls back to `midclt`.

`mode=resource` ensures an object exists/does not exist, found via `<namespace>.query`. The lookup must match at most one object.

`mode=config` manages a singleton configuration (`<namespace>.config` / `<namespace>.update`).

`mode=call` performs a raw API call (not idempotent unless `read_only=true`).

`mode=app` reconciles generic catalog/custom Apps with bounded middleware jobs and runtime checks.

`mode=vm` reconciles TrueNAS virtual machines, their devices, disk zvols and GPU passthrough with bounded middleware jobs and runtime checks.

Only keys present in *config* are compared. Lists of scalars compare without regard to order, and ZFS property wrappers (`parsed`/`value`/`rawvalue`) compare case-insensitively against plain values.

Updates send only the changed keys, plus any *companion_keys* and *sensitive_keys* that apply.

For `sharing.smb`, a changed `options` is sent together with `purpose`. For `sharing.nfs`, setting `maproot_*` clears `mapall_*` and the reverse, because the API treats them as mutually exclusive.

Check mode is supported in every mode and never mutates the middleware.

## Parameters

- **mode** (str, optional, default: `resource`)

  Operating mode.

- **app** (dict, optional)

  App definition used by `mode=app`. Allowed keys are `name`, `source`, `state`, `runtime`, `catalog`, `values`, `compose`, `allow_upgrade` and `allow_delete`; any other key fails.

  `name` is lowercase letters, digits and hyphens, starts with a letter, ends with a letter or digit, and is at most 40 characters.

  `source` is `catalog` or `custom`. `state` is `present` (default) or `absent`. `runtime` is `running` (default) or `stopped`.

  Catalog apps need `catalog.app`, `catalog.train` and an explicit `catalog.version` other than `latest`, plus an optional `values` mapping. Values are merged into the current configuration, so only the listed keys are compared.

  Custom apps need `compose`, a YAML string with a nonempty `services` mapping. It is compared in both directions and replaced as a whole.

  A catalog version change requires `allow_upgrade=true` and must be an available upgrade; downgrades are refused. Deletion requires `allow_delete=true` and keeps images and ix volumes.

  Converting an app between catalog and custom, or changing its catalog app or train, is refused.

  The whole definition is treated as sensitive and hidden from logs.

- **app_apply** (bool, optional, default: `false`)

  Allow app mutations; false plans using read-only queries. Check mode always prevents mutations.

- **app_job_timeout** (int, optional, default: `900`)

  Maximum seconds to wait for each Apps middleware job; a timeout does not cancel the job.

- **app_health_timeout** (int, optional, default: `180`)

  Maximum seconds to wait for each desired Apps runtime state.

- **app_poll_interval** (int, optional, default: `5`)

  Seconds between Apps job and runtime checks.

- **companion_keys** (dict, optional, default: `{}`)

  Map of trigger key to a list of keys. When the trigger key is part of the update payload, the listed keys are sent too, taken from *config*, even if they are unchanged.

  Example `{configuration: [service_type]}` for APIs that require a discriminator next to a nested object.

- **vm** (dict, optional)

  Virtual machine definition used by `mode=vm`.

  Extra disks, NICs and other devices already on the VM are never removed. The only device deletions are `cdrom=""` and GPU functions dropped from *gpus*.

  Changes to CPU, memory, firmware, clock, security settings or devices on a running VM need a stop and start, which requires *allow_restart*.

  The device payload shape is chosen from the TrueNAS version (typed attributes on 25.04 and later).

  - **name** (str, required)

    VM name (letters, digits and underscores; at most 40 characters).

  - **description** (str, optional, default: `""`)

    Free-text VM description.

  - **state** (str, optional, default: `present`)

    Whether the VM should exist.

  - **runtime** (str, optional, default: `running`)

    Desired power state when the VM is present.

  - **cpu** (dict, optional)

    CPU topology and affinity settings.

    - **vcpus** (int, optional, default: `1`)

      Virtual sockets.

    - **cores** (int, optional, default: `1`)

      Cores per socket.

    - **threads** (int, optional, default: `1`)

      Threads per core.

    - **mode** (str, optional)

      CPU virtualization mode.

    - **model** (str, optional)

      CPU model when mode is `CUSTOM`; choices come from `vm.cpu_model_choices`.

    - **cpuset** (str, optional)

      Host CPU cores to pin VM CPUs to.

    - **pin_vcpus** (bool, optional)

      Pin virtual CPUs to the specified cpuset.

    - **nodeset** (str, optional)

      NUMA nodes to constrain VM memory to.

  - **hide_from_msr** (bool, optional)

    Hide hypervisor signatures from guest MSR access.

  - **ensure_display_device** (bool, optional)

    Ensure at least one display device is configured; defaults to false for compatibility with the previous module behavior.

  - **gpus** (list, optional)

    GPU PCI slots selected from `system.advanced.get_gpu_pci_choices`, such as `0000:04:00.0`.

    Each selected GPU expands to all of its PCI functions and is added to the host's isolated GPU list; existing isolation entries are never removed.

    Omit this option to leave PCI devices unmanaged; an explicit empty list removes managed GPU functions from the VM but does not de-isolate them.

    GPUs that use devices critical to the host are refused.

  - **memory_mib** (int, optional)

    Memory in MiB (at least 256). Required when *state=present*.

  - **bootloader** (str, optional, default: `UEFI`)

    Firmware type.

  - **time** (str, optional)

    Guest system clock reference.

  - **enable_secure_boot** (bool, optional)

    Enable UEFI Secure Boot.

  - **trusted_platform_module** (bool, optional)

    Enable a virtual TPM.

  - **shutdown_timeout** (int, optional)

    Seconds to wait for graceful VM shutdown before forcing power off (5–300; default 90).

  - **autostart** (bool, optional, default: `false`)

    Start the VM when TrueNAS boots.

  - **disks** (list, optional)

    Zvol-backed disks. At least one is required when *state=present*. Missing zvols are created, and a larger *size_gib* grows an existing zvol. Shrinking is refused.

    The parent dataset of a new zvol must already exist. A zvol may appear only once per VM.

    - **zvol** (str, required)

      Zvol path such as `tank/vms/debian12`.

    - **size_gib** (int, required)

      Size in GiB.

    - **type** (str, optional, default: `VIRTIO`)

      Disk bus.

    - **sparse** (bool, optional, default: `true`)

      Create the zvol sparse.

    - **disk_sectorsize** (int, optional)

      Logical and physical sector size in bytes.

    - **order** (int, optional)

      Boot order priority (lower numbers boot first); defaults to 1001 for the first disk, then increments in list order.

  - **nics** (list, optional)

    Network interfaces. At least one is required when *state=present*.

    - **attach** (str, required)

      Bridge or interface to attach to.

    - **type** (str, optional, default: `VIRTIO`)

      NIC model.

    - **trust_guest_rx_filters** (bool, optional)

      Trust guest receive filter changes; omitted leaves it unmanaged and TrueNAS defaults to false on create.

    - **mac** (str, optional)

      Fixed MAC address; generated by TrueNAS when omitted.

    - **order** (int, optional)

      Boot order priority (lower numbers boot first); defaults to 1100 for the first NIC, then increments in list order.

  - **cdrom** (str, optional)

    Install ISO path. An empty string removes the CD-ROM device.

  - **cdrom_order** (int, optional)

    CD-ROM boot order priority (lower numbers boot first); defaults to 1000.

  - **display** (dict, optional)

    Display device. Its password cannot be read back, so it is sent on create and whenever another display attribute changes.

    - **type** (str, optional, default: `SPICE`)

      Display protocol; use `VNC` to enable a VNC display.

    - **bind** (str, optional, default: `0.0.0.0`)

      Address to bind the console to.

    - **port** (int, optional)

      Display port passed to the middleware.

    - **web_port** (int, optional)

      Web proxy port; omitted leaves it unmanaged and TrueNAS assigns it on create.

    - **wait** (bool, optional)

      Wait for a display client before booting; omitted leaves it unmanaged.

    - **web** (bool, optional)

      Enable web access for SPICE; VNC requires false and defaults to false.

    - **resolution** (str, optional)

      Console resolution.

    - **password** (str, optional)

      Console password; VNC passwords must be 1–8 characters, SPICE passwords at least 8 characters.

    - **order** (int, optional)

      Boot order priority (lower numbers boot first); defaults to 1200.

  - **allow_delete** (bool, optional, default: `false`)

    Approve deleting the VM (required for *state=absent*).

  - **allow_restart** (bool, optional, default: `false`)

    Approve stopping and restarting a running VM for changes that need it. Without it, apply fails when a restart is needed.

  - **allow_disk_delete** (bool, optional, default: `false`)

    Also destroy the VM's zvols when deleting it. Otherwise the zvols are kept.

- **vm_apply** (bool, optional, default: `false`)

  Allow VM mutations; false plans using read-only queries. Check mode always prevents mutations.

- **vm_job_timeout** (int, optional, default: `900`)

  Maximum seconds to wait for each VM middleware job; a timeout does not cancel the job.

- **vm_health_timeout** (int, optional, default: `180`)

  Maximum seconds to wait for each desired VM runtime state.

- **vm_poll_interval** (int, optional, default: `5`)

  Seconds between VM job and runtime checks.

- **namespace** (str, optional)

  API namespace, e.g. `sharing.smb`, `user`, `pool.dataset`, `directoryservices`.

- **lookup** (dict, optional, default: `{}`)

  Equality filters used to find the object (resource mode); required in that mode and must match at most one object. Names are translated by *name_to_id*.

- **config** (dict, optional, default: `{}`)

  Desired state. Only the keys listed here are compared; other attributes are left alone.

- **state** (str, optional, default: `present`)

  Whether the object should exist (resource mode).

- **id_key** (str, optional, default: `id`)

  Attribute holding the object id passed to update/delete.

- **create_only_keys** (list, optional, default: `[]`)

  Keys sent on create but never compared or sent on update.

- **skip_compare_keys** (list, optional, default: `[]`)

  Keys never compared (the API returns them in another shape than it accepts them).

- **sensitive_keys** (list, optional, default: `[]`)

  Keys that cannot be read back (passwords). Never compared and redacted from diffs. Sent on create, and on update only if *send_sensitive_on_update* or *send_sensitive_when* applies.

- **send_sensitive_on_update** (bool, optional, default: `false`)

  Send *sensitive_keys* with every update that has other changes.

- **send_sensitive_when** (list, optional, default: `[]`)

  Send *sensitive_keys* with an update only when one of these keys changed.

- **name_to_id** (dict, optional, default: `{}`)

  Map of config/lookup key to `namespace:field`. Names are replaced by ids through `namespace.query`.

  Example `{groups: 'group:name'}`.

- **no_create** (bool, optional, default: `false`)

  Fail instead of creating a missing object.

- **query_options** (dict, optional, default: `{}`)

  Second argument passed to `<namespace>.query`.

- **delete_args** (list, optional, default: `[]`)

  Extra arguments passed to `<namespace>.delete` after the id.

- **job** (bool, optional, default: `false`)

  The update (config mode) or call (call mode) is a middleware job; wait for it.

- **method** (str, optional)

  Method name for `mode=call`.

- **args** (list, optional, default: `[]`)

  Positional arguments for `mode=call`.

- **read_only** (bool, optional, default: `false`)

  `mode=call` only reads data; never reports changed and also runs in check mode.

- **ignore_error_patterns** (list, optional, default: `[]`)

  `mode=call` regular expressions; a matching error is reported as unchanged instead of failing.

- **transport** (str, optional, default: `auto`)

  Force a transport. `auto` prefers truenas_api_client and falls back to midclt; `client` fails if the client cannot be used.

## Examples

```yaml
- name: SMB share
  truenas_api:
    namespace: sharing.smb
    lookup: {name: media}
    config: {name: media, path: /mnt/tank/media, purpose: DEFAULT_SHARE}

- name: Read-only call
  truenas_api:
    mode: call
    method: system.version_short
    read_only: true
  register: ver

- name: User with group names resolved to ids
  truenas_api:
    namespace: user
    lookup: {username: alice}
    config: {username: alice, full_name: Alice, password: "{{ vault_alice_password }}", smb: true, groups: [media]}
    create_only_keys: [password]
    sensitive_keys: [password]
    send_sensitive_when: [smb]
    name_to_id: {groups: "group:name"}

- name: Singleton configuration
  truenas_api:
    mode: config
    namespace: network.configuration
    config: {nameserver1: 192.168.1.10}

- name: Middleware job, ignoring a known no-op error
  truenas_api:
    mode: call
    method: update.run
    job: true
    args: [{reboot: false}]
    ignore_error_patterns: ["(?i)no update"]

- name: Plan a custom app (set app_apply to make changes)
  truenas_api:
    mode: app
    app:
      name: example-web
      source: custom
      compose: |
        services:
          web:
            image: nginx:1.27
    app_apply: false

- name: Plan a VM (set vm_apply to make changes)
  truenas_api:
    mode: vm
    vm:
      name: debian12
      memory_mib: 4096
      disks: [{zvol: tank/vms/debian12, size_gib: 40}]
      nics: [{attach: br0}]
    vm_apply: false
```

## Return Values

- **action** (str) — returned in resource/config mode

  `created`, `updated`, `deleted` or `none` (resource/config mode).

- **changed_keys** (list) — returned in resource/config mode

  Keys that differ from the desired state.

- **id** (raw) — returned in resource mode

  Id of the object. Not returned for a planned create in check mode.

- **diff** (dict) — returned in resource/config mode, when changed

  Before and after values of the changed keys; sensitive keys are redacted on create.

- **result** (raw) — returned in call mode, unless check mode skipped the call or an error was ignored

  API return value (call mode).

- **msg** (str) — returned in call mode, when applicable

  Explanation when a call was skipped in check mode or an error was ignored.

- **ignored_error** (str) — returned in call mode, when an error was ignored

  The middleware error that matched *ignore_error_patterns*.

- **name** (str) — returned in app/vm mode

  App or VM name.

- **actions** (list) — returned in app/vm mode

  Planned or applied actions in execution order.

  App actions are `create`, `update`, `upgrade`, `delete`, `start` and `stop`.

  VM actions include `create_zvol:<zvol>`, `grow_zvol:<zvol>`, `isolate_gpu:<pci_slot>`, `stop`, `create`, `update`, `<op>_device:<dtype>`, `delete`, `delete_zvols` and `start`.

- **planned** (bool) — returned in app/vm mode

  True when nothing was applied (check mode, or *app_apply*/*vm_apply* false).

- **runtime_state** (str) — returned in app/vm mode

  Runtime state after reconciliation, or the current state when planned; `ABSENT` when the app or VM does not exist.

- **approval_required** (raw) — returned in app mode (upgrade/delete) and vm mode

  For apps, true when the planned upgrade or delete lacks its approval.

  For VMs, the list of missing approvals, such as `allow_restart` or `allow_delete`.

- **device_changes** (list) — returned in vm mode, when the VM exists

  Per-device operations with `operation`, `dtype`, `id` and, for updates, the before/after value of each differing attribute or order. Display passwords are excluded.

## Authors

- Frank Refol