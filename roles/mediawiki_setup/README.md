# 🛠️ Role: `mediawiki_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Install and configure mediawiki_setup_version.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `mediawiki_setup_version` | `"1.44.2"` |  |
| `mediawiki_setup_major_minor_version` | `"{{ mediawiki_setup_version.split('.')[:2] | join('.') }}"` |  |
| `mediawiki_setup_archive` | `"mediawiki-{{ mediawiki_setup_version }}.tar.gz"` |  |
| `mediawiki_setup_download_url` | `"https://releases.wikimedia.org/mediawiki/{{ mediawiki_setup_major_minor_version }}/{{ mediawiki_setup_archive }}"` |  |
| `mediawiki_setup_install_dir` | `/opt/mediawiki-{{ mediawiki_setup_version }}` |  |
| `mediawiki_setup_webroot_symlink` | `"/var/www/html/mediawiki"` |  |
| `mediawiki_setup_upload_max_filesize` | `2M` | mediawiki_setup_db_host: |
| `mediawiki_setup_memory_limit` | `8M` |  |
| `mediawiki_setup_cirrussearch_enabled` | `true` | cirrussearch |
| `mediawiki_setup_elasticsearch_host` | `"localhost"` |  |
| `mediawiki_setup_cirrussearch_index_type` | `"external"` |  |
| `mediawiki_setup_cirrussearch_namespace_weights` | `` |  |
| `- ns` | `0` |  |
| `weight` | `1.0` |  |
| `- ns` | `1` |  |
| `weight` | `0.5` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Ensure required PHP modules are enabled
- Download and extract MediaWiki into /opt
- Create symlink /opt/mediawiki → {{ mediawiki_setup_install_dir }}
- Create symlink to web root
- Create MediaWiki MySQL user
- Grant privileges to MediaWiki MySQL user on specific DB
- Create MediaWiki database
- Get installed PHP version
- Adjust PHP upload and memory limits

## 🔔 Handlers
- Restart Apache
- Reindex cirrussearch

## 🔗 Dependencies
- `lamp_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: mediawiki_setup
```