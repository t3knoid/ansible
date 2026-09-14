# 🗂 Inventory: `truenas`

_Inventory for `truenas` hosts_

📄 **Source:** [`inventory/truenas/inventory.ini`](../../inventory/truenas/inventory.ini)

## 👥 Groups & Hosts
### `truenas`
- `truenas-01`

### `nginx`
- `truenas-01`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `cname`
- `truenas-01`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `truenas-01`
- `pihole_cname_entries`: `[{"domain": "truenas.refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `rproxy`
- `rproxy_main`
- `rproxy_secondary`
- `rproxy_primary`
