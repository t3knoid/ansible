---
name: "Create Ansible Role"
description: "Use when creating or scaffolding a new Ansible role in this repo; mirrors neighboring role layout, docker_service_deploy usage, defaults/meta structure, and validation standards without manually editing generated docs."
argument-hint: "Role name, service type, and deployment style"
agent: "agent"
---

Create or scaffold a new Ansible role in this repository using the patterns already in use.

Requirements:

- Inspect the nearest comparable role under `roles/` before editing and copy its layout conventions. Do not invent a new role structure when a local pattern already exists.
- Always include `roles/global` in the process reasoning: new roles are expected to be consumed by playbooks that run `global` first.
- Create the smallest justified role surface. Common files include `tasks/main.yml`, `defaults/main.yml` or `defaults/main/main.yml`, `meta/main.yml`, `templates/*`, `handlers/main.yml`, and `vars/main.yml`, but only add files that fit the neighboring pattern.
- For Docker-backed services, prefer delegating container lifecycle to `roles/docker_service_deploy` and render configuration through templates such as `docker-compose.yml.j2` and service config templates.
- Name variables consistently with the existing repo style, using a `<role_name>_*` prefix.
- Keep role metadata aligned with existing `meta/main.yml` files.
- Do not manually update or create role docs under `docs/roles/` or `roles/README.md`. Role documentation is generated automatically by `.github/workflows/generate-role-docs.yml`.

Validation steps:

- Run file diagnostics on all touched role files.
- Run a focused `ansible-playbook --syntax-check` using a temporary play that imports the new role and supplies minimal required variables.
- If you scaffold a Docker-backed role, ensure the rendered template variables line up with inventory variables and `docker_service_deploy` expectations.

Output expectations:

- Make the code changes directly.
- State which neighboring role(s) you mirrored.
- Call out any required inventory or vault variables the new role expects.
