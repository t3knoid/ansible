# 🧭 Inventory Index

| Inventory | Description |
|-----------|-------------|
| [`ad`](ad.md) | Inventory for `ad` hosts |
| [`ansible`](ansible.md) | Inventory for `ansible` hosts |
| [`dns`](dns.md) | Inventory for `dns` hosts |
| [`grafana`](grafana.md) | Inventory for `grafana` hosts |
| [`graphite`](graphite.md) | Inventory for `graphite` hosts |
| [`jenkins`](jenkins.md) | Inventory for `jenkins` hosts |
| [`minecraft`](minecraft.md) | Inventory for `minecraft` hosts |
| [`ombi`](ombi.md) | Inventory for `ombi` hosts |
| [`pg`](pg.md) | Inventory for `pg` hosts |
| [`plex`](plex.md) | Inventory for `plex` hosts |
| [`prometheus`](prometheus.md) | Inventory for `prometheus` hosts |
| [`pve`](pve.md) | Inventory for `pve` hosts |
| [`pxe`](pxe.md) | Inventory for `pxe` hosts |
| [`redmine`](redmine.md) | Inventory for `redmine` hosts |
| [`rproxy`](rproxy.md) | Inventory for `rproxy` hosts |
| [`semaphore`](semaphore.md) | Inventory for `semaphore` hosts |
| [`services`](services.md) | Inventory for `services` hosts |
| [`synology`](synology.md) | Inventory for `synology` hosts |
| [`tautulli`](tautulli.md) | Inventory for `tautulli` hosts |
| [`template`](template.md) | Inventory for `template` hosts |
| [`terraform`](terraform.md) | Inventory for `terraform` hosts |
| [`test`](test.md) | Inventory for `test` hosts |
| [`truenas`](truenas.md) | Inventory for `truenas` hosts |
| [`util`](util.md) | Inventory for `util` hosts |

## 🖥 Global Host Index
| Host | Inventories | Groups |
|------|-------------|--------|
| `ad0` | [`ad`](ad.md) | vms, cname, dc_master |
| `ansible-0` | [`ansible`](ansible.md), [`dns`](dns.md) | ruby, vscode, ansible, code_server, linux, vault_clients, python, nginx, azure_cli |
| `ansible-1` | [`ansible`](ansible.md) | ansible, python, linux, nginx, pgclient |
| `books-0` | [`services`](services.md) | autofs, calibre, lazylibrarian, vms, cname, calibreweb, linux |
| `dns-0` | [`dns`](dns.md) | secondary_dns, dns, vms, python, linux |
| `dns-1` | [`dns`](dns.md) | baremetal, primary_dns, dns, cname, python, linux, pxe_client, vault_servers |
| `grafana-0` | [`grafana`](grafana.md) | autofs, removable, vms, cname, linux, python, grafana |
| `graphite-0` | [`graphite`](graphite.md) | nginx_setup_proxy, vms, python, pgdb, graphite |
| `jenkins-0` | [`jenkins`](jenkins.md) | jenkins, removable, vms, cname, python |
| `lidarr-0` | [`services`](services.md) | autofs, lidarr, vms, cname, linux |
| `minecraft-1` | [`minecraft`](minecraft.md) | vms, bedrock, cname, python, linux |
| `ombi-0` | [`ombi`](ombi.md) | autofs, vms, cname, linux, python, pgclient |
| `pg-0` | [`ombi`](ombi.md), [`pg`](pg.md) | vms, pgdb, autofs, python |
| `pg-1` | [`services`](services.md), [`pg`](pg.md) | vms, python, autofs, pgdb |
| `pg-2` | [`pg`](pg.md), [`redmine`](redmine.md) | vms, pgdb, autofs, python |
| `pg-3` | [`pg`](pg.md), [`semaphore`](semaphore.md) | vms, pgdb, autofs, python |
| `pg-4` | [`pg`](pg.md), [`grafana`](grafana.md) | vms, pgdb, autofs, python |
| `plex-0` | [`plex`](plex.md) | autofs, lamp, baremetal, wikipedia, plex, cname, linux, python, pxe_client |
| `prometheus-0` | [`prometheus`](prometheus.md) | prometheus, autofs, vms, cname, linux, python |
| `pve-0` | [`pve`](pve.md) | ceph_nodes, cname, pvenodes |
| `pve-1` | [`pve`](pve.md) | ceph_nodes, pvenodes |
| `pve-2` | [`pve`](pve.md) | template, cname, ceph_nodes, pvenodes |
| `pxe-0` | [`pxe`](pxe.md), [`plex`](plex.md), [`dns`](dns.md) | vms, pxe |
| `radarr-0` | [`services`](services.md) | radarr, autofs, vms, cname, linux |
| `redmine-0` | [`redmine`](redmine.md) | autofs, ruby, removable, cname, linux, redmine |
| `rproxy-0` | [`ad`](ad.md), [`pve`](pve.md), [`truenas`](truenas.md), [`ombi`](ombi.md), [`prometheus`](prometheus.md), [`services`](services.md), [`plex`](plex.md), [`ansible`](ansible.md), [`jenkins`](jenkins.md), [`tautulli`](tautulli.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`semaphore`](semaphore.md), [`grafana`](grafana.md), [`redmine`](redmine.md) | certs, rproxy_main, vms, redis, cname, linux, python, oauth2_proxy, certbot |
| `rproxy-1` | [`ad`](ad.md), [`pve`](pve.md), [`truenas`](truenas.md), [`ombi`](ombi.md), [`prometheus`](prometheus.md), [`services`](services.md), [`plex`](plex.md), [`ansible`](ansible.md), [`jenkins`](jenkins.md), [`tautulli`](tautulli.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`semaphore`](semaphore.md), [`grafana`](grafana.md), [`redmine`](redmine.md) | vms, python, rproxy_primary, linux |
| `rproxy-2` | [`ad`](ad.md), [`pve`](pve.md), [`truenas`](truenas.md), [`ombi`](ombi.md), [`prometheus`](prometheus.md), [`services`](services.md), [`plex`](plex.md), [`ansible`](ansible.md), [`jenkins`](jenkins.md), [`tautulli`](tautulli.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`semaphore`](semaphore.md), [`grafana`](grafana.md), [`redmine`](redmine.md) | vms, python, rproxy_secondary, linux |
| `sabnzbd-0` | [`services`](services.md) | autofs, sabnzbd, vms, cname, linux |
| `semaphore-0` | [`semaphore`](semaphore.md) | autofs, ansible, vms, cname, linux, python, nginx, semaphore, pgclient |
| `sonarr-0` | [`services`](services.md) | autofs, vms, cname, linux, sonarr |
| `synology-0` | [`synology`](synology.md) | cname, synology |
| `tautulli-0` | [`tautulli`](tautulli.md) | vms, python, cname, linux |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | vms |
| `truenas-01` | [`truenas`](truenas.md) | truenas, nginx, cname |
| `ubu24-template` | [`template`](template.md) | template, ubuntu24, removable |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
