# 🗂 Inventory: `ansible`

_Inventory for `ansible` hosts_

📄 **Source:** [`inventory/ansible/inventory.ini`](../../inventory/ansible/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `ansible-0`
- `ansible-1`

### `wsl`
- `dev-0`

### `pgclient`
- `ansible-1`

### `code_server`
- `ansible-0`

### `vscode`
- `ansible-0`

### `nginx`
- `ansible-0`
- `ansible-1`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `azure_cli`
- `ansible-0`

### `oauth2_proxy`
- `rproxy-0`

### `redis`
- `rproxy-0`

### `ruby`
- `ansible-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `ansible-0`
- `vms_proxmox_node`: `pve-0`
- `pihole_cname_entries`: `[{"domain": "code.refol.us", "target": "rproxy-0.refol.us"}]`

### `ansible-1`
- `vms_proxmox_node`: `pve-1`

## 🧩 Group Children
### `linux`
- `wsl`
- `vms`

### `terraform`
- `ansible`

### `ansible`
- `wsl`
- `vms`

### `rproxy`
- `rproxy_main`
- `rproxy_primary`
- `rproxy_secondary`

### `cname`
- `code_server`

### `python`
- `wsl`
- `ansible`
