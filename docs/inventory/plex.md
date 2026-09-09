# 🗂 Inventory: `plex`

_Inventory for `plex` hosts_

📄 **Source:** [`inventory/plex/inventory.ini`](../../inventory/plex/inventory.ini)

## 👥 Groups & Hosts
### `baremetal`
- `plex-0`

### `plex`
- `plex-0`

### `pxe_client`
- `plex-0`

### `pxe`
- `pxe-0`

### `linux`
- `plex-0`

### `autofs`
- `plex-0`

### `python`
- `plex-0`

### `lamp`
- `plex-0`

### `wikipedia`
- `plex-0`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `cname`
- `plex-0`

### `node_exporter`
- `plex-0`

### `prometheus`
- `prometheus-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `plex-0`
- `pihole_cname_entries`: `[{"domain":"wikipedia.refol.us","target":"rproxy-0.refol.us"}]`

## 🧩 Group Children
### `rproxy`
- `rproxy_secondary`
- `rproxy_primary`
- `rproxy_main`
