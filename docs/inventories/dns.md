# 🗂 Inventory: `dns`

_Inventory for `dns` hosts_

📄 **Source:** [`inventory/dns/inventory.ini`](../../inventory/dns/inventory.ini)

## 👥 Groups & Hosts
### `baremetal`
- `dns-1`

### `vms`
- `dns-0`

### `dns`
- `dns-0`
- `dns-1`

### `primary_dns`
- `dns-1`

### `secondary_dns`
- `dns-0`

### `linux`
- `dns-0`
- `dns-1`

### `python`
- `dns-0`
- `dns-1`

### `pxe_client`
- `dns-1`

### `pxe`
- `pxe-0`

### `cname`
- `dns-1`

### `vault_servers`
- `dns-1`

### `vault_clients`
- `ansible-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `dns-1`
- `pihole_cname_entries`: `[{"domain": "vault.refol.us", "target": "dns-1.refol.us"}]`

### `dns-0`
- `vms_proxmox_node`: `pve-0`

## 🧩 Group Children
_No child groups defined._
