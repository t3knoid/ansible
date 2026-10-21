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
options:
  mode:
    description: Operating mode.
    type: str
    default: resource
        choices: [resource, config, call, app]
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            mode=dict(type="str", default="resource", choices=["resource", "config", "call", "app"]),
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
        ],
        supports_check_mode=True,
    )
    runner = dict(resource=run_resource, config=run_config, call=run_call, app=run_app)[module.params["mode"]]
    try:
        with Transport(module, module.params["transport"]) as tp:
            result = runner(module, tp)
    except MiddlewareError as exc:
        module.fail_json(msg=str(exc))
    module.exit_json(**result)


if __name__ == "__main__":
    main()
