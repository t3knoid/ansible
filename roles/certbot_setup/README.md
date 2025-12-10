# 🛠️ Role: `certbot_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
It deploys certbot following instructions documented in https://certbot.eff.org/instructions?ws=nginx&os=pip. Target hosts must be in a group named *[certbot]* in its inventory. Certbot is used to obtain SSL/TLS certificates from Let's Encrypt.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `certbot_setup_python_modules` | `` |  |
| `certbot_setup_bin_link` | `/usr/bin/certbot` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install Certbot and Certbot Nginx plugin
- Create symbolic link for Certbot command

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: certbot_setup
```