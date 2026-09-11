# 🗂 Inventory: `synology`

_Inventory for `synology` hosts_

📄 **Source:** [`inventory/synology/inventory.ini`](../../inventory/synology/inventory.ini)

## 👥 Groups & Hosts
### `synology`
- `synology-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `cname`
- `synology-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `synology-0`
- `pihole_cname_entries`: `[{"domain": "synology.refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `rproxy`
- `rproxy_secondary`
- `rproxy_primary`
- `rproxy_main`
