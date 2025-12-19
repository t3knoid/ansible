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
| `ad0` | [`ad`](ad.md) | cname, dc_master, vms |
| `ansible-0` | [`ansible`](ansible.md), [`dns`](dns.md) | vscode, ruby, vault_clients, nginx, azure_cli, linux, code_server, python, ansible |
| `ansible-1` | [`ansible`](ansible.md) | nginx, pgclient, linux, python, ansible |
| `books-0` | [`services`](services.md) | cname, calibre, lazylibrarian, linux, calibreweb, autofs, vms |
| `dns-0` | [`dns`](dns.md) | dns, linux, python, secondary_dns, vms |
| `dns-1` | [`dns`](dns.md) | dns, cname, baremetal, vault_servers, linux, python, pxe_client, primary_dns |
| `grafana-0` | [`grafana`](grafana.md) | removable, cname, grafana, linux, python, autofs, vms |
| `graphite-0` | [`graphite`](graphite.md) | python, pgdb, graphite, nginx_setup_proxy, vms |
| `jenkins-0` | [`jenkins`](jenkins.md) | cname, python, vms, jenkins, removable |
| `lidarr-0` | [`services`](services.md) | lidarr, cname, linux, autofs, vms |
| `minecraft-1` | [`minecraft`](minecraft.md) | cname, linux, python, vms, bedrock |
| `ombi-0` | [`ombi`](ombi.md) | cname, pgclient, linux, python, autofs, vms |
| `pg-0` | [`pg`](pg.md), [`ombi`](ombi.md) | python, autofs, vms, pgdb |
| `pg-1` | [`pg`](pg.md), [`services`](services.md) | autofs, pgdb, python, vms |
| `pg-2` | [`pg`](pg.md), [`redmine`](redmine.md) | python, autofs, vms, pgdb |
| `pg-3` | [`pg`](pg.md), [`semaphore`](semaphore.md) | python, autofs, vms, pgdb |
| `pg-4` | [`pg`](pg.md), [`grafana`](grafana.md) | python, autofs, vms, pgdb |
| `plex-0` | [`plex`](plex.md) | plex, baremetal, cname, linux, python, lamp, pxe_client, wikipedia, autofs |
| `prometheus-0` | [`prometheus`](prometheus.md) | cname, linux, python, prometheus, autofs, vms |
| `pve-0` | [`pve`](pve.md) | cname, pvenodes, ceph_nodes |
| `pve-1` | [`pve`](pve.md) | pvenodes, ceph_nodes |
| `pve-2` | [`pve`](pve.md) | cname, pvenodes, template, ceph_nodes |
| `pxe-0` | [`plex`](plex.md), [`pxe`](pxe.md), [`dns`](dns.md) | pxe, vms |
| `radarr-0` | [`services`](services.md) | cname, radarr, linux, autofs, vms |
| `redmine-0` | [`redmine`](redmine.md) | cname, ruby, redmine, linux, autofs, removable |
| `rproxy-0` | [`tautulli`](tautulli.md), [`pve`](pve.md), [`plex`](plex.md), [`ombi`](ombi.md), [`grafana`](grafana.md), [`ad`](ad.md), [`redmine`](redmine.md), [`semaphore`](semaphore.md), [`prometheus`](prometheus.md), [`truenas`](truenas.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`ansible`](ansible.md), [`jenkins`](jenkins.md), [`services`](services.md) | oauth2_proxy, cname, rproxy_main, certbot, linux, python, redis, certs, vms |
| `rproxy-1` | [`tautulli`](tautulli.md), [`pve`](pve.md), [`plex`](plex.md), [`ombi`](ombi.md), [`grafana`](grafana.md), [`ad`](ad.md), [`redmine`](redmine.md), [`semaphore`](semaphore.md), [`prometheus`](prometheus.md), [`truenas`](truenas.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`ansible`](ansible.md), [`jenkins`](jenkins.md), [`services`](services.md) | linux, python, rproxy_primary, vms |
| `rproxy-2` | [`tautulli`](tautulli.md), [`pve`](pve.md), [`plex`](plex.md), [`ombi`](ombi.md), [`grafana`](grafana.md), [`ad`](ad.md), [`redmine`](redmine.md), [`semaphore`](semaphore.md), [`prometheus`](prometheus.md), [`truenas`](truenas.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`ansible`](ansible.md), [`jenkins`](jenkins.md), [`services`](services.md) | linux, python, rproxy_secondary, vms |
| `sabnzbd-0` | [`services`](services.md) | cname, sabnzbd, linux, autofs, vms |
| `semaphore-0` | [`semaphore`](semaphore.md) | cname, nginx, pgclient, linux, python, semaphore, ansible, autofs, vms |
| `sonarr-0` | [`services`](services.md) | sonarr, cname, linux, autofs, vms |
| `synology-0` | [`synology`](synology.md) | cname, synology |
| `tautulli-0` | [`tautulli`](tautulli.md) | cname, linux, python, vms |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | vms |
| `truenas-01` | [`truenas`](truenas.md) | cname, nginx, truenas |
| `ubu24-template` | [`template`](template.md) | template, ubuntu24, removable |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
