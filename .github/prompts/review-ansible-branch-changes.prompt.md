---
name: "Review Ansible Branch Changes"
description: "Use when reviewing the latest staged changes or the latest committed changes on the current branch in this repo; checks for bugs, regressions, missing validation, and deviations from .github/copilot-instructions.md and relevant .cursor/rules/*.mdc files."
argument-hint: "Optional scope or files to emphasize"
agent: "agent"
---

Review the latest staged changes in this repository. If there are no staged changes, review the latest committed changes on the current branch against `main`.

Review baseline:

- Use `.github/copilot-instructions.md` as the primary repository standard.
- Use `.cursor/rules/ansible-general.mdc` for repository-wide standards.
- Use the relevant Cursor rules for the touched surface:
  - `.cursor/rules/ansible-role-standards.mdc` for changes under `roles/`
  - `.cursor/rules/ansible-playbook-standards.mdc` for changes under `playbooks/`
  - `.cursor/rules/ansible-inventory-standards.mdc` for changes under `inventory/` and `roles/global/vars/main.yml`
- If the touched files match other local instruction or prompt files, treat them as additional context, not as overrides of the repository standards above.

Diff selection rules:

- First check for staged changes and review those if present.
- If nothing is staged, review the committed diff between the current branch and `main`.
- Keep the review scoped to the latest current-branch work unless the user explicitly asks for a broader audit.

Review priorities:

- Bugs, broken behavior, invalid assumptions, and rollout failures.
- Violations of the repo's inventory, role, and playbook conventions.
- Missing prerequisites, dependency ordering problems, and handler/service lifecycle issues.
- Missing validation steps required by the repo instructions.
- Security or exposure issues such as unintended public listeners, secrets handling mistakes, or unsafe defaults.
- Regressions caused by changing generated-docs surfaces or repo-managed structure.

Expected review process:

- Inspect the relevant diff first rather than rereading the whole repo.
- Read only the nearby owning files needed to validate behavior and conventions.
- Prefer concrete, falsifiable findings tied to the changed code.
- Confirm whether the change aligns with the nearest comparable role, playbook, or inventory pattern.
- Note when a check was not run or when a validation gap remains.

Required output format:

- Start with findings only, ordered by severity.
- For each finding, include the impacted file path, the specific risk, and why it violates behavior or repo rules.
- After findings, include `Open Questions / Assumptions` only if needed.
- End with a short `Change Summary` only after the findings.
- If no findings are present, say so explicitly and then mention residual risks or testing gaps.

File reference rules for the review:

- Use clickable file references with line numbers when possible.
- Do not paste large diffs unless a small excerpt is necessary to explain a defect.

Validation guidance:

- Prefer the narrowest relevant executable checks already expected by the repo, such as `ansible-playbook --syntax-check` or `ansible-inventory --graph` for touched surfaces.
- If validation was skipped or impossible, say so explicitly in the review.
