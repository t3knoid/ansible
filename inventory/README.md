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
| `ansible-0` | [`ansible`](ansible.md), [`dns`](dns.md) | vscode, vault_clients, nginx, code_server, python, linux, ansible, azure_cli |
| `ansible-1` | [`ansible`](ansible.md) | pgclient, nginx, python, linux, ansible |
| `books-0` | [`services`](services.md) | calibre, vms, lazylibrarian, cname, linux, autofs, calibreweb |
| `dns-0` | [`dns`](dns.md) | secondary_dns, vms, python, linux, dns |
| `dns-1` | [`dns`](dns.md) | primary_dns, python, cname, linux, dns, vault_servers, baremetal, pxe_client |
| `grafana-0` | [`grafana`](grafana.md) | vms, python, cname, linux, grafana, autofs, removable |
| `graphite-0` | [`graphite`](graphite.md) | graphite, pgdb, vms, python, nginx_setup_proxy |
| `jenkins-0` | [`jenkins`](jenkins.md) | jenkins, vms, python, cname, removable |
| `lidarr-0` | [`services`](services.md) | lidarr, vms, cname, linux, autofs |
| `minecraft-1` | [`minecraft`](minecraft.md) | bedrock, vms, python, cname, linux |
| `ombi-0` | [`ombi`](ombi.md) | pgclient, vms, python, cname, linux, autofs |
| `pg-0` | [`ombi`](ombi.md), [`pg`](pg.md) | python, autofs, vms, pgdb |
| `pg-1` | [`services`](services.md), [`pg`](pg.md) | pgdb, python, autofs, vms |
| `pg-2` | [`redmine`](redmine.md), [`pg`](pg.md) | python, autofs, vms, pgdb |
| `pg-3` | [`semaphore`](semaphore.md), [`pg`](pg.md) | python, autofs, vms, pgdb |
| `pg-4` | [`grafana`](grafana.md), [`pg`](pg.md) | python, autofs, vms, pgdb |
| `plex-0` | [`plex`](plex.md) | wikipedia, python, cname, linux, autofs, lamp, baremetal, pxe_client, plex |
| `prometheus-0` | [`prometheus`](prometheus.md) | prometheus, vms, python, cname, linux, autofs |
| `pve-0` | [`pve`](pve.md) | ceph_nodes, cname, pvenodes |
| `pve-1` | [`pve`](pve.md) | ceph_nodes, pvenodes |
| `pve-2` | [`pve`](pve.md) | ceph_nodes, cname, pvenodes, template |
| `pxe-0` | [`pxe`](pxe.md), [`dns`](dns.md), [`plex`](plex.md) | pxe, vms |
| `radarr-0` | [`services`](services.md) | radarr, vms, cname, linux, autofs |
| `redmine-0` | [`redmine`](redmine.md) | removable, cname, linux, autofs, redmine, ruby |
| `rproxy-0` | [`jenkins`](jenkins.md), [`ombi`](ombi.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`prometheus`](prometheus.md), [`tautulli`](tautulli.md), [`truenas`](truenas.md), [`ansible`](ansible.md), [`pve`](pve.md), [`ad`](ad.md), [`semaphore`](semaphore.md), [`grafana`](grafana.md), [`redmine`](redmine.md), [`services`](services.md), [`plex`](plex.md) | certs, oauth2_proxy, redis, vms, rproxy_main, python, cname, linux, certbot |
| `rproxy-1` | [`jenkins`](jenkins.md), [`ombi`](ombi.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`prometheus`](prometheus.md), [`tautulli`](tautulli.md), [`truenas`](truenas.md), [`ansible`](ansible.md), [`pve`](pve.md), [`ad`](ad.md), [`semaphore`](semaphore.md), [`grafana`](grafana.md), [`redmine`](redmine.md), [`services`](services.md), [`plex`](plex.md) | rproxy_primary, linux, vms, python |
| `rproxy-2` | [`jenkins`](jenkins.md), [`ombi`](ombi.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`prometheus`](prometheus.md), [`tautulli`](tautulli.md), [`truenas`](truenas.md), [`ansible`](ansible.md), [`pve`](pve.md), [`ad`](ad.md), [`semaphore`](semaphore.md), [`grafana`](grafana.md), [`redmine`](redmine.md), [`services`](services.md), [`plex`](plex.md) | python, linux, rproxy_secondary, vms |
| `sabnzbd-0` | [`services`](services.md) | vms, cname, linux, autofs, sabnzbd |
| `semaphore-0` | [`semaphore`](semaphore.md) | pgclient, nginx, vms, python, cname, linux, ansible, semaphore, autofs |
| `sonarr-0` | [`services`](services.md) | sonarr, vms, cname, linux, autofs |
| `synology-0` | [`synology`](synology.md) | cname, synology |
| `tautulli-0` | [`tautulli`](tautulli.md) | python, cname, linux, vms |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | vms |
| `truenas-01` | [`truenas`](truenas.md) | truenas, nginx, cname |
| `ubu24-template` | [`template`](template.md) | removable, ubuntu24, template |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
