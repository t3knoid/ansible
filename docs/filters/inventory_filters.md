# 🧩 Ansible Filter Plugin: `find_inventory_files`

## 📖 Overview
The `find_inventory_files` filter is a custom Ansible filter plugin that recursively scans an inventory directory and returns a list of all matching inventory files (typically `inventory.ini`).  

This filter is especially useful in roles that need to dynamically discover all inventories without hardcoding paths — such as the **semaphoreui** role, which builds a structured list of inventories for Semaphore’s UI configuration.

---

# ✅ What the Filter Does

### In plain terms:
It walks the directory tree starting at `inventory/` and returns a list of all files named `inventory.ini`.

### More specifically:
- Accepts two parameters:
  - `root_path` → directory to scan (default: `"inventory"`)
  - `filename` → file to search for (default: `"inventory.ini"`)
- Uses `os.walk()` to recursively traverse all subdirectories
- Checks whether the target filename exists in each directory
- Appends the full path to a list
- Returns the list of discovered inventory files

If the root directory does not exist, the filter returns an empty list.

---

# 📁 Example Directory Structure

```
inventory/
├── prod/
│   └── inventory.ini
├── dev/
│   └── inventory.ini
└── lab/
    └── inventory.ini
```

Running the filter returns:

```yaml
[
  "inventory/prod/inventory.ini",
  "inventory/dev/inventory.ini",
  "inventory/lab/inventory.ini"
]
```

---

# ✅ Example Usage in Ansible

### Basic usage

```yaml
inventory_files: "{{ '' | find_inventory_files }}"
```

### Using a custom root path

```yaml
inventory_files: "{{ '' | find_inventory_files('my_inventory_root') }}"
```

### Using a custom filename

```yaml
yaml_inventories: "{{ '' | find_inventory_files('inventory', 'hosts.yml') }}"
```

---

# 🧠 Why This Filter Exists

This filter is designed for roles that need to:

- Dynamically discover all inventories  
- Avoid hardcoding environment names  
- Build structured lists of inventories for external systems  
- Support multi‑environment homelab setups  

It pairs naturally with roles that need to **enumerate inventories**, such as the `semaphoreui` role.

---

# 🚀 Real‑World Usage: The `semaphoreui` Role

The `semaphoreui` role uses this filter to automatically build a structured list of inventories that Semaphore can import.

### ✅ Step 1: Discover all inventory.ini files

```yaml
- name: Get inventory files
  ansible.builtin.set_fact:
    inventory_files: "{{ 'inventory/' | find_inventory_files }}"
```

This produces a list like:

```yaml
inventory_files:
  - inventory/prod/inventory.ini
  - inventory/dev/inventory.ini
  - inventory/lab/inventory.ini
```

---

### ✅ Step 2: Build structured inventory objects for Semaphore

```yaml
- name: Build structured inventory list
  ansible.builtin.set_fact:
    semaphoreui_setup_inventories: "{{ semaphoreui_setup_inventories | default([]) + [ {
      'name': item | regex_replace('^.*/([^/]+)/inventory.ini$', '\\1'),
      'type': 'file',
      'credentials': 'Semaphore user credentials',
      'sudo_credentials': '',
      'inventory': item
      } ] }}"
  loop: "{{ inventory_files }}"
  when: item is match('^.*/[^/]+/inventory.ini$')
```

### ✅ What this does

For each inventory file:

- Extracts the folder name using regex  
  - `inventory/prod/inventory.ini` → `prod`  
  - `inventory/dev/inventory.ini` → `dev`  
- Builds a structured dictionary for Semaphore:

```yaml
{
  "name": "prod",
  "type": "file",
  "credentials": "Semaphore user credentials",
  "sudo_credentials": "",
  "inventory": "inventory/prod/inventory.ini"
}
```

### ✅ Final result

```yaml
semaphoreui_setup_inventories:
  - name: prod
    type: file
    credentials: Semaphore user credentials
    sudo_credentials: ""
    inventory: inventory/prod/inventory.ini

  - name: dev
    type: file
    credentials: Semaphore user credentials
    sudo_credentials: ""
    inventory: inventory/dev/inventory.ini

  - name: lab
    type: file
    credentials: Semaphore user credentials
    sudo_credentials: ""
    inventory: inventory/lab/inventory.ini
```

Semaphore can now import these inventories automatically.

---

# 🔍 How the Filter Works (Technical Breakdown)

### 1. Validate the root directory
```python
if not os.path.isdir(root_path):
    return inventory_list
```

### 2. Recursively walk the directory tree
```python
for dirpath, dirnames, filenames in os.walk(root_path):
```

### 3. Check for the target filename
```python
if filename in filenames:
```

### 4. Append the full path
```python
inventory_list.append(os.path.join(dirpath, filename))
```

### 5. Return the list
```python
return inventory_list
```

---

# ✅ Filter Registration

The filter is exposed to Ansible via:

```python
class FilterModule(object):
    def filters(self):
        return {
            'find_inventory_files': find_inventory_files
        }
```

This makes it available in any playbook or role as:

```yaml
{{ '' | find_inventory_files }}
```

---

# ⚠️ Limitations & Notes

- Only searches for **one specific filename** at a time  
- Does not parse or validate inventory contents  
- Returns **relative paths** based on the Ansible working directory  
- Does not support glob patterns (e.g., `inventory*.ini`)  

---

# ✅ Summary

The `find_inventory_files` filter:

- Recursively scans an inventory directory  
- Finds all files matching a given filename  
- Returns a list of full paths  
- Enables dynamic inventory discovery  
- Powers roles like `semaphoreui` that need structured inventory lists  

It’s a simple but powerful building block for multi‑environment automation.
