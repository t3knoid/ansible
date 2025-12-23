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
- `rproxy_secondary`
- `rproxy_main`
- `rproxy_primary`
