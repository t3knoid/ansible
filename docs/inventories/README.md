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
| `ansible-0` | [`dns`](dns.md), [`ansible`](ansible.md) | ansible, azure_cli, code_server, linux, nginx, python, ruby, vault_clients, vscode |
| `ansible-1` | [`ansible`](ansible.md) | ansible, linux, nginx, pgclient, python |
| `books-0` | [`services`](services.md) | autofs, calibre, calibreweb, cname, lazylibrarian, linux, vms |
| `dns-0` | [`dns`](dns.md) | dns, linux, python, secondary_dns, vms |
| `dns-1` | [`dns`](dns.md) | baremetal, cname, dns, linux, primary_dns, pxe_client, python, vault_servers |
| `grafana-0` | [`grafana`](grafana.md) | autofs, cname, grafana, linux, python, removable, vms |
| `graphite-0` | [`graphite`](graphite.md) | graphite, nginx_setup_proxy, pgdb, python, vms |
| `jenkins-0` | [`jenkins`](jenkins.md) | cname, jenkins, python, removable, vms |
| `lidarr-0` | [`services`](services.md) | autofs, cname, lidarr, linux, vms |
| `minecraft-1` | [`minecraft`](minecraft.md) | bedrock, cname, linux, python, vms |
| `ombi-0` | [`ombi`](ombi.md) | autofs, cname, linux, pgclient, python, vms |
| `pg-0` | [`ombi`](ombi.md), [`pg`](pg.md) | autofs, pgdb, python, vms |
| `pg-1` | [`services`](services.md), [`pg`](pg.md) | autofs, pgdb, python, vms |
| `pg-2` | [`redmine`](redmine.md), [`pg`](pg.md) | autofs, pgdb, python, vms |
| `pg-3` | [`semaphore`](semaphore.md), [`pg`](pg.md) | autofs, pgdb, python, vms |
| `pg-4` | [`grafana`](grafana.md), [`pg`](pg.md) | autofs, pgdb, python, vms |
| `plex-0` | [`plex`](plex.md) | autofs, baremetal, cname, lamp, linux, plex, pxe_client, python, wikipedia |
| `prometheus-0` | [`prometheus`](prometheus.md) | autofs, cname, linux, prometheus, python, vms |
| `pve-0` | [`pve`](pve.md) | ceph_nodes, cname, pvenodes |
| `pve-1` | [`pve`](pve.md) | ceph_nodes, pvenodes |
| `pve-2` | [`pve`](pve.md) | ceph_nodes, cname, pvenodes, template |
| `pxe-0` | [`pxe`](pxe.md), [`dns`](dns.md), [`plex`](plex.md) | pxe, vms |
| `radarr-0` | [`services`](services.md) | autofs, cname, linux, radarr, vms |
| `redmine-0` | [`redmine`](redmine.md) | autofs, cname, linux, redmine, removable, ruby |
| `rproxy-0` | [`rproxy`](rproxy.md), [`pve`](pve.md), [`ombi`](ombi.md), [`jenkins`](jenkins.md), [`ansible`](ansible.md), [`tautulli`](tautulli.md), [`grafana`](grafana.md), [`prometheus`](prometheus.md), [`semaphore`](semaphore.md), [`plex`](plex.md), [`services`](services.md), [`redmine`](redmine.md), [`synology`](synology.md), [`truenas`](truenas.md), [`ad`](ad.md) | certbot, certs, cname, linux, oauth2_proxy, python, redis, rproxy_main, vms |
| `rproxy-1` | [`rproxy`](rproxy.md), [`pve`](pve.md), [`ombi`](ombi.md), [`jenkins`](jenkins.md), [`ansible`](ansible.md), [`tautulli`](tautulli.md), [`grafana`](grafana.md), [`prometheus`](prometheus.md), [`semaphore`](semaphore.md), [`plex`](plex.md), [`services`](services.md), [`redmine`](redmine.md), [`synology`](synology.md), [`truenas`](truenas.md), [`ad`](ad.md) | linux, python, rproxy_primary, vms |
| `rproxy-2` | [`rproxy`](rproxy.md), [`pve`](pve.md), [`ombi`](ombi.md), [`jenkins`](jenkins.md), [`ansible`](ansible.md), [`tautulli`](tautulli.md), [`grafana`](grafana.md), [`prometheus`](prometheus.md), [`semaphore`](semaphore.md), [`plex`](plex.md), [`services`](services.md), [`redmine`](redmine.md), [`synology`](synology.md), [`truenas`](truenas.md), [`ad`](ad.md) | linux, python, rproxy_secondary, vms |
| `sabnzbd-0` | [`services`](services.md) | autofs, cname, linux, sabnzbd, vms |
| `semaphore-0` | [`semaphore`](semaphore.md) | ansible, autofs, cname, linux, nginx, pgclient, python, semaphore, vms |
| `sonarr-0` | [`services`](services.md) | autofs, cname, linux, sonarr, vms |
| `synology-0` | [`synology`](synology.md) | cname, synology |
| `tautulli-0` | [`tautulli`](tautulli.md) | cname, linux, python, vms |
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
