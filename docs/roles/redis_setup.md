# 🛠️ Role: `redis_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures Redis.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `redis_setup_version` | `"6:8.4.0-1rl1"` | run `sudo apt policy redis` to find the latest version available |
| `redis_setup_password` | `"" # Set a password for Redis, leave empty for no password` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Add Redis official APT repository key
- Add Redis official APT repository
- Update apt cache
- Unhold package versions
- Install Redis from official package
- Hold package versions
- Remove Redis password block if not set
- Configure Redis with password and persistence
- Ensure Redis service is enabled and running

## 🔔 Handlers
- Restart Redis service

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: redis_setup
```