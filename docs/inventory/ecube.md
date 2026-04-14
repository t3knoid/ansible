# 🗂 Inventory: `ecube`

_Inventory for `ecube` hosts_

📄 **Source:** [`inventory/ecube/inventory.ini`](../../inventory/ecube/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `ecube-0`

### `linux`
- `ecube-0`

### `pgdb`
- `ecube-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `cname`
- `ecube-0`

### `removable`
- `ecube-0`

### `vscode`
- `ecube-0`

### `python`
- `ecube-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `ecube-0`
- `vms_proxmox_node`: `pve-2`
- `vms_clone`: `false`
- `pihole_cname_entries`: `[{"domain": "www.ecube.one", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `rproxy`
- `rproxy_main`
- `rproxy_primary`
- `rproxy_secondary`
