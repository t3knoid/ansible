# 🗂 Inventory: `tautulli`

_Inventory for `tautulli` hosts_

📄 **Source:** [`inventory/tautulli/inventory.ini`](../../inventory/tautulli/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `tautulli-0`

### `linux`
- `tautulli-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `cname`
- `tautulli-0`

### `python`
- `tautulli-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `tautulli-0`
- `vms_proxmox_node`: `pve-2`
- `pihole_cname_entries`: `[{"domain": "tautulli.refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `tautulli`
- `vms`

### `rproxy`
- `rproxy_main`
- `rproxy_primary`
- `rproxy_secondary`
