# consolidated_variable -- Consolidate a list variable across several inventories

## Synopsis

Loads every inventory found under <code><strong>inventory\_dir</strong></code> independently\.

Role <code>defaults</code> and <code>vars</code> are injected as lowest\-precedence variables on the <code>all</code> group\.

Each host\'s value is rendered in that host\'s own variable context\, then results are concatenated\.

## Practical Example

The certificate-generation playbook uses this lookup to gather reverse-proxy site definitions from the repository's inventories:

```yaml
vars:
  inventory_dir_root: "{{ lookup('ansible.builtin.config', 'DEFAULT_HOST_LIST')[0] }}"
  roles_dir_root: "{{ lookup('ansible.builtin.config', 'DEFAULT_ROLES_PATH')[0] }}"
  rproxy_setup_sites: >-
    {{ query('consolidated_variable', 'rproxy_setup_sites',
             inventory_dir=inventory_dir_root,
             roles_dir=roles_dir_root,
             include_hostvars=false,
             dedupe=true) }}
```

This is the pattern used in [`playbooks/certs/generate_all_certs.yml`](../../playbooks/certs/generate_all_certs.yml). The repository's `ansible.cfg` sets `inventory=inventory/`, so the lookup processes each inventory directory directly under `inventory/`, such as `inventory/grafana/` and `inventory/ansible/`. In this example, `rproxy_setup_sites` is defined for Grafana in [`inventory/grafana/group_vars/all/main.yml`](../../inventory/grafana/group_vars/all/main.yml), and the resulting site definitions are available to the `certs` role.

`query()` is used because the result is a list. The lookup finds the named variable on each host in each inventory, renders it using that host's variables, and appends its list items. By default, identical rendered items are included only once. Role defaults and vars are supplied as fallback values; inventory and host/group variables take precedence.

## Behavior and Limitations

- `inventory_dir` must contain one or more inventory directories as direct children. Each child is loaded as an independent inventory; symlinked directories pointing to the same location are processed once.
- The lookup requires exactly one term: the variable name. Hosts without that variable are skipped, but every value found must render to a list.
- Items are concatenated, not recursively merged. With the default `dedupe: true`, duplicate items are identified by their JSON representation; set `dedupe: false` to preserve them.
- `include_hostvars: true` makes `hostvars` available during rendering, at additional cost.
- Rendering and inventory errors identify the variable, host, and inventory being processed.

## Parameters

  _terms (True, any, None)
    Name of the variable to consolidate \(exactly one\)\.

  inventory_dir (True, path, None)
    Directory whose subdirectories are individual inventories\.

  roles_dir (optional, path, None)
    Roles directory\; role <code>defaults</code> and <code>vars</code> are loaded as lowest\-precedence vars\.

  include_hostvars (optional, bool, False)
    Make <code>hostvars</code> available while rendering \(slower\)\.

  dedupe (optional, bool, True)
    Drop items that are identical after rendering\.

## Return Values

  _raw (, list, )
    The consolidated\, rendered list items\.

## Authors

- Frank Refol
