---
name: "Create Ansible Inventory"
description: "Use when creating or scaffolding a new Ansible inventory in this repo; mirrors existing inventory, group_vars, VM, docker, and validation conventions without manually editing generated docs."
argument-hint: "Inventory name, host/group intent, and service type"
agent: "agent"
---

Create or scaffold a new Ansible inventory in this repository using the standards already in use.

Requirements:

- Start by inspecting the closest existing inventory under `inventory/` and mirror its structure instead of inventing a new one.
- Create `inventory/<name>/inventory.ini` and only the `group_vars` files that are justified by neighboring inventories.
- Update `roles/global/vars/main.yml` when adding a new host so `global_ip_addresses` contains an entry for that host.
- If the user does not specify an IP address, infer the correct subnet from the closest comparable hosts and assign the next available non-conflicting IP address in `global_ip_addresses`.
- When auto-assigning an IP address, inspect the existing `global_ip_addresses` map first, preserve the repo's current addressing pattern for similar hosts, and avoid reusing an address that is already assigned.
- Keep host naming and grouping consistent with the repo. Reuse patterns such as `<service>-0`, `vms`, `linux`, `python`, `docker`, `autofs`, `cname`, `pgdb`, `pgclient`, `rproxy`, and service-specific groups only when they are actually needed.
- For VM-backed inventories, preserve the current `vms_*` variable conventions used in `group_vars/all/main.yml`, including `vms_config`, `vms_os`, `vms_autoinstall`, `vms_enable_serial_terminal`, `vms_additional_packages`, and `python3_version` where appropriate.
- For Docker-backed inventories, expose variables that match the target role’s existing naming and deployment pattern instead of inventing ad hoc names.
- Keep comments concise and practical. Use comments to point to vault-provided values when the repo already uses that pattern.
- Do not manually update or create inventory docs under `docs/inventory/` or `inventory/README.md`. Inventory documentation is generated automatically by `.github/workflows/generate-inventory-docs.yml`.

Validation steps:

- Run `ansible-inventory -i inventory/<name>/inventory.ini --graph` after editing.
- Run file diagnostics on the touched inventory files and fix any syntax issues.
- Verify that any new `global_ip_addresses` entry in `roles/global/vars/main.yml` is unique and matches the intended host name.

Output expectations:

- Make the code changes directly.
- Summarize the inferred conventions you followed.
- Mention any assumptions about groups, VM placement, required vault values, and IP/subnet selection.
