# 🛠️ Role: `nebulasync_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs nebula-sync as documented in its [GitHub page](https://github.com/lovelaze/nebula-sync?tab=readme-ov-file#installation). This role requires that pi-hole role is configured on the target host. The target host is assumed to be the first host listed in the "primary_dns" inventory group.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `nebulasync_setup_version` | `0.2.5` |  |
| `nebulasync_setup_archive` | `"nebula-sync_{{ nebulasync_setup_version }}_linux_amd64.tar.gz"` |  |
| `nebulasync_setup_download` | `"https://github.com/lovelaze/nebula-sync/releases/download/v{{ nebulasync_setup_version }}/{{ nebulasync_setup_archive }}"` |  |
| `nebulasync_setup_installdir` | `"/usr/local/bin"` |  |
| `nebulasync_setup_envfilepath` | `"/etc/nebula-sync.env"` |  |
| `nebulasync_setup_primary` | `"{{ global_ip_addresses[groups['primary_dns'][0]] }}|{{ nebulasync_setup_primary_password }}"` |  |
| `nebulasync_setup_replicas` | `"{{ global_ip_addresses[groups['secondary_dns'][0]] }}|{{ nebulasync_setup_replicas_password }}"` |  |
| `nebulasync_setup_settings` | `` | Settings |
| `- { key` | `'PRIMARY', value: "{{ nebulasync_setup_primary }}" }` |  |
| `- { key` | `'REPLICAS', value: "{{ nebulasync_setup_replicas }}" }` |  |
| `- { key` | `'CRON', value: '0 * * * *' }` |  |
| `- { key` | `'TZ', value: 'Americas/New_York' }` |  |
| `- { key` | `'FULL_SYNC', value: 'true' } # Settings after this are only set if FULL_SYNC=false` |  |
| `- { key` | `'SYNC_CONFIG_DNS', value: 'false' }` |  |
| `- { key` | `'SYNC_CONFIG_NTP', value: 'false' }` |  |
| `- { key` | `'SYNC_CONFIG_RESOLVER', value: 'false' }` |  |
| `- { key` | `'SYNC_CONFIG_DATABASE', value: 'false' }` |  |
| `- { key` | `'SYNC_CONFIG_MISC', value: 'false' }` |  |
| `- { key` | `'SYNC_CONFIG_DEBUG', value: 'false' }` |  |
| `- { key` | `'SYNC_GRAVITY_DHCP_LEASES', value: 'false' }` |  |
| `- { key` | `'SYNC_GRAVITY_GROUP', value: 'false' }` |  |
| `- { key` | `'SYNC_GRAVITY_AD_LIST', value: 'false' }` |  |
| `- { key` | `'SYNC_GRAVITY_AD_LIST_BY_GROUP', value: 'false' }` |  |
| `- { key` | `'SYNC_GRAVITY_DOMAIN_LIST', value: 'false' }` |  |
| `- { key` | `'SYNC_GRAVITY_DOMAIN_LIST_BY_GROUP', value: 'false' }` |  |
| `- { key` | `'SYNC_GRAVITY_CLIENT', value: 'false' }` |  |
| `- { key` | `'SYNC_GRAVITY_CLIENT_BY_GROUP', value: 'false' }` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Download the latest release of nebula-sync
- Extract the downloaded tarball
- Clean up the tarball
- Create environment file
- Create service file
- Ensure nebula-sync service is started

## 🔔 Handlers
- Restart nebula-sync service

## 🔗 Dependencies
- `java_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: nebulasync_setup
```