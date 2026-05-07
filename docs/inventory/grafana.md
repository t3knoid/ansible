# 🗂 Inventory: `grafana`

_Inventory for `grafana` hosts_

📄 **Source:** [`inventory/grafana/inventory.ini`](../../inventory/grafana/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `grafana-0`

### `linux`
- `grafana-0`

### `grafana`
- `grafana-0`

### `pgdb`
- `pg-4`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `cname`
- `grafana-0`

### `removable`
- `grafana-0`

### `autofs`
- `grafana-0`

### `python`
- `grafana-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `grafana-0`
- `vms_proxmox_node`: `pve-2`
- `vms_clone`: `false`
- `pihole_cname_entries`: `[{"domain": "grafana.refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `rproxy`
- `rproxy_secondary`
- `rproxy_main`
- `rproxy_primary`
