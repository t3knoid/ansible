# Ansible Inventory Documentation Workflow

This script automates documentation for all Ansible inventories in the repository. It parses INI-style inventories, identifies hosts, host variables, group variables, and child groups. It generates per-inventory Markdown documentation under `docs/inventories/` and a **global inventory index**.
The global index is copied both to `docs/inventories/README.md` **and** `inventory/README.md` for easy reference.
It is executed by the **Generate Ansible Inventory Docs** GitHub Action workflow.

---

## 🐍 Python Script: `generate_inventory_docs.py`

The script performs the following steps:

---

## 1. **Inventory Parsing**

* Function: `parse_ini_inventory(path)`
* Reads the inventory file line by line.
* Distinguishes between:

  * **Host sections** (regular hosts)
  * **Group variables** (`[group:vars]`)
  * **Child groups** (`[group:children]`)
* Handles hosts with inline variables and quoted JSON-like values using `shlex.split`.
* Returns four dictionaries:

  * `groups` → hosts per group
  * `host_vars` → variables assigned directly to hosts
  * `group_vars` → variables assigned to groups
  * `group_children` → child group memberships

**Nuance:** Host variables on the same line as the host are merged into `host_vars`, avoiding multiple host entries for the same host.

---

## 2. **Per-Inventory Documentation Generation**

* Function: `generate_inventory_doc(inv_path)`
* Builds a Markdown document containing:

  * Title (`# 🗂 Inventory: <name>`)
  * Description inferred from folder or inventory name
  * Source link to the INI file
  * **Groups & Hosts** table
  * **Host Variables**
  * **Group Variables**
  * **Child Groups**
* Updates global `HOST_INDEX` to track which inventories and groups each host belongs to.
* Detects duplicate host entries across inventories and optionally halts in **strict mode**.

**Nuance:** Groups listed under `[group:children]` are **never added to the host index**.

---

## 3. **Global Host Index & Inventory Meta**

* Global dictionaries:

  * `HOST_INDEX` → maps hosts to inventories and groups
  * `INVENTORY_META` → stores metadata for each inventory (description, path, doc link)
* Function: `write_inventory_index()`

  * Generates the global inventory index at `docs/inventories/README.md`.
  * **Also copies the index to `inventory/README.md`** for easier navigation.
  * Contains:

    * Table of all inventories with links to per-inventory docs
    * Global host index:

      * Host
      * Inventories it belongs to (linked)
      * Groups

---

## 4. **Duplicate Host Detection**

* Function: `report_duplicate_hosts()`
* Detects hosts present in more than one inventory
* Logs a warning for each duplicate host
* Halts execution if `--strict` mode is enabled

> **📌 Note – Duplicate Hosts**
>
> Each host should ideally have a **single canonical definition** across inventories. Duplicate hosts can lead to:
>
> * Conflicting host or group variables
> * Unpredictable playbook behavior
> * Confusion about which inventory is authoritative
> * Maintenance complexity and automation errors
>
> **Contributor Guidance:**
>
> * Consider refactoring inventories if a host appears in multiple places.
> * Ensure variables and roles are defined consistently.
> * Use `--strict` mode to enforce uniqueness.
> * This note is displayed in the documentation to help contributors identify potential issues before merging changes.

---

## 5. **Single Inventory Debug Mode**

If the script is run with a specific inventory file:

```bash
python generate_inventory_docs.py --inventory inventory/ad/inventory.ini
```

* Only that inventory’s documentation is generated under `docs/inventories/`.
* Duplicate host detection is still performed.
* Global index is updated with just the parsed inventory.

---

## 6. **CLI Options**

| Option               | Description                                          |
| -------------------- | ---------------------------------------------------- |
| `--debug`            | Enables debug logging                                |
| `--strict`           | Halts on duplicate hosts                             |
| `--inventory <file>` | Processes only a single inventory file for debugging |

---

# 📂 Example Outputs

## Per-Inventory Documentation (`docs/inventories/ad.md`)

```markdown
# 🗂 Inventory: `ad`

_Inventory for `ad` hosts_

📄 **Source:** [`inventory/ad/inventory.ini`](../../inventory/ad/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `ad0`

### `dc_master`
- `ad0`

### `cname`
- `ad0`

### `certs`
- `rproxy-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `windows`
- _No direct hosts, children only_

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `ad0`
- `vms_proxmox_node`: `pve-0`
- `pihole_cname_entries`: `[{"domain": "refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `windows`
- `vms`

### `rproxy`
- `rproxy_main`
- `rproxy_primary`
- `rproxy_secondary`
```

---

## Global Inventory Index (`docs/inventories/README.md` & `inventory/README.md`)

```markdown
# 🧭 Inventory Index

| Inventory | Description |
|-----------|-------------|
| [`ad`](ad.md) | Inventory for `ad` hosts |
| [`dns`](dns.md) | Inventory for `dns` hosts |
| [`jenkins`](jenkins.md) | Inventory for `jenkins` hosts |

## 🖥 Global Host Index

| Host | Inventories | Groups |
|------|-------------|--------|
| `ad0` | [`ad`](ad.md) | vms, dc_master, cname |
| `rproxy-0` | [`ad`](ad.md) | certs, rproxy_main |
| `rproxy-1` | [`ad`](ad.md) | rproxy_primary |
| `rproxy-2` | [`ad`](ad.md) | rproxy_secondary |

## ⚠️ Duplicate Hosts

> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.  
> Use `--strict` mode to enforce uniqueness.
```

---

# ✅ Contributor Expectations

* All hosts should be listed in their respective inventory `[group]` sections.
* Inline host variables must remain on the **same line** as the host to avoid duplicate entries.
* `[group:children]` entries are **not treated as hosts**.
* Include `[group:vars]` sections if necessary.
* Use `--strict` mode to enforce uniqueness across inventories.
* Use `--debug` mode when generating documentation for a single inventory for easier troubleshooting.
* Updates to inventories should be reflected automatically via the **GitHub Action workflow**.
* Pay attention to the **Duplicate Hosts Note** to prevent misconfigurations.
* The global index README is **mirrored both under `docs/inventories/` and `inventory/`** for easy access.
