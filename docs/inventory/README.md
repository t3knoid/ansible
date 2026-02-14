# 🧭 Inventory Index

| Inventory | Description |
|-----------|-------------|
| [`ad`](ad.md) | Inventory for `ad` hosts |
| [`ansible`](ansible.md) | Inventory for `ansible` hosts |
| [`dns`](dns.md) | Inventory for `dns` hosts |
| [`grafana`](grafana.md) | Inventory for `grafana` hosts |
| [`graphite`](graphite.md) | Inventory for `graphite` hosts |
| [`ha`](ha.md) | Inventory for `ha` hosts |
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
| `ansible-0` | [`ansible`](ansible.md), [`dns`](dns.md) | azure_cli, code_server, nginx, ruby, vault_clients, vms, vscode |
| `ansible-1` | [`ansible`](ansible.md) | nginx, pgclient, vms |
| `books-0` | [`services`](services.md) | autofs, calibre, calibreweb, cname, lazylibrarian, linux, vms |
| `dev-0` | [`ansible`](ansible.md) | wsl |
| `dns-0` | [`dns`](dns.md) | dns, linux, python, secondary_dns, unbound, vms |
| `dns-1` | [`dns`](dns.md) | baremetal, cname, dns, linux, primary_dns, pxe_client, python, unbound, vault_servers |
| `grafana-0` | [`grafana`](grafana.md) | autofs, cname, grafana, linux, python, removable, vms |
| `graphite-0` | [`graphite`](graphite.md) | graphite, nginx_setup_proxy, pgdb, python, vms |
| `ha-0` | [`ha`](ha.md) | home_assistant, vms |
| `jenkins-0` | [`jenkins`](jenkins.md) | cname, jenkins, python, removable, vms |
| `lidarr-0` | [`services`](services.md) | autofs, cname, lidarr, linux, vms |
| `minecraft-1` | [`minecraft`](minecraft.md) | bedrock, cname, linux, python, vms |
| `ombi-0` | [`ombi`](ombi.md) | autofs, cname, linux, pgclient, python, vms |
| `pg-0` | [`pg`](pg.md), [`ombi`](ombi.md) | autofs, pgdb, python, vms |
| `pg-1` | [`pg`](pg.md), [`services`](services.md) | autofs, pgdb, python, vms |
| `pg-2` | [`pg`](pg.md), [`redmine`](redmine.md) | autofs, pgdb, python, vms |
| `pg-3` | [`pg`](pg.md), [`semaphore`](semaphore.md) | autofs, pgdb, python, vms |
| `pg-4` | [`pg`](pg.md), [`grafana`](grafana.md) | autofs, pgdb, python, vms |
| `plex-0` | [`plex`](plex.md) | autofs, baremetal, cname, lamp, linux, plex, pxe_client, python, wikipedia |
| `prometheus-0` | [`prometheus`](prometheus.md) | autofs, cname, linux, prometheus, python, vms |
| `pve-0` | [`pve`](pve.md) | ceph_nodes, cname, pvenodes |
| `pve-1` | [`pve`](pve.md) | ceph_nodes, pvenodes |
| `pve-2` | [`pve`](pve.md) | ceph_nodes, cname, pvenodes, template |
| `pxe-0` | [`plex`](plex.md), [`pxe`](pxe.md), [`dns`](dns.md) | pxe, vms |
| `radarr-0` | [`services`](services.md) | autofs, cname, linux, radarr, vms |
| `redmine-0` | [`redmine`](redmine.md) | autofs, cname, linux, redmine, removable, ruby |
| `rproxy-0` | [`semaphore`](semaphore.md), [`jenkins`](jenkins.md), [`grafana`](grafana.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`tautulli`](tautulli.md), [`ansible`](ansible.md), [`ombi`](ombi.md), [`pve`](pve.md), [`redmine`](redmine.md), [`ad`](ad.md), [`truenas`](truenas.md), [`plex`](plex.md), [`prometheus`](prometheus.md), [`services`](services.md) | certbot, certs, cname, linux, oauth2_proxy, python, redis, rproxy_main, vms |
| `rproxy-1` | [`semaphore`](semaphore.md), [`jenkins`](jenkins.md), [`grafana`](grafana.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`tautulli`](tautulli.md), [`ansible`](ansible.md), [`ombi`](ombi.md), [`pve`](pve.md), [`redmine`](redmine.md), [`ad`](ad.md), [`truenas`](truenas.md), [`plex`](plex.md), [`prometheus`](prometheus.md), [`services`](services.md) | linux, python, rproxy_primary, vms |
| `rproxy-2` | [`semaphore`](semaphore.md), [`jenkins`](jenkins.md), [`grafana`](grafana.md), [`rproxy`](rproxy.md), [`synology`](synology.md), [`tautulli`](tautulli.md), [`ansible`](ansible.md), [`ombi`](ombi.md), [`pve`](pve.md), [`redmine`](redmine.md), [`ad`](ad.md), [`truenas`](truenas.md), [`plex`](plex.md), [`prometheus`](prometheus.md), [`services`](services.md) | linux, python, rproxy_secondary, vms |
| `sabnzbd-0` | [`services`](services.md) | autofs, cname, linux, sabnzbd, vms |
| `semaphore-0` | [`semaphore`](semaphore.md) | ansible, autofs, cname, linux, nginx, pgclient, python, semaphore, vms |
| `sonarr-0` | [`services`](services.md) | autofs, cname, linux, sonarr, vms |
| `synology-0` | [`synology`](synology.md) | cname, synology |
| `tautulli-0` | [`tautulli`](tautulli.md) | cname, linux, python, vms |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | python, removable, vms |
| `truenas-01` | [`truenas`](truenas.md) | cname, nginx, truenas |
| `ubu24-template` | [`template`](template.md) | removable, ubuntu24 |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
