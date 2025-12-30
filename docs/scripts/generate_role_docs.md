# 📘 Ansible Role Documentation Workflow

## 🔧 Overview
This workflow automatically generates documentation for every Ansible role by parsing metadata, variables, tasks, handlers, and dependencies defined inside each role folder.  
It ensures that:

- Every role has standardized documentation  
- All roles appear in a central index  
- Documentation is stored in a consistent location under `docs/roles/`  

This script is executed by the **Generate Ansible Role Docs** GitHub Action workflow.

---

## 🐍 Python Script: `generate_role_docs.py`

The script performs the following steps:

---

### 1. **Iterates through all role folders**
All directories under:

```
roles/
```

are scanned. A role is processed only if it contains:

```
roles/<role>/meta/main.yml
```

---

### 2. **Reads metadata**
Metadata is loaded from:

```
roles/<role>/meta/main.yml
```

This includes:

- Description  
- Author  
- License  
- Minimum Ansible version  
- Supported platforms  
- Dependencies  

This information populates the **Overview** and **Requirements** sections of the generated documentation.

---

### 3. **Extracts variables**
Variables are collected from:

- `defaults/main.yml`  
- `defaults/main/main.yml` (if present)  
- `vars/main.yml`  

Comments above variables are preserved and included in the documentation.

Two tables are generated:

- **Defaults** — variables from `defaults/`  
- **Vars** — variables from `vars/`  

---

### 4. **Parses tasks and handlers**
The script reads:

- `tasks/main.yml`  
- `handlers/main.yml`  

Task and handler names are extracted and listed in human‑readable form.

---

### 5. **Generates role documentation**
Instead of writing documentation inside each role folder, the script now writes:

```
docs/roles/<role>.md
```

Each generated document includes:

- Title  
- Overview  
- Requirements  
- Defaults table  
- Vars table  
- Tasks  
- Handlers  
- Dependencies  
- Example usage  

This keeps the `roles/` directory clean and makes documentation easier to browse.

---

### 6. **Creates a central role index**
A global index is generated at:

```
docs/roles/README.md
```

This index contains:

- A table of all roles  
- Links to each role’s documentation under `docs/roles/`  
- Each role’s description  

Additionally, a simplified index is written to:

```
roles/README.md
```

This version links to the docs under `docs/roles/` for convenience when browsing the repository.

---

## 📄 Example Role Documentation

Generated documentation follows a consistent structure.  
For example, the `global` role documentation includes:

- **Overview:** High‑level description from `meta/main.yml`  
- **Requirements:** Minimum Ansible version and supported platforms  
- **Defaults:** Variables with default values and comments  
- **Vars:** Constant variables  
- **Tasks:** Human‑readable list of tasks  
- **Handlers:** Handler names  
- **Dependencies:** Other roles required  
- **Example Usage:** A YAML snippet showing how to include the role  

---

## 📑 Example Metadata File

Example `meta/main.yml`:

```yaml
galaxy_info:
  role_name: global
  author: Francis Refol
  description: Provides tasks to install and configure Ansible on a control node.
  license: MIT
  min_ansible_version: "2.9"
  platforms:
    - name: EL
      versions:
        - "7"
        - "8"
    - name: Ubuntu
      versions:
        - bionic
        - focal
```

This metadata is used to populate the **Overview** and **Requirements** sections of the generated documentation.

---

## 📚 Role Index

The script generates a central index at:

```
docs/roles/README.md
```

Example:

```markdown
# 📚 Role Index

| Role | Description |
|------|-------------|
| [`ansible_setup`](ansible_setup.md) | Provides tasks to install and configure Ansible on a control node. |
| [`another_role`](another_role.md) | Description of another role. |
```

A simplified version is also written to:

```
roles/README.md
```

with links pointing to `../docs/roles/<role>.md`.
