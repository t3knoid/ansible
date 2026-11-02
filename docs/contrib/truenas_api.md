# truenas_api -- Idempotently manage TrueNAS objects through the local middleware API

## Synopsis

Runs on the TrueNAS host and talks to the middleware over its local socket\.

Uses <code>truenas\_api\_client</code> when it can be imported\, otherwise falls back to <code>midclt</code>\.

<code>mode\=resource</code> ensures an object exists/does not exist\, found via <code>\<namespace\>\.query</code>\. The lookup must match at most one object\.

<code>mode\=config</code> manages a singleton configuration \(<code>\<namespace\>\.config</code> / <code>\<namespace\>\.update</code>\)\.

<code>mode\=call</code> performs a raw API call \(not idempotent unless <code>read\_only\=true</code>\)\.

<code>mode\=app</code> reconciles generic catalog/custom Apps with bounded middleware jobs and runtime checks\.

<code>mode\=vm</code> reconciles TrueNAS virtual machines\, their devices\, disk zvols and GPU passthrough with bounded middleware jobs and runtime checks\.

Only keys present in <em>config</em> are compared\. Lists of scalars compare without regard to order\, and ZFS property wrappers \(<code>parsed</code>/<code>value</code>/<code>rawvalue</code>\) compare case\-insensitively against plain values\.

Updates send only the changed keys\, plus any <em>companion\_keys</em> and <em>sensitive\_keys</em> that apply\.

For <code>sharing\.smb</code>\, a changed <code>options</code> is sent together with <code>purpose</code>\. For <code>sharing\.nfs</code>\, setting <code>maproot\_\*</code> clears <code>mapall\_\*</code> and the reverse\, because the API treats them as mutually exclusive\.

Check mode is supported in every mode and never mutates the middleware\.




## Parameters

  mode (optional, str, resource)
    Operating mode\.

  app (optional, dict, None)
    App definition used by <code>mode\=app</code>\. Allowed keys are <code>name</code>\, <code>source</code>\, <code>state</code>\, <code>runtime</code>\, <code>catalog</code>\, <code>values</code>\, <code>compose</code>\, <code>allow\_upgrade</code> and <code>allow\_delete</code>\; any other key fails\.

    <code>name</code> is lowercase letters\, digits and hyphens\, starts with a letter\, ends with a letter or digit\, and is at most 40 characters\.

    <code>source</code> is <code>catalog</code> or <code>custom</code>\. <code>state</code> is <code>present</code> \(default\) or <code>absent</code>\. <code>runtime</code> is <code>running</code> \(default\) or <code>stopped</code>\.

    Catalog apps need <code>catalog\.app</code>\, <code>catalog\.train</code> and an explicit <code>catalog\.version</code> other than <code>latest</code>\, plus an optional <code>values</code> mapping\. Values are merged into the current configuration\, so only the listed keys are compared\.

    Custom apps need <code>compose</code>\, a YAML string with a nonempty <code>services</code> mapping\. It is compared in both directions and replaced as a whole\.

    A catalog version change requires <code>allow\_upgrade\=true</code> and must be an available upgrade\; downgrades are refused\. Deletion requires <code>allow\_delete\=true</code> and keeps images and ix volumes\.

    Converting an app between catalog and custom\, or changing its catalog app or train\, is refused\.

    The whole definition is treated as sensitive and hidden from logs\.

  app_apply (optional, bool, False)
    Allow app mutations\; false plans using read\-only queries\. Check mode always prevents mutations\.

  app_job_timeout (optional, int, 900)
    Maximum seconds to wait for each Apps middleware job\; a timeout does not cancel the job\.

  app_health_timeout (optional, int, 180)
    Maximum seconds to wait for each desired Apps runtime state\.

  app_poll_interval (optional, int, 5)
    Seconds between Apps job and runtime checks\.

  companion_keys (optional, dict, {})
    Map of trigger key to a list of keys\. When the trigger key is part of the update payload\, the listed keys are sent too\, taken from <em>config</em>\, even if they are unchanged\.

    Example <code>\{configuration\: \[service\_type\]\}</code> for APIs that require a discriminator next to a nested object\.

  vm (optional, dict, None)
    Virtual machine definition used by <code>mode\=vm</code>\.

    Extra disks\, NICs and other devices already on the VM are never removed\. The only device deletions are <code>cdrom\=\"\"</code> and GPU functions dropped from <em>gpus</em>\.

    Changes to CPU\, memory\, firmware\, clock\, security settings or devices on a running VM need a stop and start\, which requires <em>allow\_restart</em>\.

    The device payload shape is chosen from the TrueNAS version \(typed attributes on 25\.04 and later\)\.

    name (True, str, None)
      VM name \(letters\, digits and underscores\; at most 40 characters\)\.

    description (optional, str, )
      Free\-text VM description\.

    state (optional, str, present)
      Whether the VM should exist\.

    runtime (optional, str, running)
      Desired power state when the VM is present\.

    cpu (optional, dict, None)
      CPU topology and affinity settings\.

      vcpus (optional, int, 1)
        Virtual sockets\.

      cores (optional, int, 1)
        Cores per socket\.

      threads (optional, int, 1)
        Threads per core\.

      mode (optional, str, None)
        CPU virtualization mode\.

      model (optional, str, None)
        CPU model when mode is CUSTOM\; choices come from vm\.cpu\_model\_choices\.

      cpuset (optional, str, None)
        Host CPU cores to pin VM CPUs to\.

      pin_vcpus (optional, bool, None)
        Pin virtual CPUs to the specified cpuset\.

      nodeset (optional, str, None)
        NUMA nodes to constrain VM memory to\.


    hide_from_msr (optional, bool, None)
      Hide hypervisor signatures from guest MSR access\.

    ensure_display_device (optional, bool, None)
      Ensure at least one display device is configured\; defaults to false for compatibility with the previous module behavior\.

    gpus (optional, list, None)
      GPU PCI slots selected from <code>system\.advanced\.get\_gpu\_pci\_choices</code>\, such as <code>0000\:04\:00\.0</code>\.

      Each selected GPU expands to all of its PCI functions and is added to the host\'s isolated GPU list\; existing isolation entries are never removed\.

      Omit this option to leave PCI devices unmanaged\; an explicit empty list removes managed GPU functions from the VM but does not de\-isolate them\.

      GPUs that use devices critical to the host are refused\.

    memory_mib (optional, int, None)
      Memory in MiB \(at least 256\)\. Required when <em>state\=present</em>\.

    bootloader (optional, str, UEFI)
      Firmware type\.

    time (optional, str, None)
      Guest system clock reference\.

    enable_secure_boot (optional, bool, None)
      Enable UEFI Secure Boot\.

    trusted_platform_module (optional, bool, None)
      Enable a virtual TPM\.

    shutdown_timeout (optional, int, None)
      Seconds to wait for graceful VM shutdown before forcing power off \(5\-300\; default 90\)\.

    autostart (optional, bool, False)
      Start the VM when TrueNAS boots\.

    disks (optional, list, None)
      Zvol\-backed disks\. At least one is required when <em>state\=present</em>\. Missing zvols are created\, and a larger <em>size\_gib</em> grows an existing zvol\. Shrinking is refused\.

      The parent dataset of a new zvol must already exist\. A zvol may appear only once per VM\.

      zvol (True, str, None)
        Zvol path such as <code>tank/vms/debian12</code>\.

      size_gib (True, int, None)
        Size in GiB\.

      type (optional, str, VIRTIO)
        Disk bus\.

      sparse (optional, bool, True)
        Create the zvol sparse\.

      disk_sectorsize (optional, int, None)
        Logical and physical sector size in bytes\.

      order (optional, int, None)
        Boot order priority \(lower numbers boot first\)\; defaults to 1001 for the first disk\, then increments in list order\.


    nics (optional, list, None)
      Network interfaces\. At least one is required when <em>state\=present</em>\.

      attach (True, str, None)
        Bridge or interface to attach to\.

      type (optional, str, VIRTIO)
        NIC model\.

      trust_guest_rx_filters (optional, bool, None)
        Trust guest receive filter changes\; omitted leaves it unmanaged and TrueNAS defaults to false on create\.

      mac (optional, str, None)
        Fixed MAC address\; generated by TrueNAS when omitted\.

      order (optional, int, None)
        Boot order priority \(lower numbers boot first\)\; defaults to 1100 for the first NIC\, then increments in list order\.


    cdrom (optional, str, None)
      Install ISO path\. An empty string removes the CD\-ROM device\.

    cdrom_order (optional, int, None)
      CD\-ROM boot order priority \(lower numbers boot first\)\; defaults to 1000\.

    display (optional, dict, None)
      Display device\. Its password cannot be read back\, so it is sent on create and whenever another display attribute changes\.

      type (optional, str, SPICE)
        Display protocol\; use VNC to enable a VNC display\.

      bind (optional, str, 0.0.0.0)
        Address to bind the console to\.

      port (optional, int, None)
        Display port passed to the middleware\.

      web_port (optional, int, None)
        Web proxy port\; omitted leaves it unmanaged and TrueNAS assigns it on create\.

      wait (optional, bool, None)
        Wait for a display client before booting\; omitted leaves it unmanaged\.

      web (optional, bool, None)
        Enable web access for SPICE\; VNC requires false and defaults to false\.

      resolution (optional, str, None)
        Console resolution\.

      password (optional, str, None)
        Console password\; VNC passwords must be 1\-8 characters\, SPICE passwords at least 8 characters\.

      order (optional, int, None)
        Boot order priority \(lower numbers boot first\)\; defaults to 1200\.


    allow_delete (optional, bool, False)
      Approve deleting the VM \(required for <em>state\=absent</em>\)\.

    allow_restart (optional, bool, False)
      Approve stopping and restarting a running VM for changes that need it\. Without it\, apply fails when a restart is needed\.

    allow_disk_delete (optional, bool, False)
      Also destroy the VM\'s zvols when deleting it\. Otherwise the zvols are kept\.


  vm_apply (optional, bool, False)
    Allow VM mutations\; false plans using read\-only queries\. Check mode always prevents mutations\.

  vm_job_timeout (optional, int, 900)
    Maximum seconds to wait for each VM middleware job\; a timeout does not cancel the job\.

  vm_health_timeout (optional, int, 180)
    Maximum seconds to wait for each desired VM runtime state\.

  vm_poll_interval (optional, int, 5)
    Seconds between VM job and runtime checks\.

  namespace (optional, str, None)
    API namespace\, e\.g\. <code>sharing\.smb</code>\, <code>user</code>\, <code>pool\.dataset</code>\, <code>directoryservices</code>\.

  lookup (optional, dict, {})
    Equality filters used to find the object \(resource mode\)\; required in that mode and must match at most one object\. Names are translated by <em>name\_to\_id</em>\.

  config (optional, dict, {})
    Desired state\. Only the keys listed here are compared\; other attributes are left alone\.

  state (optional, str, present)
    Whether the object should exist \(resource mode\)\.

  id_key (optional, str, id)
    Attribute holding the object id passed to update/delete\.

  create_only_keys (optional, list, [])
    Keys sent on create but never compared or sent on update\.

  skip_compare_keys (optional, list, [])
    Keys never compared \(the API returns them in another shape than it accepts them\)\.

  sensitive_keys (optional, list, [])
    Keys that cannot be read back \(passwords\)\. Never compared and redacted from diffs\. Sent on create\, and on update only if <em>send\_sensitive\_on\_update</em> or <em>send\_sensitive\_when</em> applies\.

  send_sensitive_on_update (optional, bool, False)
    Send <em>sensitive\_keys</em> with every update that has other changes\.

  send_sensitive_when (optional, list, [])
    Send <em>sensitive\_keys</em> with an update only when one of these keys changed\.

  name_to_id (optional, dict, {})
    Map of config/lookup key to <code>namespace\:field</code>\. Names are replaced by ids through <code>namespace\.query</code>\.

    Example <code>\{groups\: \'group\:name\'\}</code>\.

  no_create (optional, bool, False)
    Fail instead of creating a missing object\.

  query_options (optional, dict, {})
    Second argument passed to <code>\<namespace\>\.query</code>\.

  delete_args (optional, list, [])
    Extra arguments passed to <code>\<namespace\>\.delete</code> after the id\.

  job (optional, bool, False)
    The update \(config mode\) or call \(call mode\) is a middleware job\; wait for it\.

  method (optional, str, None)
    Method name for <code>mode\=call</code>\.

  args (optional, list, [])
    Positional arguments for <code>mode\=call</code>\.

  read_only (optional, bool, False)
    <code>mode\=call</code> only reads data\; never reports changed and also runs in check mode\.

  ignore_error_patterns (optional, list, [])
    <code>mode\=call</code> regular expressions\; a matching error is reported as unchanged instead of failing\.

  transport (optional, str, auto)
    Force a transport\. <code>auto</code> prefers truenas\_api\_client and falls back to midclt\; <code>client</code> fails if the client cannot be used\.



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

  action (resource/config, str, )
    created\, updated\, deleted or none \(resource/config mode\)\.

  changed_keys (resource/config, list, )
    Keys that differ from the desired state\.

  id (resource, raw, )
    Id of the object\. Not returned for a planned create in check mode\.

  diff (resource/config, when changed, dict, )
    Before and after values of the changed keys\; sensitive keys are redacted on create\.

  result (call, unless check mode skipped the call or an error was ignored, raw, )
    API return value \(call mode\)\.

  msg (call, when applicable, str, )
    Explanation when a call was skipped in check mode or an error was ignored\.

  ignored_error (call, when an error was ignored, str, )
    The middleware error that matched <em>ignore\_error\_patterns</em>\.

  name (app/vm, str, )
    App or VM name\.

  actions (app/vm, list, )
    Planned or applied actions in execution order\.
    App actions are <code>create</code>\, <code>update</code>\, <code>upgrade</code>\, <code>delete</code>\, <code>start</code> and <code>stop</code>\.
    VM actions include <code>create\_zvol\:\<zvol\></code>\, <code>grow\_zvol\:\<zvol\></code>\, <code>isolate\_gpu\:\<pci\_slot\></code>\, <code>stop</code>\, <code>create</code>\, <code>update</code>\, <code>\<op\>\_device\:\<dtype\></code>\, <code>delete</code>\, <code>delete\_zvols</code> and <code>start</code>\.

  planned (app/vm, bool, )
    True when nothing was applied \(check mode\, or <em>app\_apply</em>/<em>vm\_apply</em> false\)\.

  runtime_state (app/vm, str, )
    Runtime state after reconciliation\, or the current state when planned\; <code>ABSENT</code> when the app or VM does not exist\.

  approval_required (app (upgrade/delete) and vm, raw, )
    For apps\, true when the planned upgrade or delete lacks its approval\.
    For VMs\, the list of missing approvals\, such as <code>allow\_restart</code> or <code>allow\_delete</code>\.

  device_changes (vm, when the VM exists, list, )
    Per\-device operations with <code>operation</code>\, <code>dtype</code>\, <code>id</code> and\, for updates\, the before/after value of each differing attribute or order\. Display passwords are excluded\.



## Status


## Authors

- Frank Refol
