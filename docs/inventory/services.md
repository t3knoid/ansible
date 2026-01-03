# 🗂 Inventory: `services`

_Inventory for `services` hosts_

📄 **Source:** [`inventory/services/inventory.ini`](../../inventory/services/inventory.ini)

## 👥 Groups & Hosts
### `vms`
- `books-0`
- `lidarr-0`
- `radarr-0`
- `sabnzbd-0`
- `sonarr-0`

### `linux`
- `books-0`
- `lidarr-0`
- `radarr-0`
- `sabnzbd-0`
- `sonarr-0`

### `sonarr`
- `sonarr-0`

### `lidarr`
- `lidarr-0`

### `radarr`
- `radarr-0`

### `sabnzbd`
- `sabnzbd-0`

### `calibre`
- `books-0`

### `calibreweb`
- `books-0`

### `lazylibrarian`
- `books-0`

### `pgdb`
- `pg-1`

### `rproxy_main`
- `rproxy-0`

### `rproxy_primary`
- `rproxy-1`

### `rproxy_secondary`
- `rproxy-2`

### `certs`
- `rproxy-0`

### `cname`
- `books-0`
- `lidarr-0`
- `radarr-0`
- `sabnzbd-0`
- `sonarr-0`

### `autofs`
- `books-0`
- `lidarr-0`
- `radarr-0`
- `sabnzbd-0`
- `sonarr-0`

## ⚙️ Group Variables
_No group variables defined._

## 🖥 Host Variables
### `sonarr-0`
- `vms_proxmox_node`: `pve-0`
- `pihole_cname_entries`: `[{"domain": "sonarr.refol.us", "target": "rproxy-0.refol.us"}]`

### `lidarr-0`
- `vms_proxmox_node`: `pve-0`
- `pihole_cname_entries`: `[{"domain": "lidarr.refol.us", "target": "rproxy-0.refol.us"}]`

### `radarr-0`
- `vms_proxmox_node`: `pve-1`
- `pihole_cname_entries`: `[{"domain": "radarr.refol.us", "target": "rproxy-0.refol.us"}]`

### `sabnzbd-0`
- `vms_proxmox_node`: `pve-2`
- `pihole_cname_entries`: `[{"domain": "sabnzbd.refol.us", "target": "rproxy-0.refol.us"}]`

### `books-0`
- `vms_proxmox_node`: `pve-1`
- `pihole_cname_entries`: `[{"domain": "books.refol.us", "target": "rproxy-0.refol.us"}, {"domain": "lazy.refol.us", "target": "rproxy-0.refol.us"}, {"domain": "catalog.refol.us", "target": "rproxy-0.refol.us"}]`

## 🧩 Group Children
### `multimedia`
- `radarr`
- `sonarr`
- `sabnzbd`
- `lidarr`

### `books`
- `calibreweb`
- `calibre`
- `lazylibrarian`

### `docker`
- `sonarr`
- `calibreweb`
- `calibre`
- `lazylibrarian`
- `radarr`
- `sabnzbd`
- `; lidarr, radarr, sonarr use postgresql for their backend database`

### `rproxy`
- `rproxy_primary`
- `rproxy_main`
- `rproxy_secondary`

### `python`
- `sonarr`
- `calibreweb`
- `calibre`
- `lazylibrarian`
- `radarr`
- `sabnzbd`
- `lidarr`
