# 🛠️ Role: `global`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Provides global defaults common to all roles. It provides the IP definition of each host in the datacenter. Every host must be defined here with its corresponding IP address. Other global variables are also defined here.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `global_proxmox_api_host` | `192.168.2.200` |  |
| `global_proxmox_api_port` | `8006` |  |
| `global_os` | `` |  |
| `ubuntu_24_server` | `` |  |
| `distro` | `ubuntu` |  |
| `type` | `server` |  |
| `release_download_url` | `"https://releases.ubuntu.com/noble"` |  |
| `iso` | `ubuntu-24.04.1-live-server-amd64.iso` |  |
| `cloudinit_download_url` | `https://cloud-images.ubuntu.com/noble/current` |  |
| `cloudinit_img` | `noble-server-cloudimg-amd64.img` |  |
| `tarball` | `ubuntu-24.04.1-netboot-amd64.tar.gz` |  |
| `template` | `ubuntu-server-24.04-cloudinit` |  |
| `version` | `24.4` |  |
| `win_2022_server` | `` |  |
| `distro` | `windows` |  |
| `type` | `server` |  |
| `iso` | `en-us_windows_server_2022_updated_aug_2024_x64_dvd_17b2bb17.iso` |  |
| `template` | `` |  |
| `version` | `2022` |  |
| `win_11_business` | `` |  |
| `distro` | `windows` |  |
| `type` | `server` |  |
| `iso` | `en-us_windows_11_business-editions_version_23h2_updated_aug_2024_x64_dvd_4b6aa6b4.iso` |  |
| `template` | `` |  |
| `version` | `11` |  |
| `global_domain_name` | `"refol.us"` |  |
| `global_dns_servers` | `` |  |
| `global_timezone` | `"America/New_York"` |  |
| `global_packages_list` | `` |  |
| `global_host` | `"{{ global_hosts[inventory_hostname] }}"` | non-standard route. |
| `global_ip_address` | `"{{ global_host.ip }}"` |  |
| `global_network` | `"{{ global_networks[global_host.network] }}"` |  |
| `global_gateway` | `"{{ global_network.gateway }}"` |  |
| `global_prefix` | `"{{ global_network.cidr.split('/')[1] }}"` |  |
| `global_pihole_api_host` | `"{{ global_ip_addresses['dns-1'] }}"` |  |

## 📦 Vars
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `global_ansible_root_dir` | `"{{ playbook_dir | dirname | dirname }}"` |  |
| `global_terraform_root_dir` | `"{{ global_ansible_root_dir }}/terraform"` |  |
| `global_inventory_dir_name` | `"{{ inventory_dir | basename }}"` |  |
| `global_networks` | `` | Subnets; each global_hosts entry's network must be one of these keys. |
| `lan0` | `` |  |
| `cidr` | `192.168.0.0/24` |  |
| `gateway` | `192.168.0.1` |  |
| `lan2` | `` |  |
| `cidr` | `192.168.2.0/24` |  |
| `gateway` | `192.168.2.1` |  |
| `lan20` | `` |  |
| `cidr` | `192.168.20.0/24` |  |
| `gateway` | `192.168.20.1` |  |
| `lan30` | `` |  |
| `cidr` | `192.168.30.0/24` |  |
| `gateway` | `192.168.30.1` |  |
| `lan90` | `` |  |
| `cidr` | `192.168.90.0/24` |  |
| `gateway` | `192.168.90.1` |  |
| `global_hosts` | `` | Hostname -> IP and network for every host in the homelab. |
| `ansible-0` | `{ ip: 192.168.20.101, network: lan20 }` |  |
| `ansible-1` | `{ ip: 192.168.20.102, network: lan20 } # hosted in TrueNAS` |  |
| `test-0` | `{ ip: 192.168.20.103, network: lan20 }` |  |
| `semaphore-0` | `{ ip: 192.168.20.110, network: lan20 }` |  |
| `sonarr-0` | `{ ip: 192.168.20.150, network: lan20 }` |  |
| `lidarr-0` | `{ ip: 192.168.20.151, network: lan20 }` |  |
| `radarr-0` | `{ ip: 192.168.20.152, network: lan20 }` |  |
| `sabnzbd-0` | `{ ip: 192.168.20.153, network: lan20 }` |  |
| `ombi-0` | `{ ip: 192.168.20.155, network: lan20 }` |  |
| `tautulli-0` | `{ ip: 192.168.20.157, network: lan20 }` |  |
| `books-0` | `{ ip: 192.168.20.160, network: lan20 }` |  |
| `minecraft-1` | `{ ip: 192.168.30.166, network: lan30 }` |  |
| `pg-0` | `{ ip: 192.168.20.170, network: lan20 }` |  |
| `pg-1` | `{ ip: 192.168.20.171, network: lan20 }` |  |
| `pg-2` | `{ ip: 192.168.20.172, network: lan20 }` |  |
| `pg-3` | `{ ip: 192.168.20.173, network: lan20 }` |  |
| `pg-4` | `{ ip: 192.168.20.174, network: lan20 }` |  |
| `jenkins-0` | `{ ip: 192.168.20.180, network: lan20 }` |  |
| `rosie-0` | `{ ip: 192.168.20.182, network: lan20 }` |  |
| `ha-0` | `{ ip: 192.168.20.184, network: lan20 }` |  |
| `redmine-0` | `{ ip: 192.168.20.186, network: lan20 }` |  |
| `prometheus-0` | `{ ip: 192.168.20.192, network: lan20 }` |  |
| `loki-0` | `{ ip: 192.168.20.193, network: lan20 }` |  |
| `grafana-0` | `{ ip: 192.168.20.195, network: lan20 }` |  |
| `ecube-2` | `{ ip: 192.168.90.196, network: lan90 }` |  |
| `ecube-1` | `{ ip: 192.168.90.197, network: lan90 }` |  |
| `ecube-0` | `{ ip: 192.168.20.198, network: lan20 }` |  |
| `ubu24-template` | `{ ip: 192.168.20.199, network: lan20 }` |  |
| `pve-0` | `{ ip: 192.168.2.200, network: lan2 }` |  |
| `pve-1` | `{ ip: 192.168.2.201, network: lan2 }` |  |
| `pve-2` | `{ ip: 192.168.2.202, network: lan2 }` |  |
| `rproxy-0` | `{ ip: 192.168.30.210, network: lan30 }` |  |
| `rproxy-1` | `{ ip: 192.168.20.211, network: lan20 }` |  |
| `rproxy-2` | `{ ip: 192.168.20.212, network: lan20 }` |  |
| `plex-0` | `{ ip: 192.168.2.220, network: lan2 }` |  |
| `synology-0` | `{ ip: 192.168.2.240, network: lan2 }` |  |
| `truenas-01` | `{ ip: 192.168.2.250, network: lan2 }` |  |
| `ad0` | `{ ip: 192.168.20.251, network: lan20 }` |  |
| `dns-0` | `{ ip: 192.168.20.252, network: lan20 }` |  |
| `dns-1` | `{ ip: 192.168.20.253, network: lan20 }` |  |
| `pxe-0` | `{ ip: 192.168.20.254, network: lan20 }` |  |
| `util-0` | `{ ip: 192.168.0.56, network: lan0 }` |  |
| `global_ip_addresses` | `"{{ dict(global_hosts.keys() | zip(global_hosts.values() | map(attribute='ip'))) }}"` | Flat hostname -> IP map derived from global_hosts; most roles use this. |

## 📑 Tasks
- Global
- Validate global_hosts against global_networks
- Warn when this host has no entry in global_hosts
- Expose global_ip_addresses as a fact for cross-host lookups

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: global
```