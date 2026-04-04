# 🗂 Inventory: `redmine`

_Inventory for `redmine` hosts_

📄 **Source:** [`inventory/redmine/inventory.ini`](../../inventory/redmine/inventory.ini)

## 👥 Groups & Hosts
### `redmine`
- `redmine-0`

### `removable`
- `redmine-0`

### `pgdb`
- `pg-2`

### `linux`
- `redmine-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `cname`
- `redmine-0`

### `ruby`
- `redmine-0`

### `autofs`
- `redmine-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `redmine-0`
- `vms_proxmox_node`: `pve-1`
- `pihole_cname_entries`: `[{"domain": "lab.refol.us", "target": "rproxy-0.refol.us"}, {"domain": "api.redmine.refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `vms`
- `redmine`

### `rproxy`
- `rproxy_secondary`
- `rproxy_primary`
- `rproxy_main`
