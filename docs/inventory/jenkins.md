# 🗂 Inventory: `jenkins`

_Inventory for `jenkins` hosts_

📄 **Source:** [`inventory/jenkins/inventory.ini`](../../inventory/jenkins/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `jenkins-0`

### `jenkins`
- `jenkins-0`

### `cname`
- `jenkins-0`

### `removable`
- `jenkins-0`

### `certs`
- `rproxy-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `python`
- `jenkins-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `jenkins-0`
- `vms_proxmox_node`: `pve-2`
- `pihole_cname_entries`: `[{"domain": "jenkins.refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `rproxy`
- `rproxy_primary`
- `rproxy_main`
- `rproxy_secondary`
