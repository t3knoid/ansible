# 🗂 Inventory: `ecube`

_Inventory for `ecube` hosts_

📄 **Source:** [`inventory/ecube/inventory.ini`](../../inventory/ecube/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `ecube-0`
- `ecube-1`

### `baremetal`
- `ecube-2`

### `linux`
- `ecube-0`
- `ecube-1`
- `ecube-2`

### `ecube`
- `ecube-0`
- `ecube-1`
- `ecube-2`

### `pgdb`
- `ecube-0`
- `ecube-1`
- `ecube-2`

### `ecube_demo`
- `ecube-2`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `removable`
- `ecube-0`
- `ecube-1`

### `python`
- `ecube-0`
- `ecube-1`
- `ecube-2`

### `certs`
- `rproxy-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `ecube-0`
- `vms_proxmox_node`: `pve-2`
- `vms_clone`: `false`

### `ecube-1`
- `vms_proxmox_node`: `pve-1`
- `vms_clone`: `false`

### `ecube-2`
- `pihole_cname_entries`: `[{"domain": "demo.ecube.com", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `rproxy`
- `rproxy_main`
- `rproxy_secondary`
- `rproxy_primary`
