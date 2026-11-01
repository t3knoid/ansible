from __future__ import annotations

DOCUMENTATION = r'''
name: consolidated_variable
author: Frank Refol
short_description: Consolidate a list variable across several inventories
description:
  - Loads every inventory found under O(inventory_dir) independently.
  - Role C(defaults) and C(vars) are injected as lowest-precedence variables on the C(all) group.
  - Each host's value is rendered in that host's own variable context, then results are concatenated.
options:
  _terms:
    description: Name of the variable to consolidate (exactly one).
    required: true
  inventory_dir:
    description: Directory whose subdirectories are individual inventories.
    type: path
    required: true
  roles_dir:
    description: Roles directory; role C(defaults) and C(vars) are loaded as lowest-precedence vars.
    type: path
  include_hostvars:
    description: Make C(hostvars) available while rendering (slower).
    type: bool
    default: false
  dedupe:
    description: Drop items that are identical after rendering.
    type: bool
    default: true
'''

RETURN = r'''
_raw:
  description: The consolidated, rendered list items.
  type: list
  elements: raw
'''

import json
import os
from collections.abc import Mapping

from ansible.errors import AnsibleLookupError
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.compat.version import LooseVersion
from ansible.plugins.lookup import LookupBase
from ansible.release import __version__ as ANSIBLE_VERSION
from ansible.vars.manager import VariableManager

VAR_EXTS = (".yml", ".yaml", ".json")
LAZY_TEMPLATING = LooseVersion(ANSIBLE_VERSION.split("rc")[0].split("b")[0]) >= LooseVersion("2.19")


def _materialize(value):
    """Recursively read every value so lazy templates render now, inside the plugin."""
    if isinstance(value, Mapping):
        return {k: _materialize(value[k]) for k in value}
    if isinstance(value, (list, tuple)):
        return [_materialize(v) for v in value]
    return value


class LookupModule(LookupBase):

    def _role_vars(self, roles_dir):
        """Role defaults first, then role vars (vars win). Later roles win alphabetically."""
        out = {}
        if not roles_dir:
            return out
        if not os.path.isdir(roles_dir):
            raise AnsibleLookupError(f"roles_dir not found: {roles_dir}")
        for sub in ("defaults", "vars"):
            for role in sorted(os.listdir(roles_dir)):
                d = os.path.join(roles_dir, role, sub)
                if not os.path.isdir(d):
                    continue
                for root, _, files in os.walk(d):
                    for name in sorted(files):
                        if name.endswith(VAR_EXTS):
                            path = os.path.join(root, name)
                            data = self._loader.load_from_file(path)
                            if data is None:
                                continue
                            if not isinstance(data, Mapping):
                                raise AnsibleLookupError(f"{path} is not a YAML mapping")
                            out.update(data)
        return out

    def run(self, terms, variables=None, **kwargs):
        if len(terms) != 1:
            raise AnsibleLookupError("consolidated_variable takes exactly one term: the variable name")
        target = terms[0]
        self.set_options(var_options=variables, direct=kwargs)

        base = self.get_option("inventory_dir")
        if not base or not os.path.isdir(base):
            raise AnsibleLookupError(f"inventory_dir not found: {base}")
        role_vars = self._role_vars(self.get_option("roles_dir"))
        include_hostvars = self.get_option("include_hostvars")
        dedupe = self.get_option("dedupe")

        # one source per subdirectory; realpath-dedupe handles symlinked inventories
        sources, seen_src = [], set()
        for name in sorted(os.listdir(base)):
            path = os.path.join(base, name)
            real = os.path.realpath(path)
            if os.path.isdir(path) and real not in seen_src:
                seen_src.add(real)
                sources.append(path)
        if not sources:
            raise AnsibleLookupError(f"no inventories found under {base}")

        results, seen_items = [], set()
        for src in sources:
            inv_name = os.path.basename(src)
            inv = InventoryManager(loader=self._loader, sources=[src])

            # Lowest-precedence injection: inventory files and group_vars/host_vars still override.
            all_group = inv.groups["all"]
            for k, v in role_vars.items():
                if k not in all_group.vars:
                    all_group.set_variable(k, v)

            vm = VariableManager(loader=self._loader, inventory=inv)

            for host in sorted(inv.hosts.values(), key=lambda h: h.name):
                # Do NOT copy this mapping: copying would render every variable eagerly.
                hv = vm.get_vars(host=host, include_hostvars=include_hostvars)
                if target not in hv:
                    continue

                try:
                    value = hv[target]
                    if not LAZY_TEMPLATING:
                        from ansible.template import Templar
                        value = Templar(loader=self._loader, variables=hv).template(value)
                    rendered = _materialize(value)
                except Exception as e:
                    raise AnsibleLookupError(
                        f"Failed rendering {target} for host '{host.name}' "
                        f"in inventory '{inv_name}': {e}")

                if not isinstance(rendered, list):
                    raise AnsibleLookupError(
                        f"{target} for host '{host.name}' in inventory '{inv_name}' "
                        f"is {type(rendered).__name__}, expected a list")

                for item in rendered:
                    if dedupe:
                        key = json.dumps(item, sort_keys=True, default=str)
                        if key in seen_items:
                            continue
                        seen_items.add(key)
                    results.append(item)
        return results