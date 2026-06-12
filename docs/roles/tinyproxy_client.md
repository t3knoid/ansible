# 🛠️ Role: `tinyproxy_client`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian | Windows](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian%20|%20Windows-orange.svg)

## 📖 Overview
Configures Linux clients to use a Tinyproxy forward proxy for shell and APT traffic and Windows clients for machine environment, WinINet, and WinHTTP proxy settings using the WinHttpProxy PowerShell module, which must already be available on Windows target hosts.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (jammy, noble)
- Supported on: `Debian` (bullseye, bookworm)
- Supported on: `Windows` (2019, 2022)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `tinyproxy_client_enabled` | `true` |  |
| `tinyproxy_client_proxy_scheme` | `http` |  |
| `tinyproxy_client_proxy_host` | `"{{ groups['fproxy'] | first }}"` |  |
| `tinyproxy_client_proxy_port` | `"{{ hostvars[groups['fproxy'] | first].tinyproxy_setup_port | default(8888) }}"` |  |
| `tinyproxy_client_manage_shell_proxy` | `true` |  |
| `tinyproxy_client_manage_apt_proxy` | `true` |  |
| `tinyproxy_client_manage_windows_environment` | `true` |  |
| `tinyproxy_client_manage_windows_wininet` | `true` |  |
| `tinyproxy_client_manage_windows_winhttp` | `true` |  |
| `tinyproxy_client_no_proxy` | `` |  |
| `-` | `:1` |  |
| `tinyproxy_client_shell_proxy_path` | `/etc/profile.d/fproxy-proxy.sh` |  |
| `tinyproxy_client_apt_proxy_path` | `/etc/apt/apt.conf.d/80fproxy-proxy` |  |
| `tinyproxy_client_proxy_url` | `>-` |  |
| `tinyproxy_client_proxy_scheme ~ '` | `//' ~` |  |
| `tinyproxy_client_proxy_host ~ '` | `' ~` |  |
| `tinyproxy_client_no_proxy_value` | `"{{ tinyproxy_client_no_proxy | join(',') }}"` |  |
| `tinyproxy_client_windows_proxy_bypass` | `"{{ tinyproxy_client_no_proxy | join(';') }}"` |  |
| `tinyproxy_client_windows_proxy_server` | `"{{ tinyproxy_client_proxy_host }}:{{ tinyproxy_client_proxy_port }}"` |  |
| `tinyproxy_client_windows_internet_settings_policy_path` | `HKLM:\Software\Policies\Microsoft\Windows\CurrentVersion\Internet Settings` |  |
| `tinyproxy_client_windows_internet_settings_path` | `HKLM:\Software\Microsoft\Windows\CurrentVersion\Internet Settings` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Configure Tinyproxy client on Linux
- Configure Tinyproxy client on Windows

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: tinyproxy_client
```