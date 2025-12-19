# Ansible Inventory Documentation Workflow

This document describes how inventory documentation is automatically generated for Ansible inventories in this repository.
It explains how the documentation generator works, what conventions contributors must follow, and how the GitHub Action workflow integrates with this system.

The goal is to keep inventory documentation **accurate, discoverable, and self-maintaining**, with a global host index and inventory summaries generated entirely from source inventory files.

---

## 🐍 Python Script: `generate_inventory_docs.py`

The core of this workflow is the Python script:

```
scripts/generate_inventory_docs.py
```

This script parses Ansible inventory files, extracts hosts, groups, and variables, and generates Markdown documentation under `docs/inventory/`.
It also builds a **global inventory index** that is mirrored into both documentation and the inventory root.

---

## 1. Inventory Discovery & Parsing

### Inventory Structure

Inventories are expected to live under the `inventory/` directory and use **INI-style syntax**:

```
inventory/ad/inventory.ini
inventory/dns/inventory.ini
inventory/jenkins/inventory.ini
```

Each inventory is treated as a **logical unit** for documentation purposes.

### Parsing Behavior

The parser:

* Reads inventory files line by line
* Identifies:

  * Host definitions
  * Groups (`[group]`)
  * Group variables (`[group:vars]`)
  * Child groups (`[group:children]`)
* Supports **inline host variables**, for example:

```
ad0 vms_proxmox_node=pve-0 ansible_host=10.0.0.10
```

Special care is taken to ensure:

* Variables on host lines are **not mis-parsed as additional hosts**
* Quoted, list-like, and JSON-like values remain intact

---

## 2. Per-Inventory Documentation Generation

For each inventory, the script generates a dedicated Markdown document containing:

* Groups and their member hosts
* Group variables (if present)
* Host variables (if present)
* Group child relationships (if present)

These documents are written to:

```
docs/inventory/<inventory>.md
```

No documentation is written inside the inventory folders themselves.

---

## 3. Global Inventory Index

A global index is generated that provides a repository-wide view of inventories and hosts.

### Inventory Overview Table

The index includes a table listing:

* Inventory name
* Inventory description
* A 📌 **pin icon** next to inventories containing **multiple hosts**

The pin subtly draws attention to larger or more complex inventories without cluttering the table.

### Global Host Index

A second table lists:

* Each host
* All inventories it appears in
* All groups it belongs to

This makes it easy to answer questions like:

* *“Where is this host defined?”*
* *“Which inventory owns this machine?”*

### Index Locations

The generated index is written to **two locations**:

```
docs/inventory/README.md
inventory/README.md
```

This ensures the index is easily discoverable whether browsing documentation or inventory files directly.

---

## 4. Duplicate Host Detection

While parsing, the script tracks **all host definitions across all inventories**.

If a host is found in more than one inventory:

* A warning is logged
* The host is flagged in the global host index

### Why This Matters

Duplicate host definitions can cause:

* Variable conflicts
* Confusing group membership
* Non-deterministic playbook behavior

### 📌 Note — Duplicate Hosts

> Hosts appearing in multiple inventories may have conflicting variables or group memberships.
> Contributors should review these cases and consider refactoring inventories so each host has a single authoritative definition.
>
> A `--strict` mode is available to enforce this rule and fail the run when duplicates are detected.

This feature is intentionally advisory by default, encouraging cleanup without immediately breaking workflows.

---

## 5. Multi-Host Inventory Highlighting

Inventories containing more than one host are marked with a 📌 icon in the global inventory table.

This provides a quick visual cue for:

* Shared services
* Clustered systems
* Inventories that may require extra care when modifying

The icon is intentionally subtle to keep the table readable.

---

## 6. Single Inventory Mode (Debugging)

For easier debugging and development, the script supports processing **a single inventory file**:

```bash
python scripts/generate_inventory_docs.py \
  --inventory inventory/ad/inventory.ini \
  --debug
```

Behavior in this mode:

* Only the specified inventory is parsed
* Per-inventory documentation is generated
* The global index is still rebuilt
* DEBUG-level logging is enabled for easier troubleshooting

---

## 7. CLI Options

| Option               | Description                          |
| -------------------- | ------------------------------------ |
| `--inventory <file>` | Process a single inventory file      |
| `--debug`            | Enable verbose debug logging         |
| `--strict`           | Fail if duplicate hosts are detected |

---

## 📂 Example Outputs

### Per-Inventory Documentation

```
docs/inventory/ad.md
```

Includes:

* Group → host mappings
* Host variables
* Group variables
* Group children

---

### Global Inventory Index

```
docs/inventory/README.md
inventory/README.md
```

Includes:

* Inventory overview table (with 📌 multi-host indicators)
* Global host index
* Duplicate host advisory note

---

## ⚙️ GitHub Actions Integration

This workflow is executed automatically by the **Generate Inventory Docs** GitHub Action.

On every push or pull request:

1. The repository is checked out
2. Python dependencies are installed
3. `generate_inventory_docs.py` is executed
4. Documentation changes are committed back to the branch

This ensures inventory documentation is always current and requires **no manual maintenance**.

---

## ✅ Contributor Expectations

* Inventories must use valid INI syntax
* Inline host variables are supported and encouraged where appropriate
* Avoid defining the same host in multiple inventories
* Review PR diffs — documentation updates will include:

  * `docs/inventory/<inventory>.md`
  * `docs/inventory/README.md`
  * `inventory/README.md`

---

## 🧭 Summary

This workflow ensures that:

* Inventories remain the **single source of truth**
* Documentation is always up-to-date
* Duplicate hosts are visible and actionable
* Large or complex inventories are easy to spot
* Contributors spend less time maintaining docs and more time improving infrastructure

All with zero manual documentation effort.
