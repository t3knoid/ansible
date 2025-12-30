# 🧭 Inventory Index

| Inventory | Description |
|-----------|-------------|
| [`ad`](../docs/inventories/ad.md) | Inventory for `ad` hosts |
| [`ansible`](../docs/inventories/ansible.md) | Inventory for `ansible` hosts |
| [`dns`](../docs/inventories/dns.md) | Inventory for `dns` hosts |
| [`grafana`](../docs/inventories/grafana.md) | Inventory for `grafana` hosts |
| [`graphite`](../docs/inventories/graphite.md) | Inventory for `graphite` hosts |
| [`jenkins`](../docs/inventories/jenkins.md) | Inventory for `jenkins` hosts |
| [`minecraft`](../docs/inventories/minecraft.md) | Inventory for `minecraft` hosts |
| [`ombi`](../docs/inventories/ombi.md) | Inventory for `ombi` hosts |
| [`pg`](../docs/inventories/pg.md) | Inventory for `pg` hosts |
| [`plex`](../docs/inventories/plex.md) | Inventory for `plex` hosts |
| [`prometheus`](../docs/inventories/prometheus.md) | Inventory for `prometheus` hosts |
| [`pve`](../docs/inventories/pve.md) | Inventory for `pve` hosts |
| [`pxe`](../docs/inventories/pxe.md) | Inventory for `pxe` hosts |
| [`redmine`](../docs/inventories/redmine.md) | Inventory for `redmine` hosts |
| [`rproxy`](../docs/inventories/rproxy.md) | Inventory for `rproxy` hosts |
| [`semaphore`](../docs/inventories/semaphore.md) | Inventory for `semaphore` hosts |
| [`services`](../docs/inventories/services.md) | Inventory for `services` hosts |
| [`synology`](../docs/inventories/synology.md) | Inventory for `synology` hosts |
| [`tautulli`](../docs/inventories/tautulli.md) | Inventory for `tautulli` hosts |
| [`template`](../docs/inventories/template.md) | Inventory for `template` hosts |
| [`terraform`](../docs/inventories/terraform.md) | Inventory for `terraform` hosts |
| [`test`](../docs/inventories/test.md) | Inventory for `test` hosts |
| [`truenas`](../docs/inventories/truenas.md) | Inventory for `truenas` hosts |
| [`util`](../docs/inventories/util.md) | Inventory for `util` hosts |

## 🖥 Global Host Index
| Host | Inventories | Groups |
|------|-------------|--------|
| `ad0` | [`ad`](../docs/inventories/ad.md) | cname, dc_master, vms |
| `ansible-0` | [`dns`](../docs/inventories/dns.md), [`ansible`](../docs/inventories/ansible.md) | ansible, azure_cli, code_server, linux, nginx, python, ruby, vault_clients, vscode |
| `ansible-1` | [`ansible`](../docs/inventories/ansible.md) | ansible, linux, nginx, pgclient, python |
| `books-0` | [`services`](../docs/inventories/services.md) | autofs, calibre, calibreweb, cname, lazylibrarian, linux, vms |
| `dns-0` | [`dns`](../docs/inventories/dns.md) | dns, linux, python, secondary_dns, unbound, vms |
| `dns-1` | [`dns`](../docs/inventories/dns.md) | baremetal, cname, dns, linux, primary_dns, pxe_client, python, unbound, vault_servers |
| `grafana-0` | [`grafana`](../docs/inventories/grafana.md) | autofs, cname, grafana, linux, python, removable, vms |
| `graphite-0` | [`graphite`](../docs/inventories/graphite.md) | graphite, nginx_setup_proxy, pgdb, python, vms |
| `jenkins-0` | [`jenkins`](../docs/inventories/jenkins.md) | cname, jenkins, python, removable, vms |
| `lidarr-0` | [`services`](../docs/inventories/services.md) | autofs, cname, lidarr, linux, vms |
| `minecraft-1` | [`minecraft`](../docs/inventories/minecraft.md) | bedrock, cname, linux, python, vms |
| `ombi-0` | [`ombi`](../docs/inventories/ombi.md) | autofs, cname, linux, pgclient, python, vms |
| `pg-0` | [`ombi`](../docs/inventories/ombi.md), [`pg`](../docs/inventories/pg.md) | autofs, pgdb, python, vms |
| `pg-1` | [`pg`](../docs/inventories/pg.md), [`services`](../docs/inventories/services.md) | autofs, pgdb, python, vms |
| `pg-2` | [`redmine`](../docs/inventories/redmine.md), [`pg`](../docs/inventories/pg.md) | autofs, pgdb, python, vms |
| `pg-3` | [`semaphore`](../docs/inventories/semaphore.md), [`pg`](../docs/inventories/pg.md) | autofs, pgdb, python, vms |
| `pg-4` | [`pg`](../docs/inventories/pg.md), [`grafana`](../docs/inventories/grafana.md) | autofs, pgdb, python, vms |
| `plex-0` | [`plex`](../docs/inventories/plex.md) | autofs, baremetal, cname, lamp, linux, plex, pxe_client, python, wikipedia |
| `prometheus-0` | [`prometheus`](../docs/inventories/prometheus.md) | autofs, cname, linux, prometheus, python, vms |
| `pve-0` | [`pve`](../docs/inventories/pve.md) | ceph_nodes, cname, pvenodes |
| `pve-1` | [`pve`](../docs/inventories/pve.md) | ceph_nodes, pvenodes |
| `pve-2` | [`pve`](../docs/inventories/pve.md) | ceph_nodes, cname, pvenodes, template |
| `pxe-0` | [`dns`](../docs/inventories/dns.md), [`plex`](../docs/inventories/plex.md), [`pxe`](../docs/inventories/pxe.md) | pxe, vms |
| `radarr-0` | [`services`](../docs/inventories/services.md) | autofs, cname, linux, radarr, vms |
| `redmine-0` | [`redmine`](../docs/inventories/redmine.md) | autofs, cname, linux, redmine, removable, ruby |
| `rproxy-0` | [`prometheus`](../docs/inventories/prometheus.md), [`services`](../docs/inventories/services.md), [`pve`](../docs/inventories/pve.md), [`ansible`](../docs/inventories/ansible.md), [`semaphore`](../docs/inventories/semaphore.md), [`grafana`](../docs/inventories/grafana.md), [`redmine`](../docs/inventories/redmine.md), [`jenkins`](../docs/inventories/jenkins.md), [`truenas`](../docs/inventories/truenas.md), [`ombi`](../docs/inventories/ombi.md), [`ad`](../docs/inventories/ad.md), [`tautulli`](../docs/inventories/tautulli.md), [`synology`](../docs/inventories/synology.md), [`plex`](../docs/inventories/plex.md), [`rproxy`](../docs/inventories/rproxy.md) | certbot, certs, cname, linux, oauth2_proxy, python, redis, rproxy_main, vms |
| `rproxy-1` | [`prometheus`](../docs/inventories/prometheus.md), [`services`](../docs/inventories/services.md), [`pve`](../docs/inventories/pve.md), [`ansible`](../docs/inventories/ansible.md), [`semaphore`](../docs/inventories/semaphore.md), [`grafana`](../docs/inventories/grafana.md), [`redmine`](../docs/inventories/redmine.md), [`jenkins`](../docs/inventories/jenkins.md), [`truenas`](../docs/inventories/truenas.md), [`ombi`](../docs/inventories/ombi.md), [`ad`](../docs/inventories/ad.md), [`tautulli`](../docs/inventories/tautulli.md), [`synology`](../docs/inventories/synology.md), [`plex`](../docs/inventories/plex.md), [`rproxy`](../docs/inventories/rproxy.md) | linux, python, rproxy_primary, vms |
| `rproxy-2` | [`prometheus`](../docs/inventories/prometheus.md), [`services`](../docs/inventories/services.md), [`pve`](../docs/inventories/pve.md), [`ansible`](../docs/inventories/ansible.md), [`semaphore`](../docs/inventories/semaphore.md), [`grafana`](../docs/inventories/grafana.md), [`redmine`](../docs/inventories/redmine.md), [`jenkins`](../docs/inventories/jenkins.md), [`truenas`](../docs/inventories/truenas.md), [`ombi`](../docs/inventories/ombi.md), [`ad`](../docs/inventories/ad.md), [`tautulli`](../docs/inventories/tautulli.md), [`synology`](../docs/inventories/synology.md), [`plex`](../docs/inventories/plex.md), [`rproxy`](../docs/inventories/rproxy.md) | linux, python, rproxy_secondary, vms |
| `sabnzbd-0` | [`services`](../docs/inventories/services.md) | autofs, cname, linux, sabnzbd, vms |
| `semaphore-0` | [`semaphore`](../docs/inventories/semaphore.md) | ansible, autofs, cname, linux, nginx, pgclient, python, semaphore, vms |
| `sonarr-0` | [`services`](../docs/inventories/services.md) | autofs, cname, linux, sonarr, vms |
| `synology-0` | [`synology`](../docs/inventories/synology.md) | cname, synology |
| `tautulli-0` | [`tautulli`](../docs/inventories/tautulli.md) | cname, linux, python, vms |
| `terraform-0` | [`terraform`](../docs/inventories/terraform.md) | vms |
| `test-0` | [`test`](../docs/inventories/test.md) | vms |
| `truenas-01` | [`truenas`](../docs/inventories/truenas.md) | cname, nginx, truenas |
| `ubu24-template` | [`template`](../docs/inventories/template.md) | removable, template, ubuntu24 |
| `util-0` | [`util`](../docs/inventories/util.md) | linux |

## ⚠️ Duplicate Hosts
| `util-0` | [`util`](util.md) | linux |