# 🛠️ Role: `wikipedia_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu](https://img.shields.io/badge/platforms-Ubuntu-orange.svg)

## 📖 Overview
Deploys and configures a Wikipedia instance using MediaWiki.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (20.04, 22.04)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `wikipedia_setup_dump_dir` | `/opt/wikimedia_dumps` |  |
| `wikipedia_setup_dump_files` | `` |  |
| `wikipedia_setup_latest_dump_root_url` | `"https://dumps.wikimedia.org/enwiki/latest"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Ensure dump directory exists
- Download Wikimedia dump files

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: wikipedia_setup
```