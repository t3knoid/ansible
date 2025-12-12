# Ansible Playbook Documentation Workflow

This script automates documentation for all Ansible playbooks in the repository. It enforces the presence of a `# Purpose:` comment, generates per‑playbook documentation under `docs/playbooks/`, builds folder‑level summaries inside the `playbooks/` tree, and maintains a global index of all playbooks.  
It is executed by the **Generate Ansible Playbook Docs** GitHub Action workflow.

---

## 🐍 Python Script: `generate_playbook_docs.py`

The script performs the following steps:

---

## 1. **Purpose Extraction**

- Function: `get_playbook_purpose(playbook_path)`
- Reads the playbook file line by line.
- Skips YAML document markers (`---`) and blank lines.
- Collects all consecutive comment lines beginning with `# Purpose:`.
- Supports multi‑line purpose blocks.
- Returns a single combined purpose string.
- Raises an error if the purpose block is missing.

---

## 2. **Role Detection**

- Function: `get_roles(playbook_path)`
- Parses the playbook YAML using `PyYAML`.
- Detects roles defined via:
  - `roles:` (string or dict form)
  - `tasks:` entries using `ansible.builtin.import_role`
- Returns a list of role names.

---

## 3. **Per‑Playbook Documentation Generation**

- Function: `generate_playbook_markdown(playbook_path, playbooks_dir)`
- Builds a Markdown document containing:
  - Title (`# 📖 Playbook: <relative path>`)
  - Purpose section
  - Roles applied (linked to `docs/roles/<role>.md`)
  - Usage example (`ansible-playbook playbooks/<path>`)
- **Writes the generated documentation to:**

```
docs/playbooks/<playbook>.md
```

- No documentation files are written inside the `playbooks/` directory.

---

## 4. **Global Playbook Index**

- In `main()`, all playbooks are discovered recursively using `rglob("*.yml")`.
- Entries are grouped into:
  - **Root entries** — playbooks directly under `playbooks/`
  - **Subfolder entries** — playbooks inside nested directories
- A global index is generated at:

```
docs/playbooks/README.md
```

- The index contains two tables:
  - Playbooks in the root directory
  - Playbooks in subfolders (with relative paths)

---

## 5. **Folder‑Level Indexes**

- For each subfolder under `playbooks/`, a `README.md` is generated inside that folder.
- These folder‑level indexes contain:
  - A table of playbooks in that folder
  - Links pointing to `docs/playbooks/<playbook>.md`
- The root `playbooks/` folder is skipped to avoid overwriting the global index.

---

## 6. **Single Playbook Mode**

If the script is run with a specific playbook path:

```bash
python scripts/generate_playbook_docs.py playbooks/infra/prepare-node.yml
```

- Only that playbook’s documentation is generated under `docs/playbooks/`.
- No global index or folder‑level indexes are updated.

---

# 📂 Example Outputs

## Per‑Playbook Documentation (`docs/playbooks/deploy-ansible.md`)

```markdown
# 📖 Playbook: deploy-ansible.yml

## 🛠 Purpose
Sets up the Ansible control node and prepares managed nodes with required roles.

## 🔗 Roles Applied
- [`global`](../roles/global.md)
- [`ansible_node`](../roles/ansible_node.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/deploy-ansible.yml
```
```

---

## Folder Index (`playbooks/ansible/README.md`)

```markdown
# 📚 Playbooks in `ansible`

| Playbook | Purpose |
|----------|---------|
| [`deploy_ansible.yml`](../../docs/playbooks/deploy_ansible.md) | Prepares VMs and baremetal hosts for Ansible management |
```

---

## Global Index (`docs/playbooks/README.md`)

```markdown
# 📚 Playbook Index

## 📂 Playbooks in root `playbooks/`

| Playbook | Purpose |
|----------|---------|
| [`deploy-ansible.yml`](deploy-ansible.md) | Sets up the Ansible control node and prepares managed nodes |

## 📂 Playbooks in subfolders

| Playbook Path | Purpose |
|----------------|---------|
| [`infra/prepare-node.yml`](prepare-node.md) | Prepares VMs and baremetal hosts for Ansible management |
| [`security/firewall.yml`](firewall.md) | Configures firewall rules for managed nodes |
```

---

# ✅ Contributor Expectations

- Always include a `# Purpose:` comment at the top of each playbook.
- Keep the purpose concise but meaningful — it appears in indexes and documentation.
- Declare roles properly (`roles:` or `import_role`) so they are detected.
- Review the PR diff — updates will include:
  - Per‑playbook docs under `docs/playbooks/`
  - Folder‑level indexes under `playbooks/`
  - The global index under `docs/playbooks/README.md`
