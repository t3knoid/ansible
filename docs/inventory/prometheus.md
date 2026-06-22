# 🗂 Inventory: `prometheus`

_Inventory for `prometheus` hosts_

📄 **Source:** [`inventory/prometheus/inventory.ini`](../../inventory/prometheus/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `prometheus-0`

### `linux`
- `prometheus-0`

### `alertmanager`
- `prometheus-0`

### `prometheus`
- `prometheus-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `cname`
- `prometheus-0`

### `autofs`
- `prometheus-0`

### `python`
- `prometheus-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `prometheus-0`
- `vms_proxmox_node`: `pve-1`
- `vms_clone`: `false`
- `pihole_cname_entries`: `[{"domain":"prometheus.refol.us", "target":"rproxy-0.refol.us"}]`

## 🧩 Group Children
### `rproxy`
- `rproxy_main`
- `rproxy_secondary`
- `rproxy_primary`
