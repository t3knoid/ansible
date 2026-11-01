# 🗂 Inventory: `ansible`

_Inventory for `ansible` hosts_

📄 **Source:** [`inventory/ansible/inventory.ini`](../../inventory/ansible/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `ansible-0`
- `ansible-1`

### `code_server`
- `ansible-1`

### `vscode`
- `ansible-1`

### `nginx`
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
- `ansible-1`

### `oauth2_proxy`
- `rproxy-0`

### `entra_id`
- `ansible-1`

### `redis`
- `rproxy-0`

### `ruby`
- `ansible-0`
- `ansible-1`

### `docker`
- `ansible-0`
- `ansible-1`

### `gh_cli`
- `ansible-0`
- `ansible-1`

### `node_exporter`
- `ansible-0`
- `ansible-1`

### `prometheus`
- `prometheus-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `ansible-0`
- `ansible_connection`: `local`
- `vms_proxmox_node`: `pve-0`

### `ansible-1`
- `pihole_cname_entries`: `[{"domain": "code.refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `linux`
- `vms`

### `terraform`
- `ansible`

### `ansible`
- `vms`

### `rproxy`
- `rproxy_secondary`
- `rproxy_main`
- `rproxy_primary`

### `cname`
- `code_server`

### `python`
- `ansible`
