# 👩‍💻 Contributor Guide: Adding or Updating an Ansible Inventory

## 📖 Purpose

This guide explains how to add a new Ansible inventory or update an existing one in the repository. It ensures that documentation is automatically generated, a global host index is maintained, and duplicate hosts are flagged.

The documentation system enforces consistent structure, extracts host/group metadata from the inventory files, and updates indexes automatically. All changes are processed by the **Generate Ansible Inventory Docs** GitHub Action workflow.

---

## 🛠 Steps to Add or Update an Inventory

### 1. **Create or edit the inventory file**

Inventory files are located under the `inventory/` directory.

Examples:

```
inventory/ad/inventory.ini
inventory/grafana/inventory.ini
inventory/new_service/inventory.ini
```

* Organize inventories by service, environment, or host type.
* Each inventory should be a valid **INI-style Ansible inventory**.

---

### 2. **Define groups and hosts properly**

A typical inventory may contain:

```ini
[webservers]
web-0 ansible_host=10.0.0.10
web-1 ansible_host=10.0.0.11

[dbservers]
db-0 ansible_host=10.0.0.20

[web:children]
webservers

[all:vars]
ntp_server=ntp.local
```

Guidelines:

* Hosts can have **inline variables** (`key=value`), e.g., `web-0 ansible_host=10.0.0.10`.
* Child groups are supported via `:children` sections.
* Group variables are supported via `:vars` sections.
* Avoid defining the same host in multiple inventories unless intentional (see Duplicate Hosts section below).

---

### 3. **Commit your changes**

Push your branch or open a pull request. The GitHub Action will automatically:

* Parse the inventory(s)
* Generate per-inventory Markdown documentation under `docs/inventory/`
* Build a global host index showing hosts, groups, and the inventories they belong to
* Update the global inventory index at both:

  * `docs/inventory/README.md`
  * `inventory/README.md`

---

## ⚙️ What Happens Next

The **Generate Ansible Inventory Docs** GitHub Action runs automatically on push/PR.

It executes:

```
scripts/generate_inventory_docs.py
```

The script:

✅ Parses all `.ini` files under `inventory/` (or a single file if using `--inventory`)
✅ Extracts hosts, groups, group variables, host variables, and child groups
✅ Generates per-inventory Markdown docs:

```
docs/inventory/<inventory>.md
```

✅ Builds a **Global Host Index**:

```
docs/inventory/README.md
inventory/README.md
```

✅ Detects duplicate hosts across inventories and logs a warning
✅ Supports **strict mode** (`--strict`) to enforce unique host definitions

> ⚠️ **Duplicate Hosts Note**
> Hosts that appear in multiple inventories may have conflicting variables or group memberships. Contributors should review these carefully and consider refactoring to maintain a single authoritative definition per host.

---

### 4. **Highlight inventories with multiple hosts**

To help contributors spot inventories with multiple hosts:

* Inventories with **more than one host** are flagged with a 📌 pin next to their name in the global index.
* Example:

```markdown
| Inventory | Description |
|-----------|-------------|
| [`ad`](ad.md) 📌 | Inventory for `ad` hosts |
| [`plex`](plex.md) | Inventory for `plex` hosts |
| [`minecraft`](minecraft.md) 📌 | Inventory for `minecraft` hosts |
```

* This draws attention to larger inventories without adding extra columns.
* It helps identify inventories where duplicate hosts or complex group structures may exist.

---

### 5. **Single-inventory debug mode**

To debug a specific inventory file:

```bash
python scripts/generate_inventory_docs.py --inventory inventory/ad/inventory.ini --debug
```

* Only the specified inventory is parsed and documented.
* Global host index is updated with its hosts.
* Helpful logging is printed to diagnose parsing issues.

---

### 6. **Commit and push changes from the workflow**

The GitHub Action automatically:

1. Adds generated docs:

```
inventory/README.md
docs/inventory/README.md
docs/inventory/*.md
```

2. Commits with:

```
chore(docs): auto-generate inventory documentation
```

3. Pushes to the current branch if there are changes.

No manual editing of the documentation files is required.

---

## ✅ Contributor Expectations

* Use **valid INI syntax** for hosts, groups, and variables
* Avoid duplicate hosts unless necessary; review warnings
* Child groups and group variables must be correctly defined
* Review the PR diff — you’ll see:

  * `docs/inventory/<inventory>.md` per inventory
  * Updated global index in `docs/inventory/README.md` and `inventory/README.md`
* Inventories with multiple hosts will be visually flagged with 📌

---

## 🚀 Example

Adding a new inventory for a hypothetical service `ombi`:

```ini
[ombi]
ombi-0 vms_proxmox_node=pve-0 pihole_cname_entries='[{"domain": "ombi.refol.us","target":"rproxy-0.refol.us"}]'

[services:children]
ombi

[all:vars]
ntp_server=ntp.local
```

After committing:

* `docs/inventory/ombi.md` is generated
* Global host index updated in `docs/inventory/README.md` and `inventory/README.md`
* Duplicate hosts (if any) are logged as warnings
* If `ombi` contained multiple hosts, a 📌 pin appears next to it in the global index

---

## ✅ Summary

Adding or updating inventories is simple:

1. Create or edit an `.ini` inventory under `inventory/`
2. Define hosts, groups, children, and variables correctly
3. Commit and push

The automation handles:

* Markdown documentation for each inventory
* Global host index
* Duplicate host detection and strict mode enforcement
* Multi-host inventories flagged with 📌
* Updates to the root inventory README
