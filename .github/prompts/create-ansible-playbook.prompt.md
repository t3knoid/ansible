---
name: "Create Ansible Playbook"
description: "Use when creating or scaffolding a new Ansible playbook in this repo; mirrors existing deploy playbook structure, role ordering, validation, and generated-docs workflow expectations."
argument-hint: "Playbook path, target group, and role chain"
agent: "agent"
---

Create or scaffold a new Ansible playbook in this repository using the conventions already present under `playbooks/`.

Requirements:

- Inspect the nearest comparable playbook before editing and match its shape, file placement, and comments.
- Place the playbook in the appropriate domain folder under `playbooks/` and follow existing naming conventions such as `deploy_<service>.yml`.
- Include a short purpose comment at the top when neighboring playbooks do.
- Playbooks that deploy hosts or services must include roles in the established order unless a nearby pattern clearly differs:
  1. `global`
  2. `users`
  3. prerequisite roles such as `autofs`, `docker_setup`, `python3`, database/bootstrap roles, or other infrastructure roles
  4. the target setup role
- Ensure `roles/global` is included in the playbook process and normally appears first in the role list.
- Use `become: true` for deployment playbooks unless the local pattern proves otherwise.
- Only set `gather_facts: false` when nearby comparable playbooks do the same.
- If the service requires prerequisite playbooks, use `import_playbook` in the same style as neighboring files.
- Do not manually update or create playbook docs under `docs/playbooks/` or `playbooks/README.md`. Playbook documentation is generated automatically by `.github/workflows/generate-playbook-docs.yml`.

Validation steps:

- Run file diagnostics on the new playbook.
- Run `ansible-playbook --syntax-check` against the most relevant inventory.
- If the playbook references a newly created inventory or role, validate those surfaces first before concluding.

Output expectations:

- Make the code changes directly.
- State which neighboring playbook pattern you followed.
- Mention any prerequisites, imported playbooks, or inventory assumptions.
