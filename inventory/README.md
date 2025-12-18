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
| `ansible-0` | [`ansible`](ansible.md), [`dns`](dns.md) | nginx, linux, python, ruby, code_server, azure_cli, ansible, vscode, vault_clients |
| `ansible-1` | [`ansible`](ansible.md) | nginx, linux, python, pgclient, ansible |
| `books-0` | [`services`](services.md) | vms, linux, calibreweb, cname, lazylibrarian, calibre, autofs |
| `dns-0` | [`dns`](dns.md) | vms, secondary_dns, linux, python, dns |
| `dns-1` | [`dns`](dns.md) | linux, python, vault_servers, cname, baremetal, primary_dns, pxe_client, dns |
| `grafana-0` | [`grafana`](grafana.md) | vms, linux, python, grafana, cname, autofs, removable |
| `graphite-0` | [`graphite`](graphite.md) | graphite, vms, pgdb, python, nginx_setup_proxy |
| `jenkins-0` | [`jenkins`](jenkins.md) | jenkins, vms, python, cname, removable |
| `lidarr-0` | [`services`](services.md) | vms, linux, cname, autofs, lidarr |
| `minecraft-1` | [`minecraft`](minecraft.md) | vms, linux, python, cname, bedrock |
| `ombi-0` | [`ombi`](ombi.md) | vms, linux, python, cname, pgclient, autofs |
| `pg-0` | [`ombi`](ombi.md), [`pg`](pg.md) | vms, pgdb, python, autofs |
| `pg-1` | [`services`](services.md), [`pg`](pg.md) | vms, pgdb, python, autofs |
| `pg-2` | [`redmine`](redmine.md), [`pg`](pg.md) | vms, pgdb, python, autofs |
| `pg-3` | [`semaphore`](semaphore.md), [`pg`](pg.md) | vms, pgdb, python, autofs |
| `pg-4` | [`grafana`](grafana.md), [`pg`](pg.md) | vms, pgdb, python, autofs |
| `plex-0` | [`plex`](plex.md) | linux, plex, python, cname, baremetal, pxe_client, autofs, lamp, wikipedia |
| `prometheus-0` | [`prometheus`](prometheus.md) | vms, linux, python, cname, prometheus, autofs |
| `pve-0` | [`pve`](pve.md) | cname, pvenodes, ceph_nodes |
| `pve-1` | [`pve`](pve.md) | pvenodes, ceph_nodes |
| `pve-2` | [`pve`](pve.md) | template, cname, pvenodes, ceph_nodes |
| `pxe-0` | [`pxe`](pxe.md), [`plex`](plex.md), [`dns`](dns.md) | vms, pxe |
| `radarr-0` | [`services`](services.md) | vms, linux, cname, autofs, radarr |
| `redmine-0` | [`redmine`](redmine.md) | linux, ruby, cname, redmine, autofs, removable |
| `rproxy-0` | [`jenkins`](jenkins.md), [`tautulli`](tautulli.md), [`plex`](plex.md), [`grafana`](grafana.md), [`redmine`](redmine.md), [`semaphore`](semaphore.md), [`ad`](ad.md), [`prometheus`](prometheus.md), [`ombi`](ombi.md), [`services`](services.md), [`ansible`](ansible.md), [`pve`](pve.md), [`truenas`](truenas.md), [`rproxy`](rproxy.md), [`synology`](synology.md) | vms, linux, certs, python, cname, redis, oauth2_proxy, certbot, rproxy_main |
| `rproxy-1` | [`jenkins`](jenkins.md), [`tautulli`](tautulli.md), [`plex`](plex.md), [`grafana`](grafana.md), [`redmine`](redmine.md), [`semaphore`](semaphore.md), [`ad`](ad.md), [`prometheus`](prometheus.md), [`ombi`](ombi.md), [`services`](services.md), [`ansible`](ansible.md), [`pve`](pve.md), [`truenas`](truenas.md), [`rproxy`](rproxy.md), [`synology`](synology.md) | vms, rproxy_primary, python, linux |
| `rproxy-2` | [`jenkins`](jenkins.md), [`tautulli`](tautulli.md), [`plex`](plex.md), [`grafana`](grafana.md), [`redmine`](redmine.md), [`semaphore`](semaphore.md), [`ad`](ad.md), [`prometheus`](prometheus.md), [`ombi`](ombi.md), [`services`](services.md), [`ansible`](ansible.md), [`pve`](pve.md), [`truenas`](truenas.md), [`rproxy`](rproxy.md), [`synology`](synology.md) | vms, rproxy_secondary, python, linux |
| `sabnzbd-0` | [`services`](services.md) | vms, linux, cname, autofs, sabnzbd |
| `semaphore-0` | [`semaphore`](semaphore.md) | nginx, vms, linux, python, semaphore, pgclient, cname, ansible, autofs |
| `sonarr-0` | [`services`](services.md) | vms, linux, cname, sonarr, autofs |
| `synology-0` | [`synology`](synology.md) | cname, synology |
| `tautulli-0` | [`tautulli`](tautulli.md) | cname, vms, python, linux |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | vms |
| `truenas-01` | [`truenas`](truenas.md) | nginx, cname, truenas |
| `ubu24-template` | [`template`](template.md) | template, ubuntu24, removable |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
