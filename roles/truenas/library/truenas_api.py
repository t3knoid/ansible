#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: truenas_api
short_description: Idempotently manage TrueNAS objects through the local middleware API
description:
  - Runs on the TrueNAS host and talks to the middleware over its local socket.
  - Uses C(truenas_api_client) when it can be imported, otherwise falls back to C(midclt).
  - C(mode=resource) ensures an object exists/does not exist, found via C(<namespace>.query).
  - C(mode=config) manages a singleton configuration (C(<namespace>.config) / C(<namespace>.update)).
  - C(mode=call) performs a raw API call (not idempotent unless C(read_only=true)).
  - C(mode=app) reconciles generic catalog/custom Apps with bounded middleware jobs and runtime checks.
  - C(mode=vm) reconciles TrueNAS virtual machines with bounded middleware jobs and runtime checks.
options:
  mode:
    description: Operating mode.
    type: str
    default: resource
    choices: [resource, config, call, app, vm]
  app:
    description: App definition with name, source, state, runtime, catalog/values or compose, and explicit allow_upgrade/allow_delete approvals.
    type: dict
  app_apply:
    description: Allow app mutations; false plans using read-only queries. Check mode always prevents mutations.
    type: bool
    default: false
  app_job_timeout:
    description: Maximum seconds to wait for each Apps middleware job; a timeout does not cancel the job.
    type: int
    default: 900
  app_health_timeout:
    description: Maximum seconds to wait for each desired Apps runtime state.
    type: int
    default: 180
  app_poll_interval:
    description: Seconds between Apps job and runtime checks.
    type: int
    default: 5
  vm:
    description:
      - Virtual machine definition used by C(mode=vm).
      - Extra disks, NICs and other devices already on the VM are never removed.
    type: dict
    suboptions:
      name:
        description: VM name (letters, digits and underscores; at most 40 characters).
        type: str
        required: true
      description:
        description: Free-text VM description.
        type: str
        default: ""
      state:
        description: Whether the VM should exist.
        type: str
        default: present
        choices: [present, absent]
      runtime:
        description: Desired power state when the VM is present.
        type: str
        default: running
        choices: [running, stopped]
      cpu:
        description: CPU topology and affinity settings.
        type: dict
        suboptions:
          vcpus: {description: Virtual sockets., type: int, default: 1}
          cores: {description: Cores per socket., type: int, default: 1}
          threads: {description: Threads per core., type: int, default: 1}
          mode: {description: CPU virtualization mode., type: str, choices: [CUSTOM, HOST-MODEL, HOST-PASSTHROUGH]}
          model: {description: CPU model when mode is CUSTOM; choices come from vm.cpu_model_choices., type: str}
          cpuset: {description: Host CPU cores to pin VM CPUs to., type: str}
          pin_vcpus: {description: Pin virtual CPUs to the specified cpuset., type: bool}
          nodeset: {description: NUMA nodes to constrain VM memory to., type: str}
            hide_from_msr:
                description: Hide hypervisor signatures from guest MSR access.
                type: bool
            ensure_display_device:
                description: Ensure at least one display device is configured; defaults to false for compatibility with the previous module behavior.
                type: bool
            gpus:
                description:
                    - GPU PCI slots selected from C(system.advanced.get_gpu_pci_choices), such as C(0000:04:00.0).
                    - Each selected GPU expands to all of its PCI functions. Omit this option to leave PCI devices unmanaged; an explicit empty list removes managed GPU functions.
                type: list
                elements: str
      memory_mib:
        description: Memory in MiB (at least 256). Required when I(state=present).
        type: int
      bootloader:
        description: Firmware type.
        type: str
        default: UEFI
        choices: [UEFI, UEFI_CSM]
            time:
                description: Guest system clock reference.
                type: str
                choices: [LOCAL, UTC]
            enable_secure_boot:
                description: Enable UEFI Secure Boot.
                type: bool
            trusted_platform_module:
                description: Enable a virtual TPM.
                type: bool
            shutdown_timeout:
                description: Seconds to wait for graceful VM shutdown before forcing power off (5-300; default 90).
                type: int
      autostart:
        description: Start the VM when TrueNAS boots.
        type: bool
        default: false
      disks:
        description: Zvol-backed disks. Missing zvols are created, and a larger I(size_gib) grows an existing zvol. Shrinking is refused.
        type: list
        elements: dict
        suboptions:
          zvol: {description: Zvol path such as C(tank/vms/debian12)., type: str, required: true}
          size_gib: {description: Size in GiB., type: int, required: true}
          type: {description: Disk bus., type: str, default: VIRTIO, choices: [VIRTIO, AHCI]}
          sparse: {description: Create the zvol sparse., type: bool, default: true}
          disk_sectorsize: {description: Logical and physical sector size in bytes., type: int, choices: [512, 4096]}
          order: {description: Boot order priority (lower numbers boot first)., type: int}
      nics:
        description: Network interfaces.
        type: list
        elements: dict
        suboptions:
          attach: {description: Bridge or interface to attach to., type: str, required: true}
          type: {description: NIC model., type: str, default: VIRTIO, choices: [VIRTIO, E1000]}
          trust_guest_rx_filters: {description: Trust guest receive filter changes; omitted leaves it unmanaged and TrueNAS defaults to false on create., type: bool}
          mac: {description: Fixed MAC address; generated by TrueNAS when omitted., type: str}
          order: {description: Boot order priority (lower numbers boot first)., type: int}
      cdrom:
        description: Install ISO path. An empty string removes the CD-ROM device.
        type: str
            cdrom_order:
                description: CD-ROM boot order priority (lower numbers boot first); defaults to 1000.
                type: int
      display:
        description: Display device. Its password cannot be read back, so it is sent on create and whenever another display attribute changes.
        type: dict
        suboptions:
          type: {description: Display protocol; use VNC to enable a VNC display., type: str, default: SPICE, choices: [SPICE, VNC]}
          bind: {description: Address to bind the console to., type: str, default: 0.0.0.0}
          port: {description: Display port passed to the middleware., type: int}
          web_port: {description: Web proxy port; omitted leaves it unmanaged and TrueNAS assigns it on create., type: int}
          wait: {description: Wait for a display client before booting; omitted leaves it unmanaged., type: bool}
          web: {description: Enable web access for SPICE; VNC requires false and defaults to false., type: bool}
          resolution: {description: Console resolution., type: str}
          password: {description: Console password; VNC passwords must be 1-8 characters, SPICE passwords at least 8 characters., type: str}
          order: {description: Boot order priority (lower numbers boot first)., type: int}
      allow_delete:
        description: Approve deleting the VM (required for I(state=absent)).
        type: bool
        default: false
      allow_restart:
        description: Approve stopping and restarting a running VM for changes that need it.
        type: bool
        default: false
      allow_disk_delete:
        description: Also destroy the VM's zvols when deleting it.
        type: bool
        default: false
  vm_apply:
    description: Allow VM mutations; false plans using read-only queries. Check mode always prevents mutations.
    type: bool
    default: false
  vm_job_timeout:
    description: Maximum seconds to wait for each VM middleware job; a timeout does not cancel the job.
    type: int
    default: 900
  vm_health_timeout:
    description: Maximum seconds to wait for each desired VM runtime state.
    type: int
    default: 180
  vm_poll_interval:
    description: Seconds between VM job and runtime checks.
    type: int
    default: 5
  namespace:
    description: API namespace, e.g. C(sharing.smb), C(user), C(pool.dataset), C(directoryservices).
    type: str
  lookup:
    description: Equality filters used to find the object (resource mode). Names are translated by I(name_to_id).
    type: dict
    default: {}
  config:
    description: Desired state. Only the keys listed here are compared; other attributes are left alone.
    type: dict
    default: {}
  state:
    description: Whether the object should exist (resource mode).
    type: str
    default: present
    choices: [present, absent]
  id_key:
    description: Attribute holding the object id passed to update/delete.
    type: str
    default: id
  create_only_keys:
    description: Keys sent on create but never compared or sent on update.
    type: list
    elements: str
    default: []
  skip_compare_keys:
    description: Keys never compared (the API returns them in another shape than it accepts them).
    type: list
    elements: str
    default: []
  sensitive_keys:
    description: Keys that cannot be read back (passwords). Sent on create, and on update only if requested.
    type: list
    elements: str
    default: []
  send_sensitive_on_update:
    description: Always send I(sensitive_keys) with an update.
    type: bool
    default: false
  send_sensitive_when:
    description: Send I(sensitive_keys) with an update only when one of these keys changed.
    type: list
    elements: str
    default: []
  name_to_id:
    description:
      - Map of config/lookup key to C(namespace:field). Names are replaced by ids through C(namespace.query).
      - Example C({groups: "group:name"}).
    type: dict
    default: {}
  no_create:
    description: Fail instead of creating a missing object.
    type: bool
    default: false
  query_options:
    description: Second argument passed to C(<namespace>.query).
    type: dict
    default: {}
  delete_args:
    description: Extra arguments passed to C(<namespace>.delete) after the id.
    type: list
    elements: raw
    default: []
  job:
    description: The update (config mode) or call (call mode) is a middleware job; wait for it.
    type: bool
    default: false
  method:
    description: Method name for C(mode=call).
    type: str
  args:
    description: Positional arguments for C(mode=call).
    type: list
    elements: raw
    default: []
  read_only:
    description: C(mode=call) only reads data; never reports changed and also runs in check mode.
    type: bool
    default: false
  ignore_error_patterns:
    description: C(mode=call) regular expressions; a matching error is reported as unchanged instead of failing.
    type: list
    elements: str
    default: []
  transport:
    description: Force a transport. C(auto) prefers truenas_api_client.
    type: str
    default: auto
    choices: [auto, client, midclt]
author:
  - truenas role
"""

EXAMPLES = r"""
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
"""

RETURN = r"""
action:
  description: created, updated, deleted or none (resource/config mode).
  returned: resource/config
  type: str
changed_keys:
  description: Keys that differ from the desired state.
  returned: resource/config
  type: list
id:
  description: Id of the object.
  returned: resource
  type: raw
result:
  description: API return value (call mode).
  returned: call
  type: raw
"""

import copy
import json
import re
import time
from typing import Any, Dict, List, NamedTuple, Optional, Set

import yaml

from ansible.module_utils.basic import AnsibleModule

try:  # present on TrueNAS hosts
    from truenas_api_client import Client as _MiddlewareClient
except Exception:  # pragma: no cover - depends on the target system
    _MiddlewareClient = None


class MiddlewareError(Exception):
    pass


# --------------------------------------------------------------------------- #
# transport
# --------------------------------------------------------------------------- #
class Transport(object):
    def __init__(self, module, transport="auto"):
        self.module = module
        self.transport = transport
        self.client = None

    def __enter__(self):
        if self.transport == "client" and _MiddlewareClient is None:
            raise MiddlewareError("truenas_api_client is not importable on this host")
        if self.transport in ("auto", "client") and _MiddlewareClient is not None:
            try:
                self.client = _MiddlewareClient()
                self.client.__enter__()
            except Exception as exc:
                self.client = None
                if self.transport == "client":
                    raise MiddlewareError("cannot connect with truenas_api_client: %s" % exc)
        return self

    def __exit__(self, *exc_info):
        if self.client is not None:
            try:
                self.client.__exit__(*exc_info)
            except Exception:
                pass
        return False

    @staticmethod
    def _format(method, exc):
        text = getattr(exc, "error", None) or str(exc)
        extra = getattr(exc, "extra", None)
        if extra:
            text = "%s (%s)" % (text, json.dumps(extra, default=str))
        return "%s failed: %s" % (method, text)

    def call(self, method, *args, **kwargs):
        job = kwargs.get("job", False)
        if self.client is not None:
            try:
                return self.client.call(method, *args, job=job)
            except Exception as exc:
                raise MiddlewareError(self._format(method, exc))
        return self._midclt(method, args, job)

    def _midclt(self, method, args, job):
        cmd = ["midclt", "call"]
        if job:
            cmd.append("-job")
        cmd.append(method)
        cmd.extend(json.dumps(a) for a in args)
        rc, out, err = self.module.run_command(cmd)
        if rc != 0:
            raise MiddlewareError("%s failed (rc=%s): %s" % (method, rc, (err or out).strip()))
        out = (out or "").strip()
        if not out:
            return None
        try:
            return json.loads(out)
        except ValueError:
            for line in reversed(out.splitlines()):
                try:
                    return json.loads(line)
                except ValueError:
                    continue
            return out


# --------------------------------------------------------------------------- #
# comparison helpers
# --------------------------------------------------------------------------- #
def _scalar_eq(want, have, ci=False):
    if want == have:
        return True
    if isinstance(want, bool) or isinstance(have, bool):
        return False
    if want is None or have is None:
        return False
    a, b = str(want), str(have)
    return a.lower() == b.lower() if ci else a == b


def matches(want, have):
    """True when `have` already satisfies `want` (subset semantics for dicts)."""
    # ZFS style property wrappers: {"parsed":..., "rawvalue":..., "value":...}
    if isinstance(have, dict) and "rawvalue" in have and not isinstance(want, (dict, list)):
        return any(_scalar_eq(want, have.get(k), ci=True) for k in ("parsed", "value", "rawvalue"))
    if isinstance(want, dict):
        if not isinstance(have, dict):
            return False
        return all(matches(v, have.get(k)) for k, v in want.items())
    if isinstance(want, list):
        if not isinstance(have, list) or len(want) != len(have):
            return False
        if all(not isinstance(x, (dict, list)) for x in want):
            return sorted(str(x) for x in want) == sorted(str(x) for x in have)
        remaining = list(have)
        for item in want:
            for idx, cand in enumerate(remaining):
                if matches(item, cand):
                    remaining.pop(idx)
                    break
            else:
                return False
        return True
    return _scalar_eq(want, have)


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def resolve_names(tp, data, spec):
    """Replace names by ids in `data` in place, following spec {key: 'ns:field'}."""
    for key, target in (spec or {}).items():
        if key not in data or data[key] is None:
            continue
        namespace, _, field = target.partition(":")
        if not field:
            raise MiddlewareError("name_to_id entry '%s' must look like namespace:field" % key)
        value = data[key]
        names = value if isinstance(value, list) else [value]
        todo = [n for n in names if not _is_int(n)]
        if not todo:
            continue
        rows = tp.call(namespace + ".query", [[field, "in", todo]])
        mapping = dict((row[field], row["id"]) for row in rows)
        missing = [n for n in todo if n not in mapping]
        if missing:
            raise MiddlewareError("%s: %s not found for '%s'" % (namespace, ", ".join(map(str, missing)), key))
        resolved = [n if _is_int(n) else mapping[n] for n in names]
        data[key] = resolved if isinstance(value, list) else resolved[0]


def diff_keys(desired, current, skip):
    changes = {}
    for key, want in desired.items():
        if key in skip:
            continue
        if not matches(want, current.get(key)):
            changes[key] = want
    return changes


def redact(data, sensitive):
    return dict((k, ("<redacted>" if k in sensitive else v)) for k, v in data.items())


# --------------------------------------------------------------------------- #
# modes
# --------------------------------------------------------------------------- #
def _sensitive_payload(p, desired, changes, payload):
    sensitive = set(p["sensitive_keys"])
    if not changes or not sensitive:
        return
    if p["send_sensitive_on_update"] or any(k in changes for k in p["send_sensitive_when"]):
        for key in sensitive:
            if key in desired:
                payload[key] = desired[key]


def run_resource(module, tp):
    p = module.params
    ns = p["namespace"]
    if not p["lookup"]:
        raise MiddlewareError("resource mode needs a non-empty lookup")
    lookup = copy.deepcopy(p["lookup"])
    desired = copy.deepcopy(p["config"])
    resolve_names(tp, lookup, p["name_to_id"])
    resolve_names(tp, desired, p["name_to_id"])

    filters = [[k, "=", v] for k, v in sorted(lookup.items())]
    query_args = [filters]
    if p["query_options"]:
        query_args.append(p["query_options"])
    rows = tp.call(ns + ".query", *query_args)
    if len(rows) > 1:
        raise MiddlewareError("lookup %s matched %d objects in %s" % (json.dumps(lookup), len(rows), ns))
    current = rows[0] if rows else None

    sensitive = set(p["sensitive_keys"])
    skip = sensitive | set(p["create_only_keys"]) | set(p["skip_compare_keys"])
    id_key = p["id_key"]
    result = dict(changed=False, action="none", changed_keys=[])

    if p["state"] == "absent":
        if current is None:
            return result
        result.update(changed=True, action="deleted", id=current.get(id_key))
        if not module.check_mode:
            tp.call(ns + ".delete", current[id_key], *p["delete_args"])
        return result

    if current is None:
        if p["no_create"]:
            raise MiddlewareError("%s %s does not exist and no_create is set" % (ns, json.dumps(lookup)))
        result.update(changed=True, action="created", changed_keys=sorted(desired))
        result["diff"] = dict(before={}, after=redact(desired, sensitive))
        if not module.check_mode:
            created = tp.call(ns + ".create", desired)
            if isinstance(created, dict):
                result["id"] = created.get(id_key)
        return result

    changes = diff_keys(desired, current, skip)
    result["id"] = current.get(id_key)
    if not changes:
        return result
    payload = dict(changes)
    if ns == "sharing.smb" and "options" in payload and "purpose" in desired and "purpose" not in payload:
        payload["purpose"] = desired["purpose"]
    if ns == "sharing.nfs":
        if "maproot_user" in desired or "maproot_group" in desired:
            payload.setdefault("mapall_user", None)
            payload.setdefault("mapall_group", None)
        if "mapall_user" in desired or "mapall_group" in desired:
            payload.setdefault("maproot_user", None)
            payload.setdefault("maproot_group", None)
    _sensitive_payload(p, desired, changes, payload)
    result.update(changed=True, action="updated", changed_keys=sorted(changes))
    result["diff"] = dict(before=dict((k, current.get(k)) for k in changes), after=changes)
    if not module.check_mode:
        tp.call(ns + ".update", current[id_key], payload)
    return result


def run_config(module, tp):
    p = module.params
    ns = p["namespace"]
    desired = copy.deepcopy(p["config"])
    resolve_names(tp, desired, p["name_to_id"])
    current = tp.call(ns + ".config")
    skip = set(p["sensitive_keys"]) | set(p["create_only_keys"]) | set(p["skip_compare_keys"])
    changes = diff_keys(desired, current, skip)
    result = dict(changed=False, action="none", changed_keys=[])
    if not changes:
        return result
    payload = dict(changes)
    _sensitive_payload(p, desired, changes, payload)
    result.update(changed=True, action="updated", changed_keys=sorted(changes))
    result["diff"] = dict(before=dict((k, current.get(k)) for k in changes), after=changes)
    if not module.check_mode:
        tp.call(ns + ".update", payload, job=p["job"])
    return result


def run_call(module, tp):
    p = module.params
    if p["read_only"]:
        return dict(changed=False, result=tp.call(p["method"], *p["args"], job=p["job"]))
    if module.check_mode:
        return dict(changed=True, msg="check mode: would call %s" % p["method"])
    try:
        out = tp.call(p["method"], *p["args"], job=p["job"])
    except MiddlewareError as exc:
        for pattern in p["ignore_error_patterns"]:
            if re.search(pattern, str(exc)):
                return dict(changed=False, msg="ignored: %s" % exc, ignored_error=str(exc))
        raise
    return dict(changed=True, result=out)


def app_job(tp, method, args, timeout, interval):
    job_id = tp.call(method, *args)
    if not _is_int(job_id):
        raise MiddlewareError("%s did not return a job ID" % method)
    deadline = time.monotonic() + timeout
    while True:
        jobs = tp.call("core.get_jobs", [["id", "=", job_id]])
        if len(jobs) != 1:
            raise MiddlewareError("Cannot find %s job %s" % (method, job_id))
        state = jobs[0]["state"]
        if state == "SUCCESS":
            return jobs[0].get("result")
        if state in ("FAILED", "ABORTED"):
            raise MiddlewareError("%s job %s ended in %s; inspect TrueNAS job logs" % (method, job_id, state))
        if time.monotonic() >= deadline:
            raise MiddlewareError("%s job %s timed out; it may still be running; inspect before retrying" % (method, job_id))
        time.sleep(min(interval, max(0, deadline - time.monotonic())))


def app_config_matches(desired, current):
    if isinstance(desired, dict):
        return isinstance(current, dict) and all(
            key in current and app_config_matches(value, current[key])
            for key, value in desired.items()
        )
    if isinstance(desired, list):
        return isinstance(current, list) and len(desired) == len(current) and all(
            app_config_matches(want, have) for want, have in zip(desired, current)
        )
    return type(desired) is type(current) and desired == current


def app_wait_state(tp, name, expected, timeout, interval):
    deadline = time.monotonic() + timeout
    while True:
        rows = tp.call("app.query", [["id", "=", name]])
        if expected == "ABSENT" and not rows:
            return "ABSENT"
        current = rows[0].get("state") if len(rows) == 1 else "ABSENT"
        if current == expected:
            return current
        if time.monotonic() >= deadline:
            raise MiddlewareError("App %s did not reach %s (last state: %s); inspect TrueNAS" % (name, expected, current))
        time.sleep(min(interval, max(0, deadline - time.monotonic())))


def app_merge(current, desired):
    result = copy.deepcopy(current)
    for key, value in desired.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = app_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def run_app(module, tp):
    definition = module.params["app"]
    allowed = {"name", "source", "state", "runtime", "catalog", "values", "compose", "allow_delete", "allow_upgrade"}
    if set(definition) - allowed:
        raise MiddlewareError("Unrecognized top-level Apps fields; place application settings inside values or compose")
    name = definition.get("name", "")
    source = definition.get("source")
    desired_state = definition.get("state", "present")
    runtime = definition.get("runtime", "running")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z](?:[-a-z0-9]*[a-z0-9])?", name) or len(name) > 40:
        raise MiddlewareError("App name must be lowercase, start with a letter, end with an alphanumeric, and be at most 40 characters")
    if source not in ("catalog", "custom") or desired_state not in ("present", "absent") or runtime not in ("running", "stopped"):
        raise MiddlewareError("Invalid app source, state, or runtime")
    for gate in ("allow_delete", "allow_upgrade"):
        if gate in definition and not isinstance(definition[gate], bool):
            raise MiddlewareError("%s must be a boolean" % gate)
    timeout = module.params["app_job_timeout"]
    health_timeout = module.params["app_health_timeout"]
    interval = module.params["app_poll_interval"]
    if min(timeout, health_timeout, interval) <= 0:
        raise MiddlewareError("Apps job timeout, health timeout, and polling interval must be positive")
    dry_run = module.check_mode or not module.params["app_apply"]
    result = dict(changed=False, name=name, actions=[], planned=dry_run)
    payload = {}
    catalog = {}
    if desired_state == "present":
        if source == "custom":
            if "catalog" in definition or "values" in definition:
                raise MiddlewareError("Custom apps cannot specify catalog or values")
            try:
                compose = yaml.safe_load(definition.get("compose", ""))
            except (yaml.YAMLError, TypeError):
                raise MiddlewareError("Custom app compose must be valid YAML")
            if not isinstance(compose, dict) or not isinstance(compose.get("services"), dict) or not compose["services"]:
                raise MiddlewareError("Custom compose requires a nonempty services mapping")
            payload = {"custom_compose_config": compose}
        else:
            catalog = definition.get("catalog", {})
            if not isinstance(catalog, dict) or any(
                not isinstance(catalog.get(key), str) or not catalog[key].strip()
                for key in ("app", "train", "version")
            ) or catalog["version"] == "latest":
                raise MiddlewareError("Catalog apps require app, train, and an explicit version other than latest")
            if "compose" in definition or not isinstance(definition.get("values", {}), dict):
                raise MiddlewareError("Catalog apps require mapping values and cannot specify compose")
            payload = {"values": definition.get("values", {})}
    rows = tp.call("app.query", [["id", "=", name]])
    if len(rows) > 1:
        raise MiddlewareError("App identity is ambiguous")
    current = rows[0] if rows else None
    if current and current.get("custom_app") is not (source == "custom"):
        raise MiddlewareError("Existing app source differs; automatic source conversion is refused")
    if desired_state == "absent":
        if current is None:
            return result
        result.update(changed=True, actions=["delete"], approval_required=not definition.get("allow_delete", False))
        if not dry_run:
            if not definition.get("allow_delete", False):
                raise MiddlewareError("App deletion requires allow_delete: true and a reviewed backup/data-retention plan")
            app_job(tp, "app.delete", [name, {"remove_images": False, "remove_ix_volumes": False}], timeout, interval)
            result["runtime_state"] = app_wait_state(tp, name, "ABSENT", health_timeout, interval)
        return result
    if current and source == "catalog":
        metadata = current.get("metadata", {})
        if metadata.get("name") != catalog["app"] or metadata.get("train") != catalog["train"]:
            raise MiddlewareError("Existing catalog app/train differs; automatic catalog replacement is refused")
    if current is None:
        result["actions"].append("create")
        create = dict(payload, app_name=name, custom_app=(source == "custom"))
        if source == "catalog":
            create.update(catalog_app=catalog["app"], train=catalog["train"], version=catalog["version"])
        if not dry_run:
            app_job(tp, "app.create", [create], timeout, interval)
    else:
        current_config = tp.call("app.config", name)
        if not isinstance(current_config, dict):
            raise MiddlewareError("App configuration is not a mapping")
        if source == "catalog" and current.get("version") != catalog["version"]:
            result["actions"].append("upgrade")
            result["approval_required"] = not definition.get("allow_upgrade", False)
            if not dry_run:
                if not definition.get("allow_upgrade", False):
                    raise MiddlewareError("Catalog version change requires allow_upgrade: true; downgrades require a separate rollback workflow")
                summary = tp.call("app.upgrade_summary", name, {"app_version": catalog["version"]})
                if summary.get("upgrade_version") != catalog["version"]:
                    raise MiddlewareError("Requested catalog version is not an available upgrade")
                app_job(tp, "app.upgrade", [name, {"app_version": catalog["version"], "values": app_merge(current_config, payload["values"])}], timeout, interval)
        elif source == "custom":
            desired = payload["custom_compose_config"]
            if not (app_config_matches(desired, current_config) and app_config_matches(current_config, desired)):
                result["actions"].append("update")
                if not dry_run:
                    app_job(tp, "app.update", [name, payload], timeout, interval)
        elif not app_config_matches(payload["values"], current_config):
            result["actions"].append("update")
            if not dry_run:
                app_job(tp, "app.update", [name, {"values": app_merge(current_config, payload["values"])}], timeout, interval)
    expected = "RUNNING" if runtime == "running" else "STOPPED"
    if not dry_run:
        rows = tp.call("app.query", [["id", "=", name]])
        if len(rows) != 1:
            raise MiddlewareError("App missing after reconciliation")
        current = rows[0]
    current_state = current.get("state") if current else None
    if runtime == "stopped" and current_state != "STOPPED":
        result["actions"].append("stop")
        if not dry_run:
            app_job(tp, "app.stop", [name], timeout, interval)
    elif runtime == "running" and current_state in ("STOPPED", "CRASHED"):
        result["actions"].append("start")
        if not dry_run:
            app_job(tp, "app.start", [name], timeout, interval)
    result["changed"] = bool(result["actions"])
    if not dry_run:
        result["runtime_state"] = app_wait_state(tp, name, expected, health_timeout, interval)
    else:
        result["runtime_state"] = current_state or "ABSENT"
    return result

# --------------------------------------------------------------------------- #
# vm mode
# --------------------------------------------------------------------------- #
VM_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
VM_ZVOL = re.compile(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.:-]+)+")
VM_RESTART_KEYS = (
    "vcpus", "cores", "threads", "memory", "bootloader", "cpu_mode", "cpu_model",
    "cpuset", "pin_vcpus", "nodeset", "hide_from_msr", "ensure_display_device",
    "time", "enable_secure_boot", "trusted_platform_module",
)
GIB = 1024 ** 3


def vm_status(row):
    return ((row or {}).get("status") or {}).get("state")


def vm_wait_state(tp, name, expected, timeout, interval):
    deadline = time.monotonic() + timeout
    while True:
        rows = tp.call("vm.query", [["name", "=", name]])
        current = vm_status(rows[0]) if len(rows) == 1 else "ABSENT"
        if current == expected:
            return current
        if time.monotonic() >= deadline:
            raise MiddlewareError("VM %s did not reach %s (last state: %s); inspect TrueNAS" % (name, expected, current))
        time.sleep(min(interval, max(0, deadline - time.monotonic())))


def vm_dev_type(dev):
    return dev.get("dtype") or (dev.get("attributes") or {}).get("dtype")


def vm_dev_attrs(dev):
    return dict(dev.get("attributes") or {})


def vm_device_shape(tp):
    """25.04+ puts dtype inside attributes; earlier releases keep it top-level.
    Verify against /api/docs/ on your release; this is the only place to change."""
    match = re.match(r"(\d+)\.(\d+)", str(tp.call("system.version_short")))
    return "typed" if match and (int(match.group(1)), int(match.group(2))) >= (25, 4) else "flat"


def vm_device_data(shape, dtype, attrs, vm_id=None, order=None):
    if shape == "typed":
        data = {"attributes": dict(attrs, dtype=dtype)}
    else:
        data = {"dtype": dtype, "attributes": dict(attrs)}
    if vm_id is not None:
        data["vm"] = vm_id
    if order is not None:
        data["order"] = order
    return data


def vm_zfs_int(value):
    if isinstance(value, dict):
        value = value.get("parsed", value.get("rawvalue"))
    return int(value)


def vm_desired_devices(d) -> List[Dict[str, Any]]:
    devices = []
    if d.get("cdrom"):
        order = d.get("cdrom_order")
        devices.append(dict(dtype="CDROM", order=1000 if order is None else order, attrs={"path": d["cdrom"]}))
    for i, disk in enumerate(d["disks"]):
        attrs = {"path": "/dev/zvol/%s" % disk["zvol"], "type": disk["type"]}
        if disk.get("disk_sectorsize") is not None:
            attrs["logical_sectorsize"] = disk["disk_sectorsize"]
            attrs["physical_sectorsize"] = disk["disk_sectorsize"]
        order = disk.get("order")
        devices.append(dict(dtype="DISK", order=1001 + i if order is None else order, attrs=attrs))
    for i, nic in enumerate(d["nics"]):
        attrs = {"type": nic["type"], "nic_attach": nic["attach"]}
        if nic.get("trust_guest_rx_filters") is not None:
            attrs["trust_guest_rx_filters"] = nic["trust_guest_rx_filters"]
        if nic.get("mac"):
            attrs["mac"] = nic["mac"]
        order = nic.get("order")
        devices.append(dict(dtype="NIC", order=1100 + i if order is None else order, attrs=attrs))
    display = d.get("display")
    if display:
        attrs = {"type": display["type"], "bind": display["bind"]}
        for key in ("web_port", "wait", "web"):
            if display.get(key) is not None:
                attrs[key] = display[key]
        if display["type"] == "VNC":
            if display.get("web") is True:
                raise MiddlewareError("VNC displays require web: false; use SPICE for web access")
            attrs["web"] = False
        if display.get("port") is not None:
            attrs["port"] = display["port"]
        if display.get("resolution"):
            attrs["resolution"] = display["resolution"]
        order = display.get("order")
        devices.append(dict(dtype="DISPLAY", order=1200 if order is None else order, attrs=attrs,
                            secret={"password": display["password"]}))
    return devices


def vm_device_changes(current_devices, ops):
    current_by_id = {dev["id"]: dev for dev in current_devices or []}
    details = []
    for operation, want, device_id, _attrs in ops:
        have = current_by_id.get(device_id, {})
        before = vm_dev_attrs(have)
        fields = {}
        if operation == "update":
            for key, value in want["attrs"].items():
                if key != "password" and not matches(value, before.get(key)):
                    fields[key] = {"before": before.get(key), "after": value}
            if have.get("order") != want["order"]:
                fields["order"] = {"before": have.get("order"), "after": want["order"]}
        details.append(dict(operation=operation, dtype=want["dtype"], id=device_id, fields=fields))
    return details


def vm_plan_devices(current_devices, desired, drop_cdrom, managed_pptdevs=None):
    """Create missing devices and update drifted ones. Extra devices are never
    removed (they may hold data); the only deletion is an explicit cdrom: ''."""
    by_type = {}
    for dev in current_devices or []:
        by_type.setdefault(vm_dev_type(dev), []).append(dev)
    seen = {}
    ops = []
    for want in desired:
        dtype = want["dtype"]
        pool = by_type.get(dtype, [])
        if dtype == "DISK":
            have = next((x for x in pool if vm_dev_attrs(x).get("path") == want["attrs"]["path"]), None)
        elif dtype == "PCI":
            have = next((x for x in pool if vm_dev_attrs(x).get("pptdev") == want["attrs"]["pptdev"]), None)
        else:
            idx = seen.get(dtype, 0)
            seen[dtype] = idx + 1
            have = pool[idx] if idx < len(pool) else None
        secret = want.get("secret", {})
        if have is None:
            ops.append(("create", want, None, dict(want["attrs"], **secret)))
        elif have.get("order") != want["order"] or not matches(want["attrs"], vm_dev_attrs(have)):
            merged = dict(vm_dev_attrs(have), **want["attrs"])
            merged.update(secret)
            ops.append(("update", want, have["id"], merged))
    if managed_pptdevs is not None:
        desired_pptdevs = set(
            want["attrs"]["pptdev"] for want in desired if want["dtype"] == "PCI"
        )
        for dev in by_type.get("PCI", []):
            pptdev = vm_dev_attrs(dev).get("pptdev")
            if pptdev in managed_pptdevs and pptdev not in desired_pptdevs:
                ops.append(("delete", {"dtype": "PCI", "attrs": {"pptdev": pptdev}}, dev["id"], None))
    if drop_cdrom:
        for dev in by_type.get("CDROM", []):
            ops.append(("delete", {"dtype": "CDROM"}, dev["id"], None))
    return ops


def vm_plan_zvols(tp, disks):
    plan = []
    for disk in disks:
        zvol = disk["zvol"]
        want = disk["size_gib"] * GIB
        rows = tp.call("pool.dataset.query", [["id", "=", zvol]])
        if not rows:
            parent = zvol.rsplit("/", 1)[0]
            if not tp.call("pool.dataset.query", [["id", "=", parent]]):
                raise MiddlewareError("Parent dataset %s for zvol %s does not exist" % (parent, zvol))
            plan.append(("create", zvol, want, disk["sparse"]))
            continue
        if rows[0].get("type") != "VOLUME":
            raise MiddlewareError("%s exists but is not a zvol" % zvol)
        have = vm_zfs_int(rows[0]["volsize"])
        if want < have:
            raise MiddlewareError("Refusing to shrink zvol %s from %d to %d GiB" % (zvol, have // GIB, want // GIB))
        if want > have:
            plan.append(("grow", zvol, want, None))
    return plan


class VmGpuPlan(NamedTuple):
    devices: List[Dict[str, Any]]
    managed_pptdevs: Optional[Set[str]]
    isolate: List[str]


def vm_gpu_plan(tp, selected_gpus: Optional[List[str]]) -> VmGpuPlan:
    if selected_gpus is None:
        return VmGpuPlan([], None, [])
    if len(set(selected_gpus)) != len(selected_gpus):
        raise MiddlewareError("GPU selections must not contain duplicate PCI slots")

    choices = tp.call("system.advanced.get_gpu_pci_choices")
    choices_by_slot = {
        choice.get("pci_slot"): choice
        for choice in choices.values()
        if isinstance(choice, dict) and choice.get("pci_slot")
    }
    for pci_slot in selected_gpus:
        choice = choices_by_slot.get(pci_slot)
        if choice is None:
            raise MiddlewareError("GPU PCI slot %s is not available for passthrough" % pci_slot)
        if choice.get("uses_system_critical_devices", False):
            reason = choice.get("critical_reason") or "it uses devices critical to the host"
            raise MiddlewareError("GPU PCI slot %s cannot be passed through: %s" % (pci_slot, reason))

    gpu_rows = tp.call("device.get_info", [{"type": "GPU"}])
    gpu_by_slot = {
        (gpu.get("addr") or {}).get("pci_slot"): gpu
        for gpu in gpu_rows
        if isinstance(gpu, dict) and (gpu.get("addr") or {}).get("pci_slot")
    }
    managed_pptdevs = set()
    for gpu in gpu_rows:
        for function in gpu.get("devices", []) if isinstance(gpu, dict) else []:
            pptdev = function.get("vm_pci_slot") if isinstance(function, dict) else None
            if pptdev:
                managed_pptdevs.add(pptdev)

    devices = []
    seen_pptdevs = set()
    for pci_slot in selected_gpus:
        gpu = gpu_by_slot.get(pci_slot)
        if gpu is None:
            raise MiddlewareError("GPU PCI slot %s has no device information" % pci_slot)
        functions = [
            function.get("vm_pci_slot")
            for function in gpu.get("devices", [])
            if isinstance(function, dict) and function.get("vm_pci_slot")
        ]
        if not functions:
            raise MiddlewareError("GPU PCI slot %s has no passthrough functions" % pci_slot)
        for pptdev in functions:
            if pptdev in seen_pptdevs:
                continue
            seen_pptdevs.add(pptdev)
            devices.append(dict(dtype="PCI", order=1300 + len(devices), attrs={"pptdev": pptdev}))

    config = tp.call("system.advanced.config")
    isolated = config.get("isolated_gpu_pci_ids", []) if isinstance(config, dict) else []
    isolate = [pci_slot for pci_slot in selected_gpus if pci_slot not in isolated]
    return VmGpuPlan(devices, managed_pptdevs, isolate)


def vm_apply_gpu_isolation(tp, selected_gpus):
    if not selected_gpus:
        return
    config = tp.call("system.advanced.config")
    isolated = config.get("isolated_gpu_pci_ids", []) if isinstance(config, dict) else []
    merged = list(dict.fromkeys(isolated + selected_gpus))
    if merged != isolated:
        tp.call("system.advanced.update_gpu_pci_ids", merged)

def run_vm(module, tp):
    d = module.params["vm"]
    name = d["name"]
    state, runtime = d["state"], d["runtime"]
    if not VM_NAME.fullmatch(name) or len(name) > 40:
        raise MiddlewareError("VM name must start with a letter, use only letters, digits and underscores, and be at most 40 characters")
    timeout = module.params["vm_job_timeout"]
    health_timeout = module.params["vm_health_timeout"]
    interval = module.params["vm_poll_interval"]
    if min(timeout, health_timeout, interval) <= 0:
        raise MiddlewareError("VM job timeout, health timeout, and polling interval must be positive")
    dry_run = module.check_mode or not module.params["vm_apply"]
    result = dict(changed=False, name=name, actions=[], planned=dry_run, approval_required=[])
    actions = result["actions"]

    rows = tp.call("vm.query", [["name", "=", name]])
    if len(rows) > 1:
        raise MiddlewareError("VM identity is ambiguous")
    current = rows[0] if rows else None
    status = vm_status(current)
    running = status == "RUNNING"
    result["runtime_state"] = status or "ABSENT"
    stop_args = {"force": False, "force_after_timeout": True}

    if state == "absent":
        if current is None:
            return result
        if running:
            actions.append("stop")
        actions.append("delete")
        if d["allow_disk_delete"]:
            actions.append("delete_zvols")
        if not d["allow_delete"]:
            result["approval_required"].append("allow_delete")
        result["changed"] = True
        if not dry_run:
            if not d["allow_delete"]:
                raise MiddlewareError("VM deletion requires allow_delete: true and a reviewed backup/data-retention plan")
            if running:
                app_job(tp, "vm.stop", [current["id"], stop_args], timeout, interval)
                vm_wait_state(tp, name, "STOPPED", health_timeout, interval)
            tp.call("vm.delete", current["id"], {"zvols": bool(d["allow_disk_delete"]), "force": False})
            result["runtime_state"] = "ABSENT"
        return result

    # ---- validate desired hardware -------------------------------------- #
    if not d["memory_mib"] or d["memory_mib"] < 256:
        raise MiddlewareError("memory_mib must be at least 256")
    if not d["disks"] or not d["nics"]:
        raise MiddlewareError("A VM needs at least one disk and one NIC")
    for disk in d["disks"]:
        if not VM_ZVOL.fullmatch(disk["zvol"]) or disk["size_gib"] <= 0:
            raise MiddlewareError("Each disk needs a pool/path zvol name and a positive size_gib")
    if len(set(x["zvol"] for x in d["disks"])) != len(d["disks"]):
        raise MiddlewareError("Duplicate zvol within one VM")
    if d["display"]:
        display_password = d["display"].get("password") or ""
        if d["display"]["type"] == "VNC" and not 1 <= len(display_password) <= 8:
            raise MiddlewareError("VNC display passwords must be between 1 and 8 characters")
        if d["display"]["type"] != "VNC" and len(display_password) < 8:
            raise MiddlewareError("SPICE display passwords must be at least 8 characters")
    cpu = d["cpu"] or {}
    desired = dict(
        name=name,
        description=d["description"] or "",
        vcpus=cpu.get("vcpus") or 1,
        cores=cpu.get("cores") or 1,
        threads=cpu.get("threads") or 1,
        memory=d["memory_mib"],
        bootloader=d["bootloader"],
        autostart=bool(d["autostart"]),
    )
    cpu_fields = {
        "mode": "cpu_mode",
        "model": "cpu_model",
        "cpuset": "cpuset",
        "pin_vcpus": "pin_vcpus",
        "nodeset": "nodeset",
    }
    cpu_mode = cpu.get("mode")
    if cpu.get("model") and cpu_mode not in (None, "CUSTOM"):
        raise MiddlewareError("cpu.model is only valid when cpu.mode is CUSTOM")
    for key, api_key in cpu_fields.items():
        value = cpu.get(key)
        if value is not None:
            if key in ("model", "cpuset", "nodeset") and value == "":
                value = None
            desired[api_key] = value
    if cpu.get("model") and cpu_mode is None:
        desired["cpu_mode"] = "CUSTOM"
    for key in ("hide_from_msr", "ensure_display_device"):
        if d.get(key) is not None:
            desired[key] = d[key]
    for key in ("time", "enable_secure_boot", "trusted_platform_module", "shutdown_timeout"):
        if d.get(key) is not None:
            desired[key] = d[key]
    if "shutdown_timeout" in desired and not 5 <= desired["shutdown_timeout"] <= 300:
        raise MiddlewareError("shutdown_timeout must be between 5 and 300 seconds")

    gpu_plan = vm_gpu_plan(tp, d.get("gpus"))
    gpu_devices = gpu_plan.devices
    managed_pptdevs = gpu_plan.managed_pptdevs
    gpu_isolation = gpu_plan.isolate
    devices = vm_desired_devices(d) + gpu_devices
    zvol_plan = vm_plan_zvols(tp, d["disks"])

    changes, ops = {}, []
    if current is not None:
        changes = diff_keys(desired, current, set())
        ops = vm_plan_devices(
            current.get("devices"), devices, d["cdrom"] == "", managed_pptdevs
        )
    result["device_changes"] = vm_device_changes((current or {}).get("devices"), ops)
    restart_needed = bool(ops) or any(k in changes for k in VM_RESTART_KEYS)
    need_stop = running and (runtime == "stopped" or restart_needed)
    if need_stop and runtime == "running" and not d["allow_restart"]:
        result["approval_required"].append("allow_restart")

    # ---- plan, in execution order --------------------------------------- #
    for op, zvol, _size, _sparse in zvol_plan:
        actions.append("%s_zvol:%s" % (op, zvol))
    actions.extend("isolate_gpu:%s" % pci_slot for pci_slot in gpu_isolation)
    if need_stop:
        actions.append("stop")
    if current is None:
        actions.append("create")
        actions.extend("create_device:%s" % dev["dtype"] for dev in devices)
    else:
        if changes:
            actions.append("update")
        actions.extend("%s_device:%s" % (op, want["dtype"]) for op, want, _i, _a in ops)
    if runtime == "running" and (not running or need_stop):
        actions.append("start")
    result["changed"] = bool(actions)
    if dry_run:
        return result
    if result["approval_required"]:
        raise MiddlewareError("Restarting running VM %s requires allow_restart: true" % name)

    # ---- apply ---------------------------------------------------------- #
    for op, zvol, size, sparse in zvol_plan:
        if op == "create":
            tp.call("pool.dataset.create", {"name": zvol, "type": "VOLUME", "volsize": size, "sparse": sparse})
        else:
            tp.call("pool.dataset.update", zvol, {"volsize": size})
    if need_stop:
        app_job(tp, "vm.stop", [current["id"], stop_args], timeout, interval)
        vm_wait_state(tp, name, "STOPPED", health_timeout, interval)
    shape = vm_device_shape(tp) if (devices or ops) else None
    if current is None:
        created = tp.call("vm.create", dict(desired, ensure_display_device=d.get("ensure_display_device") is True))
        vm_id = created["id"]
        vm_apply_gpu_isolation(tp, d.get("gpus"))
        for dev in devices:
            attrs = dict(dev["attrs"], **dev.get("secret", {}))
            tp.call("vm.device.create", vm_device_data(shape, dev["dtype"], attrs, vm_id, dev["order"]))
    else:
        vm_id = current["id"]
        if changes:
            tp.call("vm.update", vm_id, changes)
        vm_apply_gpu_isolation(tp, d.get("gpus"))
        for op, want, dev_id, attrs in ops:
            if op == "create":
                tp.call("vm.device.create", vm_device_data(shape, want["dtype"], attrs, vm_id, want["order"]))
            elif op == "update":
                tp.call("vm.device.update", dev_id, vm_device_data(shape, want["dtype"], attrs, order=want["order"]))
            else:
                tp.call("vm.device.delete", dev_id)
    if "start" in actions:
        tp.call("vm.start", vm_id, {"overcommit": False})
    expected = "RUNNING" if runtime == "running" else "STOPPED"
    result["runtime_state"] = vm_wait_state(tp, name, expected, health_timeout, interval)
    return result

def main():
    module = AnsibleModule(
        argument_spec=dict(
            mode=dict(type="str", default="resource", choices=["resource", "config", "call", "app", "vm"]),
            vm=dict(type="dict", options=dict(
                name=dict(type="str", required=True),
                description=dict(type="str", default=""),
                state=dict(type="str", default="present", choices=["present", "absent"]),
                runtime=dict(type="str", default="running", choices=["running", "stopped"]),
                cpu=dict(type="dict", options=dict(
                    vcpus=dict(type="int", default=1),
                    cores=dict(type="int", default=1),
                    threads=dict(type="int", default=1),
                    mode=dict(type="str", choices=["CUSTOM", "HOST-MODEL", "HOST-PASSTHROUGH"]),
                    model=dict(type="str"),
                    cpuset=dict(type="str"),
                    pin_vcpus=dict(type="bool"),
                    nodeset=dict(type="str"),
                )),
                hide_from_msr=dict(type="bool"),
                ensure_display_device=dict(type="bool"),
                gpus=dict(type="list", elements="str"),
                memory_mib=dict(type="int"),
                bootloader=dict(type="str", default="UEFI", choices=["UEFI", "UEFI_CSM"]),
                time=dict(type="str", choices=["LOCAL", "UTC"]),
                enable_secure_boot=dict(type="bool"),
                trusted_platform_module=dict(type="bool"),
                shutdown_timeout=dict(type="int", min=5, max=300),
                autostart=dict(type="bool", default=False),
                disks=dict(type="list", elements="dict", default=[], options=dict(
                    zvol=dict(type="str", required=True),
                    size_gib=dict(type="int", required=True),
                    type=dict(type="str", default="VIRTIO", choices=["VIRTIO", "AHCI"]),
                    sparse=dict(type="bool", default=True),
                    disk_sectorsize=dict(type="int", choices=[512, 4096]),
                    order=dict(type="int"),
                )),
                nics=dict(type="list", elements="dict", default=[], options=dict(
                    attach=dict(type="str", required=True),
                    type=dict(type="str", default="VIRTIO", choices=["VIRTIO", "E1000"]),
                    trust_guest_rx_filters=dict(type="bool"),
                    mac=dict(type="str"),
                    order=dict(type="int"),
                )),
                cdrom=dict(type="str"),
                cdrom_order=dict(type="int"),
                display=dict(type="dict", options=dict(
                    type=dict(type="str", default="SPICE", choices=["SPICE", "VNC"]),
                    bind=dict(type="str", default="0.0.0.0"),
                    port=dict(type="int"),
                    web_port=dict(type="int"),
                    wait=dict(type="bool"),
                    web=dict(type="bool"),
                    resolution=dict(type="str"),
                    password=dict(type="str", no_log=True),
                    order=dict(type="int"),
                )),
                allow_delete=dict(type="bool", default=False),
                allow_restart=dict(type="bool", default=False),
                allow_disk_delete=dict(type="bool", default=False),
            )),
            vm_apply=dict(type="bool", default=False),
            vm_job_timeout=dict(type="int", default=900),
            vm_health_timeout=dict(type="int", default=180),
            vm_poll_interval=dict(type="int", default=5),
            app=dict(type="dict", no_log=True),
            app_apply=dict(type="bool", default=False),
            app_job_timeout=dict(type="int", default=900),
            app_health_timeout=dict(type="int", default=180),
            app_poll_interval=dict(type="int", default=5),
            namespace=dict(type="str"),
            lookup=dict(type="dict", default={}),
            config=dict(type="dict", default={}),
            state=dict(type="str", default="present", choices=["present", "absent"]),
            id_key=dict(type="str", default="id"),
            create_only_keys=dict(type="list", elements="str", default=[]),
            skip_compare_keys=dict(type="list", elements="str", default=[]),
            sensitive_keys=dict(type="list", elements="str", default=[], no_log=False),
            send_sensitive_on_update=dict(type="bool", default=False),
            send_sensitive_when=dict(type="list", elements="str", default=[]),
            name_to_id=dict(type="dict", default={}),
            no_create=dict(type="bool", default=False),
            query_options=dict(type="dict", default={}),
            delete_args=dict(type="list", elements="raw", default=[]),
            job=dict(type="bool", default=False),
            method=dict(type="str"),
            args=dict(type="list", elements="raw", default=[]),
            read_only=dict(type="bool", default=False),
            ignore_error_patterns=dict(type="list", elements="str", default=[]),
            transport=dict(type="str", default="auto", choices=["auto", "client", "midclt"]),
        ),
        required_if=[
            ("mode", "resource", ["namespace"]),
            ("mode", "config", ["namespace"]),
            ("mode", "call", ["method"]),
            ("mode", "app", ["app"]),
            ("mode", "vm", ["vm"]),
        ],
        supports_check_mode=True,
    )
    runner = dict(resource=run_resource, config=run_config, call=run_call, app=run_app, vm=run_vm)[module.params["mode"]]
    try:
        with Transport(module, module.params["transport"]) as tp:
            result = runner(module, tp)
    except MiddlewareError as exc:
        module.fail_json(msg=str(exc))
    module.exit_json(**result)


if __name__ == "__main__":
    main()
