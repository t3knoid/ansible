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
| `ansible-0` | [`ansible`](ansible.md), [`dns`](dns.md) | vscode, vault_clients, nginx, code_server, python, ansible, azure_cli, linux |
| `ansible-1` | [`ansible`](ansible.md) | nginx, python, ansible, pgclient, linux |
| `books-0` | [`services`](services.md) | calibre, calibreweb, cname, vms, autofs, linux, lazylibrarian |
| `dns-0` | [`dns`](dns.md) | secondary_dns, python, vms, dns, linux |
| `dns-1` | [`dns`](dns.md) | primary_dns, pxe_client, baremetal, python, cname, dns, vault_servers, linux |
| `grafana-0` | [`grafana`](grafana.md) | python, grafana, cname, vms, linux, removable, autofs |
| `graphite-0` | [`graphite`](graphite.md) | python, pgdb, graphite, nginx_setup_proxy, vms |
| `jenkins-0` | [`jenkins`](jenkins.md) | python, cname, vms, jenkins, removable |
| `lidarr-0` | [`services`](services.md) | lidarr, cname, vms, linux, autofs |
| `minecraft-1` | [`minecraft`](minecraft.md) | bedrock, python, cname, vms, linux |
| `ombi-0` | [`ombi`](ombi.md) | python, cname, pgclient, vms, linux, autofs |
| `pg-0` | [`ombi`](ombi.md), [`pg`](pg.md) | python, pgdb, vms, autofs |
| `pg-1` | [`services`](services.md), [`pg`](pg.md) | python, pgdb, vms, autofs |
| `pg-2` | [`pg`](pg.md), [`redmine`](redmine.md) | python, pgdb, vms, autofs |
| `pg-3` | [`pg`](pg.md), [`semaphore`](semaphore.md) | python, pgdb, vms, autofs |
| `pg-4` | [`grafana`](grafana.md), [`pg`](pg.md) | python, pgdb, vms, autofs |
| `plex-0` | [`plex`](plex.md) | plex, pxe_client, wikipedia, baremetal, python, cname, lamp, linux, autofs |
| `prometheus-0` | [`prometheus`](prometheus.md) | prometheus, python, cname, vms, linux, autofs |
| `pve-0` | [`pve`](pve.md) | cname, pvenodes, ceph_nodes |
| `pve-1` | [`pve`](pve.md) | pvenodes, ceph_nodes |
| `pve-2` | [`pve`](pve.md) | cname, template, pvenodes, ceph_nodes |
| `pxe-0` | [`pxe`](pxe.md), [`dns`](dns.md), [`plex`](plex.md) | pxe, vms |
| `radarr-0` | [`services`](services.md) | cname, vms, radarr, linux, autofs |
| `redmine-0` | [`redmine`](redmine.md) | ruby, redmine, cname, linux, removable, autofs |
| `rproxy-0` | [`services`](services.md), [`plex`](plex.md), [`ombi`](ombi.md), [`semaphore`](semaphore.md), [`pve`](pve.md), [`redmine`](redmine.md), [`truenas`](truenas.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`ad`](ad.md), [`ansible`](ansible.md), [`grafana`](grafana.md), [`prometheus`](prometheus.md), [`tautulli`](tautulli.md), [`jenkins`](jenkins.md) | rproxy_main, oauth2_proxy, redis, certs, python, cname, vms, certbot, linux |
| `rproxy-1` | [`services`](services.md), [`plex`](plex.md), [`ombi`](ombi.md), [`semaphore`](semaphore.md), [`pve`](pve.md), [`redmine`](redmine.md), [`truenas`](truenas.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`ad`](ad.md), [`ansible`](ansible.md), [`grafana`](grafana.md), [`prometheus`](prometheus.md), [`tautulli`](tautulli.md), [`jenkins`](jenkins.md) | python, linux, rproxy_primary, vms |
| `rproxy-2` | [`services`](services.md), [`plex`](plex.md), [`ombi`](ombi.md), [`semaphore`](semaphore.md), [`pve`](pve.md), [`redmine`](redmine.md), [`truenas`](truenas.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`ad`](ad.md), [`ansible`](ansible.md), [`grafana`](grafana.md), [`prometheus`](prometheus.md), [`tautulli`](tautulli.md), [`jenkins`](jenkins.md) | python, linux, vms, rproxy_secondary |
| `sabnzbd-0` | [`services`](services.md) | sabnzbd, cname, vms, linux, autofs |
| `semaphore-0` | [`semaphore`](semaphore.md) | semaphore, nginx, python, cname, ansible, pgclient, vms, linux, autofs |
| `sonarr-0` | [`services`](services.md) | sonarr, cname, vms, linux, autofs |
| `synology-0` | [`synology`](synology.md) | synology, cname |
| `tautulli-0` | [`tautulli`](tautulli.md) | cname, linux, vms, python |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | vms |
| `truenas-01` | [`truenas`](truenas.md) | cname, nginx, truenas |
| `ubu24-template` | [`template`](template.md) | removable, template, ubuntu24 |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
