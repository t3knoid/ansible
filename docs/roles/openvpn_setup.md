# 🛠️ Role: `openvpn_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs and configures an OpenVPN client with optional fail-closed egress rules for the forward proxy host; expects inventory or environment-provided credentials, CA certificate, and remote server, applies IPv4 OUTPUT fail-closed rules, and resolves the VPN endpoint at deploy time

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (jammy, noble)
- Supported on: `Debian` (bullseye, bookworm)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `openvpn_enabled` | `false` |  |
| `openvpn_setup_enabled` | `"{{ openvpn_enabled }}"` |  |
| `openvpn_setup_profile_name` | `privado` |  |
| `openvpn_setup_interface` | `tun0` |  |
| `openvpn_setup_remote_server` | `""` |  |
| `openvpn_setup_remote_port` | `1194` |  |
| `openvpn_setup_remote_protocol` | `udp` |  |
| `openvpn_setup_packages` | `` |  |
| `openvpn_setup_client_config_path` | `"/etc/openvpn/client/{{ openvpn_setup_profile_name }}.conf"` |  |
| `openvpn_setup_auth_file` | `"/etc/openvpn/client/{{ openvpn_setup_profile_name }}.auth"` |  |
| `openvpn_setup_ca_cert_path` | `"/etc/openvpn/client/{{ openvpn_setup_profile_name }}-ca.crt"` |  |
| `openvpn_setup_service_name` | `"openvpn-client@{{ openvpn_setup_profile_name }}"` |  |
| `openvpn_setup_auth_username` | `"{{ lookup('env', 'OPENVPN_SETUP_AUTH_USERNAME') | default('', true) }}"` |  |
| `openvpn_setup_auth_password` | `"{{ lookup('env', 'OPENVPN_SETUP_AUTH_PASSWORD') | default('', true) }}"` |  |
| `openvpn_setup_ca_cert` | `""` |  |
| `openvpn_setup_redirect_gateway` | `true` |  |
| `openvpn_setup_route_ipv6_default` | `false` |  |
| `openvpn_setup_ipv6_default_route` | `::/0` |  |
| `openvpn_setup_manage_dns` | `true` |  |
| `openvpn_setup_dns_servers` | `[]` |  |
| `openvpn_setup_dns_search_domains` | `[]` |  |
| `openvpn_setup_cipher` | `AES-256-CBC` |  |
| `openvpn_setup_data_ciphers` | `` |  |
| `openvpn_setup_auth_digest` | `SHA256` |  |
| `openvpn_setup_log_verbosity` | `3` |  |
| `openvpn_setup_extra_directives` | `[]` |  |
| `openvpn_setup_apply_fail_closed_firewall` | `true` |  |
| `openvpn_setup_firewall_chain` | `OPENVPN_FAIL_CLOSED` |  |
| `openvpn_setup_firewall_chain_v6` | `OPENVPN_FAIL_CLOSED_V6` |  |
| `openvpn_setup_firewall_script_path` | `/usr/local/sbin/openvpn-fail-closed.sh` |  |
| `openvpn_setup_firewall_exempt_cidrs` | `[]` |  |
| `openvpn_setup_firewall_exempt_cidrs_v6` | `[]` |  |
| `openvpn_setup_verify_default_route` | `true` |  |
| `openvpn_setup_verify_default_route_ipv6` | `"{{ openvpn_setup_route_ipv6_default }}"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Stop OpenVPN client when disabled
- Remove fail-closed firewall rules when disabled
- Save netfilter rules after firewall cleanup
- Remove OpenVPN client artifacts when disabled
- Validate OpenVPN settings
- Ensure OpenVPN packages are installed
- Ensure OpenVPN client directory exists
- Resolve VPN server address for fail-closed firewall
- Resolve VPN server IPv6 address for fail-closed firewall
- Store VPN server address for fail-closed firewall
- Store VPN server IPv6 address for fail-closed firewall
- Deploy OpenVPN credential file
- Deploy OpenVPN CA certificate
- Deploy OpenVPN client configuration
- Deploy fail-closed firewall helper
- Apply fail-closed firewall rules
- Persist fail-closed firewall rules
- Ensure OpenVPN client service is enabled and started
- Wait for VPN interface to become available
- Verify default route uses the VPN interface
- Verify IPv6 default route uses the VPN interface

## 🔔 Handlers
- Restart OpenVPN client
- Save netfilter rules

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: openvpn_setup
```