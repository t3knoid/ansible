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
| `ad0` | [`ad`](ad.md) | vms, dc_master, cname |
| `ansible-0` | [`ansible`](ansible.md), [`dns`](dns.md) | vault_clients, vscode, python, code_server, azure_cli, linux, ruby, ansible, nginx |
| `ansible-1` | [`ansible`](ansible.md) | nginx, python, linux, ansible, pgclient |
| `books-0` | [`services`](services.md) | autofs, calibre, linux, cname, lazylibrarian, vms, calibreweb |
| `dns-0` | [`dns`](dns.md) | secondary_dns, python, linux, vms, dns |
| `dns-1` | [`dns`](dns.md) | baremetal, python, vault_servers, primary_dns, linux, cname, dns, pxe_client |
| `grafana-0` | [`grafana`](grafana.md) | grafana, autofs, python, removable, linux, cname, vms |
| `graphite-0` | [`graphite`](graphite.md) | graphite, pgdb, python, nginx_setup_proxy, vms |
| `jenkins-0` | [`jenkins`](jenkins.md) | python, removable, cname, jenkins, vms |
| `lidarr-0` | [`services`](services.md) | lidarr, autofs, linux, cname, vms |
| `minecraft-1` | [`minecraft`](minecraft.md) | bedrock, python, linux, cname, vms |
| `ombi-0` | [`ombi`](ombi.md) | autofs, python, linux, cname, vms, pgclient |
| `pg-0` | [`pg`](pg.md), [`ombi`](ombi.md) | vms, autofs, python, pgdb |
| `pg-1` | [`pg`](pg.md), [`services`](services.md) | vms, autofs, pgdb, python |
| `pg-2` | [`pg`](pg.md), [`redmine`](redmine.md) | vms, autofs, python, pgdb |
| `pg-3` | [`semaphore`](semaphore.md), [`pg`](pg.md) | vms, autofs, python, pgdb |
| `pg-4` | [`grafana`](grafana.md), [`pg`](pg.md) | vms, autofs, python, pgdb |
| `plex-0` | [`plex`](plex.md) | baremetal, autofs, python, linux, cname, plex, lamp, wikipedia, pxe_client |
| `prometheus-0` | [`prometheus`](prometheus.md) | autofs, python, linux, prometheus, cname, vms |
| `pve-0` | [`pve`](pve.md) | pvenodes, ceph_nodes, cname |
| `pve-1` | [`pve`](pve.md) | pvenodes, ceph_nodes |
| `pve-2` | [`pve`](pve.md) | pvenodes, ceph_nodes, cname, template |
| `pxe-0` | [`plex`](plex.md), [`dns`](dns.md), [`pxe`](pxe.md) | vms, pxe |
| `radarr-0` | [`services`](services.md) | autofs, linux, cname, vms, radarr |
| `redmine-0` | [`redmine`](redmine.md) | autofs, redmine, removable, linux, cname, ruby |
| `rproxy-0` | [`tautulli`](tautulli.md), [`grafana`](grafana.md), [`services`](services.md), [`pve`](pve.md), [`semaphore`](semaphore.md), [`redmine`](redmine.md), [`ombi`](ombi.md), [`ad`](ad.md), [`prometheus`](prometheus.md), [`rproxy`](rproxy.md), [`jenkins`](jenkins.md), [`ansible`](ansible.md), [`plex`](plex.md), [`synology`](synology.md), [`truenas`](truenas.md) | certbot, certs, python, oauth2_proxy, redis, linux, cname, vms, rproxy_main |
| `rproxy-1` | [`tautulli`](tautulli.md), [`grafana`](grafana.md), [`services`](services.md), [`pve`](pve.md), [`semaphore`](semaphore.md), [`redmine`](redmine.md), [`ombi`](ombi.md), [`ad`](ad.md), [`prometheus`](prometheus.md), [`rproxy`](rproxy.md), [`jenkins`](jenkins.md), [`ansible`](ansible.md), [`plex`](plex.md), [`synology`](synology.md), [`truenas`](truenas.md) | vms, python, rproxy_primary, linux |
| `rproxy-2` | [`tautulli`](tautulli.md), [`grafana`](grafana.md), [`services`](services.md), [`pve`](pve.md), [`semaphore`](semaphore.md), [`redmine`](redmine.md), [`ombi`](ombi.md), [`ad`](ad.md), [`prometheus`](prometheus.md), [`rproxy`](rproxy.md), [`jenkins`](jenkins.md), [`ansible`](ansible.md), [`plex`](plex.md), [`synology`](synology.md), [`truenas`](truenas.md) | rproxy_secondary, vms, python, linux |
| `sabnzbd-0` | [`services`](services.md) | sabnzbd, autofs, linux, cname, vms |
| `semaphore-0` | [`semaphore`](semaphore.md) | ansible, nginx, semaphore, autofs, python, linux, cname, vms, pgclient |
| `sonarr-0` | [`services`](services.md) | autofs, linux, cname, vms, sonarr |
| `synology-0` | [`synology`](synology.md) | synology, cname |
| `tautulli-0` | [`tautulli`](tautulli.md) | vms, python, cname, linux |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | vms |
| `truenas-01` | [`truenas`](truenas.md) | nginx, cname, truenas |
| `ubu24-template` | [`template`](template.md) | ubuntu24, removable, template |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
