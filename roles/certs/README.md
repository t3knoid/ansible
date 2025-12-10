# 🛠️ Role: `certs`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Provides tasks to request and renew SSL/TLS certificates from Let's Encrypt. It also provides tasks to stage certificates for eventual use by the Nginx reverse proxy and other services.


## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `certs_rsa_key_size` | `4096` |  |
| `certs_email` | `"" # Adding a valid address is strongly recommended` |  |
| `certs_staging_arg` | `""` |  |
| `certs_staging` | `false # Set to true if you're testing your setup to avoid hitting request limits` |  |
| `certs_home` | `/data/letsencrypt` |  |
| `certs_stage` | `/data/certs` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Ensure custom certbot folders exist
- Set certs_email_arg for no email by default
- Set email_arg for non-empty email
- Set to staging by default
- Request certificates for each domain name

## 🔔 Handlers
- Restart nginx
- Restart pveproxy

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: certs
```