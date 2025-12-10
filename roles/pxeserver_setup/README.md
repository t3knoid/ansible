# 🛠️ Role: `pxeserver_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
The pxeserver_setup role is used to install and configure a [PXE server](https://ubuntu.com/server/docs/how-to-netboot-the-server-installer-on-amd64). For this to work under TP-Link Omada router, enable the "Legal DHCP Servers" setting and set it to the PXE server IP address.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `pxeserver_setup_host` | `"{{ groups['pxe'][0] }}"` |  |
| `pxeserver_setup_ip` | `"{{ global_ip_addresses[pxeserver_setup_host] }}"` |  |
| `pxeserver_setup_tftp_dir` | `"/data/tftpboot"` |  |
| `pxeserver_setup_iso_url` | `"http://{{ pxeserver_setup_ip }}/{{ global_os[vms_os].iso }}"` |  |
| `pxeserver_setup_interface` | `"ens18"` |  |
| `pxeserver_setup_client_hostname` | `"{{ inventory_hostname }}"` |  |
| `pxeserver_setup_client_ip` | `"{{ global_ip_address }}"` |  |
| `pxeserver_setup_dhcp_range` | `"{{ pxeserver_setup_client_ip }},{{ pxeserver_setup_client_ip }},255.255.255.0" # note only 1 ip address` |  |
| `pxeserver_setup_dhcp_lease` | `"6h"` |  |
| `pxeserver_setup_client_nic` | `"ens18"` |  |
| `pxeserver_setup_ip_reservations` | `` |  |
| `- { mac_address` | `'BC:24:11:71:2D:34', ip_address: "{{ pxeserver_setup_client_ip }}" }` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Include reset_dns.yml tasks
- Create tftp root directory
- Install required packages
- Download and extract netboot tarball
- Download live server ISO
- Copy netboot files to tftp root folder
- Find all directories
- Ensure tftp folders has proper access
- Ensure tftp root directory has proper access
- Include nginx.yml tasks

## 🔔 Handlers
- Restart dnsmasq
- Restart nginx

## 🔗 Dependencies
- `python3`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: pxeserver_setup
```