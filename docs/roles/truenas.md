# 🛠️ Role: `truenas`

![License: GPL-3.0-or-later](https://img.shields.io/badge/license-GPL-3.0-or-later-blue.svg)
![Ansible >= 2.14](https://img.shields.io/badge/ansible-%3E%3D%202.14-green.svg)
![Platforms: ](https://img.shields.io/badge/platforms--orange.svg)

## 📖 Overview
Configure TrueNAS 25.10+ (updates, admin, users, Active Directory, datasets, shares, services) through the middleware API

## 📋 Requirements
- Minimum Ansible version: `2.14`

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `truenas_become` | `true` | truenas_admin has sudo, so keep this true when connecting as that user. |
| `truenas_no_log` | `true` | Hide task arguments/results (they contain passwords). Set to false only to debug. |
| `truenas_min_version` | `"25.10"` | Refuse to run on anything older than this (major.minor). |
| `truenas_update_enabled` | `false` | new boot environment). Nothing happens when already up to date. |
| `truenas_update_reboot` | `false` | Reboot into the new boot environment automatically after an update. |
| `truenas_update_train` | `""` | Optional: pin a train or a version. Empty = newest version for the selected profile. |
| `truenas_update_version` | `""` |  |
| `truenas_update_reboot_timeout` | `1800` |  |
| `truenas_update_noop_patterns` | `` | update.run errors that just mean "nothing to do". |
| `truenas_groups` | `[]` | state: absent |
| `truenas_admin` | `{}` | sudo_commands_nopasswd: [ALL]          # lets Ansible `become` without a password |
| `truenas_admin_groups` | `` | always added to these. Verify with: midclt call privilege.query |
| `truenas_users` | `[]` | state: absent |
| `truenas_user_create_only_keys` | `` | Keys that are sent when a user is created but never compared/updated afterwards. |
| `truenas_network_configuration` | `{}` | domain: corp.example.com |
| `truenas_ad` | `{}` | idmap: {}                          # optional, see directoryservices.update docs |
| `truenas_datasets` | `[]` | quota: 1099511627776 |
| `truenas_dataset_create_only_keys` | `` |  |
| `truenas_smb_shares` | `[]` | hostsallow: ["192.168.1."] |
| `truenas_nfs_shares` | `[]` | maproot_user: root |
| `truenas_resources` | `[]` | sensitive_keys, send_sensitive_on_update, name_to_id, delete_args. |
| `truenas_post_calls` | `[]` | - {path: /mnt/tank/media, mode: "770", uid: 0, gid: 3000} |
| `truenas_services` | `[]` | - {name: nfs,  enable: true, state: started} |
| `truenas_apps_mode` | `plan` |  |
| `truenas_apps` | `[]` |  |
| `truenas_apps_job_timeout` | `900` |  |
| `truenas_apps_health_timeout` | `180` |  |
| `truenas_apps_poll_interval` | `5` |  |
| `truenas_vms_mode` | `plan` | allow_disk_delete: false      # required to destroy zvols on delete |
| `truenas_vms` | `[]` |  |
| `truenas_vms_job_timeout` | `900` |  |
| `truenas_vms_health_timeout` | `180` |  |
| `truenas_vms_poll_interval` | `5` |  |

## 📦 Vars
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `truenas_ad_base` | `` |  |
| `service_type` | `ACTIVEDIRECTORY` |  |
| `enable` | `"{{ truenas_ad.enable | default(true) }}"` |  |
| `enable_account_cache` | `"{{ truenas_ad.enable_account_cache | default(true) }}"` |  |
| `enable_dns_updates` | `"{{ truenas_ad.enable_dns_updates | default(true) }}"` |  |
| `timeout` | `"{{ truenas_ad.timeout | default(60) }}"` |  |
| `credential` | `` |  |
| `credential_type` | `KERBEROS_USER` |  |
| `username` | `"{{ truenas_ad.username }}"` |  |
| `password` | `"{{ truenas_ad.password }}"` |  |
| `configuration` | `>-` |  |
| `{{ {'hostname'` | `truenas_ad.hostname, 'domain': truenas_ad.domain | upper}` |  |
| `| combine({'idmap'` | `truenas_ad.idmap} if truenas_ad.idmap | default({}) | length > 0 else {}) }}` |  |
| `truenas_ad_config` | `>-` |  |
| `{{ truenas_ad_base | combine({'kerberos_realm'` | `truenas_ad.kerberos_realm | upper} if truenas_ad.kerberos_realm is defined else {}) }}` |  |

## 📑 Tasks
- Configure TrueNAS through the middleware API

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: truenas
```