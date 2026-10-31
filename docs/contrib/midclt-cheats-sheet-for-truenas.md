# midclt Cheat Sheet for TrueNAS

Run these on the TrueNAS host (SSH or Shell). Method names and payloads change between releases, so when a call errors, check `core.get_methods` or the API docs at `https://<truenas-host>/api/docs/` for your version. Lines marked `# changes state` modify the system. Everything else is read-only.

## 1. Basics

```bash
midclt -h                              # list subcommands and options
midclt call -h                         # help for the call subcommand
midclt call core.ping                  # connectivity check, returns pong
midclt call <method> [json-arg ...]    # call a method; each argument is JSON
midclt call -j <method> [args]         # the method is a job: wait for it to finish
```

**Quoting.** Plain strings and numbers can be passed bare (`midclt call vm.status 5`, `midclt call app.config myapp`). Lists and objects must be valid JSON wrapped in single quotes, so strings inside them use double quotes.

**Jobs.** Some methods return a bare number. That is a job id. Rerun with `-j` to wait for it, or follow it with `core.get_jobs`.

**Pretty-printing.**

```bash
midclt call interface.query | python3 -m json.tool
midclt call interface.query | jq .          # only if jq is installed
```

## 2. Queries: filters and options

Every `<namespace>.query` method takes a list of filters and an optional options object:

```bash
midclt call <namespace>.query '[<filters>]' '{<options>}'

midclt call user.query '[["username","=","admin"]]'
midclt call user.query '[["builtin","=",false]]' '{"select":["username","uid"],"order_by":["username"],"limit":10}'
midclt call user.query '[]' '{"count":true}'
midclt call vm.query '[["name","=","ansible"]]' '{"get":true}'
midclt call vm.query '[["OR",[[["name","=","a"],["name","=","b"]]]]]'
```

| Filter operator | Meaning |
| --- | --- |
| `=` , `!=` | Equal, not equal |
| `>` , `>=` , `<` , `<=` | Comparisons |
| `in` , `nin` | Value is in, or not in, the given list |
| `^` , `!^` | Starts with, does not start with |
| `$` , `!$` | Ends with, does not end with |
| `~` | Regular expression match |
| `rin` , `rnin` | A list-valued field contains, or does not contain, the value |

| Option | Meaning |
| --- | --- |
| `select` | Return only these fields |
| `order_by` | Sort by these fields; prefix a field with `-` for descending |
| `limit` , `offset` | Paging |
| `count` | Return the number of matches instead of the rows |
| `get` | Return a single object instead of a list (errors if there is not exactly one match) |

## 3. Discovering methods

```bash
midclt call core.get_methods | python3 -m json.tool | less
midclt call core.get_methods | python3 -c 'import sys,json; print("\n".join(sorted(k for k in json.load(sys.stdin) if k.startswith("vm."))))'
midclt call core.get_services
```

The second command lists every method that starts with `vm.`. Change the prefix to explore another area.

## 4. System

```bash
midclt call system.version
midclt call system.version_short
midclt call system.info
midclt call system.ready
midclt call system.general.config
midclt call system.advanced.config
midclt call auth.me
```

## 5. Jobs

```bash
midclt call core.get_jobs '[["state","=","RUNNING"]]'
midclt call core.get_jobs '[["id","=",123]]'
midclt call core.get_jobs '[["method","=","vm.stop"]]' '{"order_by":["-id"],"limit":5}'
midclt call core.job_abort 123              # changes state
```

Job states include `RUNNING`, `SUCCESS`, `FAILED` and `ABORTED`. A timeout in a client does not cancel the job, so check `core.get_jobs` before retrying.

## 6. Network

```bash
# Interfaces: configured settings plus live state
midclt call interface.query | python3 -m json.tool
midclt call interface.query '[["name","=","br20"]]' | python3 -m json.tool
midclt call interface.query '[]' '{"select":["name","type","aliases","mtu"]}' | python3 -m json.tool

# DNS, hostname, domain, default gateways
midclt call network.configuration.config | python3 -m json.tool
midclt call network.general.summary | python3 -m json.tool

# Pending changes and what can be attached
midclt call interface.has_pending_changes
midclt call interface.bridge_members_choices | python3 -m json.tool
midclt call vm.device.nic_attach_choices | python3 -m json.tool

midclt call interface.rollback              # changes state: discards uncommitted interface changes
```

Top-level interface fields are the configured settings (`name`, `type`, `aliases`, `ipv4_dhcp`, `mtu`, `bridge_members`, `vlan_tag`, `lag_ports` and so on). The `state` object holds the live kernel state (`link_state`, `link_address`, assigned addresses). Interface changes are staged until committed, so check `interface.has_pending_changes` if what you see does not match what is running.

Compact table of interfaces and addresses:

```bash
midclt call interface.query | python3 -c '
import json, sys
for i in json.load(sys.stdin):
    s = i.get("state", {})
    ips = [a["address"] for a in s.get("aliases", []) if a.get("type") == "INET"]
    print(i["name"], i["type"], s.get("link_state", "?"), ",".join(ips))
'
```

## 7. Storage

```bash
midclt call pool.query
midclt call pool.dataset.query '[["id","=","Data/vms"]]'
midclt call pool.dataset.get_instance Data/vms
midclt call pool.dataset.query '[["type","=","VOLUME"]]' '{"select":["id","volsize"]}'
midclt call pool.snapshot.query '[["dataset","=","Data/vms"]]' '{"select":["name"]}'
midclt call disk.query '[]' '{"select":["name","size","serial","pool"]}'
midclt call disk.get_unused

# changes state
midclt call pool.dataset.create '{"name":"Data/vms/test","type":"VOLUME","volsize":10737418240,"sparse":true}'
midclt call pool.dataset.update Data/vms/test '{"volsize":21474836480}'
midclt call pool.snapshot.create '{"dataset":"Data/vms","name":"manual-1"}'
```

Sizes are in bytes (10737418240 is 10 GiB). Many ZFS properties come back as objects with `parsed`, `rawvalue` and `value` keys.

## 8. Services

```bash
midclt call service.query '[]' '{"select":["service","enable","state"]}'
midclt call service.query '[["service","=","cifs"]]'

# changes state
midclt call service.start cifs
midclt call service.stop cifs
midclt call service.restart cifs
midclt call service.update cifs '{"enable":true}'
```

Newer releases add `service.control` (for example `midclt call -j service.control START cifs`). Check `core.get_methods` to see which your version supports.

## 9. Users, groups and shares

```bash
midclt call user.query '[["builtin","=",false]]' '{"select":["username","uid","home"]}'
midclt call group.query '[["builtin","=",false]]' '{"select":["name","gid"]}'
midclt call sharing.smb.query
midclt call sharing.nfs.query

# changes state
midclt call user.create '{"full_name":"John Doe","username":"user","password":"pass","group_create":true}'
```

Avoid putting real passwords on the command line, because they end up in shell history.

## 10. Directory services (Active Directory)

```bash
# Config with the credential stripped
midclt call directoryservices.config | python3 -c 'import sys,json; c=json.load(sys.stdin); c.pop("credential",None); print(json.dumps(c, indent=2))'

midclt call directoryservices.status        # newer releases
midclt call kerberos.realm.query
midclt call network.configuration.config    # nameservers used for the domain
```

While directory services are enabled, only account caching, DNS updates and timeouts can be changed. Other changes need directory services disabled first, ideally in a maintenance window. Compare the live values with your variables exactly, including case (the middleware stores the domain in upper case).

## 11. Virtual machines

```bash
midclt call vm.query '[]' '{"select":["id","name","memory","vcpus","autostart","status"]}'
midclt call vm.query '[["name","=","ansible"]]' '{"get":true}'
midclt call vm.status 5
midclt call vm.device.query '[["vm","=",5]]'
midclt call vm.virtualization_details
midclt call vm.get_available_memory
midclt call vm.cpu_model_choices
midclt call vm.device.nic_attach_choices
midclt call vm.device.disk_choices

# changes state
midclt call vm.start 5 '{"overcommit":false}'
midclt call -j vm.stop 5 '{"force":false,"force_after_timeout":true}'
midclt call -j vm.restart 5
midclt call vm.poweroff 5
midclt call vm.delete 5 '{"zvols":false,"force":false}'
```

The number after the method is the VM's id, not its name. Get it from `vm.query`. The keys returned by `vm.device.nic_attach_choices` are the values you can use as a NIC's attach target.

## 12. Apps

```bash
midclt call docker.config                   # shows the configured Apps pool
midclt call docker.status
midclt call app.query '[]' '{"select":["id","name","state","version"]}'
midclt call app.query '[["id","=","myapp"]]' '{"get":true}'
midclt call app.config myapp
midclt call app.upgrade_summary myapp '{"app_version":"1.2.3"}'

# changes state
midclt call -j app.start myapp
midclt call -j app.stop myapp
```

## 13. Alerts and updates

```bash
midclt call alert.list
midclt call update.check_available
midclt call alert.dismiss <uuid>            # changes state
```

## 14. Running midclt remotely

The `midclt` client is preinstalled on TrueNAS and is also available from the `truenas_api_client` Python package for other hosts.

```bash
midclt --uri wss://truenas-01/api/current -K <api-key> call system.info
midclt --uri ws://truenas-01/api/current -U <user> -P <password> call system.info
```

API keys require an HTTPS/WSS connection. Keep keys and passwords out of shell history and shared logs.

## 15. Using the same calls from Ansible

Each midclt argument becomes one item in `args`, and `-j` becomes `job: true`:

```yaml
- name: Look up a VM
  truenas_api:
    mode: call
    method: vm.query
    args:
      - [["name", "=", "ansible"]]
      - {get: true}
    read_only: true
  register: vm_info
```

Set `read_only: true` only for calls that do not change anything. Such calls are also safe in check mode.

## 16. Habits worth keeping

- Try a read-only `query` or `config` call before an `update` or `create`, and compare the live values with what you intend to send.
- Use `select` to keep output short, and strip credentials before pasting output anywhere.
- After a failed job, read `core.get_jobs` for the job's error before retrying.
- Check `interface.has_pending_changes` after network work.
- When a method or field is not found, run `core.get_methods` or open `/api/docs/` on the host, because names change between releases.
