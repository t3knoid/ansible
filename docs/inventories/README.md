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
| `ansible-0` | [`ansible`](ansible.md), [`dns`](dns.md) | ruby, ansible, vscode, code_server, azure_cli, vault_clients, python, nginx, linux |
| `ansible-1` | [`ansible`](ansible.md) | ansible, python, nginx, linux, pgclient |
| `books-0` | [`services`](services.md) | calibre, lazylibrarian, cname, calibreweb, autofs, vms, linux |
| `dns-0` | [`dns`](dns.md) | vms, python, dns, linux, secondary_dns |
| `dns-1` | [`dns`](dns.md) | primary_dns, cname, baremetal, pxe_client, python, dns, linux, vault_servers |
| `grafana-0` | [`grafana`](grafana.md) | cname, grafana, autofs, removable, vms, python, linux |
| `graphite-0` | [`graphite`](graphite.md) | pgdb, graphite, vms, python, nginx_setup_proxy |
| `jenkins-0` | [`jenkins`](jenkins.md) | cname, jenkins, removable, vms, python |
| `lidarr-0` | [`services`](services.md) | cname, lidarr, autofs, vms, linux |
| `minecraft-1` | [`minecraft`](minecraft.md) | cname, bedrock, vms, python, linux |
| `ombi-0` | [`ombi`](ombi.md) | cname, autofs, vms, python, linux, pgclient |
| `pg-0` | [`ombi`](ombi.md), [`pg`](pg.md) | autofs, python, pgdb, vms |
| `pg-1` | [`services`](services.md), [`pg`](pg.md) | autofs, pgdb, python, vms |
| `pg-2` | [`redmine`](redmine.md), [`pg`](pg.md) | autofs, python, pgdb, vms |
| `pg-3` | [`semaphore`](semaphore.md), [`pg`](pg.md) | autofs, python, pgdb, vms |
| `pg-4` | [`grafana`](grafana.md), [`pg`](pg.md) | autofs, python, pgdb, vms |
| `plex-0` | [`plex`](plex.md) | cname, baremetal, autofs, pxe_client, lamp, python, plex, wikipedia, linux |
| `prometheus-0` | [`prometheus`](prometheus.md) | cname, autofs, vms, python, linux, prometheus |
| `pve-0` | [`pve`](pve.md) | pvenodes, ceph_nodes, cname |
| `pve-1` | [`pve`](pve.md) | pvenodes, ceph_nodes |
| `pve-2` | [`pve`](pve.md) | template, pvenodes, ceph_nodes, cname |
| `pxe-0` | [`plex`](plex.md), [`dns`](dns.md), [`pxe`](pxe.md) | vms, pxe |
| `radarr-0` | [`services`](services.md) | cname, autofs, radarr, vms, linux |
| `redmine-0` | [`redmine`](redmine.md) | redmine, ruby, cname, autofs, removable, linux |
| `rproxy-0` | [`redmine`](redmine.md), [`tautulli`](tautulli.md), [`truenas`](truenas.md), [`ansible`](ansible.md), [`ombi`](ombi.md), [`grafana`](grafana.md), [`services`](services.md), [`jenkins`](jenkins.md), [`ad`](ad.md), [`rproxy`](rproxy.md), [`plex`](plex.md), [`synology`](synology.md), [`semaphore`](semaphore.md), [`prometheus`](prometheus.md), [`pve`](pve.md) | cname, redis, vms, rproxy_main, certs, python, oauth2_proxy, linux, certbot |
| `rproxy-1` | [`redmine`](redmine.md), [`tautulli`](tautulli.md), [`truenas`](truenas.md), [`ansible`](ansible.md), [`ombi`](ombi.md), [`grafana`](grafana.md), [`services`](services.md), [`jenkins`](jenkins.md), [`ad`](ad.md), [`rproxy`](rproxy.md), [`plex`](plex.md), [`synology`](synology.md), [`semaphore`](semaphore.md), [`prometheus`](prometheus.md), [`pve`](pve.md) | python, rproxy_primary, linux, vms |
| `rproxy-2` | [`redmine`](redmine.md), [`tautulli`](tautulli.md), [`truenas`](truenas.md), [`ansible`](ansible.md), [`ombi`](ombi.md), [`grafana`](grafana.md), [`services`](services.md), [`jenkins`](jenkins.md), [`ad`](ad.md), [`rproxy`](rproxy.md), [`plex`](plex.md), [`synology`](synology.md), [`semaphore`](semaphore.md), [`prometheus`](prometheus.md), [`pve`](pve.md) | python, linux, vms, rproxy_secondary |
| `sabnzbd-0` | [`services`](services.md) | cname, autofs, vms, linux, sabnzbd |
| `semaphore-0` | [`semaphore`](semaphore.md) | ansible, cname, autofs, vms, python, nginx, linux, semaphore, pgclient |
| `sonarr-0` | [`services`](services.md) | sonarr, cname, autofs, vms, linux |
| `synology-0` | [`synology`](synology.md) | synology, cname |
| `tautulli-0` | [`tautulli`](tautulli.md) | python, cname, linux, vms |
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
