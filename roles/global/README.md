# Role: `global`

## 📖 Overview
Provides global defaults common to all roles. It also provides the IP definition of each host in the datacenter.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## 🧮 Defaults
- `global_proxmox_api_host`: `192.168.2.200`
- `global_proxmox_api_port`: `8006`
- `global_os`: ``
- `ubuntu_24_server`: ``
- `distro`: `ubuntu`
- `type`: `server`
- `release_download_url`: `"https://releases.ubuntu.com/noble"`
- `iso`: `ubuntu-24.04.1-live-server-amd64.iso`
- `cloudinit_download_url`: `https://cloud-images.ubuntu.com/noble/current`
- `cloudinit_img`: `noble-server-cloudimg-amd64.img`
- `tarball`: `ubuntu-24.04.1-netboot-amd64.tar.gz`
- `template`: `ubuntu-server-24.04-cloudinit`
- `version`: `24.4`
- `win_2022_server`: ``
- `distro`: `windows`
- `type`: `server`
- `iso`: `en-us_windows_server_2022_updated_aug_2024_x64_dvd_17b2bb17.iso`
- `template`: ``
- `version`: `2022`
- `win_11_business`: ``
- `distro`: `windows`
- `type`: `server`
- `iso`: `en-us_windows_11_business-editions_version_23h2_updated_aug_2024_x64_dvd_4b6aa6b4.iso`
- `template`: ``
- `version`: `11`
- `global_domain_name`: `"refol.us"`
- `global_dns_servers`: ``
- `global_gateway`: `192.168.2.1`
- `global_timezone`: `"America/New_York"`
- `global_packages_list`: ``

## 🧮 Vars
- `global_ip_addresses`: ``
- `ansible-0`: `192.168.2.101`
- `ansible-1`: `192.168.2.102`
- `semaphore-0`: `192.168.2.110`
- `sonarr-0`: `192.168.2.150`
- `lidarr-0`: `192.168.2.151`
- `radarr-0`: `192.168.2.152`
- `sabnzbd-0`: `192.168.2.153`
- `readarr-0`: `192.168.2.154`
- `ombi-0`: `192.168.2.155`
- `tautulli-0`: `192.168.2.157`
- `calibre-0`: `192.168.2.160`
- `lazy-0`: `192.168.2.162`
- `minecraft-1`: `192.168.2.166`
- `pg-0`: `192.168.2.170`
- `pg-1`: `192.168.2.171`
- `pg-2`: `192.168.2.172`
- `pg-3`: `192.168.2.173`
- `jenkins-0`: `192.168.2.180`
- `redmine-0`: `192.168.2.186`
- `plex-0`: `192.168.2.220`
- `graphite-0`: `192.168.2.190`
- `ubu24-template`: `192.168.2.199`
- `pve-0`: `192.168.2.200`
- `pve-1`: `192.168.2.201`
- `pve-2`: `192.168.2.202`
- `rproxy-0`: `192.168.2.210`
- `rproxy-1`: `192.168.2.211`
- `rproxy-2`: `192.168.2.212`
- `synology-0`: `192.168.2.240`
- `truenas-01`: `192.168.2.250`
- `ad0`: `192.168.2.251`
- `dns-0`: `192.168.2.252`
- `dns-1`: `192.168.2.253`
- `pxe-0`: `192.168.2.254`
- `util-0`: `192.168.0.56`
- `global_ip_address`: `"{{ global_ip_addresses[inventory_hostname] }}"`
- `global_pihole_api_host`: `"{{ global_ip_addresses['dns-0'] }}"`

## 🛠 Tasks
- Global

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: global
```