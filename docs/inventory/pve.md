# 🗂 Inventory: `pve`

_Inventory for `pve` hosts_

📄 **Source:** [`inventory/pve/inventory.ini`](../../inventory/pve/inventory.ini)

## 👥 Groups & Hosts
### `pvenodes`
- `pve-0`
- `pve-1`
- `pve-2`

### `template`
- `pve-2`

### `cname`
- `pve-0`
- `pve-2`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `ceph_nodes`
- `pve-0`
- `pve-1`
- `pve-2`

### `prometheus`
- `prometheus-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `pve-0`
- `pve_ceph_network_ip_assignment`: `10.0.2.200`

### `pve-1`
- `pve_ceph_network_ip_assignment`: `10.0.2.201`

### `pve-2`
- `pve_ceph_network_ip_assignment`: `10.0.2.202`

## 🧩 Group Children
### `linux`
- `pvenodes`

### `pbs`
- `pvenodes`
- `pbsnodes`

### `rproxy`
- `rproxy_secondary`
- `rproxy_main`
- `rproxy_primary`

### `node_exporter`
- `pvenodes`

### `pve_exporter`
- `pvenodes`
