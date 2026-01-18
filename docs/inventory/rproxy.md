# 🗂 Inventory: `rproxy`

_Inventory for `rproxy` hosts_

📄 **Source:** [`inventory/rproxy/inventory.ini`](../../inventory/rproxy/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `rproxy-0`
- `rproxy-1`
- `rproxy-2`

### `certbot`
- `rproxy-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `linux`
- `rproxy-0`
- `rproxy-1`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `python`
- `rproxy-0`
- `rproxy-1`
- `rproxy-2`

### `cname`
- `rproxy-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `rproxy-0`
- `vms_proxmox_node`: `pve-0`
- `pihole_cname_entries`: `[{"domain": "auth.refol.us", "target": "rproxy-0.refol.us"}]`

### `rproxy-1`
- `vms_proxmox_node`: `pve-1`

### `rproxy-2`
- `vms_proxmox_node`: `pve-2`

## 🧩 Group Children
### `nginx`
- `vms`

### `rproxy`
- `rproxy_secondary`
- `rproxy_main`
- `rproxy_primary`
