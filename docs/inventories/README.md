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
| `ansible-0` | [`ansible`](ansible.md), [`dns`](dns.md) | ruby, linux, nginx, code_server, ansible, vscode, azure_cli, python, vault_clients |
| `ansible-1` | [`ansible`](ansible.md) | linux, nginx, ansible, pgclient, python |
| `books-0` | [`services`](services.md) | linux, calibreweb, calibre, autofs, lazylibrarian, vms, cname |
| `dns-0` | [`dns`](dns.md) | linux, secondary_dns, dns, vms, python |
| `dns-1` | [`dns`](dns.md) | pxe_client, linux, baremetal, vault_servers, dns, python, primary_dns, cname |
| `grafana-0` | [`grafana`](grafana.md) | linux, removable, autofs, grafana, vms, python, cname |
| `graphite-0` | [`graphite`](graphite.md) | nginx_setup_proxy, graphite, pgdb, vms, python |
| `jenkins-0` | [`jenkins`](jenkins.md) | removable, jenkins, vms, python, cname |
| `lidarr-0` | [`services`](services.md) | linux, lidarr, autofs, vms, cname |
| `minecraft-1` | [`minecraft`](minecraft.md) | bedrock, linux, vms, python, cname |
| `ombi-0` | [`ombi`](ombi.md) | linux, autofs, pgclient, vms, python, cname |
| `pg-0` | [`pg`](pg.md), [`ombi`](ombi.md) | vms, python, autofs, pgdb |
| `pg-1` | [`pg`](pg.md), [`services`](services.md) | vms, pgdb, python, autofs |
| `pg-2` | [`pg`](pg.md), [`redmine`](redmine.md) | vms, python, autofs, pgdb |
| `pg-3` | [`pg`](pg.md), [`semaphore`](semaphore.md) | vms, python, autofs, pgdb |
| `pg-4` | [`pg`](pg.md), [`grafana`](grafana.md) | vms, python, autofs, pgdb |
| `plex-0` | [`plex`](plex.md) | pxe_client, linux, baremetal, autofs, plex, wikipedia, lamp, python, cname |
| `prometheus-0` | [`prometheus`](prometheus.md) | linux, prometheus, autofs, vms, python, cname |
| `pve-0` | [`pve`](pve.md) | cname, ceph_nodes, pvenodes |
| `pve-1` | [`pve`](pve.md) | ceph_nodes, pvenodes |
| `pve-2` | [`pve`](pve.md) | template, cname, ceph_nodes, pvenodes |
| `pxe-0` | [`plex`](plex.md), [`pxe`](pxe.md), [`dns`](dns.md) | vms, pxe |
| `radarr-0` | [`services`](services.md) | linux, radarr, autofs, vms, cname |
| `redmine-0` | [`redmine`](redmine.md) | ruby, removable, linux, redmine, autofs, cname |
| `rproxy-0` | [`semaphore`](semaphore.md), [`ad`](ad.md), [`ombi`](ombi.md), [`pve`](pve.md), [`jenkins`](jenkins.md), [`services`](services.md), [`prometheus`](prometheus.md), [`redmine`](redmine.md), [`ansible`](ansible.md), [`rproxy`](rproxy.md), [`grafana`](grafana.md), [`plex`](plex.md), [`synology`](synology.md), [`truenas`](truenas.md), [`tautulli`](tautulli.md) | rproxy_main, linux, certs, oauth2_proxy, redis, certbot, vms, python, cname |
| `rproxy-1` | [`semaphore`](semaphore.md), [`ad`](ad.md), [`ombi`](ombi.md), [`pve`](pve.md), [`jenkins`](jenkins.md), [`services`](services.md), [`prometheus`](prometheus.md), [`redmine`](redmine.md), [`ansible`](ansible.md), [`rproxy`](rproxy.md), [`grafana`](grafana.md), [`plex`](plex.md), [`synology`](synology.md), [`truenas`](truenas.md), [`tautulli`](tautulli.md) | python, vms, rproxy_primary, linux |
| `rproxy-2` | [`semaphore`](semaphore.md), [`ad`](ad.md), [`ombi`](ombi.md), [`pve`](pve.md), [`jenkins`](jenkins.md), [`services`](services.md), [`prometheus`](prometheus.md), [`redmine`](redmine.md), [`ansible`](ansible.md), [`rproxy`](rproxy.md), [`grafana`](grafana.md), [`plex`](plex.md), [`synology`](synology.md), [`truenas`](truenas.md), [`tautulli`](tautulli.md) | python, vms, linux, rproxy_secondary |
| `sabnzbd-0` | [`services`](services.md) | linux, autofs, sabnzbd, vms, cname |
| `semaphore-0` | [`semaphore`](semaphore.md) | semaphore, linux, nginx, ansible, autofs, pgclient, vms, python, cname |
| `sonarr-0` | [`services`](services.md) | linux, sonarr, autofs, vms, cname |
| `synology-0` | [`synology`](synology.md) | synology, cname |
| `tautulli-0` | [`tautulli`](tautulli.md) | python, vms, linux, cname |
| `terraform-0` | [`terraform`](terraform.md) | vms |
| `test-0` | [`test`](test.md) | vms |
| `truenas-01` | [`truenas`](truenas.md) | truenas, nginx, cname |
| `ubu24-template` | [`template`](template.md) | ubuntu24, template, removable |
| `util-0` | [`util`](util.md) | linux |

## ⚠️ Duplicate Hosts
> **📌 Note – Duplicate Hosts**
>
> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.
> Use `--strict` mode to enforce uniqueness.
