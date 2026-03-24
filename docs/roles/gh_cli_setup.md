# 🛠️ Role: `gh_cli_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.10](https://img.shields.io/badge/ansible-%3E%3D%202.10-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Install GitHub CLI (gh) on Debian/Ubuntu

## 📋 Requirements
- Minimum Ansible version: `2.10`
- Supported on: `Debian` (all)
- Supported on: `Ubuntu` (all)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `gh_cli_setup_keyring_path` | `/etc/apt/keyrings/githubcli-archive-keyring.gpg` |  |
| `gh_cli_setup_keyring_url` | `https://cli.github.com/packages/githubcli-archive-keyring.gpg` |  |
| `gh_cli_setup_repo_url` | `https://cli.github.com/packages` |  |
| `gh_cli_setup_sources_list_path` | `/etc/apt/sources.list.d/github-cli.list` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install wget
- Create keyrings directory
- Download GitHub CLI GPG key
- Add GitHub CLI apt repository
- Install GitHub CLI

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: gh_cli_setup
```