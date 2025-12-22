# 🗂 Inventory: `ombi`

_Inventory for `ombi` hosts_

📄 **Source:** [`inventory/ombi/inventory.ini`](../../inventory/ombi/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `ombi-0`

### `pgdb`
- `pg-0`

### `pgclient`
- `ombi-0`

### `linux`
- `ombi-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `cname`
- `ombi-0`

### `autofs`
- `ombi-0`

### `python`
- `ombi-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `ombi-0`
- `vms_proxmox_node`: `pve-1`
- `pihole_cname_entries`: `[{"domain": "ombi.refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `ombi`
- `vms`

### `rproxy`
- `rproxy_primary`
- `rproxy_main`
- `rproxy_secondary`
