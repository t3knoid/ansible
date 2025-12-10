# ⚙️ GitHub Action: Generate Playbook Docs

## 📖 Purpose
This GitHub Action ensures that every playbook in the repository is **self‑documented**. It enforces a mandatory `# Purpose:` comment at the top of each playbook, generates a `README.md` for each playbook, builds folder‑level summaries, and maintains a global index of all playbooks.

---

## 🛠 How It Works
- **Purpose enforcement**  
  - Each playbook must begin with a `# Purpose:` comment (after the `---` YAML marker).  
  - Multi‑line comments are supported — all consecutive `#` lines after `# Purpose:` are collected.  
  - If missing, the Action fails.

- **Per‑playbook README**  
  - For every `*.yml` playbook, a `README.md` is generated alongside it.  
  - Includes:
    - Purpose text
    - Roles applied (linked to their role docs)
    - Example usage (`ansible-playbook playbooks/...`)

- **Folder‑level README**  
  - Each subfolder under `playbooks/` gets its own `README.md`.  
  - Summarizes all playbooks in that folder in a table (Playbook → Purpose).

- **Global index**  
  - `playbooks/README.md` lists all playbooks across the repo in a table with relative paths and purposes.

---

## 📂 Example Output

### Per‑playbook README (`playbooks/deploy-ansible.md`)
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

## ✅ Contributor Expectations
- Always include a `# Purpose:` comment at the top of each playbook.  
- Keep purpose concise but meaningful — it appears in indexes and READMEs.  
- Roles should be declared properly (`roles:` or `import_role`) so they’re detected.  
- Check the PR diff — you’ll see updated playbook READMEs, folder summaries, and the global index.  
