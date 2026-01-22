# 🧭 Inventory Index

| Inventory | Description |
|-----------|-------------|
| [`ad`](../docs/inventory/ad.md) | Inventory for `ad` hosts |
| [`ansible`](../docs/inventory/ansible.md) | Inventory for `ansible` hosts |
| [`dns`](../docs/inventory/dns.md) | Inventory for `dns` hosts |
| [`grafana`](../docs/inventory/grafana.md) | Inventory for `grafana` hosts |
| [`graphite`](../docs/inventory/graphite.md) | Inventory for `graphite` hosts |
| [`ha`](../docs/inventory/ha.md) | Inventory for `ha` hosts |
| [`jenkins`](../docs/inventory/jenkins.md) | Inventory for `jenkins` hosts |
| [`minecraft`](../docs/inventory/minecraft.md) | Inventory for `minecraft` hosts |
| [`ombi`](../docs/inventory/ombi.md) | Inventory for `ombi` hosts |
| [`pg`](../docs/inventory/pg.md) | Inventory for `pg` hosts |
| [`plex`](../docs/inventory/plex.md) | Inventory for `plex` hosts |
| [`prometheus`](../docs/inventory/prometheus.md) | Inventory for `prometheus` hosts |
| [`pve`](../docs/inventory/pve.md) | Inventory for `pve` hosts |
| [`pxe`](../docs/inventory/pxe.md) | Inventory for `pxe` hosts |
| [`redmine`](../docs/inventory/redmine.md) | Inventory for `redmine` hosts |
| [`rproxy`](../docs/inventory/rproxy.md) | Inventory for `rproxy` hosts |
| [`semaphore`](../docs/inventory/semaphore.md) | Inventory for `semaphore` hosts |
| [`services`](../docs/inventory/services.md) | Inventory for `services` hosts |
| [`synology`](../docs/inventory/synology.md) | Inventory for `synology` hosts |
| [`tautulli`](../docs/inventory/tautulli.md) | Inventory for `tautulli` hosts |
| [`template`](../docs/inventory/template.md) | Inventory for `template` hosts |
| [`terraform`](../docs/inventory/terraform.md) | Inventory for `terraform` hosts |
| [`test`](../docs/inventory/test.md) | Inventory for `test` hosts |
| [`truenas`](../docs/inventory/truenas.md) | Inventory for `truenas` hosts |
| [`util`](../docs/inventory/util.md) | Inventory for `util` hosts |

## 🖥 Global Host Index
| Host | Inventories | Groups |
|------|-------------|--------|
| `ad0` | [`ad`](../docs/inventory/ad.md) | cname, dc_master, vms |
| `ansible-0` | [`dns`](../docs/inventory/dns.md), [`ansible`](../docs/inventory/ansible.md) | azure_cli, code_server, nginx, ruby, vault_clients, vms, vscode |
| `ansible-1` | [`ansible`](../docs/inventory/ansible.md) | nginx, pgclient, vms |
| `books-0` | [`services`](../docs/inventory/services.md) | autofs, calibre, calibreweb, cname, lazylibrarian, linux, vms |
| `dev-0` | [`ansible`](../docs/inventory/ansible.md) | wsl |
| `dns-0` | [`dns`](../docs/inventory/dns.md) | dns, linux, python, secondary_dns, unbound, vms |
| `dns-1` | [`dns`](../docs/inventory/dns.md) | baremetal, cname, dns, linux, primary_dns, pxe_client, python, unbound, vault_servers |
| `grafana-0` | [`grafana`](../docs/inventory/grafana.md) | autofs, cname, grafana, linux, python, removable, vms |
| `graphite-0` | [`graphite`](../docs/inventory/graphite.md) | graphite, nginx_setup_proxy, pgdb, python, vms |
| `ha-0` | [`ha`](../docs/inventory/ha.md) | home_assistant, vms |
| `jenkins-0` | [`jenkins`](../docs/inventory/jenkins.md) | cname, jenkins, python, removable, vms |
| `lidarr-0` | [`services`](../docs/inventory/services.md) | autofs, cname, lidarr, linux, vms |
| `minecraft-1` | [`minecraft`](../docs/inventory/minecraft.md) | bedrock, cname, linux, python, vms |
| `ombi-0` | [`ombi`](../docs/inventory/ombi.md) | autofs, cname, linux, pgclient, python, vms |
| `pg-0` | [`pg`](../docs/inventory/pg.md), [`ombi`](../docs/inventory/ombi.md) | autofs, pgdb, python, vms |
| `pg-1` | [`pg`](../docs/inventory/pg.md), [`services`](../docs/inventory/services.md) | autofs, pgdb, python, vms |
| `pg-2` | [`redmine`](../docs/inventory/redmine.md), [`pg`](../docs/inventory/pg.md) | autofs, pgdb, python, vms |
| `pg-3` | [`semaphore`](../docs/inventory/semaphore.md), [`pg`](../docs/inventory/pg.md) | autofs, pgdb, python, vms |
| `pg-4` | [`pg`](../docs/inventory/pg.md), [`grafana`](../docs/inventory/grafana.md) | autofs, pgdb, python, vms |
| `plex-0` | [`plex`](../docs/inventory/plex.md) | autofs, baremetal, cname, lamp, linux, plex, pxe_client, python, wikipedia |
| `prometheus-0` | [`prometheus`](../docs/inventory/prometheus.md) | autofs, cname, linux, prometheus, python, vms |
| `pve-0` | [`pve`](../docs/inventory/pve.md) | ceph_nodes, cname, pvenodes |
| `pve-1` | [`pve`](../docs/inventory/pve.md) | ceph_nodes, pvenodes |
| `pve-2` | [`pve`](../docs/inventory/pve.md) | ceph_nodes, cname, pvenodes, template |
| `pxe-0` | [`plex`](../docs/inventory/plex.md), [`pxe`](../docs/inventory/pxe.md), [`dns`](../docs/inventory/dns.md) | pxe, vms |
| `radarr-0` | [`services`](../docs/inventory/services.md) | autofs, cname, linux, radarr, vms |
| `redmine-0` | [`redmine`](../docs/inventory/redmine.md) | autofs, cname, linux, redmine, removable, ruby |
| `rproxy-0` | [`redmine`](../docs/inventory/redmine.md), [`plex`](../docs/inventory/plex.md), [`pve`](../docs/inventory/pve.md), [`semaphore`](../docs/inventory/semaphore.md), [`rproxy`](../docs/inventory/rproxy.md), [`services`](../docs/inventory/services.md), [`ombi`](../docs/inventory/ombi.md), [`synology`](../docs/inventory/synology.md), [`ad`](../docs/inventory/ad.md), [`ansible`](../docs/inventory/ansible.md), [`truenas`](../docs/inventory/truenas.md), [`grafana`](../docs/inventory/grafana.md), [`tautulli`](../docs/inventory/tautulli.md), [`jenkins`](../docs/inventory/jenkins.md), [`prometheus`](../docs/inventory/prometheus.md) | certbot, certs, cname, linux, oauth2_proxy, python, redis, rproxy_main, vms |
| `rproxy-1` | [`redmine`](../docs/inventory/redmine.md), [`plex`](../docs/inventory/plex.md), [`pve`](../docs/inventory/pve.md), [`semaphore`](../docs/inventory/semaphore.md), [`rproxy`](../docs/inventory/rproxy.md), [`services`](../docs/inventory/services.md), [`ombi`](../docs/inventory/ombi.md), [`synology`](../docs/inventory/synology.md), [`ad`](../docs/inventory/ad.md), [`ansible`](../docs/inventory/ansible.md), [`truenas`](../docs/inventory/truenas.md), [`grafana`](../docs/inventory/grafana.md), [`tautulli`](../docs/inventory/tautulli.md), [`jenkins`](../docs/inventory/jenkins.md), [`prometheus`](../docs/inventory/prometheus.md) | linux, python, rproxy_primary, vms |
| `rproxy-2` | [`redmine`](../docs/inventory/redmine.md), [`plex`](../docs/inventory/plex.md), [`pve`](../docs/inventory/pve.md), [`semaphore`](../docs/inventory/semaphore.md), [`rproxy`](../docs/inventory/rproxy.md), [`services`](../docs/inventory/services.md), [`ombi`](../docs/inventory/ombi.md), [`synology`](../docs/inventory/synology.md), [`ad`](../docs/inventory/ad.md), [`ansible`](../docs/inventory/ansible.md), [`truenas`](../docs/inventory/truenas.md), [`grafana`](../docs/inventory/grafana.md), [`tautulli`](../docs/inventory/tautulli.md), [`jenkins`](../docs/inventory/jenkins.md), [`prometheus`](../docs/inventory/prometheus.md) | linux, python, rproxy_secondary, vms |
| `sabnzbd-0` | [`services`](../docs/inventory/services.md) | autofs, cname, linux, sabnzbd, vms |
| `semaphore-0` | [`semaphore`](../docs/inventory/semaphore.md) | ansible, autofs, cname, linux, nginx, pgclient, python, semaphore, vms |
| `sonarr-0` | [`services`](../docs/inventory/services.md) | autofs, cname, linux, sonarr, vms |
| `synology-0` | [`synology`](../docs/inventory/synology.md) | cname, synology |
| `tautulli-0` | [`tautulli`](../docs/inventory/tautulli.md) | cname, linux, python, vms |
| `terraform-0` | [`terraform`](../docs/inventory/terraform.md) | vms |
| `test-0` | [`test`](../docs/inventory/test.md) | python, removable, vms |
| `truenas-01` | [`truenas`](../docs/inventory/truenas.md) | cname, nginx, truenas |
| `ubu24-template` | [`template`](../docs/inventory/template.md) | removable, template, ubuntu24 |
| `util-0` | [`util`](../docs/inventory/util.md) | linux |

## ⚠️ Duplicate Hosts
| `util-0` | [`util`](util.md) | linux |