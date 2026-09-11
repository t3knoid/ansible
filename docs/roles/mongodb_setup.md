# 🛠️ Role: `mongodb_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs [MongoDB](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `mongodb_setup_repo_key_url` | `https://pgp.mongodb.com/server-8.0.asc` |  |
| `mongodb_setup_repo_key_local` | `/usr/share/keyrings/mongodb-server-8.0.gpg` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Ensure gnupg is installed
- Remove existing Mongodb repo key
- Download MongoDB GPG key
- Convert MongoDB GPG key to keyring format
- Remove existing Mongodb repo list file
- Create MongoDB repo list file
- Update APT package cache
- Gather installed package facts
- Unhold MongoDB package versions
- Install MongoDB
- Enable and start the MongoDB service
- Hold MongoDB package versions

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: mongodb_setup
```