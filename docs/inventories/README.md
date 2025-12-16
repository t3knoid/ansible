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
| `ad0` | [`ad`](ad.md) | cname, vms, dc_master |
| `ansible-0` | [`ansible`](ansible.md), [`dns`](dns.md) | ansible, nginx, vault_clients, azure_cli, code_server, linux, vscode, python |
| `ansible-1` | [`ansible`](ansible.md) | ansible, nginx, pgclient, linux, python |
| `books-0` | [`services`](services.md) | calibre, lazylibrarian, autofs, linux, cname, vms, calibreweb |
| `dns-0` | [`dns`](dns.md) | linux, vms, secondary_dns, python, dns |
| `dns-1` | [`dns`](dns.md) | baremetal, primary_dns, pxe_client, linux, cname, vault_servers, python, dns |
| `grafana-0` | [`grafana`](grafana.md) | grafana, autofs, removable, linux, cname, vms, python |
| `graphite-0` | [`graphite`](graphite.md) | graphite, nginx_setup_proxy, vms, pgdb, python |
| `jenkins-0` | [`jenkins`](jenkins.md) | jenkins, removable, cname, vms, python |
| `lidarr-0` | [`services`](services.md) | autofs, linux, cname, vms, lidarr |
| `minecraft-1` | [`minecraft`](minecraft.md) | bedrock, linux, cname, vms, python |
| `ombi-0` | [`ombi`](ombi.md) | autofs, pgclient, linux, cname, vms, python |
| `pg-0` | [`ombi`](ombi.md), [`pg`](pg.md) | vms, pgdb, python, autofs |
| `pg-1` | [`services`](services.md), [`pg`](pg.md) | vms, pgdb, python, autofs |
| `pg-2` | [`redmine`](redmine.md), [`pg`](pg.md) | vms, pgdb, python, autofs |
| `pg-3` | [`semaphore`](semaphore.md), [`pg`](pg.md) | vms, pgdb, python, autofs |
| `pg-4` | [`grafana`](grafana.md), [`pg`](pg.md) | vms, pgdb, python, autofs |
| `plex-0` | [`plex`](plex.md) | plex, baremetal, autofs, pxe_client, linux, cname, lamp, wikipedia, python |
| `prometheus-0` | [`prometheus`](prometheus.md) | autofs, linux, prometheus, cname, vms, python |
| `pve-0` | [`pve`](pve.md) | cname, pvenodes, ceph_nodes |
| `pve-1` | [`pve`](pve.md) | pvenodes, ceph_nodes |
| `pve-2` | [`pve`](pve.md) | cname, template, pvenodes, ceph_nodes |
| `pxe-0` | [`plex`](plex.md), [`dns`](dns.md), [`pxe`](pxe.md) | vms, pxe |
| `radarr-0` | [`services`](services.md) | autofs, radarr, linux, cname, vms |
| `redmine-0` | [`redmine`](redmine.md) | autofs, ruby, removable, redmine, cname, linux |
| `rproxy-0` | [`ansible`](ansible.md), [`plex`](plex.md), [`ad`](ad.md), [`ombi`](ombi.md), [`grafana`](grafana.md), [`services`](services.md), [`jenkins`](jenkins.md), [`tautulli`](tautulli.md), [`redmine`](redmine.md), [`rproxy`](rproxy.md), [`pve`](pve.md), [`prometheus`](prometheus.md), [`semaphore`](semaphore.md), [`truenas`](truenas.md), [`synology`](synology.md) | oauth2_proxy, certs, linux, cname, vms, certbot, redis, python, rproxy_main |
| `rproxy-1` | [`ansible`](ansible.md), [`plex`](plex.md), [`ad`](ad.md), [`ombi`](ombi.md), [`grafana`](grafana.md), [`services`](services.md), [`jenkins`](jenkins.md), [`tautulli`](tautulli.md), [`redmine`](redmine.md), [`rproxy`](rproxy.md), [`pve`](pve.md), [`prometheus`](prometheus.md), [`semaphore`](semaphore.md), [`truenas`](truenas.md), [`synology`](synology.md) | rproxy_primary, python, vms, linux |
| `rproxy-2` | [`ansible`](ansible.md), [`plex`](plex.md), [`ad`](ad.md), [`ombi`](ombi.md), [`grafana`](grafana.md), [`services`](services.md), [`jenkins`](jenkins.md), [`tautulli`](tautulli.md), [`redmine`](redmine.md), [`rproxy`](rproxy.md), [`pve`](pve.md), [`prometheus`](prometheus.md), [`semaphore`](semaphore.md), [`truenas`](truenas.md), [`synology`](synology.md) | vms, python, linux, rproxy_secondary |
| `sabnzbd-0` | [`services`](services.md) | autofs, linux, cname, vms, sabnzbd |
| `semaphore-0` | [`semaphore`](semaphore.md) | ansible, nginx, autofs, pgclient, linux, cname, vms, semaphore, python |
| `sonarr-0` | [`services`](services.md) | autofs, sonarr, linux, cname, vms |
| `synology-0` | [`synology`](synology.md) | cname, synology |
| `tautulli-0` | [`tautulli`](tautulli.md) | cname, vms, python, linux |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | vms |
| `truenas-01` | [`truenas`](truenas.md) | cname, truenas, nginx |
| `ubu24-template` | [`template`](template.md) | ubuntu24, template, removable |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
