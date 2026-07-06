# 🗂 Inventory: `pg`

_Inventory for `pg` hosts_

📄 **Source:** [`inventory/pg/inventory.ini`](../../inventory/pg/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `pg-0`
- `pg-1`
- `pg-2`
- `pg-3`
- `pg-4`

### `autofs`
- `pg-0`
- `pg-1`
- `pg-2`
- `pg-3`
- `pg-4`

### `python`
- `pg-0`
- `pg-1`
- `pg-2`
- `pg-3`
- `pg-4`

### `node_exporter`
- `pg-0`
- `pg-1`
- `pg-2`
- `pg-3`
- `pg-4`

### `prometheus`
- `prometheus-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `pg-0`
- `vms_proxmox_node`: `pve-1`

### `pg-1`
- `vms_proxmox_node`: `pve-2`

### `pg-2`
- `vms_proxmox_node`: `pve-1`

### `pg-3`
- `vms_proxmox_node`: `pve-1`

### `pg-4`
- `vms_proxmox_node`: `pve-2`

## 🧩 Group Children
### `pgdb`
- `vms`

### `linux`
- `vms`
