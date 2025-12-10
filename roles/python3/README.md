# 🛠️ Role: `python3`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs Python 3 from the Python Software Foundation (PSF) repository. There is also an alternate option is to compile Python 3 from source.


## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `python3_version` | `3.12` |  |
| `python3_repo_key_local` | `"/etc/apt/trusted.gpg.d/deadsnakes.asc"` |  |
| `python3_repo_base_url` | `"https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu"` |  |
| `python3_repo_key_url` | `"https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xBA6932366A755776"` |  |
| `python3_repo_deadsnakes_signing_key` | `"4096R/F23C5A6CF475977595C89F51BA6932366A755776"` |  |
| `python3_repo_deadsnakes_ppa` | `"deb https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu noble main"` |  |
| `python3_packages_to_install` | `` |  |
| `python3_venv_folder` | `"/opt/python_{{ python3_version }}"` |  |
| `python3_venv_packages_to_install` | `` |  |
| `python3_version_to_compile` | `3.12.3` |  |
| `python3_required_packages_for_compile` | `` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Remove legacy deadsnakes.list file
- Remove legacy ppa_deadsnakes_ppa_noble.list file
- Remove existing legacy Deadsnakes repo list file
- Remove existing deadsnakes-ubuntu-ppa-noble.sources file
- Add deadsnakes apt repository key.
- Remove deadsnakes apt repository
- Add deadsnakes apt repository
- Update apt cache
- Install python3
- Register Python {{ python3_version }} as an alternative

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: python3
```