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
| `ad0` | [`ad`](ad.md) | dc_master, cname, vms |
| `ansible-0` | [`dns`](dns.md), [`ansible`](ansible.md) | ansible, vscode, python, azure_cli, linux, code_server, nginx, vault_clients |
| `ansible-1` | [`ansible`](ansible.md) | ansible, python, linux, nginx, pgclient |
| `books-0` | [`services`](services.md) | cname, vms, autofs, lazylibrarian, calibreweb, calibre, linux |
| `dns-0` | [`dns`](dns.md) | secondary_dns, vms, python, dns, linux |
| `dns-1` | [`dns`](dns.md) | cname, vault_servers, python, baremetal, dns, pxe_client, linux, primary_dns |
| `grafana-0` | [`grafana`](grafana.md) | cname, vms, autofs, python, grafana, linux, removable |
| `graphite-0` | [`graphite`](graphite.md) | graphite, vms, python, nginx_setup_proxy, pgdb |
| `jenkins-0` | [`jenkins`](jenkins.md) | jenkins, cname, vms, python, removable |
| `lidarr-0` | [`services`](services.md) | lidarr, cname, vms, autofs, linux |
| `minecraft-1` | [`minecraft`](minecraft.md) | cname, vms, python, bedrock, linux |
| `ombi-0` | [`ombi`](ombi.md) | cname, vms, autofs, python, linux, pgclient |
| `pg-0` | [`pg`](pg.md), [`ombi`](ombi.md) | autofs, pgdb, python, vms |
| `pg-1` | [`pg`](pg.md), [`services`](services.md) | autofs, python, vms, pgdb |
| `pg-2` | [`pg`](pg.md), [`redmine`](redmine.md) | autofs, pgdb, python, vms |
| `pg-3` | [`pg`](pg.md), [`semaphore`](semaphore.md) | autofs, pgdb, python, vms |
| `pg-4` | [`grafana`](grafana.md), [`pg`](pg.md) | autofs, pgdb, python, vms |
| `plex-0` | [`plex`](plex.md) | lamp, cname, autofs, baremetal, python, wikipedia, plex, pxe_client, linux |
| `prometheus-0` | [`prometheus`](prometheus.md) | cname, vms, autofs, python, prometheus, linux |
| `pve-0` | [`pve`](pve.md) | pvenodes, cname, ceph_nodes |
| `pve-1` | [`pve`](pve.md) | pvenodes, ceph_nodes |
| `pve-2` | [`pve`](pve.md) | pvenodes, cname, template, ceph_nodes |
| `pxe-0` | [`pxe`](pxe.md), [`dns`](dns.md), [`plex`](plex.md) | pxe, vms |
| `radarr-0` | [`services`](services.md) | cname, vms, autofs, linux, radarr |
| `redmine-0` | [`redmine`](redmine.md) | ruby, cname, redmine, autofs, linux, removable |
| `rproxy-0` | [`ad`](ad.md), [`jenkins`](jenkins.md), [`pve`](pve.md), [`ombi`](ombi.md), [`ansible`](ansible.md), [`redmine`](redmine.md), [`semaphore`](semaphore.md), [`rproxy`](rproxy.md), [`truenas`](truenas.md), [`plex`](plex.md), [`grafana`](grafana.md), [`prometheus`](prometheus.md), [`tautulli`](tautulli.md), [`synology`](synology.md), [`services`](services.md) | certbot, cname, vms, rproxy_main, python, redis, oauth2_proxy, certs, linux |
| `rproxy-1` | [`ad`](ad.md), [`jenkins`](jenkins.md), [`pve`](pve.md), [`ombi`](ombi.md), [`ansible`](ansible.md), [`redmine`](redmine.md), [`semaphore`](semaphore.md), [`rproxy`](rproxy.md), [`truenas`](truenas.md), [`plex`](plex.md), [`grafana`](grafana.md), [`prometheus`](prometheus.md), [`tautulli`](tautulli.md), [`synology`](synology.md), [`services`](services.md) | python, linux, rproxy_primary, vms |
| `rproxy-2` | [`ad`](ad.md), [`jenkins`](jenkins.md), [`pve`](pve.md), [`ombi`](ombi.md), [`ansible`](ansible.md), [`redmine`](redmine.md), [`semaphore`](semaphore.md), [`rproxy`](rproxy.md), [`truenas`](truenas.md), [`plex`](plex.md), [`grafana`](grafana.md), [`prometheus`](prometheus.md), [`tautulli`](tautulli.md), [`synology`](synology.md), [`services`](services.md) | python, rproxy_secondary, linux, vms |
| `sabnzbd-0` | [`services`](services.md) | cname, vms, autofs, sabnzbd, linux |
| `semaphore-0` | [`semaphore`](semaphore.md) | ansible, semaphore, cname, vms, autofs, python, linux, nginx, pgclient |
| `sonarr-0` | [`services`](services.md) | cname, vms, autofs, linux, sonarr |
| `synology-0` | [`synology`](synology.md) | synology, cname |
| `tautulli-0` | [`tautulli`](tautulli.md) | python, cname, linux, vms |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | vms |
| `truenas-01` | [`truenas`](truenas.md) | nginx, truenas, cname |
| `ubu24-template` | [`template`](template.md) | removable, ubuntu24, template |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
