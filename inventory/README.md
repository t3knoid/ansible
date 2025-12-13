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
| `ansible-0` | [`dns`](dns.md), [`ansible`](ansible.md) | vscode, python, code_server, nginx, vault_clients, azure_cli, linux, ansible |
| `ansible-1` | [`ansible`](ansible.md) | python, nginx, pgclient, linux, ansible |
| `books-0` | [`services`](services.md) | autofs, cname, vms, calibreweb, linux, calibre, lazylibrarian |
| `dns-0` | [`dns`](dns.md) | dns, python, vms, secondary_dns, linux |
| `dns-1` | [`dns`](dns.md) | vault_servers, dns, python, primary_dns, cname, linux, baremetal, pxe_client |
| `grafana-0` | [`grafana`](grafana.md) | autofs, cname, python, vms, grafana, linux, removable |
| `graphite-0` | [`graphite`](graphite.md) | python, vms, nginx_setup_proxy, graphite, pgdb |
| `jenkins-0` | [`jenkins`](jenkins.md) | python, cname, vms, jenkins, removable |
| `lidarr-0` | [`services`](services.md) | autofs, cname, lidarr, vms, linux |
| `minecraft-1` | [`minecraft`](minecraft.md) | python, cname, vms, bedrock, linux |
| `ombi-0` | [`ombi`](ombi.md) | autofs, cname, python, vms, linux, pgclient |
| `pg-0` | [`ombi`](ombi.md), [`pg`](pg.md) | vms, autofs, python, pgdb |
| `pg-1` | [`pg`](pg.md), [`services`](services.md) | vms, autofs, python, pgdb |
| `pg-2` | [`redmine`](redmine.md), [`pg`](pg.md) | vms, autofs, python, pgdb |
| `pg-3` | [`semaphore`](semaphore.md), [`pg`](pg.md) | vms, autofs, python, pgdb |
| `pg-4` | [`pg`](pg.md), [`grafana`](grafana.md) | vms, autofs, python, pgdb |
| `plex-0` | [`plex`](plex.md) | autofs, python, wikipedia, cname, linux, lamp, baremetal, pxe_client, plex |
| `prometheus-0` | [`prometheus`](prometheus.md) | autofs, cname, python, vms, prometheus, linux |
| `pve-0` | [`pve`](pve.md) | ceph_nodes, cname, pvenodes |
| `pve-1` | [`pve`](pve.md) | ceph_nodes, pvenodes |
| `pve-2` | [`pve`](pve.md) | template, ceph_nodes, cname, pvenodes |
| `pxe-0` | [`pxe`](pxe.md), [`dns`](dns.md), [`plex`](plex.md) | vms, pxe |
| `radarr-0` | [`services`](services.md) | autofs, cname, vms, radarr, linux |
| `redmine-0` | [`redmine`](redmine.md) | redmine, autofs, cname, ruby, linux, removable |
| `rproxy-0` | [`pve`](pve.md), [`redmine`](redmine.md), [`ad`](ad.md), [`truenas`](truenas.md), [`synology`](synology.md), [`services`](services.md), [`grafana`](grafana.md), [`ombi`](ombi.md), [`rproxy`](rproxy.md), [`semaphore`](semaphore.md), [`prometheus`](prometheus.md), [`ansible`](ansible.md), [`jenkins`](jenkins.md), [`plex`](plex.md), [`tautulli`](tautulli.md) | python, cname, vms, redis, rproxy_main, oauth2_proxy, linux, certbot, certs |
| `rproxy-1` | [`pve`](pve.md), [`redmine`](redmine.md), [`ad`](ad.md), [`truenas`](truenas.md), [`synology`](synology.md), [`services`](services.md), [`grafana`](grafana.md), [`ombi`](ombi.md), [`rproxy`](rproxy.md), [`semaphore`](semaphore.md), [`prometheus`](prometheus.md), [`ansible`](ansible.md), [`jenkins`](jenkins.md), [`plex`](plex.md), [`tautulli`](tautulli.md) | vms, rproxy_primary, python, linux |
| `rproxy-2` | [`pve`](pve.md), [`redmine`](redmine.md), [`ad`](ad.md), [`truenas`](truenas.md), [`synology`](synology.md), [`services`](services.md), [`grafana`](grafana.md), [`ombi`](ombi.md), [`rproxy`](rproxy.md), [`semaphore`](semaphore.md), [`prometheus`](prometheus.md), [`ansible`](ansible.md), [`jenkins`](jenkins.md), [`plex`](plex.md), [`tautulli`](tautulli.md) | vms, rproxy_secondary, python, linux |
| `sabnzbd-0` | [`services`](services.md) | autofs, cname, vms, sabnzbd, linux |
| `semaphore-0` | [`semaphore`](semaphore.md) | autofs, cname, python, vms, nginx, semaphore, linux, pgclient, ansible |
| `sonarr-0` | [`services`](services.md) | autofs, cname, vms, sonarr, linux |
| `synology-0` | [`synology`](synology.md) | cname, synology |
| `tautulli-0` | [`tautulli`](tautulli.md) | vms, python, cname, linux |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | vms |
| `truenas-01` | [`truenas`](truenas.md) | cname, truenas, nginx |
| `ubu24-template` | [`template`](template.md) | template, removable, ubuntu24 |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
