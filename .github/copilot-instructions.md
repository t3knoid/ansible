# Ansible Repository Standards

Use the existing repository patterns when creating or modifying inventories, roles, and playbooks. Do not invent new layouts when a neighboring example already exists.

## General Rules

- Inspect the closest comparable inventory, role, or playbook before editing.
- Keep changes minimal and aligned with current naming, file placement, and variable conventions.
- Prefer existing abstractions such as `roles/docker_service_deploy` for Docker-backed services instead of introducing a one-off deployment pattern.
- Keep comments short and practical.
- When values are expected from vault or runtime input, follow the repo's existing comment pattern instead of hardcoding secrets.

## Inventory Standards

- Create inventories under `inventory/<name>/`.
- Create `inventory/<name>/inventory.ini` and only the `group_vars` files justified by neighboring inventories.
- Reuse current host and group naming patterns such as `<service>-0`, `vms`, `linux`, `python`, `docker`, `autofs`, `cname`, `pgdb`, `pgclient`, `rproxy`, and service-specific groups when relevant.
- For VM-backed inventories, preserve the current `vms_*` conventions used in `group_vars/all/main.yml`, including `vms_config`, `vms_os`, `vms_autoinstall`, `vms_enable_serial_terminal`, `vms_additional_packages`, and `python3_version` when appropriate.
- For Docker-backed inventories, expose variables that match the target role's existing naming and deployment pattern.
- When adding a new host, update `roles/global/vars/main.yml` so `global_ip_addresses` contains an entry for that host.
- If the user does not provide an IP address, inspect the current `global_ip_addresses` map, infer the correct subnet from comparable hosts, and assign the next available non-conflicting address while preserving the existing addressing pattern.
- Verify any new `global_ip_addresses` entry is unique and matches the intended host name.

## Role Standards

- Create the smallest justified role surface based on a nearby role.
- Common files include `tasks/main.yml`, `defaults/main.yml` or `defaults/main/main.yml`, `meta/main.yml`, `templates/*`, `handlers/main.yml`, and `vars/main.yml`, but only add what fits the neighboring pattern.
- Name variables with a `<role_name>_*` prefix.
- Keep `meta/main.yml` aligned with existing role metadata style.
- For Docker-backed roles, prefer delegating container lifecycle to `roles/docker_service_deploy` and render configuration through templates such as `docker-compose.yml.j2` plus any service config templates.

## Playbook Standards

- Place playbooks in the appropriate domain folder under `playbooks/`.
- Follow existing naming conventions such as `deploy_<service>.yml`.
- Include a short purpose comment at the top when neighboring playbooks do.
- Deployment playbooks should usually include roles in this order unless a nearby pattern clearly differs:
  1. `global`
  2. `users`
  3. prerequisite roles such as `autofs`, `docker_setup`, `python3`, database/bootstrap roles, or other infrastructure roles
  4. the target setup role
- Include `global` in the playbook process and normally place it first in the role list.
- Use `become: true` for deployment playbooks unless the local pattern shows otherwise.
- Only set `gather_facts: false` when comparable playbooks do the same.
- If prerequisite playbooks are needed, use `import_playbook` in the same style as neighboring files.

## Documentation Rules

- Do not manually create or update generated documentation files for inventories, roles, or playbooks.
- Do not manually edit `inventory/README.md`, `playbooks/README.md`, `roles/README.md`, `docs/inventory/*.md`, `docs/playbooks/*.md`, or `docs/roles/*.md` when the purpose of the change is scaffolding repo objects.
- Documentation for these surfaces is generated automatically by GitHub workflows in `.github/workflows/`, including:
  - `generate-inventory-docs.yml`
  - `generate-role-docs.yml`
  - `generate-playbook-docs.yml`

## Validation Rules

- After inventory changes, run `ansible-inventory -i inventory/<name>/inventory.ini --graph` when possible.
- After playbook changes, run `ansible-playbook --syntax-check` against the most relevant inventory.
- After role changes, run file diagnostics and a focused `ansible-playbook --syntax-check` using a temporary play that imports the role and supplies any minimal required variables.
- Fix syntax or diagnostics issues introduced by your changes before finishing.