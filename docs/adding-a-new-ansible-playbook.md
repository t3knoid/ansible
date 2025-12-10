# ⚙️ GitHub Action: Generate Playbook Docs

## 📖 Purpose
This GitHub Action enforces documentation standards for all playbooks in the repository. It ensures every playbook has a clear purpose, generates per‑playbook READMEs, builds folder‑level summaries, and maintains a global index.

---

## 🛠 How It Works
- **Mandatory Purpose Comment**
  - Each playbook must begin with a `# Purpose:` comment (after the `---` YAML marker).
  - Multi‑line comments are supported — all consecutive `#` lines after `# Purpose:` are collected.
  - If missing, the Action fails.

- **Per‑Playbook README**
  - For every `*.yml` playbook, a `README.md` is generated alongside it.
  - Includes:
    - Purpose text
    - Roles applied (linked to their role docs)
    - Example usage (`ansible-playbook playbooks/...`)

- **Folder‑Level README**
  - Each subfolder under `playbooks/` gets its own `README.md`.
  - Summarizes all playbooks in that folder in a table (Playbook → Purpose).

- **Global Index**
  - `playbooks/README.md` lists all playbooks across the repo in a table with relative paths and purposes.

---

## 📂 Example Output

### Per‑Playbook README (`playbooks/deploy-ansible.md`)
```markdown
# 📖 Playbook: deploy-ansible.yml

## 🛠 Purpose
Sets up the Ansible control node and prepares managed nodes with required roles.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`ansible_node`](../roles/ansible_node/README.md)
- [`sshpass`](../roles/sshpass/README.md)
- [`python3`](../roles/python3/README.md)
- [`ansible_setup`](../roles/ansible_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/deploy-ansible.yml
```
```

### Folder README (`playbooks/infra/README.md`)
```markdown
# 📚 Playbooks in `infra`

| Playbook | Purpose |
|----------|---------|
| [`prepare-node.yml`](prepare-node.md) | Prepares VMs and baremetal hosts for Ansible management |
```

### Global Index (`playbooks/README.md`)
```markdown
# 📚 Playbook Index

| Playbook Path            | Purpose |
|--------------------------|---------|
| [`deploy-ansible.yml`](deploy-ansible.md) | Sets up the Ansible control node and prepares managed nodes |
| [`infra/prepare-node.yml`](infra/prepare-node.md) | Prepares VMs and baremetal hosts for Ansible management |
| [`security/firewall.yml`](security/firewall.md) | Configures firewall rules for managed nodes |
```

---

## 🚀 Usage

### Generate docs for all playbooks
```bash
python scripts/generate_playbook_docs.py
```

### Generate docs for a single playbook
```bash
python scripts/generate_playbook_docs.py playbooks/infra/prepare-node.yml
```

---

## ✅ Contributor Guide: Adding a New Playbook

1. **Create the playbook file**  
   Place it under the appropriate folder in `playbooks/`. Example:  
   ```
   playbooks/security/firewall.yml
   ```

2. **Add a Purpose comment**  
   At the very top of the file (after `---`), include:  
   ```yaml
   ---
   # Purpose: Configures firewall rules for managed nodes
   # Ensures baseline security policies are applied consistently.
   ```

3. **Define roles and tasks**  
   Use `roles:` or `import_role` so the script can detect them.

4. **Commit and push**  
   When you open a PR, the GitHub Action will:
   - Generate `firewall.md` alongside your playbook.
   - Update `playbooks/security/README.md` with a summary.
   - Update the global `playbooks/README.md` index.

---

## ✨ Contributor Expectations
- Always include a `# Purpose:` comment.  
- Keep purpose concise but meaningful — it appears in indexes and READMEs.  
- Roles should be declared properly so they’re detected.  
- Check the PR diff — you’ll see updated playbook READMEs, folder summaries, and the global index.  

Excellent — here’s a **starter playbook template** that contributors can copy‑paste when creating new playbooks. It enforces the `# Purpose:` convention, includes the YAML document marker, and provides a skeleton structure for roles and tasks.

---

## 📑 Starter Playbook Template

```yaml
---
# Purpose: Briefly describe what this playbook does.
# Add more detail if needed across multiple lines.
# Example: Sets up baseline configuration for managed nodes,
# ensures SSH access, and prepares Python environment.

- name: Example Playbook
  hosts: target_group   # Replace with inventory group (e.g., vms, baremetal, ansible)
  gather_facts: true
  become: true
  become_user: root

  roles:
    - global            # Example role
    - my_new_role       # Replace with your role(s)

  tasks:
    - name: Import another role if needed
      ansible.builtin.import_role:
        name: another_role

    - name: Example task
      ansible.builtin.debug:
        msg: "Playbook is running successfully!"
```

---

### 🔑 Key Points for Contributors
- **Always start with `---` and a `# Purpose:` comment.**  
  - Multi‑line comments are allowed — each line starts with `#`.  
- **Use meaningful playbook names** (`deploy-ansible.yml`, `prepare-node.yml`).  
- **Declare roles in `roles:`** so they’re detected by the doc generator.  
- **Add tasks only if needed** — simple playbooks may just call roles.  
- **Check the generated README** after running the docs script to confirm purpose and roles are captured correctly.  

---

### 🚀 Example Usage
```bash
ansible-playbook playbooks/example-playbook.yml
```
