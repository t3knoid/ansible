# 🗂 Inventory: `semaphore`

_Inventory for `semaphore` hosts_

📄 **Source:** [`inventory/semaphore/inventory.ini`](../../inventory/semaphore/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `semaphore-0`

### `ansible`
- `semaphore-0`

### `linux`
- `semaphore-0`

### `semaphore`
- `semaphore-0`

### `pgdb`
- `pg-3`

### `pgclient`
- `semaphore-0`

### `nginx`
- `semaphore-0`

### `oauth2_proxy`
- `rproxy-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `cname`
- `semaphore-0`

### `autofs`
- `semaphore-0`

### `python`
- `semaphore-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `semaphore-0`
- `vms_proxmox_node`: `pve-1`
- `pihole_cname_entries`: `[{"domain": "semaphore.refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `rproxy`
- `rproxy_main`
- `rproxy_secondary`
- `rproxy_primary`
