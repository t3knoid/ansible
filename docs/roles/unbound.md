# 🛠️ Role: `unbound`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs and configures Unbound DNS resolver with optional logging support.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `unbound_update_root_hints` | `true` |  |
| `unbound_enable_logging` | `false` |  |
| `unbound_root_hints_url` | `"https://www.internic.net/domain/named.cache"` |  |
| `unbound_interface` | `"127.0.0.1"` |  |
| `unbound_verbosity` | `1` |  |
| `unbound_port` | `5335` |  |
| `unbound_assert_upstream` | `true` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Ensure required packages are installed
- Optionally download updated root.hints
- Ensure Unbound configuration directory exists
- Deploy Pi-hole recommended Unbound configuration
- Disable unbound-resolvconf.service if present
- Check if /etc/resolvconf.conf exists
- Disable resolvconf_resolvers.conf generation
- Remove resolvconf_resolvers.conf if present
- Ensure Unbound log directory exists
- Ensure Unbound log file exists
- Add AppArmor rule for Unbound logging
- Ensure Unbound service is enabled and running
- Force handlers to run
- Verify Pi-hole is querying Unbound using dig
- Show dig output
- Assert that Pi-hole forwarded to Unbound (optional)

## 🔔 Handlers
- Restart unbound
- Reload apparmor

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: unbound
```