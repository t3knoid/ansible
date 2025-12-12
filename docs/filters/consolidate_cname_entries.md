# 🧩 Ansible Filter Plugin: `consolidate_cname_entries`

## 📖 Overview
The `consolidate_cname_entries` filter is a custom Ansible filter plugin used to **aggregate Pi‑hole CNAME entries** from multiple `inventory.ini` files across your inventory structure.

Each environment (prod, dev, lab, etc.) can define its own `pihole_cname_entries`, and this filter merges them into a **single unified list** that the Pi‑hole role uses to generate TOML‑compliant `cnameRecords`.

This enables decentralized DNS override definitions while still producing a centralized configuration for Pi‑hole.

---

# ✅ What the Filter Does

### In plain terms:
It scans the `inventory/` directory, finds every `inventory.ini`, extracts:

```
pihole_cname_entries = '<json list>'
```

…and merges all JSON lists into one Python list.

### More specifically:
- Walks `inventory/<folder>/`
- Looks for `inventory.ini`
- Uses regex to find `pihole_cname_entries='[...]'`
- Parses the JSON safely
- Extends a global list
- Returns the merged result

If JSON is malformed, the filter prints a warning but continues.

---

# 📁 Example Inventory Structure

```
inventory/
├── prod/
│   └── inventory.ini
├── dev/
│   └── inventory.ini
└── lab/
    └── inventory.ini
```

Each inventory may define its own CNAME entries.

---

# ✅ Example Declaration (Real‑World)

Here is a real example of how a host declares `pihole_cname_entries` inside an `inventory.ini`:

```
dns-1 pihole_cname_entries='[{"domain": "vault.refol.us", "target": "dns-1.refol.us"}]'
```

### 🔍 What this means

- The host `dns-1` defines a Pi‑hole CNAME entry
- The JSON list contains one mapping:
  - `vault.refol.us` → `dns-1.refol.us`
- The filter extracts this JSON, parses it, and merges it with entries from other inventories

### ✅ Parsed result

```json
[
  {
    "domain": "vault.refol.us",
    "target": "dns-1.refol.us"
  }
]
```

---

# 🛠 Usage in Ansible

### ✅ Basic usage

```yaml
pihole_consolidated_cname_entries: "{{ '' | consolidate_cname_entries }}"
```

### ✅ Using the result in a template

```jinja2
{% for entry in pihole_consolidated_cname_entries %}
CNAME {{ entry.domain }} {{ entry.target }}
{% endfor %}
```

---

# 🧩 How the Filter Is Used in the Pi‑hole Role

The Pi‑hole role uses the consolidated list to generate the TOML `cnameRecords` array.

Pi‑hole expects entries in the format:

```
"<cname>,<target>[,<TTL>]"
```

### ✅ Template snippet from the Pi‑hole role

```jinja2
# List of CNAME records which indicate that <cname> is really <target>. 
# If the <TTL> is given, it overwrites the value of local-ttl
#
# Allowed values are:
#     Array of CNAMEs, each one in the following form: "<cname>,<target>[,<TTL>]"
cnameRecords = [
  {% for entry in pihole_consolidated_cname_entries %}
 "{{ entry['domain'] }},{{ entry['target'] }}"{% if not loop.last %},{% endif %}{% endfor %}
] ### CHANGED, default = []
```

### ✅ Example rendered TOML

Given:

```
dns-1 pihole_cname_entries='[{"domain": "vault.refol.us", "target": "dns-1.refol.us"}]'
```

The rendered TOML becomes:

```toml
cnameRecords = [
  "vault.refol.us,dns-1.refol.us"
]
```

If multiple inventories define entries, the filter merges them:

```toml
cnameRecords = [
  "vault.refol.us,dns-1.refol.us",
  "dev-vault.refol.us,dev-dns.refol.us",
  "grafana.refol.us,grafana.internal"
]
```

---

# 🧪 Example Consolidated Output

If inventories contain:

### `inventory/prod/inventory.ini`
```
dns-1 pihole_cname_entries='[{"domain": "vault.refol.us", "target": "dns-1.refol.us"}]'
```

### `inventory/dev/inventory.ini`
```
dev-dns pihole_cname_entries='[{"domain": "dev-vault.refol.us", "target": "dev-dns.refol.us"}]'
```

### ✅ Final merged list returned by the filter:

```json
[
  {"domain": "vault.refol.us", "target": "dns-1.refol.us"},
  {"domain": "dev-vault.refol.us", "target": "dev-dns.refol.us"}
]
```

---

# 🔍 How the Filter Works (Technical Breakdown)

### 1. Default base directory
```python
def consolidate_cname_entries(base_dir="inventory"):
```

### 2. Walk through each subfolder
```python
for inventory_name in os.listdir(base_dir):
```

### 3. Look for `inventory.ini`
```python
inventory_file = os.path.join(inventory_path, "inventory.ini")
```

### 4. Regex match for the variable
```python
pattern = re.compile(r'pihole_cname_entries\s*=\s*\'(.*?)\'')
```

### 5. Parse JSON
```python
entries = json.loads(raw_json)
```

### 6. Extend the global list
```python
consolidated_cname_entries.extend(entries)
```

---

# ⚠️ Limitations & Gotchas

- JSON must be **single‑quoted** in `inventory.ini`
- Only scans `inventory/<folder>/inventory.ini`
- Does not scan YAML inventories or deeper nested folders
- Malformed JSON prints a warning but does not stop execution

---

# 🚀 When to Use This Filter

Use this filter when:

- You want a **centralized Pi‑hole configuration** built from multiple inventories  
- You maintain **multiple environments** with different DNS overrides  
- You want to avoid manually merging lists  
- You want inventory‑specific CNAME entries to remain local to each environment  

---

# ✅ Summary

The `consolidate_cname_entries` filter:

- Scans all inventory folders  
- Extracts Pi‑hole CNAME entries from each `inventory.ini`  
- Parses JSON safely  
- Merges everything into one list  
- Feeds that list into the Pi‑hole role  
- Produces TOML‑compliant `"cname,target"` strings  

This enables decentralized DNS override definitions while still generating a unified Pi‑hole configuration.
